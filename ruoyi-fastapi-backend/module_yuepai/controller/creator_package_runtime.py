from typing import Annotated

from fastapi import Path, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from module_yuepai.service.creator_public_service import CreatorPublicService
from utils.response_util import ResponseUtil


async def creator_packages(
    creator_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    rows = await CreatorPublicService.packages(query_db, creator_id)
    return ResponseUtil.success(rows=rows)


creator_package_runtime = APIRouterPro(prefix='/yuepai/creator-packages', order_num=38, tags=['91约拍Pro-创作者套餐'])
creator_package_runtime.add_api_route('/{creator_id}', creator_packages, methods=['GET'], summary='创作者服务套餐')
