from typing import Annotated

from fastapi import Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.core_vo import QuoteAccept, QuoteCreate
from module_yuepai.entity.vo.quote_vo import QuoteStatusAction
from module_yuepai.service.order_flow_service import OrderFlowService
from module_yuepai.service.quote_action_service import QuoteActionService
from module_yuepai.service.quote_query_service import QuoteQueryService
from utils.response_util import ResponseUtil


async def list_quotes(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    box: Annotated[str, Query(pattern='^(all|received|sent)$')] = 'all',
    quote_status: Annotated[str | None, Query(alias='status', max_length=20)] = None,
    page_num: Annotated[int, Query(alias='pageNum', ge=1)] = 1,
    page_size: Annotated[int, Query(alias='pageSize', ge=1, le=50)] = 20,
) -> Response:
    result = await QuoteQueryService.list_mine(
        query_db,
        current_user.user.user_id,
        box,
        quote_status,
        page_num,
        page_size,
    )
    return ResponseUtil.success(rows=result['rows'], dict_content={'hasMore': result['hasMore']})


async def get_quote(
    quote_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await QuoteQueryService.detail(query_db, quote_id, current_user.user.user_id)
    return ResponseUtil.success(data=result)


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
    result = await QuoteActionService.accept(query_db, quote_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='订单已创建')


async def reject_quote(
    quote_id: Annotated[int, Path(ge=1)],
    payload: QuoteStatusAction,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await QuoteActionService.reject(query_db, quote_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='报价已拒绝')


async def withdraw_quote(
    quote_id: Annotated[int, Path(ge=1)],
    payload: QuoteStatusAction,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await QuoteActionService.withdraw(query_db, quote_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='报价已撤回')


quote_runtime = APIRouterPro(prefix='/yuepai/quotes', order_num=31, tags=['91约拍Pro-报价'])
quote_runtime.add_api_route('', list_quotes, methods=['GET'], summary='我的报价列表', dependencies=[PreAuthDependency()])
quote_runtime.add_api_route('', create_quote, methods=['POST'], summary='创建服务报价', dependencies=[PreAuthDependency()])
quote_runtime.add_api_route('/{quote_id}', get_quote, methods=['GET'], summary='报价详情', dependencies=[PreAuthDependency()])
quote_runtime.add_api_route('/{quote_id}/accept', accept_quote, methods=['POST'], summary='接受报价并创建订单', dependencies=[PreAuthDependency()])
quote_runtime.add_api_route('/{quote_id}/reject', reject_quote, methods=['POST'], summary='拒绝报价', dependencies=[PreAuthDependency()])
quote_runtime.add_api_route('/{quote_id}/withdraw', withdraw_quote, methods=['POST'], summary='撤回报价', dependencies=[PreAuthDependency()])
