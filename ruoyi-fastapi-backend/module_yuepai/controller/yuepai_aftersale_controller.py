"""售后管理接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_admin_service import AftersaleService
from module_yuepai.entity.vo.yuepai_admin_vo import AftersaleQuery, AftersaleHandle
from utils.response_util import ResponseUtil

aftersaleController = APIRouter(prefix='/yuepai/aftersale', tags=['约拍管理-售后管理'])


@aftersaleController.get('/list', summary='售后工单列表')
async def aftersale_list(
    type: str = Query(None), status: str = Query(None),
    ticket_no: str = Query(None), page_num: int = Query(1), page_size: int = Query(20),
    db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user),
):
    query = AftersaleQuery(type=type, status=status, ticket_no=ticket_no, page_num=page_num, page_size=page_size)
    result = await AftersaleService.get_list(db, query)
    return ResponseUtil.success(data=result)


@aftersaleController.get('/{id}', summary='工单详情')
async def aftersale_detail(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user)):
    item = await AftersaleService.get_detail(db, id)
    return ResponseUtil.success(data=item) if item else Fail(msg='工单不存在')


@aftersaleController.put('/handle', summary='处理工单')
async def aftersale_handle(
    body: AftersaleHandle, db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    handler = getattr(current_user, 'user_name', 'admin')
    await AftersaleService.handle(db, body.id, body.status, handler, body.handle_result or '')
    return ResponseUtil.success(msg='处理成功')
