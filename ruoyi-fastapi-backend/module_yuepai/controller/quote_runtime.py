from typing import Annotated

from fastapi import Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.core_vo import QuoteAccept, QuoteCreate
from module_yuepai.service.order_flow_service import OrderFlowService
from utils.response_util import ResponseUtil


async def create_quote(
    payload: QuoteCreate,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await OrderFlowService.create_quote(query_db, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='报价已发送')


async def accept_quote(
    quote_id: Annotated[int, Path(ge=1)],
    payload: QuoteAccept,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await OrderFlowService.accept_quote(query_db, quote_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='订单已创建')


quote_runtime = APIRouterPro(prefix='/yuepai/quotes', order_num=31, tags=['91约拍Pro-报价'])
quote_runtime.add_api_route('', create_quote, methods=['POST'], summary='创建服务报价', dependencies=[PreAuthDependency()])
quote_runtime.add_api_route(
    '/{quote_id}/accept',
    accept_quote,
    methods=['POST'],
    summary='接受报价并创建订单',
    dependencies=[PreAuthDependency()],
)
