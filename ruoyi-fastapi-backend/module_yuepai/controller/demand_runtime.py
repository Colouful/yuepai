from typing import Annotated

from fastapi import Path, Query, Response
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.core_vo import ApplicationCreate, DemandCreate
from module_yuepai.service.demand_service import DemandService
from utils.response_util import ResponseUtil


class DemandAuditRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    approved: bool
    reason: str | None = Field(default=None, max_length=500)


async def list_demands(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    city_code: Annotated[str | None, Query(alias='cityCode', max_length=20)] = None,
    page_num: Annotated[int, Query(alias='pageNum', ge=1)] = 1,
    page_size: Annotated[int, Query(alias='pageSize', ge=1, le=50)] = 20,
) -> Response:
    result = await DemandService.list_public(query_db, city_code, page_num, page_size)
    return ResponseUtil.success(rows=result['rows'], dict_content={'total': result['total']})


async def get_demand(
    demand_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    return ResponseUtil.success(data=await DemandService.detail(query_db, demand_id))


async def create_demand(
    payload: DemandCreate,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await DemandService.create(query_db, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='需求草稿已创建')


async def submit_demand(
    demand_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await DemandService.submit(query_db, demand_id, current_user.user.user_id)
    return ResponseUtil.success(data=result, msg='已提交审核')


async def audit_demand(
    demand_id: Annotated[int, Path(ge=1)],
    payload: DemandAuditRequest,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await DemandService.audit(query_db, demand_id, payload.approved, payload.reason)
    return ResponseUtil.success(data=result, msg='审核完成')


async def create_application(
    demand_id: Annotated[int, Path(ge=1)],
    payload: ApplicationCreate,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await DemandService.apply(query_db, demand_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='报名成功')


async def list_applications(
    demand_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    rows = await DemandService.list_applications(query_db, demand_id, current_user.user.user_id)
    return ResponseUtil.success(rows=rows)


demand_runtime = APIRouterPro(prefix='/yuepai/demands', order_num=30, tags=['91约拍Pro-约拍需求'])
demand_runtime.add_api_route('', list_demands, methods=['GET'], summary='公开需求列表')
demand_runtime.add_api_route('/{demand_id}', get_demand, methods=['GET'], summary='公开需求详情')
demand_runtime.add_api_route(
    '', create_demand, methods=['POST'], summary='创建约拍需求', dependencies=[PreAuthDependency()]
)
demand_runtime.add_api_route(
    '/{demand_id}/submit',
    submit_demand,
    methods=['POST'],
    summary='提交需求审核',
    dependencies=[PreAuthDependency()],
)
demand_runtime.add_api_route(
    '/{demand_id}/audit',
    audit_demand,
    methods=['PUT'],
    summary='审核约拍需求',
    dependencies=[PreAuthDependency(), UserInterfaceAuthDependency('yuepai:demand:audit')],
)
demand_runtime.add_api_route(
    '/{demand_id}/applications',
    create_application,
    methods=['POST'],
    summary='报名约拍需求',
    dependencies=[PreAuthDependency()],
)
demand_runtime.add_api_route(
    '/{demand_id}/applications',
    list_applications,
    methods=['GET'],
    summary='需求报名列表',
    dependencies=[PreAuthDependency()],
)
