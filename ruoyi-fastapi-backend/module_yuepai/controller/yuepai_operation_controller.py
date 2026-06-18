"""运营管理接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_admin_service import OperationService
from module_yuepai.entity.vo.yuepai_admin_vo import OperationQuery, OperationSave
from utils.response_util import ResponseUtil

operationController = APIRouter(prefix='/yuepai/operation', tags=['约拍管理-运营管理'])


@operationController.get('/list', summary='运营内容列表')
async def op_list(
    type: str = Query(None), status: str = Query(None),
    page_num: int = Query(1), page_size: int = Query(50),
    db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user),
):
    query = OperationQuery(type=type, status=status, page_num=page_num, page_size=page_size)
    result = await OperationService.get_list(db, query)
    return ResponseUtil.success(data=result)


@operationController.get('/{id}', summary='运营详情')
async def op_detail(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user)):
    item = await OperationService.get_detail(db, id)
    return ResponseUtil.success(data=item) if item else Fail(msg='记录不存在')


@operationController.post('/save', summary='保存运营内容')
async def op_save(
    body: OperationSave, db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    data = body.model_dump(exclude_none=True)
    if not data.get('create_by'):
        data['create_by'] = getattr(current_user, 'user_name', 'admin')
    await OperationService.save(db, data)
    return ResponseUtil.success(msg='保存成功')


@operationController.delete('/{id}', summary='删除运营内容')
async def op_delete(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user)):
    await OperationService.delete(db, id)
    return ResponseUtil.success(msg='删除成功')
