from __future__ import annotations

import secrets
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.creator_do import YpCreatorProfile
from module_yuepai.entity.do.demand_do import YpDemand
from module_yuepai.entity.do.trade_do import YpOrder, YpOrderEvent, YpQuote
from module_yuepai.entity.vo.core_vo import QuoteAccept
from module_yuepai.entity.vo.quote_vo import QuoteStatusAction
from module_yuepai.service.order_flow_service import OrderFlowService


class QuoteActionService:
    @classmethod
    async def accept(cls, db: AsyncSession, quote_id: int, user_id: int, payload: QuoteAccept) -> dict:
        old_event = await db.scalar(select(YpOrderEvent).where(YpOrderEvent.request_id == payload.request_id))
        if old_event:
            return OrderFlowService.order_to_dict(await db.get(YpOrder, old_event.order_id))

        quote = await db.get(YpQuote, quote_id, with_for_update=True)
        if not quote:
            raise HTTPException(status_code=404, detail='报价不存在')
        if quote.receiver_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅报价接收方可以接受报价')
        if quote.status not in {'pending', 'negotiating'}:
            raise HTTPException(status_code=409, detail='报价当前状态不可接受')
        now = datetime.now(quote.expires_at.tzinfo) if quote.expires_at.tzinfo else datetime.now()
        if quote.expires_at <= now:
            quote.status = 'expired'
            quote.version += 1
            await db.commit()
            raise HTTPException(status_code=409, detail='报价已失效')

        buyer_id, seller_id = await cls._resolve_parties(db, quote)
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
            location_snapshot_json=OrderFlowService._dumps(payload.location_snapshot),
            contact_snapshot_json=OrderFlowService._dumps(payload.contact_snapshot),
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
        quote.version += 1
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            old_event = await db.scalar(select(YpOrderEvent).where(YpOrderEvent.request_id == payload.request_id))
            if old_event:
                return OrderFlowService.order_to_dict(await db.get(YpOrder, old_event.order_id))
            raise HTTPException(status_code=409, detail='订单创建冲突，请刷新后重试') from exc
        await db.refresh(order)
        return OrderFlowService.order_to_dict(order)

    @classmethod
    async def reject(cls, db: AsyncSession, quote_id: int, user_id: int, payload: QuoteStatusAction) -> dict:
        quote = await db.get(YpQuote, quote_id, with_for_update=True)
        if not quote:
            raise HTTPException(status_code=404, detail='报价不存在')
        if quote.receiver_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅报价接收方可以拒绝报价')
        await cls._change_status(db, quote, payload, 'rejected')
        return OrderFlowService.quote_to_dict(quote)

    @classmethod
    async def withdraw(cls, db: AsyncSession, quote_id: int, user_id: int, payload: QuoteStatusAction) -> dict:
        quote = await db.get(YpQuote, quote_id, with_for_update=True)
        if not quote:
            raise HTTPException(status_code=404, detail='报价不存在')
        if quote.sender_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅报价发送方可以撤回报价')
        await cls._change_status(db, quote, payload, 'withdrawn')
        return OrderFlowService.quote_to_dict(quote)

    @staticmethod
    async def _change_status(db: AsyncSession, quote: YpQuote, payload: QuoteStatusAction, target: str) -> None:
        if quote.version != payload.expected_version:
            raise HTTPException(status_code=409, detail='报价状态已变化，请刷新后重试')
        if quote.status not in {'pending', 'negotiating'}:
            raise HTTPException(status_code=409, detail='报价当前状态不可操作')
        quote.status = target
        if payload.reason:
            quote.remark = f'{quote.remark or ""}\n处理原因：{payload.reason}'.strip()
        quote.version += 1
        await db.commit()
        await db.refresh(quote)

    @classmethod
    async def _resolve_parties(cls, db: AsyncSession, quote: YpQuote) -> tuple[int, int]:
        if quote.demand_id:
            demand = await db.get(YpDemand, quote.demand_id)
            if not demand:
                raise HTTPException(status_code=409, detail='报价关联需求不存在')
            buyer_id = demand.owner_user_id
            seller_id = quote.sender_user_id if quote.sender_user_id != buyer_id else quote.receiver_user_id
            return buyer_id, seller_id

        snapshot = OrderFlowService._loads(quote.service_snapshot_json, {})
        creator_id = snapshot.get('creatorId')
        if creator_id:
            creator = await db.get(YpCreatorProfile, int(creator_id))
            if not creator:
                raise HTTPException(status_code=409, detail='套餐关联创作者不存在')
            seller_id = creator.user_id
            if seller_id not in {quote.sender_user_id, quote.receiver_user_id}:
                raise HTTPException(status_code=409, detail='套餐创作者与报价参与人不一致')
            buyer_id = quote.receiver_user_id if quote.sender_user_id == seller_id else quote.sender_user_id
            return buyer_id, seller_id

        return quote.receiver_user_id, quote.sender_user_id
