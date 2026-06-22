from typing import Annotated

from fastapi import Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from module_yuepai.service.work_public_service import WorkPublicService
from utils.response_util import ResponseUtil


async def list_works(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    creator_id: Annotated[int | None, Query(alias='creatorId', ge=1)] = None,
    category: Annotated[str | None, Query(max_length=32)] = None,
    keyword: Annotated[str | None, Query(max_length=80)] = None,
    sort_by: Annotated[str, Query(alias='sortBy', pattern='^(latest|popular)$')] = 'latest',
    page_num: Annotated[int, Query(alias='pageNum', ge=1)] = 1,
    page_size: Annotated[int, Query(alias='pageSize', ge=1, le=50)] = 20,
) -> Response:
    result = await WorkPublicService.list_works(
        query_db,
        creator_id,
        category,
        keyword,
        sort_by,
        page_num,
        page_size,
    )
    return ResponseUtil.success(rows=result['rows'], dict_content={'total': result['total']})


async def work_detail(
    work_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    return ResponseUtil.success(data=await WorkPublicService.detail(query_db, work_id))


work_public_runtime = APIRouterPro(prefix='/yuepai/works', order_num=40, tags=['91约拍Pro-作品'])
work_public_runtime.add_api_route('', list_works, methods=['GET'], summary='公开作品列表')
work_public_runtime.add_api_route('/{work_id}', work_detail, methods=['GET'], summary='作品详情')
