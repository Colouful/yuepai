from __future__ import annotations

import json
import secrets
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.demand_do import YpApplication, YpDemand
from module_yuepai.entity.do.trade_do import YpOrder, YpOrderEvent, YpQuote
from module_yuepai.entity.vo.core_vo import OrderTransition, QuoteAccept, QuoteCreate


ORDER_TRANSITIONS = {
    'pending_payment': {'cancelled'},
    'paid': {'pending_service', 'refund_requested'},
    'pending_service': {'in_service', 'cancel_requested', 'refund_requested'},
    'in_service': {'pending_upload', 'dispute'},
    'pending_upload': {'pending_acceptance', 'dispute'},
    'pending_acceptance': {'modifying', 'completed', 'dispute'},
    'modifying': {'pending_acceptance', 'dispute'},
    'completed': {'reviewed', 'refund_requested'},
    'cancel_requested': {'cancelled', 'pending_service'},
    'refund_requested': {'refunding', 'completed', 'dispute'},
    'refunding': {'refunded', 'dispute'},
    'dispute': {'completed', 'refunded', 'closed'},
}

BUYER_ONLY = {
    ('pending_payment', 'cancelled'),
    ('pending_service', 'cancel_requested'),
    ('pending_service', 'refund_requested'),
    ('pending_acceptance', 'modifying'),
    ('pending_acceptance', 'completed'),
    ('completed', 'reviewed'),
    ('completed', 'refund_requested'),
}

SELLER_ONLY = {
    ('paid', 'pending_service'),
    ('pending_service', 'in_service'),
    ('in_service', 'pending_upload'),
    ('pending_upload', 'pending_acceptance'),
    ('modifying', 'pending_acceptance'),
}


