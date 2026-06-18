"""作品动态管理接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_post_service import YuepaiPostService
from module_yuepai.entity.vo.yuepai_user_vo import YuepaiPostQuery
from utils.response_util import ResponseUtil

yuepaiPostController = APIRouter(prefix='/yuepai/post', tags=['约拍管理-内容审核'])


@yuepaiPostController.get('/list', summary='作品列表')
async def get_post_list(
    type: str = Query(None), audit_status: str = Query(None),
    status: str = Query(None), keyword: str = Query(None),
    page_num: int = Query(1), page_size: int = Query(20),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    query = YuepaiPostQuery(type=type, audit_status=audit_status, status=status, keyword=keyword, page_num=page_num, page_size=page_size)
    result = await YuepaiPostService.get_post_list_services(db, query)
    return ResponseUtil.success(data=result)


@yuepaiPostController.put('/audit', summary='审核作品')
async def audit_post(
    post_id: int, audit_status: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    await YuepaiPostService.audit_post_services(db, post_id, audit_status)
    return ResponseUtil.success(msg='审核成功')
