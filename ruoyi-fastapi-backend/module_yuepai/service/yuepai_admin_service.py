"""约拍管理后台Service"""
from sqlalchemy.ext.asyncio import AsyncSession
from module_yuepai.dao.yuepai_admin_dao import CertReviewDao, AftersaleDao, OperationDao, RiskDao
from module_yuepai.entity.vo.yuepai_admin_vo import (
    CertReviewQuery, AftersaleQuery, OperationQuery, RiskQuery
)
from utils.page_util import PageUtil


class CertReviewService:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: CertReviewQuery):
        q = await CertReviewDao.get_list(db, query)
        return await PageUtil.paginate(db, q, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def get_detail(cls, db: AsyncSession, id: int):
        return await CertReviewDao.get_by_id(db, id)

    @classmethod
    async def audit(cls, db: AsyncSession, id: int, status: str, reviewer: str, remark: str):
        await CertReviewDao.audit(db, id, status, reviewer, remark)


class AftersaleService:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: AftersaleQuery):
        q = await AftersaleDao.get_list(db, query)
        return await PageUtil.paginate(db, q, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def get_detail(cls, db: AsyncSession, id: int):
        return await AftersaleDao.get_by_id(db, id)

    @classmethod
    async def handle(cls, db: AsyncSession, id: int, status: str, handler: str, result: str):
        await AftersaleDao.handle(db, id, status, handler, result)


class OperationService:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: OperationQuery):
        q = await OperationDao.get_list(db, query)
        return await PageUtil.paginate(db, q, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def get_detail(cls, db: AsyncSession, id: int):
        return await OperationDao.get_by_id(db, id)

    @classmethod
    async def save(cls, db: AsyncSession, data: dict):
        await OperationDao.save(db, data)

    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        await OperationDao.delete(db, id)


class RiskService:
    @classmethod
    async def get_list(cls, db: AsyncSession, query: RiskQuery):
        q = await RiskDao.get_list(db, query)
        return await PageUtil.paginate(db, q, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def get_detail(cls, db: AsyncSession, id: int):
        return await RiskDao.get_by_id(db, id)

    @classmethod
    async def save(cls, db: AsyncSession, data: dict):
        await RiskDao.save(db, data)

    @classmethod
    async def update_status(cls, db: AsyncSession, id: int, status: str, operator: str):
        await RiskDao.update_status(db, id, status, operator)
