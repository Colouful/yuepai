from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from module_yuepai.entity.do.trade_do import YpQuote
from module_yuepai.service.order_flow_service import OrderFlowService


class QuoteQueryService:
    @classmethod
    async def list_mine(
        cls,
        db: AsyncSession,
        user_id: int,
        box: str,
        quote_status: str | None,
        page_num: int,
        page_size: int,
    ) -> dict:
        conditions = []
        if box == 'received':
            conditions.append(YpQuote.receiver_user_id == user_id)
        elif box == 'sent':
            conditions.append(YpQuote.sender_user_id == user_id)
        else:
            conditions.append(or_(YpQuote.sender_user_id == user_id, YpQuote.receiver_user_id == user_id))
        if quote_status:
            conditions.append(YpQuote.status == quote_status)
        rows = (
            await db.scalars(
                select(YpQuote)
                .where(and_(*conditions))
                .order_by(YpQuote.create_time.desc())
                .offset((page_num - 1) * page_size)
                .limit(page_size)
            )
        ).all()
        return {
            'rows': [OrderFlowService.quote_to_dict(row) for row in rows],
            'hasMore': len(rows) == page_size,
        }

    @classmethod
    async def detail(cls, db: AsyncSession, quote_id: int, user_id: int) -> dict:
        row = await db.get(YpQuote, quote_id)
        if not row:
            raise HTTPException(status_code=404, detail='报价不存在')
        if user_id not in {row.sender_user_id, row.receiver_user_id}:
            raise HTTPException(status_code=403, detail='无权查看该报价')
        return OrderFlowService.quote_to_dict(row)
