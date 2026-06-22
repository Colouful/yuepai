"""create order delivery table

Revision ID: yp_delivery_0006
Revises: yp_message_0005
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'yp_delivery_0006'
down_revision: str | None = 'yp_message_0005'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'yp_delivery',
        sa.Column('delivery_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('order_id', sa.BigInteger(), nullable=False),
        sa.Column('uploader_user_id', sa.BigInteger(), nullable=False),
        sa.Column('delivery_version', sa.Integer(), nullable=False),
        sa.Column('original_assets_json', sa.Text(), nullable=True),
        sa.Column('retouched_assets_json', sa.Text(), nullable=False),
        sa.Column('note', sa.String(1000), nullable=True),
        sa.Column('status', sa.String(24), server_default='submitted', nullable=False),
        sa.Column('revision_reason', sa.String(1000), nullable=True),
        sa.Column('request_id', sa.String(64), nullable=False),
        sa.Column('submitted_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('accepted_at', sa.DateTime(), nullable=True),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['yp_order.order_id'], name='fk_yp_delivery_order'),
        sa.ForeignKeyConstraint(['uploader_user_id'], ['sys_user.user_id'], name='fk_yp_delivery_uploader'),
        sa.PrimaryKeyConstraint('delivery_id'),
        sa.UniqueConstraint('order_id', 'delivery_version', name='uk_yp_delivery_order_version'),
        sa.UniqueConstraint('request_id', name='uk_yp_delivery_request_id'),
        comment='约拍作品交付版本',
    )
    op.create_index('idx_yp_delivery_order_status', 'yp_delivery', ['order_id', 'status'])


def downgrade() -> None:
    op.drop_index('idx_yp_delivery_order_status', table_name='yp_delivery')
    op.drop_table('yp_delivery')
