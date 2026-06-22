from typing import Annotated

from fastapi import Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.core_vo import OrderTransition
from module_yuepai.service.order_flow_service import OrderFlowService
from utils.response_util import ResponseUtil


async def list_orders(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    order_status: Annotated[str | None, Query(alias='status', max_length=32)] = None,
) -> Response:
    rows = await OrderFlowService.list_orders(query_db, current_user.user.user_id, order_status)
    return ResponseUtil.success(rows=rows)


async def get_order(
    order_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await OrderFlowService.detail(query_db, order_id, current_user.user.user_id)
    return ResponseUtil.success(data=result)


async def transition_order(
    order_id: Annotated[int, Path(ge=1)],
    payload: OrderTransition,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await OrderFlowService.transition(query_db, order_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='订单状态已更新')


order_runtime = APIRouterPro(prefix='/yuepai/orders', order_num=32, tags=['91约拍Pro-订单'])
order_runtime.add_api_route('', list_orders, methods=['GET'], summary='我的订单列表', dependencies=[PreAuthDependency()])
order_runtime.add_api_route(
    '/{order_id}', get_order, methods=['GET'], summary='订单详情', dependencies=[PreAuthDependency()]
)
order_runtime.add_api_route(
    '/{order_id}/transition',
    transition_order,
    methods=['POST'],
    summary='订单状态流转',
    dependencies=[PreAuthDependency()],
)
