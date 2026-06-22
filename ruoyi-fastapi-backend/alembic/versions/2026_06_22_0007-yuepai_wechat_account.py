"""create wechat mini-program account table

Revision ID: yp_wechat_account_0007
Revises: yp_delivery_0006
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'yp_wechat_account_0007'
down_revision: str | None = 'yp_delivery_0006'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'yp_wechat_account',
        sa.Column('account_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('subject_hash', sa.String(64), nullable=False),
        sa.Column('subject_secret', sa.Text(), nullable=False),
        sa.Column('union_hash', sa.String(64), nullable=True),
        sa.Column('union_secret', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), server_default='active', nullable=False),
        sa.Column('last_login_time', sa.DateTime(), nullable=True),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['sys_user.user_id'], name='fk_yp_wechat_account_user'),
        sa.PrimaryKeyConstraint('account_id'),
        sa.UniqueConstraint('user_id', name='uk_yp_wechat_account_user'),
        sa.UniqueConstraint('subject_hash', name='uk_yp_wechat_account_subject'),
        comment='微信小程序账号绑定',
    )
    op.create_index('idx_yp_wechat_union_hash', 'yp_wechat_account', ['union_hash'])


def downgrade() -> None:
    op.drop_index('idx_yp_wechat_union_hash', table_name='yp_wechat_account')
    op.drop_table('yp_wechat_account')
