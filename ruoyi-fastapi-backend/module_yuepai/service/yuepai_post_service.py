"""作品动态服务"""
from sqlalchemy.ext.asyncio import AsyncSession
from module_yuepai.dao.yuepai_post_dao import YuepaiPostDao
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiPostQuery
from utils.page_util import PageUtil


class YuepaiPostService:
    @classmethod
    async def get_post_list_services(cls, db: AsyncSession, query: YuepaiPostQuery):
        query_obj = await YuepaiPostDao.get_post_list(db, query)
        return await PageUtil.paginate(db, query_obj, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def audit_post_services(cls, db: AsyncSession, post_id: int, audit_status: str):
        await YuepaiPostDao.update_audit_status(db, post_id, audit_status)
