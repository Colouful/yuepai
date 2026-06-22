from typing import Annotated

from fastapi import Path, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_yuepai.entity.vo.message_vo import ConversationCreate, MessageCreate
from module_yuepai.service.message_service import MessageService
from utils.response_util import ResponseUtil


async def create_conversation(
    payload: ConversationCreate,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await MessageService.create_conversation(query_db, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data)


async def list_conversations(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    rows = await MessageService.list_conversations(query_db, current_user.user.user_id)
    return ResponseUtil.success(rows=rows)


async def list_messages(
    conversation_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    before_id: Annotated[int | None, Query(alias='beforeId', ge=1)] = None,
    page_size: Annotated[int, Query(alias='pageSize', ge=1, le=100)] = 30,
) -> Response:
    data = await MessageService.list_messages(
        query_db,
        conversation_id,
        current_user.user.user_id,
        before_id,
        page_size,
    )
    return ResponseUtil.success(rows=data['rows'], dict_content={'hasMore': data['hasMore']})


async def send_message(
    conversation_id: Annotated[int, Path(ge=1)],
    payload: MessageCreate,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    data = await MessageService.send_message(query_db, conversation_id, current_user.user.user_id, payload)
    return ResponseUtil.success(data=data, msg='消息已发送')


async def mark_read(
    conversation_id: Annotated[int, Path(ge=1)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    last_message_id: Annotated[int | None, Query(alias='lastMessageId', ge=1)] = None,
) -> Response:
    data = await MessageService.mark_read(
        query_db,
        conversation_id,
        current_user.user.user_id,
        last_message_id,
    )
    return ResponseUtil.success(data=data)


message_runtime = APIRouterPro(prefix='/yuepai/messages', order_num=46, tags=['91约拍Pro-消息'])
message_runtime.add_api_route('/conversations', list_conversations, methods=['GET'], dependencies=[PreAuthDependency()])
message_runtime.add_api_route('/conversations', create_conversation, methods=['POST'], dependencies=[PreAuthDependency()])
message_runtime.add_api_route('/conversations/{conversation_id}', list_messages, methods=['GET'], dependencies=[PreAuthDependency()])
message_runtime.add_api_route('/conversations/{conversation_id}', send_message, methods=['POST'], dependencies=[PreAuthDependency()])
message_runtime.add_api_route('/conversations/{conversation_id}/read', mark_read, methods=['POST'], dependencies=[PreAuthDependency()])
