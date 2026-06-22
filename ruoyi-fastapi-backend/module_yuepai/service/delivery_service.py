from __future__ import annotations

import json
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.delivery_do import YpDelivery
from module_yuepai.entity.do.trade_do import YpOrder, YpOrderEvent
from module_yuepai.entity.vo.delivery_vo import DeliveryDecision, DeliverySubmit


class DeliveryService:
    @staticmethod
    def _loads(value: str | None) -> list[str]:
        if not value:
            return []
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []

    @staticmethod
    def _dumps(value: list[str]) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(',', ':'))

    @classmethod
    def to_dict(cls, row: YpDelivery) -> dict:
        return {
            'deliveryId': row.delivery_id,
            'orderId': row.order_id,
            'uploaderUserId': row.uploader_user_id,
            'deliveryVersion': row.delivery_version,
            'originalAssets': cls._loads(row.original_assets_json),
            'retouchedAssets': cls._loads(row.retouched_assets_json),
            'note': row.note,
            'status': row.status,
            'revisionReason': row.revision_reason,
            'submittedAt': row.submitted_at,
            'acceptedAt': row.accepted_at,
            'createTime': row.create_time,
        }

    @classmethod
    async def latest(cls, db: AsyncSession, order_id: int, user_id: int) -> dict:
        order = await cls._order(db, order_id, user_id)
        row = await db.scalar(
            select(YpDelivery)
            .where(YpDelivery.order_id == order_id)
            .order_by(YpDelivery.delivery_version.desc())
        )
        return {
            'order': {
                'orderId': order.order_id,
                'buyerUserId': order.buyer_user_id,
                'sellerUserId': order.seller_user_id,
                'status': order.status,
                'version': order.version,
                'serviceSnapshot': json.loads(order.service_snapshot_json or '{}'),
            },
            'delivery': cls.to_dict(row) if row else None,
        }

    @classmethod
    async def versions(cls, db: AsyncSession, order_id: int, user_id: int) -> list[dict]:
        await cls._order(db, order_id, user_id)
        rows = (
            await db.scalars(
                select(YpDelivery)
                .where(YpDelivery.order_id == order_id)
                .order_by(YpDelivery.delivery_version.desc())
            )
        ).all()
        return [cls.to_dict(row) for row in rows]

    @classmethod
    async def submit(
        cls,
        db: AsyncSession,
        order_id: int,
        user_id: int,
        payload: DeliverySubmit,
    ) -> dict:
        old = await db.scalar(select(YpDelivery).where(YpDelivery.request_id == payload.request_id))
        if old:
            if old.order_id != order_id or old.uploader_user_id != user_id:
                raise HTTPException(status_code=409, detail='幂等请求号已被其他交付占用')
            return cls.to_dict(old)
        order = await db.get(YpOrder, order_id, with_for_update=True)
        if not order:
            raise HTTPException(status_code=404, detail='订单不存在')
        if order.seller_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅服务者可以提交作品')
        if order.version != payload.expected_order_version:
            raise HTTPException(status_code=409, detail='订单状态已变化，请刷新后重试')
        if order.status not in {'pending_upload', 'modifying'}:
            raise HTTPException(status_code=409, detail='订单当前状态不可提交作品')
        version = int(
            await db.scalar(
                select(func.coalesce(func.max(YpDelivery.delivery_version), 0)).where(
                    YpDelivery.order_id == order_id
                )
            )
            or 0
        ) + 1
        previous = await db.scalar(
            select(YpDelivery)
            .where(YpDelivery.order_id == order_id)
            .order_by(YpDelivery.delivery_version.desc())
            .limit(1)
        )
        if previous and previous.status in {'submitted', 'revision_requested'}:
            previous.status = 'superseded'
        row = YpDelivery(
            order_id=order_id,
            uploader_user_id=user_id,
            delivery_version=version,
            original_assets_json=cls._dumps(payload.original_assets),
            retouched_assets_json=cls._dumps(payload.retouched_assets),
            note=payload.note,
            status='submitted',
            request_id=payload.request_id,
        )
        db.add(row)
        from_status = order.status
        order.status = 'pending_acceptance'
        order.version += 1
        await db.flush()
        db.add(
            YpOrderEvent(
                order_id=order_id,
                operator_user_id=user_id,
                from_status=from_status,
                to_status='pending_acceptance',
                event_type='delivery_submitted',
                request_id=payload.request_id,
            )
        )
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            old = await db.scalar(select(YpDelivery).where(YpDelivery.request_id == payload.request_id))
            if old:
                return cls.to_dict(old)
            raise HTTPException(status_code=409, detail='作品提交冲突，请刷新后重试') from exc
        await db.refresh(row)
        return cls.to_dict(row)

    @classmethod
    async def decide(
        cls,
        db: AsyncSession,
        order_id: int,
        user_id: int,
        payload: DeliveryDecision,
    ) -> dict:
        old_event = await db.scalar(select(YpOrderEvent).where(YpOrderEvent.request_id == payload.request_id))
        if old_event:
            row = await db.scalar(
                select(YpDelivery)
                .where(YpDelivery.order_id == order_id)
                .order_by(YpDelivery.delivery_version.desc())
            )
            return cls.to_dict(row)
        order = await db.get(YpOrder, order_id, with_for_update=True)
        if not order:
            raise HTTPException(status_code=404, detail='订单不存在')
        if order.buyer_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅下单用户可以验收作品')
        if order.version != payload.expected_order_version:
            raise HTTPException(status_code=409, detail='订单状态已变化，请刷新后重试')
        if order.status != 'pending_acceptance':
            raise HTTPException(status_code=409, detail='订单当前状态不可验收')
        row = await db.scalar(
            select(YpDelivery)
            .where(YpDelivery.order_id == order_id, YpDelivery.status == 'submitted')
            .order_by(YpDelivery.delivery_version.desc())
            .with_for_update()
        )
        if not row:
            raise HTTPException(status_code=409, detail='没有待验收的作品版本')
        if payload.accepted:
            row.status = 'accepted'
            row.accepted_at = datetime.now()
            order.status = 'completed'
            target = 'completed'
            event_type = 'delivery_accepted'
        else:
            if not (payload.reason or '').strip():
                raise HTTPException(status_code=422, detail='申请修改必须填写具体原因')
            row.status = 'revision_requested'
            row.revision_reason = payload.reason.strip()
            order.status = 'modifying'
            target = 'modifying'
            event_type = 'delivery_revision_requested'
        order.version += 1
        db.add(
            YpOrderEvent(
                order_id=order_id,
                operator_user_id=user_id,
                from_status='pending_acceptance',
                to_status=target,
                event_type=event_type,
                reason=payload.reason,
                request_id=payload.request_id,
            )
        )
        await db.commit()
        await db.refresh(row)
        return cls.to_dict(row)

    @staticmethod
    async def _order(db: AsyncSession, order_id: int, user_id: int) -> YpOrder:
        order = await db.get(YpOrder, order_id)
        if not order:
            raise HTTPException(status_code=404, detail='订单不存在')
        if user_id not in {order.buyer_user_id, order.seller_user_id}:
            raise HTTPException(status_code=403, detail='无权查看该订单交付')
        return order
