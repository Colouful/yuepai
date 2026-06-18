"""约拍用户管理接口"""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_user_service import YuepaiUserService
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiUserQuery
from utils.response_util import ResponseUtil
from utils.log_util import logger

yuepaiUserController = APIRouter(prefix='/yuepai/user', tags=['约拍管理-用户管理'])


@yuepaiUserController.get('/list', summary='用户列表')
async def get_user_list(
    request: Request,
    uid: str = Query(None, description='用户UID'),
    role: str = Query(None, description='角色'),
    city: str = Query(None, description='城市'),
    status: str = Query(None, description='状态'),
    is_verified: str = Query(None, description='认证状态'),
    page_num: int = Query(1, description='页码'),
    page_size: int = Query(20, description='每页数量'),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    query = YuepaiUserQuery(uid=uid, role=role, city=city, status=status, is_verified=is_verified, page_num=page_num, page_size=page_size)
    result = await YuepaiUserService.get_user_list_services(db, query)
    return ResponseUtil.success(data=result)


@yuepaiUserController.get('/{user_id}', summary='用户详情')
async def get_user_detail(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    result = await YuepaiUserService.get_user_detail_services(db, user_id)
    return ResponseUtil.success(data=result)


@yuepaiUserController.put('/status', summary='修改用户状态')
async def update_user_status(
    user_id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    await YuepaiUserService.update_user_status_services(db, user_id, status)
    return ResponseUtil.success(msg='操作成功')


@yuepaiUserController.put('/verify', summary='审核实名认证')
async def audit_verify(
    user_id: int,
    is_verified: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    await YuepaiUserService.audit_verify_services(db, user_id, is_verified)
    return ResponseUtil.success(msg='审核成功')
