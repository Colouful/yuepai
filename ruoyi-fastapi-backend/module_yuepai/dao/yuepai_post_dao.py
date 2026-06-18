"""作品动态DAO"""
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.yuepai_user_do import YuepaiPost
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiPostQuery


class YuepaiPostDao:
    @classmethod
    async def get_post_list(cls, db: AsyncSession, query: YuepaiPostQuery):
        query_obj = select(YuepaiPost).where(YuepaiPost.del_flag == '0')
        if query.type:
            query_obj = query_obj.where(YuepaiPost.type == query.type)
        if query.audit_status is not None:
            query_obj = query_obj.where(YuepaiPost.audit_status == query.audit_status)
        if query.status is not None:
            query_obj = query_obj.where(YuepaiPost.status == query.status)
        if query.keyword:
            query_obj = query_obj.where(YuepaiPost.title.like(f'%{query.keyword}%'))
        return query_obj

    @classmethod
    async def update_audit_status(cls, db: AsyncSession, post_id: int, audit_status: str):
        await db.execute(update(YuepaiPost).where(YuepaiPost.id == post_id).values(audit_status=audit_status))
