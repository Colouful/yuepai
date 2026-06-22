from __future__ import annotations

import json
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.demand_do import YpApplication, YpDemand
from module_yuepai.entity.vo.core_vo import ApplicationCreate, DemandCreate


class DemandService:
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
    def demand_to_dict(cls, row: YpDemand) -> dict:
        return {
            'demandId': row.demand_id,
            'ownerUserId': row.owner_user_id,
            'title': row.title,
            'description': row.description,
            'demandType': row.demand_type,
            'cityCode': row.city_code,
            'locationName': row.location_name,
            'shootAt': row.shoot_at,
            'durationMinutes': row.duration_minutes,
            'roles': cls._loads(row.roles_json, []),
            'referenceAssets': cls._loads(row.reference_assets_json, []),
            'budgetType': row.budget_type,
            'budgetMin': row.budget_min,
            'budgetMax': row.budget_max,
            'applicantLimit': row.applicant_limit,
            'applicationDeadline': row.application_deadline,
            'auditStatus': row.audit_status,
            'status': row.status,
            'version': row.version,
            'createTime': row.create_time,
            'updateTime': row.update_time,
        }

    @classmethod
    def application_to_dict(cls, row: YpApplication) -> dict:
        return {
            'applicationId': row.application_id,
            'demandId': row.demand_id,
            'applicantUserId': row.applicant_user_id,
            'roleCode': row.role_code,
            'introduction': row.introduction,
            'quoteAmount': row.quote_amount,
            'portfolioAssets': cls._loads(row.portfolio_assets_json, []),
            'status': row.status,
            'rejectReason': row.reject_reason,
            'version': row.version,
            'createTime': row.create_time,
            'updateTime': row.update_time,
        }

    @classmethod
    async def create(cls, db: AsyncSession, user_id: int, payload: DemandCreate) -> dict:
        row = YpDemand(
            owner_user_id=user_id,
            title=payload.title.strip(),
            description=payload.description.strip(),
            demand_type=payload.demand_type,
            city_code=payload.city_code,
            location_name=payload.location_name,
            shoot_at=payload.shoot_at,
            duration_minutes=payload.duration_minutes,
            roles_json=cls._dumps(payload.roles),
            reference_assets_json=cls._dumps(payload.reference_assets),
            budget_type=payload.budget_type,
            budget_min=payload.budget_min,
            budget_max=payload.budget_max,
            applicant_limit=payload.applicant_limit,
            application_deadline=payload.application_deadline,
            status='draft',
            audit_status='pending',
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return cls.demand_to_dict(row)

    @classmethod
    async def list_public(cls, db: AsyncSession, city_code: str | None, page_num: int, page_size: int) -> dict:
        conditions = [YpDemand.status == 'published', YpDemand.audit_status == 'approved']
        if city_code:
            conditions.append(YpDemand.city_code == city_code)
        total = await db.scalar(select(func.count()).select_from(YpDemand).where(*conditions))
        rows = (
            await db.scalars(
                select(YpDemand)
                .where(*conditions)
                .order_by(YpDemand.create_time.desc())
                .offset((page_num - 1) * page_size)
                .limit(page_size)
            )
        ).all()
        return {'rows': [cls.demand_to_dict(row) for row in rows], 'total': total or 0}

    @classmethod
    async def detail(cls, db: AsyncSession, demand_id: int, user_id: int | None = None) -> dict:
        row = await db.get(YpDemand, demand_id)
        if not row:
            raise HTTPException(status_code=404, detail='约拍需求不存在')
        if row.status != 'published' or row.audit_status != 'approved':
            if user_id != row.owner_user_id:
                raise HTTPException(status_code=404, detail='约拍需求不存在')
        return cls.demand_to_dict(row)

    @classmethod
    async def submit(cls, db: AsyncSession, demand_id: int, user_id: int) -> dict:
        row = await db.get(YpDemand, demand_id)
        if not row:
            raise HTTPException(status_code=404, detail='约拍需求不存在')
        if row.owner_user_id != user_id:
            raise HTTPException(status_code=403, detail='无权提交该需求')
        if row.status not in {'draft', 'rejected'}:
            raise HTTPException(status_code=409, detail='当前状态不可提交审核')
        row.status = 'pending_audit'
        row.audit_status = 'pending'
        row.version += 1
        await db.commit()
        await db.refresh(row)
        return cls.demand_to_dict(row)

    @classmethod
    async def audit(cls, db: AsyncSession, demand_id: int, approved: bool, reason: str | None) -> dict:
        row = await db.get(YpDemand, demand_id)
        if not row:
            raise HTTPException(status_code=404, detail='约拍需求不存在')
        if row.status != 'pending_audit':
            raise HTTPException(status_code=409, detail='需求不在待审核状态')
        row.audit_status = 'approved' if approved else 'rejected'
        row.status = 'published' if approved else 'rejected'
        row.version += 1
        await db.commit()
        await db.refresh(row)
        return cls.demand_to_dict(row)

    @classmethod
    async def apply(cls, db: AsyncSession, demand_id: int, user_id: int, payload: ApplicationCreate) -> dict:
        demand = await db.get(YpDemand, demand_id)
        if not demand or demand.status != 'published' or demand.audit_status != 'approved':
            raise HTTPException(status_code=404, detail='可报名需求不存在')
        if demand.owner_user_id == user_id:
            raise HTTPException(status_code=409, detail='不能报名自己发布的需求')
        now = datetime.now(demand.application_deadline.tzinfo) if demand.application_deadline.tzinfo else datetime.now()
        if demand.application_deadline <= now:
            raise HTTPException(status_code=409, detail='报名已截止')
        if payload.role_code not in cls._loads(demand.roles_json, []):
            raise HTTPException(status_code=422, detail='报名身份不在招募角色中')
        count = await db.scalar(
            select(func.count()).select_from(YpApplication).where(
                YpApplication.demand_id == demand_id,
                YpApplication.status.notin_(['withdrawn', 'rejected', 'expired']),
            )
        )
        if (count or 0) >= demand.applicant_limit:
            raise HTTPException(status_code=409, detail='报名人数已满')
        row = YpApplication(
            demand_id=demand_id,
            applicant_user_id=user_id,
            role_code=payload.role_code,
            introduction=payload.introduction.strip(),
            quote_amount=payload.quote_amount,
            portfolio_assets_json=cls._dumps(payload.portfolio_assets),
        )
        db.add(row)
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(status_code=409, detail='已使用该身份报名') from exc
        await db.refresh(row)
        return cls.application_to_dict(row)

    @classmethod
    async def list_applications(cls, db: AsyncSession, demand_id: int, user_id: int) -> list[dict]:
        demand = await db.get(YpDemand, demand_id)
        if not demand:
            raise HTTPException(status_code=404, detail='约拍需求不存在')
        if demand.owner_user_id != user_id:
            raise HTTPException(status_code=403, detail='无权查看报名列表')
        rows = (
            await db.scalars(
                select(YpApplication)
                .where(YpApplication.demand_id == demand_id)
                .order_by(YpApplication.create_time.desc())
            )
        ).all()
        return [cls.application_to_dict(row) for row in rows]
