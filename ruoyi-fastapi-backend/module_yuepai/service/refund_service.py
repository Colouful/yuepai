from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.payment_do import YpPayment, YpPaymentEvent, YpRefund
from module_yuepai.entity.do.trade_do import YpOrder, YpOrderEvent
from module_yuepai.entity.vo.payment_vo import RefundCreateRequest
from module_yuepai.integration.wechat_pay_gateway import WechatPayGateway, WechatPayGatewayError


class RefundService:
    REFUNDABLE_STATUSES = {
        'paid',
        'pending_service',
        'in_service',
        'pending_upload',
        'pending_acceptance',
        'completed',
    }

    @staticmethod
    def _to_fen(amount: Decimal) -> int:
        return int((amount * Decimal('100')).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    @staticmethod
    def _refund_no() -> str:
        return f"REF{datetime.now():%Y%m%d%H%M%S}{secrets.randbelow(1000000):06d}"

    @classmethod
    async def create_request(
        cls,
        db: AsyncSession,
        order_id: int,
        user_id: int,
        payload: RefundCreateRequest,
    ) -> dict:
        old = await db.scalar(select(YpRefund).where(YpRefund.request_id == payload.request_id))
        if old:
            if old.order_id != order_id or old.applicant_user_id != user_id:
                raise HTTPException(status_code=409, detail='幂等请求号已被占用')
            return cls._to_dict(old)

        order = await db.get(YpOrder, order_id, with_for_update=True)
        if not order:
            raise HTTPException(status_code=404, detail='订单不存在')
        if order.buyer_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅下单用户可申请退款')
        if order.payment_status != 'paid' or order.status not in cls.REFUNDABLE_STATUSES:
            raise HTTPException(status_code=409, detail='订单当前状态不可退款')
        if order.status == 'completed' and order.update_time and order.update_time < datetime.now() - timedelta(days=7):
            raise HTTPException(status_code=409, detail='订单完成超过七天，已超出退款申请期')

        amount = Decimal(payload.amount)
        paid_amount = Decimal(order.paid_amount)
        existing_refunded = await db.scalar(
            select(YpRefund).where(
                YpRefund.order_id == order_id,
                YpRefund.status.in_(['requested', 'refunding', 'refunded']),
            )
        )
        if existing_refunded:
            raise HTTPException(status_code=409, detail='订单已有退款流程')
        if amount <= 0 or amount > paid_amount:
            raise HTTPException(status_code=422, detail='退款金额不能超过实付金额')

        payment = await db.scalar(
            select(YpPayment)
            .where(YpPayment.order_id == order_id, YpPayment.status == 'paid')
            .order_by(YpPayment.paid_at.desc())
        )
        if not payment:
            raise HTTPException(status_code=409, detail='未找到有效支付单')

        refund = YpRefund(
            refund_no=cls._refund_no(),
            order_id=order_id,
            payment_id=payment.payment_id,
            applicant_user_id=user_id,
            amount=amount,
            reason=payload.reason.strip(),
            status='requested',
            request_id=payload.request_id,
            evidence_json=json.dumps(payload.evidence, ensure_ascii=False, separators=(',', ':')),
        )
        db.add(refund)
        previous = order.status
        order.refund_status = 'requested'
        order.status = 'refund_requested'
        order.version += 1
        await db.flush()
        db.add(
            YpOrderEvent(
                order_id=order.order_id,
                operator_user_id=user_id,
                from_status=previous,
                to_status='refund_requested',
                event_type='refund_requested',
                reason=payload.reason,
                request_id=f'refund-request-{refund.refund_no}',
            )
        )
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            old = await db.scalar(select(YpRefund).where(YpRefund.request_id == payload.request_id))
            if old:
                return cls._to_dict(old)
            raise HTTPException(status_code=409, detail='退款申请冲突，请刷新后重试') from exc
        await db.refresh(refund)
        return cls._to_dict(refund)

    @classmethod
    async def approve(cls, db: AsyncSession, refund_id: int, operator_user_id: int) -> dict:
        refund = await db.get(YpRefund, refund_id, with_for_update=True)
        if not refund:
            raise HTTPException(status_code=404, detail='退款申请不存在')
        if refund.status != 'requested':
            raise HTTPException(status_code=409, detail='退款申请当前状态不可审核')
        payment = await db.get(YpPayment, refund.payment_id)
        order = await db.get(YpOrder, refund.order_id, with_for_update=True)
        if not payment or not order:
            raise HTTPException(status_code=409, detail='退款关联支付或订单不存在')
        gateway = cls._gateway()
        try:
            provider_result = await gateway.request_refund(
                payment_no=payment.payment_no,
                refund_no=refund.refund_no,
                total_fen=cls._to_fen(Decimal(payment.amount)),
                refund_fen=cls._to_fen(Decimal(refund.amount)),
                reason=refund.reason,
            )
        except (RuntimeError, WechatPayGatewayError) as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        refund.provider_refund_id = str(provider_result.get('refund_id') or '')[:64]
        refund.status = 'refunding'
        refund.version += 1
        order.refund_status = 'refunding'
        order.status = 'refunding'
        order.version += 1
        db.add(
            YpOrderEvent(
                order_id=order.order_id,
                operator_user_id=operator_user_id,
                from_status='refund_requested',
                to_status='refunding',
                event_type='refund_approved',
                request_id=f'refund-approve-{refund.refund_no}',
            )
        )
        await db.commit()
        await db.refresh(refund)
        return cls._to_dict(refund)

    @classmethod
    async def process_notification(
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
        if not event_id:
            raise HTTPException(status_code=400, detail='退款回调缺少事件ID')
        old_event = await db.scalar(select(YpPaymentEvent).where(YpPaymentEvent.provider_event_id == event_id))
        if old_event and old_event.process_status == 'processed':
            return {'duplicate': True}

        refund_no = str(resource.get('out_refund_no') or '').strip()
        refund = await db.scalar(select(YpRefund).where(YpRefund.refund_no == refund_no).with_for_update())
        if not refund:
            raise HTTPException(status_code=404, detail='退款单不存在')
        payment = await db.get(YpPayment, refund.payment_id, with_for_update=True)
        order = await db.get(YpOrder, refund.order_id, with_for_update=True)
        if not payment or not order:
            raise HTTPException(status_code=409, detail='退款关联数据不存在')

        event = old_event or YpPaymentEvent(
            payment_id=payment.payment_id,
            provider_event_id=event_id,
            event_type=str(envelope.get('event_type') or 'REFUND.NOTIFY'),
            payload_digest=hashlib.sha256(body).hexdigest(),
            process_status='received',
        )
        if not old_event:
            db.add(event)

        refund_status = str(resource.get('refund_status') or '')
        if refund_status == 'SUCCESS':
            actual_fen = int((resource.get('amount') or {}).get('refund') or 0)
            expected_fen = cls._to_fen(Decimal(refund.amount))
            if actual_fen != expected_fen:
                event.process_status = 'failed'
                event.error_message = '退款金额不一致'
                await db.commit()
                raise HTTPException(status_code=409, detail='退款回调金额不一致')
            refund.status = 'refunded'
            refund.version += 1
            order.refund_status = 'refunded'
            order.status = 'refunded'
            order.version += 1
            if Decimal(refund.amount) >= Decimal(payment.amount):
                payment.status = 'refunded'
                order.payment_status = 'refunded'
            else:
                payment.status = 'partial_refunded'
                order.payment_status = 'partial_refunded'
            payment.version += 1
            db.add(
                YpOrderEvent(
                    order_id=order.order_id,
                    operator_user_id=order.buyer_user_id,
                    from_status='refunding',
                    to_status='refunded',
                    event_type='refund_succeeded',
                    request_id=f'wxrefund-{hashlib.sha256(event_id.encode()).hexdigest()[:44]}',
                )
            )
        elif refund_status in {'CLOSED', 'ABNORMAL'}:
            refund.status = 'failed'
            refund.version += 1
            order.refund_status = 'failed'
            order.status = 'dispute'
            order.version += 1

        event.process_status = 'processed'
        event.processed_at = datetime.now()
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            duplicate = await db.scalar(select(YpPaymentEvent).where(YpPaymentEvent.provider_event_id == event_id))
            if duplicate:
                return {'duplicate': True}
            raise
        return {'duplicate': False, 'refundStatus': refund_status}

    @staticmethod
    def _to_dict(refund: YpRefund) -> dict:
        return {
            'refundId': refund.refund_id,
            'refundNo': refund.refund_no,
            'orderId': refund.order_id,
            'amount': refund.amount,
            'reason': refund.reason,
            'status': refund.status,
            'version': refund.version,
            'createTime': refund.create_time,
            'updateTime': refund.update_time,
        }

    @staticmethod
    def _gateway() -> WechatPayGateway:
        try:
            return WechatPayGateway()
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
