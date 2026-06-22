"""create yuepai payment tables

Revision ID: yp_payment_0002
Revises: yp_mvp_core_0001
Create Date: 2026-06-22 00:02:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'yp_payment_0002'
down_revision: str | None = 'yp_mvp_core_0001'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'yp_payment',
        sa.Column('payment_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('payment_no', sa.String(length=40), nullable=False),
        sa.Column('order_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('provider', sa.String(length=20), server_default='wechat', nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.String(length=8), server_default='CNY', nullable=False),
        sa.Column('status', sa.String(length=20), server_default='created', nullable=False),
        sa.Column('request_id', sa.String(length=64), nullable=False),
        sa.Column('provider_transaction_id', sa.String(length=64), nullable=True),
        sa.Column('prepay_id', sa.String(length=128), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('failure_code', sa.String(length=64), nullable=True),
        sa.Column('failure_message', sa.String(length=500), nullable=True),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['yp_order.order_id'], name='fk_yp_payment_order'),
        sa.ForeignKeyConstraint(['user_id'], ['sys_user.user_id'], name='fk_yp_payment_user'),
        sa.PrimaryKeyConstraint('payment_id'),
        sa.UniqueConstraint('payment_no', name='uk_yp_payment_no'),
        sa.UniqueConstraint('request_id', name='uk_yp_payment_request_id'),
        comment='约拍支付单',
    )
    op.create_index('idx_yp_payment_order_status', 'yp_payment', ['order_id', 'status'])

    op.create_table(
        'yp_payment_event',
        sa.Column('event_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('payment_id', sa.BigInteger(), nullable=True),
        sa.Column('provider_event_id', sa.String(length=128), nullable=False),
        sa.Column('event_type', sa.String(length=64), nullable=False),
        sa.Column('payload_digest', sa.String(length=64), nullable=False),
        sa.Column('process_status', sa.String(length=20), server_default='received', nullable=False),
        sa.Column('error_message', sa.String(length=500), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['payment_id'], ['yp_payment.payment_id'], name='fk_yp_payment_event_payment'),
        sa.PrimaryKeyConstraint('event_id'),
        sa.UniqueConstraint('provider_event_id', name='uk_yp_payment_event_provider_id'),
        comment='支付回调事件',
    )
    op.create_index('idx_yp_payment_event_payment_time', 'yp_payment_event', ['payment_id', 'create_time'])

    op.create_table(
        'yp_refund',
        sa.Column('refund_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('refund_no', sa.String(length=40), nullable=False),
        sa.Column('order_id', sa.BigInteger(), nullable=False),
        sa.Column('payment_id', sa.BigInteger(), nullable=False),
        sa.Column('applicant_user_id', sa.BigInteger(), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('reason', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='requested', nullable=False),
        sa.Column('request_id', sa.String(length=64), nullable=False),
        sa.Column('provider_refund_id', sa.String(length=64), nullable=True),
        sa.Column('evidence_json', sa.Text(), nullable=True),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['applicant_user_id'], ['sys_user.user_id'], name='fk_yp_refund_user'),
        sa.ForeignKeyConstraint(['order_id'], ['yp_order.order_id'], name='fk_yp_refund_order'),
        sa.ForeignKeyConstraint(['payment_id'], ['yp_payment.payment_id'], name='fk_yp_refund_payment'),
        sa.PrimaryKeyConstraint('refund_id'),
        sa.UniqueConstraint('refund_no', name='uk_yp_refund_no'),
        sa.UniqueConstraint('request_id', name='uk_yp_refund_request_id'),
        comment='约拍退款单',
    )
    op.create_index('idx_yp_refund_order_status', 'yp_refund', ['order_id', 'status'])


def downgrade() -> None:
    op.drop_index('idx_yp_refund_order_status', table_name='yp_refund')
    op.drop_table('yp_refund')
    op.drop_index('idx_yp_payment_event_payment_time', table_name='yp_payment_event')
    op.drop_table('yp_payment_event')
    op.drop_index('idx_yp_payment_order_status', table_name='yp_payment')
    op.drop_table('yp_payment')
