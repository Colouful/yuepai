from typing import Annotated

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.creator_vo import CreatorProfileUpsert, CreatorWorkCreate, ServicePackageCreate
from module_yuepai.service.creator_manage_service import CreatorManageService
from utils.response_util import ResponseUtil


async def save_profile(
    payload: CreatorProfileUpsert,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await CreatorManageService.upsert_profile(query_db, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='创作者资料已提交审核')


async def create_work(
    payload: CreatorWorkCreate,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await CreatorManageService.create_work(query_db, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='作品已提交审核')


async def create_package(
    payload: ServicePackageCreate,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await CreatorManageService.create_package(query_db, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='服务套餐已提交审核')


creator_center_runtime = APIRouterPro(prefix='/yuepai/creator-center', order_num=43, tags=['91约拍Pro-创作者中心'])
creator_center_runtime.add_api_route('/profile', save_profile, methods=['PUT'], dependencies=[PreAuthDependency()])
creator_center_runtime.add_api_route('/works', create_work, methods=['POST'], dependencies=[PreAuthDependency()])
creator_center_runtime.add_api_route('/packages', create_package, methods=['POST'], dependencies=[PreAuthDependency()])