class OrderFlowService:
    @staticmethod
    def _dumps(value) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(',', ':'), default=str)

    @staticmethod
    def _loads(value: str | None, default):
        if not value:
            return default
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return default

    @classmethod
    def quote_to_dict(cls, row: YpQuote) -> dict:
        return {
            'quoteId': row.quote_id,
            'demandId': row.demand_id,
            'applicationId': row.application_id,
            'senderUserId': row.sender_user_id,
            'receiverUserId': row.receiver_user_id,
            'amount': row.amount,
            'feeBreakdown': cls._loads(row.fee_breakdown_json, {}),
            'serviceSnapshot': cls._loads(row.service_snapshot_json, {}),
            'remark': row.remark,
            'expiresAt': row.expires_at,
            'status': row.status,
            'version': row.version,
            'createTime': row.create_time,
            'updateTime': row.update_time,
        }

    @classmethod
    def order_to_dict(cls, row: YpOrder) -> dict:
        return {
            'orderId': row.order_id,
            'orderNo': row.order_no,
            'buyerUserId': row.buyer_user_id,
            'sellerUserId': row.seller_user_id,
            'demandId': row.demand_id,
            'quoteId': row.quote_id,
            'serviceSnapshot': cls._loads(row.service_snapshot_json, {}),
            'amount': row.amount,
            'platformFee': row.platform_fee,
            'discountAmount': row.discount_amount,
            'payableAmount': row.payable_amount,
            'paidAmount': row.paid_amount,
            'shootAt': row.shoot_at,
            'durationMinutes': row.duration_minutes,
            'locationSnapshot': cls._loads(row.location_snapshot_json, {}),
            'contactSnapshot': cls._loads(row.contact_snapshot_json, {}),
            'remark': row.remark,
            'status': row.status,
            'paymentStatus': row.payment_status,
            'refundStatus': row.refund_status,
            'version': row.version,
            'createTime': row.create_time,
            'updateTime': row.update_time,
        }

    @classmethod
    async def create_quote(cls, db: AsyncSession, user_id: int, payload: QuoteCreate) -> dict:
        if payload.receiver_user_id == user_id:
            raise HTTPException(status_code=409, detail='不能向自己报价')
        demand = await db.get(YpDemand, payload.demand_id) if payload.demand_id else None
        application = await db.get(YpApplication, payload.application_id) if payload.application_id else None
        if application and demand and application.demand_id != demand.demand_id:
            raise HTTPException(status_code=422, detail='报名与需求不匹配')
        if demand:
            allowed_users = {demand.owner_user_id}
            if application:
                allowed_users.add(application.applicant_user_id)
            if user_id not in allowed_users or payload.receiver_user_id not in allowed_users:
                raise HTTPException(status_code=403, detail='报价双方与需求不匹配')
        row = YpQuote(
            demand_id=payload.demand_id,
            application_id=payload.application_id,
            sender_user_id=user_id,
            receiver_user_id=payload.receiver_user_id,
            amount=payload.amount,
            fee_breakdown_json=cls._dumps(payload.fee_breakdown),
            service_snapshot_json=cls._dumps(payload.service_snapshot),
            remark=payload.remark,
            expires_at=payload.expires_at,
            status='pending',
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return cls.quote_to_dict(row)

    @classmethod
    async def accept_quote(cls, db: AsyncSession, quote_id: int, user_id: int, payload: QuoteAccept) -> dict:
        old_event = await db.scalar(select(YpOrderEvent).where(YpOrderEvent.request_id == payload.request_id))
        if old_event:
            return cls.order_to_dict(await db.get(YpOrder, old_event.order_id))
        quote = await db.get(YpQuote, quote_id)
        if not quote:
            raise HTTPException(status_code=404, detail='报价不存在')
        if quote.receiver_user_id != user_id:
            raise HTTPException(status_code=403, detail='无权接受该报价')
        if quote.status not in {'pending', 'negotiating'}:
            raise HTTPException(status_code=409, detail='报价当前状态不可接受')
        now = datetime.now(quote.expires_at.tzinfo) if quote.expires_at.tzinfo else datetime.now()
        if quote.expires_at <= now:
            quote.status = 'expired'
            await db.commit()
            raise HTTPException(status_code=409, detail='报价已失效')
        demand = await db.get(YpDemand, quote.demand_id) if quote.demand_id else None
        buyer_id = demand.owner_user_id if demand else quote.receiver_user_id
        seller_id = quote.sender_user_id if quote.sender_user_id != buyer_id else quote.receiver_user_id
        amount = Decimal(quote.amount)
        platform_fee = (amount * Decimal('0.05')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        order = YpOrder(
            order_no=f"YP{datetime.now():%Y%m%d%H%M%S}{secrets.randbelow(10000):04d}",
            buyer_user_id=buyer_id,
            seller_user_id=seller_id,
            demand_id=quote.demand_id,
            quote_id=quote.quote_id,
            service_snapshot_json=quote.service_snapshot_json,
            amount=amount,
            platform_fee=platform_fee,
            discount_amount=Decimal('0'),
            payable_amount=amount + platform_fee,
            shoot_at=payload.shoot_at,
            duration_minutes=payload.duration_minutes,
            location_snapshot_json=cls._dumps(payload.location_snapshot),
            contact_snapshot_json=cls._dumps(payload.contact_snapshot),
            remark=payload.remark,
            status='pending_payment',
        )
        db.add(order)
        await db.flush()
        db.add(YpOrderEvent(
            order_id=order.order_id,
            operator_user_id=user_id,
            from_status=None,
            to_status='pending_payment',
            event_type='quote_accepted',
            request_id=payload.request_id,
        ))
        quote.status = 'accepted'
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            old_event = await db.scalar(select(YpOrderEvent).where(YpOrderEvent.request_id == payload.request_id))
            if old_event:
                return cls.order_to_dict(await db.get(YpOrder, old_event.order_id))
            raise HTTPException(status_code=409, detail='订单创建冲突，请重试') from exc
        await db.refresh(order)
        return cls.order_to_dict(order)

    @classmethod
    async def list_orders(cls, db: AsyncSession, user_id: int, order_status: str | None) -> list[dict]:
        conditions = [or_(YpOrder.buyer_user_id == user_id, YpOrder.seller_user_id == user_id)]
        if order_status:
            conditions.append(YpOrder.status == order_status)
        rows = (
            await db.scalars(select(YpOrder).where(and_(*conditions)).order_by(YpOrder.create_time.desc()).limit(100))
        ).all()
        return [cls.order_to_dict(row) for row in rows]

    @classmethod
    async def detail(cls, db: AsyncSession, order_id: int, user_id: int) -> dict:
        row = await db.get(YpOrder, order_id)
        if not row:
            raise HTTPException(status_code=404, detail='订单不存在')
        if user_id not in {row.buyer_user_id, row.seller_user_id}:
            raise HTTPException(status_code=403, detail='无权查看该订单')
        return cls.order_to_dict(row)

    @classmethod
    async def transition(cls, db: AsyncSession, order_id: int, user_id: int, payload: OrderTransition) -> dict:
        old_event = await db.scalar(select(YpOrderEvent).where(YpOrderEvent.request_id == payload.request_id))
        if old_event:
            return cls.order_to_dict(await db.get(YpOrder, old_event.order_id))
        row = await db.get(YpOrder, order_id, with_for_update=True)
        if not row:
            raise HTTPException(status_code=404, detail='订单不存在')
        if user_id not in {row.buyer_user_id, row.seller_user_id}:
            raise HTTPException(status_code=403, detail='无权操作该订单')
        if row.version != payload.expected_version:
            raise HTTPException(status_code=409, detail='订单状态已变化，请刷新后重试')
        transition = (row.status, payload.to_status)
        if payload.to_status not in ORDER_TRANSITIONS.get(row.status, set()):
            raise HTTPException(status_code=409, detail=f'不允许从{row.status}流转到{payload.to_status}')
        if transition in BUYER_ONLY and user_id != row.buyer_user_id:
            raise HTTPException(status_code=403, detail='该操作仅限下单用户')
        if transition in SELLER_ONLY and user_id != row.seller_user_id:
            raise HTTPException(status_code=403, detail='该操作仅限服务者')
        previous = row.status
        row.status = payload.to_status
        row.version += 1
        db.add(YpOrderEvent(
            order_id=row.order_id,
            operator_user_id=user_id,
            from_status=previous,
            to_status=payload.to_status,
            event_type='status_transition',
            reason=payload.reason,
            request_id=payload.request_id,
        ))
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            old_event = await db.scalar(select(YpOrderEvent).where(YpOrderEvent.request_id == payload.request_id))
            if old_event:
                return cls.order_to_dict(await db.get(YpOrder, old_event.order_id))
            raise HTTPException(status_code=409, detail='重复操作或状态冲突') from exc
        await db.refresh(row)
        return cls.order_to_dict(row)
