from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.demand_do import YpApplication, YpDemand
from module_yuepai.service.demand_service import DemandService


class DemandQueryService:
    @classmethod
    async def list_public(
        cls,
        db: AsyncSession,
        city_code: str | None,
        demand_type: str | None,
        budget_type: str | None,
        role_code: str | None,
        keyword: str | None,
        sort_by: str,
        page_num: int,
        page_size: int,
    ) -> dict:
        conditions = [
            YpDemand.status == 'published',
            YpDemand.audit_status == 'approved',
            YpDemand.application_deadline > datetime.now(),
        ]
        if city_code:
            conditions.append(YpDemand.city_code == city_code)
        if demand_type:
            conditions.append(YpDemand.demand_type == demand_type)
        if budget_type == 'paid':
            conditions.append(YpDemand.budget_type.notin_(['mutual', 'free']))
        elif budget_type:
            conditions.append(YpDemand.budget_type == budget_type)
        if role_code:
            conditions.append(YpDemand.roles_json.like(f'%"{role_code}"%'))
        if keyword:
            pattern = f'%{keyword.strip()}%'
            conditions.append(
                or_(
                    YpDemand.title.like(pattern),
                    YpDemand.description.like(pattern),
                    YpDemand.location_name.like(pattern),
                )
            )

        total = await db.scalar(select(func.count()).select_from(YpDemand).where(*conditions))
        order_column = cls._order_column(sort_by)
        rows = (
            await db.scalars(
                select(YpDemand)
                .where(*conditions)
                .order_by(order_column)
                .offset((page_num - 1) * page_size)
                .limit(page_size)
            )
        ).all()

        demand_ids = [row.demand_id for row in rows]
        counts: dict[int, int] = {}
        if demand_ids:
            count_rows = (
                await db.execute(
                    select(YpApplication.demand_id, func.count(YpApplication.application_id))
                    .where(
                        YpApplication.demand_id.in_(demand_ids),
                        YpApplication.status.notin_(['withdrawn', 'rejected', 'expired']),
                    )
                    .group_by(YpApplication.demand_id)
                )
            ).all()
            counts = {int(demand_id): int(count) for demand_id, count in count_rows}

        result = []
        for row in rows:
            item = DemandService.demand_to_dict(row)
            item['applicantCount'] = counts.get(row.demand_id, 0)
            result.append(item)
        return {'rows': result, 'total': int(total or 0)}

    @staticmethod
    def _order_column(sort_by: str):
        if sort_by == 'deadline':
            return YpDemand.application_deadline.asc()
        if sort_by == 'shootAt':
            return YpDemand.shoot_at.asc()
        if sort_by == 'budget':
            return func.coalesce(YpDemand.budget_max, YpDemand.budget_min, 0).desc()
        return YpDemand.create_time.desc()
