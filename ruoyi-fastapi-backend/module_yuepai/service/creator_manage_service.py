from __future__ import annotations

import json

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.creator_do import YpCreatorProfile, YpCreatorWork, YpServicePackage
from module_yuepai.entity.vo.creator_vo import CreatorProfileUpsert, CreatorWorkCreate, ServicePackageCreate
from module_yuepai.service.creator_public_service import CreatorPublicService
from module_yuepai.service.work_public_service import WorkPublicService


class CreatorManageService:
    @staticmethod
    def dumps(value) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(',', ':'), default=str)

    @staticmethod
    async def _owned_creator(db: AsyncSession, creator_id: int, user_id: int) -> YpCreatorProfile:
        creator = await db.get(YpCreatorProfile, creator_id)
        if not creator:
            raise HTTPException(status_code=404, detail='创作者资料不存在')
        if creator.user_id != user_id:
            raise HTTPException(status_code=403, detail='无权操作该创作者资料')
        return creator

    @classmethod
    async def upsert_profile(cls, db: AsyncSession, user_id: int, payload: CreatorProfileUpsert) -> dict:
        row = await db.scalar(
            select(YpCreatorProfile).where(
                YpCreatorProfile.user_id == user_id,
                YpCreatorProfile.role_code == payload.role_code,
            )
        )
        if not row:
            row = YpCreatorProfile(user_id=user_id, role_code=payload.role_code)
            db.add(row)
        row.display_name = payload.display_name.strip()
        row.headline = payload.headline.strip() if payload.headline else None
        row.bio = payload.bio.strip() if payload.bio else None
        row.avatar_url = payload.avatar_url
        row.cover_url = payload.cover_url
        row.city_code = payload.city_code
        row.service_city_json = cls.dumps(payload.service_cities)
        row.tags_json = cls.dumps(payload.tags)
        row.years_experience = payload.years_experience
        row.base_price = payload.base_price
        row.accept_mutual = payload.accept_mutual
        row.status = 'pending_audit'
        row.certification_status = 'pending'
        row.version = int(row.version or 0) + 1
        await db.commit()
        await db.refresh(row)
        return CreatorPublicService.profile_dict(row)

    @classmethod
    async def create_work(cls, db: AsyncSession, user_id: int, payload: CreatorWorkCreate) -> dict:
        await cls._owned_creator(db, payload.creator_id, user_id)
        if not payload.assets:
            raise HTTPException(status_code=422, detail='作品至少包含一张图片')
        row = YpCreatorWork(
            creator_id=payload.creator_id,
            title=payload.title.strip(),
            description=payload.description.strip() if payload.description else None,
            category=payload.category,
            cover_url=payload.cover_url,
            assets_json=cls.dumps(payload.assets),
            tags_json=cls.dumps(payload.tags),
            city_code=payload.city_code,
            shot_date=payload.shot_date,
            status='pending_audit',
            audit_status='pending',
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return WorkPublicService.work_dict(row)

    @classmethod
    async def create_package(cls, db: AsyncSession, user_id: int, payload: ServicePackageCreate) -> dict:
        creator = await cls._owned_creator(db, payload.creator_id, user_id)
        if creator.certification_status != 'approved':
            raise HTTPException(status_code=409, detail='创作者认证通过后才能创建服务套餐')
        row = YpServicePackage(
            creator_id=payload.creator_id,
            package_name=payload.package_name.strip(),
            description=payload.description.strip(),
            cover_url=payload.cover_url,
            price=payload.price,
            duration_minutes=payload.duration_minutes,
            original_count=payload.original_count,
            retouched_count=payload.retouched_count,
            delivery_days=payload.delivery_days,
            revision_count=payload.revision_count,
            includes_json=cls.dumps(payload.includes),
            excludes_json=cls.dumps(payload.excludes),
            addons_json=cls.dumps(payload.addons),
            booking_notice=payload.booking_notice,
            refund_rule=payload.refund_rule,
            status='pending_audit',
            audit_status='pending',
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return CreatorPublicService.package_dict(row)

    @classmethod
    async def audit_profile(cls, db: AsyncSession, creator_id: int, approved: bool, reason: str | None) -> dict:
        row = await db.get(YpCreatorProfile, creator_id)
        if not row:
            raise HTTPException(status_code=404, detail='创作者资料不存在')
        if row.status != 'pending_audit':
            raise HTTPException(status_code=409, detail='创作者资料不在待审核状态')
        row.certification_status = 'approved' if approved else 'rejected'
        row.status = 'published' if approved else 'rejected'
        if not approved and reason:
            row.headline = f'{row.headline or ""} [驳回原因：{reason}]'.strip()
        row.version += 1
        await db.commit()
        await db.refresh(row)
        return CreatorPublicService.profile_dict(row)

    @classmethod
    async def audit_work(cls, db: AsyncSession, work_id: int, approved: bool) -> dict:
        row = await db.get(YpCreatorWork, work_id)
        if not row:
            raise HTTPException(status_code=404, detail='作品不存在')
        if row.status != 'pending_audit':
            raise HTTPException(status_code=409, detail='作品不在待审核状态')
        row.audit_status = 'approved' if approved else 'rejected'
        row.status = 'published' if approved else 'rejected'
        row.version += 1
        await db.commit()
        await db.refresh(row)
        return WorkPublicService.work_dict(row)

    @classmethod
    async def audit_package(cls, db: AsyncSession, package_id: int, approved: bool) -> dict:
        row = await db.get(YpServicePackage, package_id)
        if not row:
            raise HTTPException(status_code=404, detail='服务套餐不存在')
        if row.status != 'pending_audit':
            raise HTTPException(status_code=409, detail='服务套餐不在待审核状态')
        row.audit_status = 'approved' if approved else 'rejected'
        row.status = 'published' if approved else 'rejected'
        row.version += 1
        await db.commit()
        await db.refresh(row)
        return CreatorPublicService.package_dict(row)
