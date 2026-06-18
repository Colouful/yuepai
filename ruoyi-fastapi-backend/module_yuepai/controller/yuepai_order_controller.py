"""约拍订单管理接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_order_service import YuepaiOrderService
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiOrderQuery
from utils.response_util import ResponseUtil

yuepaiOrderController = APIRouter(prefix='/yuepai/order', tags=['约拍管理-订单管理'])


@yuepaiOrderController.get('/list', summary='订单列表')
async def get_order_list(
    order_no: str = Query(None), status: str = Query(None),
    page_num: int = Query(1), page_size: int = Query(20),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    query = YuepaiOrderQuery(order_no=order_no, status=status, page_num=page_num, page_size=page_size)
    result = await YuepaiOrderService.get_order_list_services(db, query)
    return ResponseUtil.success(data=result)


@yuepaiOrderController.get('/finance/stats', summary='财务统计')
async def get_finance_stats(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    result = await YuepaiOrderService.get_finance_stats_services(db)
    return ResponseUtil.success(data=result)
