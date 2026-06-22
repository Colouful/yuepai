import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.payment_do import YpPayment
from module_yuepai.entity.do.trade_do import YpOrder
from module_yuepai.entity.vo.payment_secure_vo import SecurePaymentPrepare
from module_yuepai.integration.wechat_pay_gateway import WechatPayGatewayError
from module_yuepai.service.mini_account_service import MiniAccountService
from module_yuepai.service.payment_service import PaymentService


class PaymentPrepareService:
    @classmethod
    async def prepare(
        cls,
        db: AsyncSession,
        order_id: int,
        user_id: int,
        payload: SecurePaymentPrepare,
    ) -> dict:
        existing = await db.scalar(select(YpPayment).where(YpPayment.request_id == payload.request_id))
        if existing:
            if existing.user_id != user_id or existing.order_id != order_id:
                raise HTTPException(status_code=409, detail='幂等请求号已被其他支付占用')
            if existing.status == 'prepared' and existing.prepay_id:
                gateway = PaymentService._gateway()
                params = gateway._mini_program_invoke_params(existing.prepay_id)
                return PaymentService._prepare_response(existing, params)
            if existing.status == 'paid':
                return PaymentService._prepare_response(existing, None)
            raise HTTPException(status_code=409, detail='该支付请求已处理，请更换请求号后重试')

        order = await db.get(YpOrder, order_id)
        if not order:
            raise HTTPException(status_code=404, detail='订单不存在')
        if order.buyer_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅下单用户可发起支付')
        if order.status != 'pending_payment' or order.payment_status != 'unpaid':
            raise HTTPException(status_code=409, detail='订单当前状态不可支付')
        if Decimal(order.payable_amount) <= 0:
            raise HTTPException(status_code=409, detail='订单应付金额无效')

        payer_subject = await MiniAccountService.payment_subject(db, user_id)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        payment = YpPayment(
            payment_no=PaymentService._payment_no(),
            order_id=order.order_id,
            user_id=user_id,
            amount=order.payable_amount,
            currency='CNY',
            status='created',
            request_id=payload.request_id,
            expires_at=expires_at.replace(tzinfo=None),
        )
        db.add(payment)
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            existing = await db.scalar(select(YpPayment).where(YpPayment.request_id == payload.request_id))
            if existing:
                raise HTTPException(status_code=409, detail='支付请求正在处理，请勿重复提交') from exc
            raise
        await db.refresh(payment)

        gateway = PaymentService._gateway()
        snapshot = json.loads(order.service_snapshot_json or '{}')
        description = str(snapshot.get('title') or snapshot.get('packageName') or '91约拍Pro约拍服务')
        try:
            result = await gateway.prepare_jsapi(
                payment_no=payment.payment_no,
                description=description,
                amount_fen=PaymentService._to_fen(Decimal(payment.amount)),
                payer_openid=payer_subject,
                expires_at=expires_at.isoformat(timespec='seconds'),
            )
        except (RuntimeError, WechatPayGatewayError) as exc:
            payment.status = 'failed'
            payment.failure_code = 'PROVIDER_ERROR'
            payment.failure_message = str(exc)[:500]
            payment.version += 1
            await db.commit()
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        payment.prepay_id = result['prepayId']
        payment.status = 'prepared'
        payment.version += 1
        await db.commit()
        await db.refresh(payment)
        return PaymentService._prepare_response(payment, result['invokeParams'])
