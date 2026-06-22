from typing import Annotated

from fastapi import Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from module_yuepai.service.creator_public_service import CreatorPublicService
from utils.response_util import ResponseUtil


async def list_public_reviews(
    creator_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: Annotated[int, Query(alias='pageNum', ge=1)] = 1,
    page_size: Annotated[int, Query(alias='pageSize', ge=1, le=50)] = 20,
) -> Response:
    result = await CreatorPublicService.reviews(query_db, creator_id, page_num, page_size)
    return ResponseUtil.success(rows=result['rows'], dict_content={'total': result['total']})


review_public_runtime = APIRouterPro(prefix='/yuepai/reviews', order_num=39, tags=['91约拍Pro-评价'])
review_public_runtime.add_api_route('/creator/{creator_id}', list_public_reviews, methods=['GET'], summary='创作者公开评价')
