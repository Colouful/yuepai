from typing import Annotated

from fastapi import Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.service.creator_social_service import CreatorSocialService
from utils.response_util import ResponseUtil


async def relationship_state(
    creator_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    work_id: Annotated[int | None, Query(alias='workId', ge=1)] = None,
) -> Response:
    data = await CreatorSocialService.state(query_db, current_user.user.user_id, creator_id, work_id)
    return ResponseUtil.success(data=data)


async def follow_creator(
    creator_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await CreatorSocialService.follow(query_db, current_user.user.user_id, creator_id)
    return ResponseUtil.success(data=data, msg='关注成功')


async def unfollow_creator(
    creator_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await CreatorSocialService.unfollow(query_db, current_user.user.user_id, creator_id)
    return ResponseUtil.success(data=data, msg='已取消关注')


async def favorite_work(
    work_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await CreatorSocialService.favorite_work(query_db, current_user.user.user_id, work_id)
    return ResponseUtil.success(data=data, msg='收藏成功')


async def unfavorite_work(
    work_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await CreatorSocialService.unfavorite_work(query_db, current_user.user.user_id, work_id)
    return ResponseUtil.success(data=data, msg='已取消收藏')


creator_social_runtime = APIRouterPro(prefix='/yuepai/social', order_num=41, tags=['91约拍Pro-关注收藏'])
creator_social_runtime.add_api_route(
    '/creators/{creator_id}/state', relationship_state, methods=['GET'], dependencies=[PreAuthDependency()]
)
creator_social_runtime.add_api_route(
    '/creators/{creator_id}/follow', follow_creator, methods=['POST'], dependencies=[PreAuthDependency()]
)
creator_social_runtime.add_api_route(
    '/creators/{creator_id}/follow', unfollow_creator, methods=['DELETE'], dependencies=[PreAuthDependency()]
)
creator_social_runtime.add_api_route(
    '/works/{work_id}/favorite', favorite_work, methods=['POST'], dependencies=[PreAuthDependency()]
)
creator_social_runtime.add_api_route(
    '/works/{work_id}/favorite', unfavorite_work, methods=['DELETE'], dependencies=[PreAuthDependency()]
)
