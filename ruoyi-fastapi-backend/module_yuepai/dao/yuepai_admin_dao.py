"""约拍管理后台DAO"""
from datetime import datetime
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from module_yuepai.entity.do.yuepai_admin_do import YuepaiCertReview, YuepaiAftersale, YuepaiOperation, YuepaiRisk
from module_yuepai.entity.vo.yuepai_admin_vo import (
    CertReviewQuery, AftersaleQuery, OperationQuery, RiskQuery
)


class CertReviewDao:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: CertReviewQuery):
        q = select(YuepaiCertReview)
        if query.cert_type:
            q = q.where(YuepaiCertReview.cert_type == query.cert_type)
        if query.status:
            q = q.where(YuepaiCertReview.status == query.status)
        if query.real_name:
            q = q.where(YuepaiCertReview.real_name.like(f'%{query.real_name}%'))
        return q.order_by(YuepaiCertReview.create_time.desc())

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int):
        r = await db.execute(select(YuepaiCertReview).where(YuepaiCertReview.id == id))
        return r.scalars().first()

    @classmethod
    async def audit(cls, db: AsyncSession, id: int, status: str, reviewer: str, remark: str):
        await db.execute(update(YuepaiCertReview).where(YuepaiCertReview.id == id).values(
            status=status, reviewer=reviewer, review_time=datetime.now(), review_remark=remark
        ))


class AftersaleDao:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: AftersaleQuery):
        q = select(YuepaiAftersale)
        if query.type:
            q = q.where(YuepaiAftersale.type == query.type)
        if query.status:
            q = q.where(YuepaiAftersale.status == query.status)
        if query.ticket_no:
            q = q.where(YuepaiAftersale.ticket_no.like(f'%{query.ticket_no}%'))
        return q.order_by(YuepaiAftersale.create_time.desc())

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int):
        r = await db.execute(select(YuepaiAftersale).where(YuepaiAftersale.id == id))
        return r.scalars().first()

    @classmethod
    async def handle(cls, db: AsyncSession, id: int, status: str, handler: str, result: str):
        await db.execute(update(YuepaiAftersale).where(YuepaiAftersale.id == id).values(
            status=status, handler=handler, handle_time=datetime.now(), handle_result=result
        ))


class OperationDao:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: OperationQuery):
        q = select(YuepaiOperation)
        if query.type:
            q = q.where(YuepaiOperation.type == query.type)
        if query.status:
            q = q.where(YuepaiOperation.status == query.status)
        return q.order_by(YuepaiOperation.sort_order.asc(), YuepaiOperation.create_time.desc())

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int):
        r = await db.execute(select(YuepaiOperation).where(YuepaiOperation.id == id))
        return r.scalars().first()

    @classmethod
    async def save(cls, db: AsyncSession, data: dict):
        if data.get('id'):
            await db.execute(update(YuepaiOperation).where(YuepaiOperation.id == data['id']).values(**{k: v for k, v in data.items() if k != 'id'}))
        else:
            db.add(YuepaiOperation(**data))

    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        obj = await cls.get_by_id(db, id)
        if obj:
            await db.delete(obj)


class RiskDao:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: RiskQuery):
        q = select(YuepaiRisk)
        if query.type:
            q = q.where(YuepaiRisk.type == query.type)
        if query.status:
            q = q.where(YuepaiRisk.status == query.status)
        if query.risk_level:
            q = q.where(YuepaiRisk.risk_level == query.risk_level)
        return q.order_by(YuepaiRisk.create_time.desc())

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int):
        r = await db.execute(select(YuepaiRisk).where(YuepaiRisk.id == id))
        return r.scalars().first()

    @classmethod
    async def save(cls, db: AsyncSession, data: dict):
        if data.get('id'):
            await db.execute(update(YuepaiRisk).where(YuepaiRisk.id == data['id']).values(**{k: v for k, v in data.items() if k != 'id'}))
        else:
            db.add(YuepaiRisk(**data))

    @classmethod
    async def update_status(cls, db: AsyncSession, id: int, status: str, operator: str):
        await db.execute(update(YuepaiRisk).where(YuepaiRisk.id == id).values(
            status=status, operator=operator, operate_time=datetime.now()
        ))
