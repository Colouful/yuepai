"""约拍用户服务"""
from sqlalchemy.ext.asyncio import AsyncSession
from module_yuepai.dao.yuepai_user_dao import YuepaiUserDao
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiUserQuery, YuepaiUserVO
from utils.page_util import PageUtil


class YuepaiUserService:
    @classmethod
    async def get_user_list_services(cls, db: AsyncSession, query: YuepaiUserQuery):
        query_obj = await YuepaiUserDao.get_user_list(db, query)
        return await PageUtil.paginate(db, query_obj, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def get_user_detail_services(cls, db: AsyncSession, user_id: int):
        return await YuepaiUserDao.get_user_by_id(db, user_id)

    @classmethod
    async def update_user_status_services(cls, db: AsyncSession, user_id: int, status: str):
        await YuepaiUserDao.update_user_status(db, user_id, status)

    @classmethod
    async def audit_verify_services(cls, db: AsyncSession, user_id: int, is_verified: str):
        await YuepaiUserDao.update_verify_status(db, user_id, is_verified)
