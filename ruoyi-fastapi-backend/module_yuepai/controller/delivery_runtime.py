from typing import Annotated

from fastapi import Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.delivery_vo import DeliveryDecision, DeliverySubmit
from module_yuepai.service.delivery_service import DeliveryService
from utils.response_util import ResponseUtil


async def get_latest_delivery(
    order_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await DeliveryService.latest(query_db, order_id, current_user.user.user_id)
    return ResponseUtil.success(data=data)


async def list_delivery_versions(
    order_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    rows = await DeliveryService.versions(query_db, order_id, current_user.user.user_id)
    return ResponseUtil.success(rows=rows)


async def submit_delivery(
    order_id: Annotated[int, Path(ge=1)],
    payload: DeliverySubmit,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await DeliveryService.submit(query_db, order_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='作品已提交验收')


async def decide_delivery(
    order_id: Annotated[int, Path(ge=1)],
    payload: DeliveryDecision,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await DeliveryService.decide(query_db, order_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='验收结果已提交')


delivery_runtime = APIRouterPro(prefix='/yuepai/deliveries', order_num=47, tags=['91约拍Pro-作品交付'])
delivery_runtime.add_api_route('/orders/{order_id}', get_latest_delivery, methods=['GET'], dependencies=[PreAuthDependency()])
delivery_runtime.add_api_route('/orders/{order_id}/versions', list_delivery_versions, methods=['GET'], dependencies=[PreAuthDependency()])
delivery_runtime.add_api_route('/orders/{order_id}', submit_delivery, methods=['POST'], dependencies=[PreAuthDependency()])
delivery_runtime.add_api_route('/orders/{order_id}/decision', decide_delivery, methods=['POST'], dependencies=[PreAuthDependency()])
