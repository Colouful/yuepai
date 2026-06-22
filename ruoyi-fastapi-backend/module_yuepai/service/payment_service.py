from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.payment_do import YpPayment, YpPaymentEvent
from module_yuepai.entity.do.trade_do import YpOrder, YpOrderEvent
from module_yuepai.entity.vo.payment_vo import PaymentPrepareRequest
from module_yuepai.integration.wechat_pay_gateway import WechatPayGateway, WechatPayGatewayError


class PaymentService:
    @staticmethod
    def _to_fen(amount: Decimal) -> int:
        return int((amount * Decimal('100')).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    @staticmethod
    def _payment_no() -> str:
        return f"PAY{datetime.now():%Y%m%d%H%M%S}{secrets.randbelow(1000000):06d}"

    @classmethod
    async def prepare(
        cls,
        db: AsyncSession,
        order_id: int,
        user_id: int,
        payload: PaymentPrepareRequest,
    ) -> dict:
        existing = await db.scalar(select(YpPayment).where(YpPayment.request_id == payload.request_id))
        if existing:
            if existing.user_id != user_id or existing.order_id != order_id:
                raise HTTPException(status_code=409, detail='幂等请求号已被其他支付占用')
            if existing.status == 'prepared' and existing.prepay_id:
                gateway = cls._gateway()
                return cls._prepare_response(existing, gateway._mini_program_invoke_params(existing.prepay_id))
            if existing.status == 'paid':
                return cls._prepare_response(existing, None)
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

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        payment = YpPayment(
            payment_no=cls._payment_no(),
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

        gateway = cls._gateway()
        description = str(
            (json.loads(order.service_snapshot_json or '{}').get('title'))
            or (json.loads(order.service_snapshot_json or '{}').get('packageName'))
            or '91约拍Pro约拍服务'
        )
        try:
            provider_result = await gateway.prepare_jsapi(
                payment_no=payment.payment_no,
                description=description,
                amount_fen=cls._to_fen(Decimal(payment.amount)),
                payer_openid=payload.payer_openid,
                expires_at=expires_at.isoformat(timespec='seconds').replace('+00:00', '+00:00'),
            )
        except (RuntimeError, WechatPayGatewayError) as exc:
            payment.status = 'failed'
            payment.failure_code = 'PROVIDER_ERROR'
            payment.failure_message = str(exc)[:500]
            payment.version += 1
            await db.commit()
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        payment.prepay_id = provider_result['prepayId']
        payment.status = 'prepared'
        payment.version += 1
        await db.commit()
        await db.refresh(payment)
        return cls._prepare_response(payment, provider_result['invokeParams'])

    @classmethod
    async def process_wechat_notification(
        cls,
        db: AsyncSession,
        *,
        body: bytes,
        timestamp: str,
        nonce: str,
        signature: str,
    ) -> dict:
        gateway = cls._gateway()
        try:
            notification = gateway.verify_and_decrypt_notification(
                body=body,
                timestamp=timestamp,
                nonce=nonce,
                signature=signature,
            )
        except (RuntimeError, WechatPayGatewayError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        envelope = notification['event']
        resource = notification['resource']
        event_id = str(envelope.get('id') or '').strip()
        event_type = str(envelope.get('event_type') or '').strip()
        if not event_id or not event_type:
            raise HTTPException(status_code=400, detail='回调事件缺少唯一标识')

        old_event = await db.scalar(select(YpPaymentEvent).where(YpPaymentEvent.provider_event_id == event_id))
        if old_event and old_event.process_status == 'processed':
            return {'duplicate': True}

        payment_no = str(resource.get('out_trade_no') or '').strip()
        payment = await db.scalar(
            select(YpPayment).where(YpPayment.payment_no == payment_no).with_for_update()
        )
        if not payment:
            raise HTTPException(status_code=404, detail='支付单不存在')

        digest = hashlib.sha256(body).hexdigest()
        event = old_event or YpPaymentEvent(
            payment_id=payment.payment_id,
            provider_event_id=event_id,
            event_type=event_type,
            payload_digest=digest,
            process_status='received',
        )
        if not old_event:
            db.add(event)

        trade_state = str(resource.get('trade_state') or '')
        if trade_state == 'SUCCESS':
            paid_fen = int((resource.get('amount') or {}).get('total') or 0)
            expected_fen = cls._to_fen(Decimal(payment.amount))
            if paid_fen != expected_fen:
                event.process_status = 'failed'
                event.error_message = f'支付金额不一致，期望{expected_fen}，实际{paid_fen}'
                await db.commit()
                raise HTTPException(status_code=409, detail='支付回调金额不一致')

            order = await db.get(YpOrder, payment.order_id, with_for_update=True)
            if not order:
                raise HTTPException(status_code=404, detail='支付关联订单不存在')
            if payment.status != 'paid':
                payment.status = 'paid'
                payment.provider_transaction_id = str(resource.get('transaction_id') or '')[:64]
                payment.paid_at = cls._parse_provider_time(resource.get('success_time'))
                payment.version += 1
            if order.payment_status != 'paid':
                if order.status != 'pending_payment':
                    raise HTTPException(status_code=409, detail='订单状态与支付回调不一致')
                order.payment_status = 'paid'
                order.paid_amount = payment.amount
                order.status = 'paid'
                order.version += 1
                db.add(
                    YpOrderEvent(
                        order_id=order.order_id,
                        operator_user_id=order.buyer_user_id,
                        from_status='pending_payment',
                        to_status='paid',
                        event_type='payment_succeeded',
                        request_id=f'wxpay-{hashlib.sha256(event_id.encode()).hexdigest()[:48]}',
                    )
                )
        elif trade_state in {'CLOSED', 'REVOKED', 'PAYERROR'}:
            payment.status = 'failed' if trade_state == 'PAYERROR' else 'closed'
            payment.failure_code = trade_state
            payment.failure_message = str(resource.get('trade_state_desc') or '')[:500]
            payment.version += 1

        event.process_status = 'processed'
        event.processed_at = datetime.now()
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            duplicate = await db.scalar(
                select(YpPaymentEvent).where(YpPaymentEvent.provider_event_id == event_id)
            )
            if duplicate:
                return {'duplicate': True}
            raise
        return {'duplicate': False, 'tradeState': trade_state}

    @staticmethod
    def _gateway() -> WechatPayGateway:
        try:
            return WechatPayGateway()
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @staticmethod
    def _prepare_response(payment: YpPayment, invoke_params: dict | None) -> dict:
        return {
            'paymentId': payment.payment_id,
            'paymentNo': payment.payment_no,
            'orderId': payment.order_id,
            'amount': payment.amount,
            'status': payment.status,
            'expiresAt': payment.expires_at,
            'invokeParams': invoke_params,
        }

    @staticmethod
    def _parse_provider_time(value) -> datetime:
        if not value:
            return datetime.now()
        try:
            return datetime.fromisoformat(str(value).replace('Z', '+00:00')).replace(tzinfo=None)
        except ValueError:
            return datetime.now()
