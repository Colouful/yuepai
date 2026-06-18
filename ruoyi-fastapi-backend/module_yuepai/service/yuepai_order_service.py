"""约拍订单服务"""
from sqlalchemy.ext.asyncio import AsyncSession
from module_yuepai.dao.yuepai_order_dao import YuepaiOrderDao
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiOrderQuery
from utils.page_util import PageUtil


class YuepaiOrderService:
    @classmethod
    async def get_order_list_services(cls, db: AsyncSession, query: YuepaiOrderQuery):
        query_obj = await YuepaiOrderDao.get_order_list(db, query)
        return await PageUtil.paginate(db, query_obj, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def get_finance_stats_services(cls, db: AsyncSession):
        return await YuepaiOrderDao.get_finance_stats(db)
