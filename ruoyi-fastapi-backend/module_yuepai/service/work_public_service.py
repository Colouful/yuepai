from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from module_yuepai.entity.do.creator_do import YpCreatorProfile, YpCreatorWork
from module_yuepai.service.creator_public_service import CreatorPublicService


class WorkPublicService:
    @classmethod
    def work_dict(cls, work: YpCreatorWork, creator: YpCreatorProfile | None = None) -> dict:
        item = {
            'workId': work.work_id,
            'creatorId': work.creator_id,
            'title': work.title,
            'description': work.description,
            'category': work.category,
            'coverUrl': work.cover_url,
            'assets': CreatorPublicService.loads(work.assets_json, []),
            'tags': CreatorPublicService.loads(work.tags_json, []),
            'cityCode': work.city_code,
            'shotDate': work.shot_date,
            'favoriteCount': work.favorite_count,
            'viewCount': work.view_count,
            'createTime': work.create_time,
        }
        if creator:
            item['creator'] = {
                'creatorId': creator.creator_id,
                'userId': creator.user_id,
                'displayName': creator.display_name,
                'avatarUrl': creator.avatar_url,
                'roleCode': creator.role_code,
                'certificationStatus': creator.certification_status,
            }
        return item

    @classmethod
    async def list_works(
        cls,
        db: AsyncSession,
        creator_id: int | None,
        category: str | None,
        keyword: str | None,
        sort_by: str,
        page_num: int,
        page_size: int,
    ) -> dict:
        conditions = [YpCreatorWork.status == 'published', YpCreatorWork.audit_status == 'approved']
        if creator_id:
            conditions.append(YpCreatorWork.creator_id == creator_id)
        if category:
            conditions.append(YpCreatorWork.category == category)
        if keyword:
            pattern = f'%{keyword.strip()}%'
            conditions.append(or_(YpCreatorWork.title.like(pattern), YpCreatorWork.description.like(pattern)))
        total = await db.scalar(select(func.count()).select_from(YpCreatorWork).where(*conditions))
        order_column = (
            (YpCreatorWork.favorite_count + YpCreatorWork.view_count).desc()
            if sort_by == 'popular'
            else YpCreatorWork.create_time.desc()
        )
        result = await db.execute(
            select(YpCreatorWork, YpCreatorProfile)
            .join(YpCreatorProfile, YpCreatorProfile.creator_id == YpCreatorWork.creator_id)
            .where(*conditions, YpCreatorProfile.status == 'published')
            .order_by(order_column, YpCreatorWork.work_id.desc())
            .offset((page_num - 1) * page_size)
            .limit(page_size)
        )
        return {
            'rows': [cls.work_dict(work, creator) for work, creator in result.all()],
            'total': int(total or 0),
        }

    @classmethod
    async def detail(cls, db: AsyncSession, work_id: int) -> dict:
        result = await db.execute(
            select(YpCreatorWork, YpCreatorProfile)
            .join(YpCreatorProfile, YpCreatorProfile.creator_id == YpCreatorWork.creator_id)
            .where(
                YpCreatorWork.work_id == work_id,
                YpCreatorWork.status == 'published',
                YpCreatorWork.audit_status == 'approved',
                YpCreatorProfile.status == 'published',
            )
        )
        pair = result.first()
        if not pair:
            raise HTTPException(status_code=404, detail='作品不存在或尚未公开')
        work, creator = pair
        work.view_count += 1
        await db.commit()
        await db.refresh(work)
        return cls.work_dict(work, creator)
