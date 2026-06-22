from typing import Annotated

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from module_yuepai.service.refund_service import RefundService


async def refund_notify(
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
        await RefundService.process_notification(
            query_db,
            body=body,
            timestamp=timestamp,
            nonce=nonce,
            signature=signature,
        )
        return JSONResponse(status_code=200, content={'code': 'SUCCESS', 'message': '成功'})
    except Exception:
        return JSONResponse(status_code=400, content={'code': 'FAIL', 'message': '处理失败'})


refund_callback = APIRouterPro(prefix='/yuepai/refunds/wechat', order_num=36, tags=['91约拍Pro-退款回调'])
refund_callback.add_api_route('/notify', refund_notify, methods=['POST'], summary='微信退款结果回调')
