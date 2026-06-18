"""约拍需求DAO"""
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.yuepai_user_do import YuepaiDemand
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiDemandQuery


class YuepaiDemandDao:
    @classmethod
    async def get_demand_list(cls, db: AsyncSession, query: YuepaiDemandQuery):
        query_obj = select(YuepaiDemand).where(YuepaiDemand.del_flag == '0')
        if query.demand_no:
            query_obj = query_obj.where(YuepaiDemand.demand_no.like(f'%{query.demand_no}%'))
        if query.type:
            query_obj = query_obj.where(YuepaiDemand.type == query.type)
        if query.city:
            query_obj = query_obj.where(YuepaiDemand.city.like(f'%{query.city}%'))
        if query.status is not None:
            query_obj = query_obj.where(YuepaiDemand.status == query.status)
        if query.audit_status is not None:
            query_obj = query_obj.where(YuepaiDemand.audit_status == query.audit_status)
        if query.keyword:
            query_obj = query_obj.where(YuepaiDemand.title.like(f'%{query.keyword}%'))
        return query_obj

    @classmethod
    async def get_demand_by_id(cls, db: AsyncSession, demand_id: int):
        result = await db.execute(select(YuepaiDemand).where(YuepaiDemand.id == demand_id))
        return result.scalars().first()

    @classmethod
    async def update_audit_status(cls, db: AsyncSession, demand_id: int, audit_status: str):
        await db.execute(update(YuepaiDemand).where(YuepaiDemand.id == demand_id).values(audit_status=audit_status))

    @classmethod
    async def update_status(cls, db: AsyncSession, demand_id: int, status: str):
        await db.execute(update(YuepaiDemand).where(YuepaiDemand.id == demand_id).values(status=status))
