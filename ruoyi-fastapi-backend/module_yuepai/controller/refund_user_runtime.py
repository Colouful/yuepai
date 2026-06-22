from typing import Annotated

from fastapi import Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.payment_vo import RefundCreateRequest
from module_yuepai.service.refund_service import RefundService
from utils.response_util import ResponseUtil


async def create_refund(
    order_id: Annotated[int, Path(ge=1)],
    payload: RefundCreateRequest,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await RefundService.create_request(query_db, order_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='退款申请已提交')


refund_user_runtime = APIRouterPro(prefix='/yuepai/refunds', order_num=34, tags=['91约拍Pro-退款'])
refund_user_runtime.add_api_route(
    '/orders/{order_id}',
    create_refund,
    methods=['POST'],
    summary='申请订单退款',
    dependencies=[PreAuthDependency()],
)
