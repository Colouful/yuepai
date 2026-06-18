"""风控中心接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_admin_service import RiskService
from module_yuepai.entity.vo.yuepai_admin_vo import RiskQuery, RiskSave
from utils.response_util import ResponseUtil

riskController = APIRouter(prefix='/yuepai/risk', tags=['约拍管理-风控中心'])


@riskController.get('/list', summary='风控记录列表')
async def risk_list(
    type: str = Query(None), status: str = Query(None),
    risk_level: str = Query(None), page_num: int = Query(1), page_size: int = Query(20),
    db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user),
):
    query = RiskQuery(type=type, status=status, risk_level=risk_level, page_num=page_num, page_size=page_size)
    result = await RiskService.get_list(db, query)
    return ResponseUtil.success(data=result)


@riskController.get('/{id}', summary='风控详情')
async def risk_detail(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user)):
    item = await RiskService.get_detail(db, id)
    return ResponseUtil.success(data=item) if item else Fail(msg='记录不存在')


@riskController.post('/save', summary='保存风控记录')
async def risk_save(
    body: RiskSave, db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    data = body.model_dump(exclude_none=True)
    await RiskService.save(db, data)
    return ResponseUtil.success(msg='保存成功')


@riskController.put('/status', summary='更新风控状态')
async def risk_status(
    id: int = Query(...), status: str = Query(...),
    db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user),
):
    operator = getattr(current_user, 'user_name', 'admin')
    await RiskService.update_status(db, id, status, operator)
    return ResponseUtil.success(msg='操作成功')
