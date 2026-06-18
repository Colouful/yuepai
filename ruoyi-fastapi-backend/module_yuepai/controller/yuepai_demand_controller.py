"""约拍需求管理接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_demand_service import YuepaiDemandService
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiDemandQuery
from utils.response_util import ResponseUtil

yuepaiDemandController = APIRouter(prefix='/yuepai/demand', tags=['约拍管理-需求管理'])


@yuepaiDemandController.get('/list', summary='需求列表')
async def get_demand_list(
    demand_no: str = Query(None), type: str = Query(None),
    city: str = Query(None), status: str = Query(None),
    audit_status: str = Query(None), keyword: str = Query(None),
    page_num: int = Query(1), page_size: int = Query(20),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    query = YuepaiDemandQuery(demand_no=demand_no, type=type, city=city, status=status, audit_status=audit_status, keyword=keyword, page_num=page_num, page_size=page_size)
    result = await YuepaiDemandService.get_demand_list_services(db, query)
    return ResponseUtil.success(data=result)


@yuepaiDemandController.put('/audit', summary='审核需求')
async def audit_demand(
    demand_id: int, audit_status: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    await YuepaiDemandService.audit_demand_services(db, demand_id, audit_status)
    return ResponseUtil.success(msg='审核成功')


@yuepaiDemandController.put('/status', summary='修改需求状态')
async def update_demand_status(
    demand_id: int, status: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    await YuepaiDemandService.update_demand_status_services(db, demand_id, status)
    return ResponseUtil.success(msg='操作成功')
