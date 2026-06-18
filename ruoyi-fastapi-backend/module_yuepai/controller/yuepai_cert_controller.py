"""认证审核接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_yuepai.service.yuepai_admin_service import CertReviewService
from module_yuepai.entity.vo.yuepai_admin_vo import CertReviewQuery, CertReviewAudit
from utils.response_util import ResponseUtil

certController = APIRouter(prefix='/yuepai/cert', tags=['约拍管理-认证审核'])


@certController.get('/list', summary='认证审核列表')
async def cert_list(
    cert_type: str = Query(None), status: str = Query(None),
    real_name: str = Query(None), page_num: int = Query(1), page_size: int = Query(20),
    db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user),
):
    query = CertReviewQuery(cert_type=cert_type, status=status, real_name=real_name, page_num=page_num, page_size=page_size)
    result = await CertReviewService.get_list(db, query)
    return ResponseUtil.success(data=result)


@certController.get('/{id}', summary='认证详情')
async def cert_detail(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(LoginService.get_current_user)):
    item = await CertReviewService.get_detail(db, id)
    return ResponseUtil.success(data=item) if item else Fail(msg='记录不存在')


@certController.put('/audit', summary='审核认证')
async def cert_audit(
    body: CertReviewAudit, db: AsyncSession = Depends(get_db),
    current_user=Depends(LoginService.get_current_user),
):
    reviewer = getattr(current_user, 'user_name', 'admin')
    await CertReviewService.audit(db, body.id, body.status, reviewer, body.review_remark or '')
    return ResponseUtil.success(msg='审核成功')
