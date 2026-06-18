"""约拍需求服务"""
from sqlalchemy.ext.asyncio import AsyncSession
from module_yuepai.dao.yuepai_demand_dao import YuepaiDemandDao
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiDemandQuery
from utils.page_util import PageUtil


class YuepaiDemandService:
    @classmethod
    async def get_demand_list_services(cls, db: AsyncSession, query: YuepaiDemandQuery):
        query_obj = await YuepaiDemandDao.get_demand_list(db, query)
        return await PageUtil.paginate(db, query_obj, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def audit_demand_services(cls, db: AsyncSession, demand_id: int, audit_status: str):
        await YuepaiDemandDao.update_audit_status(db, demand_id, audit_status)

    @classmethod
    async def update_demand_status_services(cls, db: AsyncSession, demand_id: int, status: str):
        await YuepaiDemandDao.update_status(db, demand_id, status)
