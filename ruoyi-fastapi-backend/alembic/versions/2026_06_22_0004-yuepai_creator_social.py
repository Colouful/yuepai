"""create creator review follow and favorite tables

Revision ID: yp_creator_social_0004
Revises: yp_creator_0003
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'yp_creator_social_0004'
down_revision: str | None = 'yp_creator_0003'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'yp_creator_review',
        sa.Column('review_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('order_id', sa.BigInteger(), nullable=False),
        sa.Column('creator_id', sa.BigInteger(), nullable=False),
        sa.Column('reviewer_user_id', sa.BigInteger(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('service_rating', sa.Integer(), nullable=False),
        sa.Column('communication_rating', sa.Integer(), nullable=False),
        sa.Column('delivery_rating', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(1000), nullable=False),
        sa.Column('assets_json', sa.Text(), nullable=True),
        sa.Column('creator_reply', sa.String(500), nullable=True),
        sa.Column('status', sa.String(20), server_default='published', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['yp_order.order_id'], name='fk_yp_review_order'),
        sa.ForeignKeyConstraint(['creator_id'], ['yp_creator_profile.creator_id'], name='fk_yp_review_creator'),
        sa.ForeignKeyConstraint(['reviewer_user_id'], ['sys_user.user_id'], name='fk_yp_review_user'),
        sa.PrimaryKeyConstraint('review_id'),
        sa.UniqueConstraint('order_id', name='uk_yp_review_order'),
        comment='订单创作者评价',
    )
    op.create_index('idx_yp_review_creator_status', 'yp_creator_review', ['creator_id', 'status'])

    op.create_table(
        'yp_creator_follow',
        sa.Column('follow_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('follower_user_id', sa.BigInteger(), nullable=False),
        sa.Column('creator_id', sa.BigInteger(), nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['follower_user_id'], ['sys_user.user_id'], name='fk_yp_follow_user'),
        sa.ForeignKeyConstraint(['creator_id'], ['yp_creator_profile.creator_id'], name='fk_yp_follow_creator'),
        sa.PrimaryKeyConstraint('follow_id'),
        sa.UniqueConstraint('follower_user_id', 'creator_id', name='uk_yp_follow_user_creator'),
        comment='用户关注创作者',
    )
    op.create_index('idx_yp_follow_creator_time', 'yp_creator_follow', ['creator_id', 'create_time'])

    op.create_table(
        'yp_work_favorite',
        sa.Column('favorite_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('work_id', sa.BigInteger(), nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['sys_user.user_id'], name='fk_yp_favorite_user'),
        sa.ForeignKeyConstraint(['work_id'], ['yp_creator_work.work_id'], name='fk_yp_favorite_work'),
        sa.PrimaryKeyConstraint('favorite_id'),
        sa.UniqueConstraint('user_id', 'work_id', name='uk_yp_favorite_user_work'),
        comment='用户收藏作品',
    )
    op.create_index('idx_yp_favorite_work_time', 'yp_work_favorite', ['work_id', 'create_time'])


def downgrade() -> None:
    op.drop_index('idx_yp_favorite_work_time', table_name='yp_work_favorite')
    op.drop_table('yp_work_favorite')
    op.drop_index('idx_yp_follow_creator_time', table_name='yp_creator_follow')
    op.drop_table('yp_creator_follow')
    op.drop_index('idx_yp_review_creator_status', table_name='yp_creator_review')
    op.drop_table('yp_creator_review')
