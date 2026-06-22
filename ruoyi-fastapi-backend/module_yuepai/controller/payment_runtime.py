from typing import Annotated

from fastapi import Path, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.payment_vo import PaymentPrepareRequest
from module_yuepai.service.payment_service import PaymentService
from utils.response_util import ResponseUtil


async def prepare_payment(
    order_id: Annotated[int, Path(ge=1)],
    payload: PaymentPrepareRequest,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    result = await PaymentService.prepare(query_db, order_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=result, msg='支付参数已生成')


async def wechat_payment_notify(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    body = await request.body()
    timestamp = request.headers.get('Wechatpay-Timestamp', '')
    nonce = request.headers.get('Wechatpay-Nonce', '')
    signature = request.headers.get('Wechatpay-Signature', '')
    if not timestamp or not nonce or not signature:
        return JSONResponse(status_code=400, content={'code': 'FAIL', 'message': '回调签名头缺失'})
    try:
        await PaymentService.process_wechat_notification(
            query_db,
            body=body,
            timestamp=timestamp,
            nonce=nonce,
            signature=signature,
        )
        return JSONResponse(status_code=200, content={'code': 'SUCCESS', 'message': '成功'})
    except Exception as exc:
        return JSONResponse(status_code=400, content={'code': 'FAIL', 'message': str(exc)[:200]})


payment_runtime = APIRouterPro(prefix='/yuepai/payments', order_num=33, tags=['91约拍Pro-支付'])
payment_runtime.add_api_route(
    '/orders/{order_id}/prepare',
    prepare_payment,
    methods=['POST'],
    summary='创建微信支付预订单',
    dependencies=[PreAuthDependency()],
)
payment_runtime.add_api_route(
    '/wechat/notify',
    wechat_payment_notify,
    methods=['POST'],
    summary='微信支付结果回调',
)
