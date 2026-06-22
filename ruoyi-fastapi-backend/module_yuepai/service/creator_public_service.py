from __future__ import annotations

import json

from fastapi import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.user_do import SysUser
from module_yuepai.entity.do.creator_do import YpCreatorProfile, YpCreatorReview, YpCreatorWork, YpServicePackage


class CreatorPublicService:
    @staticmethod
    def loads(value: str | None, default):
        if not value:
            return default
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return default

    @classmethod
    def profile_dict(cls, row: YpCreatorProfile) -> dict:
        return {
            'creatorId': row.creator_id,
            'userId': row.user_id,
            'roleCode': row.role_code,
            'displayName': row.display_name,
            'headline': row.headline,
            'bio': row.bio,
            'avatarUrl': row.avatar_url,
            'coverUrl': row.cover_url,
            'cityCode': row.city_code,
            'serviceCities': cls.loads(row.service_city_json, []),
            'tags': cls.loads(row.tags_json, []),
            'yearsExperience': row.years_experience,
            'basePrice': row.base_price,
            'responseRate': row.response_rate,
            'completedOrders': row.completed_orders,
            'rating': row.rating,
            'reviewCount': row.review_count,
            'followerCount': row.follower_count,
            'acceptMutual': row.accept_mutual,
            'certificationStatus': row.certification_status,
            'status': row.status,
            'version': row.version,
        }

    @classmethod
    def package_dict(cls, row: YpServicePackage) -> dict:
        return {
            'packageId': row.package_id,
            'creatorId': row.creator_id,
            'packageName': row.package_name,
            'description': row.description,
            'coverUrl': row.cover_url,
            'price': row.price,
            'durationMinutes': row.duration_minutes,
            'originalCount': row.original_count,
            'retouchedCount': row.retouched_count,
            'deliveryDays': row.delivery_days,
            'revisionCount': row.revision_count,
            'includes': cls.loads(row.includes_json, []),
            'excludes': cls.loads(row.excludes_json, []),
            'addons': cls.loads(row.addons_json, []),
            'bookingNotice': row.booking_notice,
            'refundRule': row.refund_rule,
        }

    @classmethod
    async def list_creators(
        cls,
        db: AsyncSession,
        role_code: str | None,
        city_code: str | None,
        keyword: str | None,
        tag: str | None,
        accept_mutual: bool | None,
        sort_by: str,
        page_num: int,
        page_size: int,
    ) -> dict:
        conditions = [YpCreatorProfile.status == 'published', YpCreatorProfile.certification_status == 'approved']
        if role_code:
            conditions.append(YpCreatorProfile.role_code == role_code)
        if city_code:
            conditions.append(YpCreatorProfile.city_code == city_code)
        if accept_mutual is not None:
            conditions.append(YpCreatorProfile.accept_mutual == accept_mutual)
        if tag:
            conditions.append(YpCreatorProfile.tags_json.like(f'%"{tag}"%'))
        if keyword:
            pattern = f'%{keyword.strip()}%'
            conditions.append(or_(YpCreatorProfile.display_name.like(pattern), YpCreatorProfile.headline.like(pattern)))
        total = await db.scalar(select(func.count()).select_from(YpCreatorProfile).where(*conditions))
        order_column = {
            'rating': YpCreatorProfile.rating.desc(),
            'orders': YpCreatorProfile.completed_orders.desc(),
            'priceAsc': YpCreatorProfile.base_price.asc(),
            'priceDesc': YpCreatorProfile.base_price.desc(),
        }.get(sort_by, YpCreatorProfile.create_time.desc())
        rows = (
            await db.scalars(
                select(YpCreatorProfile)
                .where(*conditions)
                .order_by(order_column, YpCreatorProfile.creator_id.desc())
                .offset((page_num - 1) * page_size)
                .limit(page_size)
            )
        ).all()
        creator_ids = [row.creator_id for row in rows]
        covers: dict[int, list[str]] = {}
        if creator_ids:
            works = (
                await db.scalars(
                    select(YpCreatorWork)
                    .where(
                        YpCreatorWork.creator_id.in_(creator_ids),
                        YpCreatorWork.status == 'published',
                        YpCreatorWork.audit_status == 'approved',
                    )
                    .order_by(YpCreatorWork.create_time.desc())
                )
            ).all()
            for work in works:
                values = covers.setdefault(work.creator_id, [])
                if len(values) < 3:
                    values.append(work.cover_url)
        result = []
        for row in rows:
            item = cls.profile_dict(row)
            item['workCovers'] = covers.get(row.creator_id, [])
            result.append(item)
        return {'rows': result, 'total': int(total or 0)}

    @classmethod
    async def detail(cls, db: AsyncSession, creator_id: int) -> dict:
        creator = await db.get(YpCreatorProfile, creator_id)
        if not creator or creator.status != 'published' or creator.certification_status != 'approved':
            raise HTTPException(status_code=404, detail='创作者不存在或尚未公开')
        work_count = await db.scalar(
            select(func.count()).select_from(YpCreatorWork).where(
                YpCreatorWork.creator_id == creator_id,
                YpCreatorWork.status == 'published',
                YpCreatorWork.audit_status == 'approved',
            )
        )
        package_count = await db.scalar(
            select(func.count()).select_from(YpServicePackage).where(
                YpServicePackage.creator_id == creator_id,
                YpServicePackage.status == 'published',
                YpServicePackage.audit_status == 'approved',
            )
        )
        item = cls.profile_dict(creator)
        item['workCount'] = int(work_count or 0)
        item['packageCount'] = int(package_count or 0)
        return item

    @classmethod
    async def packages(cls, db: AsyncSession, creator_id: int) -> list[dict]:
        await cls.detail(db, creator_id)
        rows = (
            await db.scalars(
                select(YpServicePackage)
                .where(
                    YpServicePackage.creator_id == creator_id,
                    YpServicePackage.status == 'published',
                    YpServicePackage.audit_status == 'approved',
                )
                .order_by(YpServicePackage.price.asc())
            )
        ).all()
        return [cls.package_dict(row) for row in rows]

    @classmethod
    async def reviews(cls, db: AsyncSession, creator_id: int, page_num: int, page_size: int) -> dict:
        await cls.detail(db, creator_id)
        conditions = [YpCreatorReview.creator_id == creator_id, YpCreatorReview.status == 'published']
        total = await db.scalar(select(func.count()).select_from(YpCreatorReview).where(*conditions))
        result = await db.execute(
            select(YpCreatorReview, SysUser)
            .join(SysUser, SysUser.user_id == YpCreatorReview.reviewer_user_id)
            .where(*conditions)
            .order_by(YpCreatorReview.create_time.desc())
            .offset((page_num - 1) * page_size)
            .limit(page_size)
        )
        rows = []
        for review, user in result.all():
            rows.append({
                'reviewId': review.review_id,
                'rating': review.rating,
                'serviceRating': review.service_rating,
                'communicationRating': review.communication_rating,
                'deliveryRating': review.delivery_rating,
                'content': review.content,
                'assets': cls.loads(review.assets_json, []),
                'creatorReply': review.creator_reply,
                'reviewer': {'userId': user.user_id, 'nickName': user.nick_name, 'avatar': user.avatar},
                'createTime': review.create_time,
            })
        return {'rows': rows, 'total': int(total or 0)}
