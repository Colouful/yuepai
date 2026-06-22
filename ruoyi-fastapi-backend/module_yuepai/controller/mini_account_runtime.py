from typing import Annotated

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.mini_account_vo import MiniAccountBind
from module_yuepai.service.mini_account_service import MiniAccountService
from utils.response_util import ResponseUtil


async def account_status(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await MiniAccountService.status(query_db, current_user.user.user_id)
    return ResponseUtil.success(data=data)


async def bind_account(
    payload: MiniAccountBind,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await MiniAccountService.bind(query_db, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='微信小程序账号已绑定')


mini_account_runtime = APIRouterPro(prefix='/yuepai/mini-account', order_num=48, tags=['91约拍Pro-小程序账号'])
mini_account_runtime.add_api_route('/status', account_status, methods=['GET'], dependencies=[PreAuthDependency()])
mini_account_runtime.add_api_route('/bind', bind_account, methods=['POST'], dependencies=[PreAuthDependency()])
