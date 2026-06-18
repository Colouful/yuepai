"""约拍订单DAO"""
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.yuepai_user_do import YuepaiOrder, YuepaiPayment
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiOrderQuery


class YuepaiOrderDao:
    @classmethod
    async def get_order_list(cls, db: AsyncSession, query: YuepaiOrderQuery):
        query_obj = select(YuepaiOrder).where(YuepaiOrder.del_flag == '0')
        if query.order_no:
            query_obj = query_obj.where(YuepaiOrder.order_no.like(f'%{query.order_no}%'))
        if query.status is not None:
            query_obj = query_obj.where(YuepaiOrder.status == query.status)
        return query_obj

    @classmethod
    async def get_order_by_id(cls, db: AsyncSession, order_id: int):
        result = await db.execute(select(YuepaiOrder).where(YuepaiOrder.id == order_id))
        return result.scalars().first()

    @classmethod
    async def get_finance_stats(cls, db: AsyncSession):
        """财务统计"""
        total_query = select(
            func.count(YuepaiOrder.id).label('total_orders'),
            func.sum(YuepaiOrder.total_amount).label('total_amount'),
            func.sum(YuepaiOrder.platform_fee).label('total_fee'),
        ).where(YuepaiOrder.del_flag == '0')
        result = await db.execute(total_query)
        return result.first()
