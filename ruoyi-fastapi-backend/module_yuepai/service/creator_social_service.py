from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.creator_do import (
    YpCreatorFollow,
    YpCreatorProfile,
    YpCreatorReview,
    YpCreatorWork,
    YpWorkFavorite,
)
from module_yuepai.entity.do.trade_do import YpOrder, YpOrderEvent
from module_yuepai.entity.vo.creator_vo import ReviewCreate


class CreatorSocialService:
    @classmethod
    async def state(cls, db: AsyncSession, user_id: int, creator_id: int, work_id: int | None = None) -> dict:
        followed = await db.scalar(
            select(func.count()).select_from(YpCreatorFollow).where(
                YpCreatorFollow.follower_user_id == user_id,
                YpCreatorFollow.creator_id == creator_id,
            )
        )
        favorited = 0
        if work_id:
            favorited = await db.scalar(
                select(func.count()).select_from(YpWorkFavorite).where(
                    YpWorkFavorite.user_id == user_id,
                    YpWorkFavorite.work_id == work_id,
                )
            )
        return {'followed': bool(followed), 'favorited': bool(favorited)}

    @classmethod
    async def follow(cls, db: AsyncSession, user_id: int, creator_id: int) -> dict:
        creator = await db.get(YpCreatorProfile, creator_id, with_for_update=True)
        if not creator or creator.status != 'published':
            raise HTTPException(status_code=404, detail='创作者不存在')
        if creator.user_id == user_id:
            raise HTTPException(status_code=409, detail='不能关注自己')
        old = await db.scalar(
            select(YpCreatorFollow).where(
                YpCreatorFollow.follower_user_id == user_id,
                YpCreatorFollow.creator_id == creator_id,
            )
        )
        if old:
            return {'followed': True, 'followerCount': creator.follower_count}
        db.add(YpCreatorFollow(follower_user_id=user_id, creator_id=creator_id))
        creator.follower_count += 1
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            creator = await db.get(YpCreatorProfile, creator_id)
            return {'followed': True, 'followerCount': creator.follower_count if creator else 0}
        return {'followed': True, 'followerCount': creator.follower_count}

    @classmethod
    async def unfollow(cls, db: AsyncSession, user_id: int, creator_id: int) -> dict:
        creator = await db.get(YpCreatorProfile, creator_id, with_for_update=True)
        if not creator:
            raise HTTPException(status_code=404, detail='创作者不存在')
        row = await db.scalar(
            select(YpCreatorFollow).where(
                YpCreatorFollow.follower_user_id == user_id,
                YpCreatorFollow.creator_id == creator_id,
            )
        )
        if row:
            await db.delete(row)
            creator.follower_count = max(int(creator.follower_count or 0) - 1, 0)
            await db.commit()
        return {'followed': False, 'followerCount': creator.follower_count}

    @classmethod
    async def favorite_work(cls, db: AsyncSession, user_id: int, work_id: int) -> dict:
        work = await db.get(YpCreatorWork, work_id, with_for_update=True)
        if not work or work.status != 'published' or work.audit_status != 'approved':
            raise HTTPException(status_code=404, detail='作品不存在')
        old = await db.scalar(
            select(YpWorkFavorite).where(YpWorkFavorite.user_id == user_id, YpWorkFavorite.work_id == work_id)
        )
        if old:
            return {'favorited': True, 'favoriteCount': work.favorite_count}
        db.add(YpWorkFavorite(user_id=user_id, work_id=work_id))
        work.favorite_count += 1
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            work = await db.get(YpCreatorWork, work_id)
            return {'favorited': True, 'favoriteCount': work.favorite_count if work else 0}
        return {'favorited': True, 'favoriteCount': work.favorite_count}

    @classmethod
    async def unfavorite_work(cls, db: AsyncSession, user_id: int, work_id: int) -> dict:
        work = await db.get(YpCreatorWork, work_id, with_for_update=True)
        if not work:
            raise HTTPException(status_code=404, detail='作品不存在')
        row = await db.scalar(
            select(YpWorkFavorite).where(YpWorkFavorite.user_id == user_id, YpWorkFavorite.work_id == work_id)
        )
        if row:
            await db.delete(row)
            work.favorite_count = max(int(work.favorite_count or 0) - 1, 0)
            await db.commit()
        return {'favorited': False, 'favoriteCount': work.favorite_count}

    @classmethod
    async def create_review(cls, db: AsyncSession, user_id: int, payload: ReviewCreate) -> dict:
        order = await db.get(YpOrder, payload.order_id, with_for_update=True)
        if not order:
            raise HTTPException(status_code=404, detail='订单不存在')
        if order.buyer_user_id != user_id:
            raise HTTPException(status_code=403, detail='仅下单用户可评价')
        if order.status not in {'completed', 'reviewed'}:
            raise HTTPException(status_code=409, detail='订单完成后才能评价')
        old = await db.scalar(select(YpCreatorReview).where(YpCreatorReview.order_id == order.order_id))
        if old:
            raise HTTPException(status_code=409, detail='该订单已经评价')
        creator = await db.scalar(
            select(YpCreatorProfile).where(
                YpCreatorProfile.user_id == order.seller_user_id,
                YpCreatorProfile.status == 'published',
            )
        )
        if not creator:
            raise HTTPException(status_code=409, detail='订单服务者没有可评价的创作者资料')
        review = YpCreatorReview(
            order_id=order.order_id,
            creator_id=creator.creator_id,
            reviewer_user_id=user_id,
            rating=payload.rating,
            service_rating=payload.service_rating,
            communication_rating=payload.communication_rating,
            delivery_rating=payload.delivery_rating,
            content=payload.content.strip(),
            assets_json=json.dumps(payload.assets, ensure_ascii=False, separators=(',', ':')),
        )
        db.add(review)
        old_total = Decimal(creator.rating or 0) * Decimal(creator.review_count or 0)
        creator.review_count += 1
        creator.rating = ((old_total + Decimal(payload.rating)) / Decimal(creator.review_count)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        previous = order.status
        order.status = 'reviewed'
        order.version += 1
        db.add(
            YpOrderEvent(
                order_id=order.order_id,
                operator_user_id=user_id,
                from_status=previous,
                to_status='reviewed',
                event_type='review_created',
                request_id=f'review-{order.order_id}-{user_id}',
            )
        )
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(status_code=409, detail='该订单已经评价') from exc
        await db.refresh(review)
        return {
            'reviewId': review.review_id,
            'orderId': review.order_id,
            'creatorId': review.creator_id,
            'rating': review.rating,
            'content': review.content,
            'createTime': review.create_time,
        }
