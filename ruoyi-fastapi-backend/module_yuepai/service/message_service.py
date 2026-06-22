from __future__ import annotations

import json
import re
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.user_do import SysUser
from module_yuepai.entity.do.message_do import YpConversation, YpConversationMember, YpMessage
from module_yuepai.entity.vo.message_vo import ConversationCreate, MessageCreate


class MessageService:
    CONTACT_PATTERN = re.compile(
        r'(1[3-9]\d{9})|([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})|'
        r'((微信|vx|v信|wechat|qq)\s*[:：]?\s*[A-Za-z0-9_-]{5,})',
        re.IGNORECASE,
    )

    @staticmethod
    def loads(value: str | None, default):
        if not value:
            return default
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return default

    @classmethod
    def message_dict(cls, row: YpMessage) -> dict:
        return {
            'messageId': row.message_id,
            'conversationId': row.conversation_id,
            'senderUserId': row.sender_user_id,
            'messageType': row.message_type,
            'text': row.text_content,
            'payload': cls.loads(row.payload_json, {}),
            'clientMessageId': row.client_message_id,
            'status': row.status,
            'recalledAt': row.recalled_at,
            'createTime': row.create_time,
        }

    @classmethod
    async def create_conversation(
        cls,
        db: AsyncSession,
        user_id: int,
        payload: ConversationCreate,
    ) -> dict:
        if payload.target_user_id == user_id:
            raise HTTPException(status_code=409, detail='不能和自己创建会话')
        target = await db.get(SysUser, payload.target_user_id)
        if not target or str(target.status) != '0' or str(target.del_flag) != '0':
            raise HTTPException(status_code=404, detail='目标用户不存在或不可用')
        low, high = sorted((user_id, payload.target_user_id))
        row = await db.scalar(
            select(YpConversation).where(
                YpConversation.user_low_id == low,
                YpConversation.user_high_id == high,
            )
        )
        if not row:
            row = YpConversation(
                user_low_id=low,
                user_high_id=high,
                creator_id=payload.creator_id,
                order_id=payload.order_id,
            )
            db.add(row)
            try:
                await db.flush()
                db.add_all([
                    YpConversationMember(conversation_id=row.conversation_id, user_id=low),
                    YpConversationMember(conversation_id=row.conversation_id, user_id=high),
                ])
                await db.commit()
            except IntegrityError:
                await db.rollback()
                row = await db.scalar(
                    select(YpConversation).where(
                        YpConversation.user_low_id == low,
                        YpConversation.user_high_id == high,
                    )
                )
                if not row:
                    raise HTTPException(status_code=409, detail='会话创建冲突')
            await db.refresh(row)
        return await cls._conversation_dict(db, row, user_id)

    @classmethod
    async def list_conversations(cls, db: AsyncSession, user_id: int) -> list[dict]:
        result = await db.execute(
            select(YpConversation, YpConversationMember)
            .join(
                YpConversationMember,
                and_(
                    YpConversationMember.conversation_id == YpConversation.conversation_id,
                    YpConversationMember.user_id == user_id,
                ),
            )
            .where(
                YpConversationMember.status == 'active',
                YpConversation.status == 'active',
            )
            .order_by(YpConversation.last_message_time.desc(), YpConversation.update_time.desc())
        )
        rows = []
        for conversation, member in result.all():
            item = await cls._conversation_dict(db, conversation, user_id)
            item['unreadCount'] = int(member.unread_count or 0)
            rows.append(item)
        return rows

    @classmethod
    async def list_messages(
        cls,
        db: AsyncSession,
        conversation_id: int,
        user_id: int,
        before_id: int | None,
        page_size: int,
    ) -> dict:
        await cls._member(db, conversation_id, user_id)
        conditions = [
            YpMessage.conversation_id == conversation_id,
            YpMessage.status != 'deleted',
        ]
        if before_id:
            conditions.append(YpMessage.message_id < before_id)
        rows = (
            await db.scalars(
                select(YpMessage)
                .where(*conditions)
                .order_by(YpMessage.message_id.desc())
                .limit(page_size)
            )
        ).all()
        rows = list(reversed(rows))
        return {'rows': [cls.message_dict(row) for row in rows], 'hasMore': len(rows) == page_size}

    @classmethod
    async def send_message(
        cls,
        db: AsyncSession,
        conversation_id: int,
        user_id: int,
        payload: MessageCreate,
    ) -> dict:
        await cls._member(db, conversation_id, user_id)
        old = await db.scalar(
            select(YpMessage).where(
                YpMessage.sender_user_id == user_id,
                YpMessage.client_message_id == payload.client_message_id,
            )
        )
        if old:
            return cls.message_dict(old)
        text = (payload.text or '').strip() or None
        if text and cls.CONTACT_PATTERN.search(text):
            raise HTTPException(status_code=422, detail='请勿在聊天中发送手机号、邮箱或站外联系方式')
        conversation = await db.get(YpConversation, conversation_id, with_for_update=True)
        if not conversation or conversation.status != 'active':
            raise HTTPException(status_code=404, detail='会话不存在或已关闭')
        row = YpMessage(
            conversation_id=conversation_id,
            sender_user_id=user_id,
            message_type=payload.message_type,
            text_content=text,
            payload_json=json.dumps(payload.payload, ensure_ascii=False, separators=(',', ':'), default=str),
            client_message_id=payload.client_message_id,
            status='sent',
        )
        db.add(row)
        await db.flush()
        preview = text or {'image': '[图片]', 'quote': '[报价]', 'order': '[订单]'}.get(payload.message_type, '[消息]')
        conversation.last_message_id = row.message_id
        conversation.last_message_preview = preview[:200]
        conversation.last_message_time = row.create_time or datetime.now()
        recipient_id = conversation.user_high_id if conversation.user_low_id == user_id else conversation.user_low_id
        recipient = await db.scalar(
            select(YpConversationMember)
            .where(
                YpConversationMember.conversation_id == conversation_id,
                YpConversationMember.user_id == recipient_id,
            )
            .with_for_update()
        )
        if recipient:
            recipient.unread_count += 1
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            old = await db.scalar(
                select(YpMessage).where(
                    YpMessage.sender_user_id == user_id,
                    YpMessage.client_message_id == payload.client_message_id,
                )
            )
            if old:
                return cls.message_dict(old)
            raise HTTPException(status_code=409, detail='消息发送冲突，请重试') from exc
        await db.refresh(row)
        return cls.message_dict(row)

    @classmethod
    async def mark_read(
        cls,
        db: AsyncSession,
        conversation_id: int,
        user_id: int,
        last_message_id: int | None,
    ) -> dict:
        member = await cls._member(db, conversation_id, user_id, lock=True)
        if last_message_id:
            message = await db.get(YpMessage, last_message_id)
            if not message or message.conversation_id != conversation_id:
                raise HTTPException(status_code=422, detail='已读消息不属于当前会话')
            member.last_read_message_id = last_message_id
        member.unread_count = 0
        await db.commit()
        return {'conversationId': conversation_id, 'unreadCount': 0, 'lastReadMessageId': member.last_read_message_id}

    @classmethod
    async def _member(
        cls,
        db: AsyncSession,
        conversation_id: int,
        user_id: int,
        lock: bool = False,
    ) -> YpConversationMember:
        statement = select(YpConversationMember).where(
            YpConversationMember.conversation_id == conversation_id,
            YpConversationMember.user_id == user_id,
            YpConversationMember.status == 'active',
        )
        if lock:
            statement = statement.with_for_update()
        member = await db.scalar(statement)
        if not member:
            raise HTTPException(status_code=403, detail='无权访问该会话')
        return member

    @classmethod
    async def _conversation_dict(cls, db: AsyncSession, row: YpConversation, user_id: int) -> dict:
        other_id = row.user_high_id if row.user_low_id == user_id else row.user_low_id
        other = await db.get(SysUser, other_id)
        return {
            'conversationId': row.conversation_id,
            'creatorId': row.creator_id,
            'orderId': row.order_id,
            'otherUser': {
                'userId': other.user_id if other else other_id,
                'nickName': other.nick_name if other else '用户',
                'avatar': other.avatar if other else None,
            },
            'lastMessageId': row.last_message_id,
            'lastMessagePreview': row.last_message_preview,
            'lastMessageTime': row.last_message_time,
            'status': row.status,
        }
