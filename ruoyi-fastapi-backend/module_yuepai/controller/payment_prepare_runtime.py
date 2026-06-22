from typing import Annotated

from fastapi import Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.payment_secure_vo import SecurePaymentPrepare
from module_yuepai.service.payment_prepare_service import PaymentPrepareService
from utils.response_util import ResponseUtil


async def prepare_payment(
    order_id: Annotated[int, Path(ge=1)],
    payload: SecurePaymentPrepare,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await PaymentPrepareService.prepare(query_db, order_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='支付参数已生成')


payment_prepare_runtime = APIRouterPro(prefix='/yuepai/payments', order_num=34, tags=['91约拍Pro-支付'])
payment_prepare_runtime.add_api_route(
    '/orders/{order_id}/prepare',
    prepare_payment,
    methods=['POST'],
    summary='创建微信支付预订单',
    dependencies=[PreAuthDependency()],
)
