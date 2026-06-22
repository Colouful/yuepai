import base64
import hashlib
import secrets
from datetime import datetime

from fastapi import HTTPException
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.config.wechat_app_config import WechatAppConfig
from module_yuepai.domain.wechat_account import YpWechatAccount
from module_yuepai.entity.vo.mini_account_vo import MiniAccountBind
from module_yuepai.integration.mini_program_client import MiniProgramClientError, exchange_login_code


class MiniAccountService:
    AAD = b'yuepai-mini-account-v1'

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    @classmethod
    def _encrypt(cls, value: str) -> str:
        nonce = secrets.token_bytes(12)
        encrypted = AESGCM(WechatAppConfig.encryption_key()).encrypt(nonce, value.encode(), cls.AAD)
        return base64.urlsafe_b64encode(nonce + encrypted).decode()

    @classmethod
    def _decrypt(cls, value: str) -> str:
        try:
            raw = base64.urlsafe_b64decode(value.encode())
            plaintext = AESGCM(WechatAppConfig.encryption_key()).decrypt(raw[:12], raw[12:], cls.AAD)
            return plaintext.decode()
        except Exception as exc:
            raise RuntimeError('小程序账号绑定数据解密失败') from exc

    @classmethod
    async def bind(cls, db: AsyncSession, user_id: int, payload: MiniAccountBind) -> dict:
        try:
            subject, union = await exchange_login_code(payload.login_code)
        except (RuntimeError, MiniProgramClientError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        subject_hash = cls._hash(subject)
        occupied = await db.scalar(select(YpWechatAccount).where(YpWechatAccount.subject_hash == subject_hash))
        if occupied and occupied.user_id != user_id:
            raise HTTPException(status_code=409, detail='该小程序账号已绑定其他用户')
        row = await db.scalar(select(YpWechatAccount).where(YpWechatAccount.user_id == user_id))
        if not row:
            row = YpWechatAccount(user_id=user_id)
            db.add(row)
        row.subject_hash = subject_hash
        row.subject_secret = cls._encrypt(subject)
        row.union_hash = cls._hash(union) if union else None
        row.union_secret = cls._encrypt(union) if union else None
        row.status = 'active'
        row.last_login_time = datetime.now()
        await db.commit()
        await db.refresh(row)
        return {
            'bound': True,
            'accountId': row.account_id,
            'lastLoginTime': row.last_login_time,
        }

    @classmethod
    async def status(cls, db: AsyncSession, user_id: int) -> dict:
        row = await db.scalar(select(YpWechatAccount).where(YpWechatAccount.user_id == user_id))
        return {
            'bound': bool(row and row.status == 'active'),
            'lastLoginTime': row.last_login_time if row else None,
        }

    @classmethod
    async def payment_subject(cls, db: AsyncSession, user_id: int) -> str:
        row = await db.scalar(
            select(YpWechatAccount).where(
                YpWechatAccount.user_id == user_id,
                YpWechatAccount.status == 'active',
            )
        )
        if not row:
            raise HTTPException(status_code=409, detail='请先绑定当前微信小程序账号后再支付')
        return cls._decrypt(row.subject_secret)
