from typing import Annotated

from fastapi import Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import PreAuthDependency
from common.router import APIRouterPro
from module_yuepai.entity.vo.creator_vo import AuditDecision
from module_yuepai.service.creator_manage_service import CreatorManageService
from utils.response_util import ResponseUtil


async def audit_profile(
    creator_id: Annotated[int, Path(ge=1)],
    payload: AuditDecision,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    data = await CreatorManageService.audit_profile(query_db, creator_id, payload.approved, payload.reason)
    return ResponseUtil.success(data=data, msg='创作者资料审核完成')


async def audit_work(
    work_id: Annotated[int, Path(ge=1)],
    payload: AuditDecision,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    data = await CreatorManageService.audit_work(query_db, work_id, payload.approved)
    return ResponseUtil.success(data=data, msg='作品审核完成')


async def audit_package(
    package_id: Annotated[int, Path(ge=1)],
    payload: AuditDecision,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    data = await CreatorManageService.audit_package(query_db, package_id, payload.approved)
    return ResponseUtil.success(data=data, msg='套餐审核完成')


creator_audit_runtime = APIRouterPro(prefix='/yuepai/admin/creator-audit', order_num=44, tags=['91约拍Pro-创作者审核'])
creator_audit_runtime.add_api_route(
    '/profiles/{creator_id}',
    audit_profile,
    methods=['PUT'],
    dependencies=[PreAuthDependency(), UserInterfaceAuthDependency('yuepai:creator:audit')],
)
creator_audit_runtime.add_api_route(
    '/works/{work_id}',
    audit_work,
    methods=['PUT'],
    dependencies=[PreAuthDependency(), UserInterfaceAuthDependency('yuepai:work:audit')],
)
creator_audit_runtime.add_api_route(
    '/packages/{package_id}',
    audit_package,
    methods=['PUT'],
    dependencies=[PreAuthDependency(), UserInterfaceAuthDependency('yuepai:package:audit')],
)
