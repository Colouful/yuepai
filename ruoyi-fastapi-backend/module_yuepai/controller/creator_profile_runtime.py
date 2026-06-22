from typing import Annotated

from fastapi import Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from module_yuepai.service.creator_public_service import CreatorPublicService
from utils.response_util import ResponseUtil


async def list_creators(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    role_code: Annotated[str | None, Query(alias='roleCode', max_length=32)] = None,
    city_code: Annotated[str | None, Query(alias='cityCode', max_length=20)] = None,
    keyword: Annotated[str | None, Query(max_length=80)] = None,
    tag: Annotated[str | None, Query(max_length=32)] = None,
    accept_mutual: Annotated[bool | None, Query(alias='acceptMutual')] = None,
    sort_by: Annotated[str, Query(alias='sortBy', pattern='^(latest|rating|orders|priceAsc|priceDesc)$')] = 'latest',
    page_num: Annotated[int, Query(alias='pageNum', ge=1)] = 1,
    page_size: Annotated[int, Query(alias='pageSize', ge=1, le=50)] = 20,
) -> Response:
    result = await CreatorPublicService.list_creators(
        query_db,
        role_code,
        city_code,
        keyword,
        tag,
        accept_mutual,
        sort_by,
        page_num,
        page_size,
    )
    return ResponseUtil.success(rows=result['rows'], dict_content={'total': result['total']})


async def creator_detail(
    creator_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    return ResponseUtil.success(data=await CreatorPublicService.detail(query_db, creator_id))


creator_profile_runtime = APIRouterPro(prefix='/yuepai/creators', order_num=37, tags=['91约拍Pro-创作者'])
creator_profile_runtime.add_api_route('', list_creators, methods=['GET'], summary='公开创作者列表')
creator_profile_runtime.add_api_route('/{creator_id}', creator_detail, methods=['GET'], summary='创作者详情')
