"""create creator profile work and package tables

Revision ID: yp_creator_0003
Revises: yp_payment_0002
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'yp_creator_0003'
down_revision: str | None = 'yp_payment_0002'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'yp_creator_profile',
        sa.Column('creator_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('role_code', sa.String(32), nullable=False),
        sa.Column('display_name', sa.String(50), nullable=False),
        sa.Column('headline', sa.String(120), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('cover_url', sa.String(500), nullable=True),
        sa.Column('city_code', sa.String(20), nullable=False),
        sa.Column('service_city_json', sa.Text(), nullable=True),
        sa.Column('tags_json', sa.Text(), nullable=True),
        sa.Column('years_experience', sa.Integer(), server_default='0', nullable=False),
        sa.Column('base_price', sa.Numeric(12, 2), nullable=True),
        sa.Column('response_rate', sa.Integer(), server_default='0', nullable=False),
        sa.Column('completed_orders', sa.Integer(), server_default='0', nullable=False),
        sa.Column('rating', sa.Numeric(3, 2), server_default='0', nullable=False),
        sa.Column('review_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('follower_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('accept_mutual', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.Column('certification_status', sa.String(20), server_default='pending', nullable=False),
        sa.Column('status', sa.String(20), server_default='draft', nullable=False),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['sys_user.user_id'], name='fk_yp_creator_user'),
        sa.PrimaryKeyConstraint('creator_id'),
        sa.UniqueConstraint('user_id', 'role_code', name='uk_yp_creator_user_role'),
        comment='约拍创作者多身份资料',
    )
    op.create_index('idx_yp_creator_role_city_status', 'yp_creator_profile', ['role_code', 'city_code', 'status'])
    op.create_index('idx_yp_creator_rating_orders', 'yp_creator_profile', ['rating', 'completed_orders'])

    op.create_table(
        'yp_creator_work',
        sa.Column('work_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('creator_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(32), nullable=False),
        sa.Column('cover_url', sa.String(500), nullable=False),
        sa.Column('assets_json', sa.Text(), nullable=False),
        sa.Column('tags_json', sa.Text(), nullable=True),
        sa.Column('city_code', sa.String(20), nullable=True),
        sa.Column('shot_date', sa.Date(), nullable=True),
        sa.Column('favorite_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('view_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('audit_status', sa.String(20), server_default='pending', nullable=False),
        sa.Column('status', sa.String(20), server_default='draft', nullable=False),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['yp_creator_profile.creator_id'], name='fk_yp_work_creator'),
        sa.PrimaryKeyConstraint('work_id'),
        comment='创作者作品',
    )
    op.create_index('idx_yp_work_creator_status', 'yp_creator_work', ['creator_id', 'status'])
    op.create_index('idx_yp_work_category_status', 'yp_creator_work', ['category', 'status'])
    op.create_index('idx_yp_work_popularity', 'yp_creator_work', ['favorite_count', 'view_count'])

    op.create_table(
        'yp_service_package',
        sa.Column('package_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('creator_id', sa.BigInteger(), nullable=False),
        sa.Column('package_name', sa.String(80), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('cover_url', sa.String(500), nullable=True),
        sa.Column('price', sa.Numeric(12, 2), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('original_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('retouched_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('delivery_days', sa.Integer(), server_default='7', nullable=False),
        sa.Column('revision_count', sa.Integer(), server_default='1', nullable=False),
        sa.Column('includes_json', sa.Text(), nullable=True),
        sa.Column('excludes_json', sa.Text(), nullable=True),
        sa.Column('addons_json', sa.Text(), nullable=True),
        sa.Column('booking_notice', sa.Text(), nullable=True),
        sa.Column('refund_rule', sa.Text(), nullable=True),
        sa.Column('audit_status', sa.String(20), server_default='pending', nullable=False),
        sa.Column('status', sa.String(20), server_default='draft', nullable=False),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['yp_creator_profile.creator_id'], name='fk_yp_package_creator'),
        sa.PrimaryKeyConstraint('package_id'),
        comment='创作者服务套餐',
    )
    op.create_index('idx_yp_package_creator_status', 'yp_service_package', ['creator_id', 'status'])
    op.create_index('idx_yp_package_price', 'yp_service_package', ['price'])


def downgrade() -> None:
    op.drop_index('idx_yp_package_price', table_name='yp_service_package')
    op.drop_index('idx_yp_package_creator_status', table_name='yp_service_package')
    op.drop_table('yp_service_package')
    op.drop_index('idx_yp_work_popularity', table_name='yp_creator_work')
    op.drop_index('idx_yp_work_category_status', table_name='yp_creator_work')
    op.drop_index('idx_yp_work_creator_status', table_name='yp_creator_work')
    op.drop_table('yp_creator_work')
    op.drop_index('idx_yp_creator_rating_orders', table_name='yp_creator_profile')
    op.drop_index('idx_yp_creator_role_city_status', table_name='yp_creator_profile')
    op.drop_table('yp_creator_profile')
