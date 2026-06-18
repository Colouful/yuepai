"""约拍用户DAO"""
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.yuepai_user_do import YuepaiUser
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiUserQuery


class YuepaiUserDao:
    @classmethod
    async def get_user_list(cls, db: AsyncSession, query: YuepaiUserQuery):
        query_obj = select(YuepaiUser).where(YuepaiUser.del_flag == '0')
        if query.uid:
            query_obj = query_obj.where(YuepaiUser.uid.like(f'%{query.uid}%'))
        if query.role:
            query_obj = query_obj.where(YuepaiUser.role == query.role)
        if query.city:
            query_obj = query_obj.where(YuepaiUser.city.like(f'%{query.city}%'))
        if query.status is not None:
            query_obj = query_obj.where(YuepaiUser.status == query.status)
        if query.is_verified is not None:
            query_obj = query_obj.where(YuepaiUser.is_verified == query.is_verified)
        return query_obj

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int):
        result = await db.execute(select(YuepaiUser).where(YuepaiUser.id == user_id, YuepaiUser.del_flag == '0'))
        return result.scalars().first()

    @classmethod
    async def update_user_status(cls, db: AsyncSession, user_id: int, status: str):
        await db.execute(update(YuepaiUser).where(YuepaiUser.id == user_id).values(status=status))

    @classmethod
    async def update_verify_status(cls, db: AsyncSession, user_id: int, is_verified: str):
        await db.execute(update(YuepaiUser).where(YuepaiUser.id == user_id).values(is_verified=is_verified))
