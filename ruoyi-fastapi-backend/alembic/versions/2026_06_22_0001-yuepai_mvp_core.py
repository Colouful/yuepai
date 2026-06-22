"""create yuepai mvp core tables

Revision ID: yp_mvp_core_0001
Revises:
Create Date: 2026-06-22 00:01:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'yp_mvp_core_0001'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'yp_demand',
        sa.Column('demand_id', sa.BigInteger(), autoincrement=True, nullable=False, comment='需求ID'),
        sa.Column('owner_user_id', sa.BigInteger(), nullable=False, comment='发布用户ID'),
        sa.Column('title', sa.String(length=80), nullable=False, comment='需求标题'),
        sa.Column('description', sa.Text(), nullable=False, comment='需求描述'),
        sa.Column('demand_type', sa.String(length=32), nullable=False, comment='约拍类型'),
        sa.Column('city_code', sa.String(length=20), nullable=False, comment='城市编码'),
        sa.Column('location_name', sa.String(length=160), nullable=True, comment='地点名称'),
        sa.Column('shoot_at', sa.DateTime(), nullable=False, comment='拍摄开始时间'),
        sa.Column('duration_minutes', sa.Integer(), server_default='120', nullable=False, comment='预计时长'),
        sa.Column('roles_json', sa.Text(), nullable=False, comment='招募角色JSON'),
        sa.Column('reference_assets_json', sa.Text(), nullable=True, comment='参考图JSON'),
        sa.Column('budget_type', sa.String(length=20), nullable=False, comment='预算类型'),
        sa.Column('budget_min', sa.Numeric(12, 2), nullable=True, comment='最低预算'),
        sa.Column('budget_max', sa.Numeric(12, 2), nullable=True, comment='最高预算'),
        sa.Column('applicant_limit', sa.Integer(), server_default='20', nullable=False, comment='报名人数上限'),
        sa.Column('application_deadline', sa.DateTime(), nullable=False, comment='报名截止时间'),
        sa.Column('audit_status', sa.String(length=16), server_default='pending', nullable=False, comment='审核状态'),
        sa.Column('status', sa.String(length=16), server_default='draft', nullable=False, comment='业务状态'),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False, comment='乐观锁版本'),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column(
            'update_time',
            sa.DateTime(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['owner_user_id'], ['sys_user.user_id'], name='fk_yp_demand_owner'),
        sa.PrimaryKeyConstraint('demand_id'),
        comment='约拍需求表',
    )
    op.create_index('idx_yp_demand_city_status_time', 'yp_demand', ['city_code', 'status', 'shoot_at'])
    op.create_index('idx_yp_demand_owner_status', 'yp_demand', ['owner_user_id', 'status'])

    op.create_table(
        'yp_application',
        sa.Column('application_id', sa.BigInteger(), autoincrement=True, nullable=False, comment='报名ID'),
        sa.Column('demand_id', sa.BigInteger(), nullable=False, comment='需求ID'),
        sa.Column('applicant_user_id', sa.BigInteger(), nullable=False, comment='报名用户ID'),
        sa.Column('role_code', sa.String(length=32), nullable=False, comment='报名身份'),
        sa.Column('introduction', sa.String(length=500), nullable=False, comment='报名说明'),
        sa.Column('quote_amount', sa.Numeric(12, 2), nullable=True, comment='报名报价'),
        sa.Column('portfolio_assets_json', sa.Text(), nullable=True, comment='作品资料JSON'),
        sa.Column('status', sa.String(length=20), server_default='pending', nullable=False, comment='报名状态'),
        sa.Column('reject_reason', sa.String(length=500), nullable=True, comment='未入选原因'),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False, comment='乐观锁版本'),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['applicant_user_id'], ['sys_user.user_id'], name='fk_yp_application_user'),
        sa.ForeignKeyConstraint(['demand_id'], ['yp_demand.demand_id'], name='fk_yp_application_demand'),
        sa.PrimaryKeyConstraint('application_id'),
        sa.UniqueConstraint(
            'demand_id', 'applicant_user_id', 'role_code', name='uk_yp_application_demand_user_role'
        ),
        comment='约拍需求报名表',
    )
    op.create_index('idx_yp_application_demand_status', 'yp_application', ['demand_id', 'status'])

    op.create_table(
        'yp_quote',
        sa.Column('quote_id', sa.BigInteger(), autoincrement=True, nullable=False, comment='报价ID'),
        sa.Column('demand_id', sa.BigInteger(), nullable=True, comment='需求ID'),
        sa.Column('application_id', sa.BigInteger(), nullable=True, comment='报名ID'),
        sa.Column('sender_user_id', sa.BigInteger(), nullable=False, comment='报价方用户ID'),
        sa.Column('receiver_user_id', sa.BigInteger(), nullable=False, comment='接收方用户ID'),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False, comment='报价总额'),
        sa.Column('fee_breakdown_json', sa.Text(), nullable=False, comment='费用明细JSON'),
        sa.Column('service_snapshot_json', sa.Text(), nullable=False, comment='服务内容快照JSON'),
        sa.Column('remark', sa.String(length=1000), nullable=True, comment='补充说明'),
        sa.Column('expires_at', sa.DateTime(), nullable=False, comment='报价失效时间'),
        sa.Column('status', sa.String(length=20), server_default='pending', nullable=False, comment='报价状态'),
        sa.Column('parent_quote_id', sa.BigInteger(), nullable=True, comment='原报价ID'),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False, comment='乐观锁版本'),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['application_id'], ['yp_application.application_id'], name='fk_yp_quote_application'),
        sa.ForeignKeyConstraint(['demand_id'], ['yp_demand.demand_id'], name='fk_yp_quote_demand'),
        sa.ForeignKeyConstraint(['receiver_user_id'], ['sys_user.user_id'], name='fk_yp_quote_receiver'),
        sa.ForeignKeyConstraint(['sender_user_id'], ['sys_user.user_id'], name='fk_yp_quote_sender'),
        sa.PrimaryKeyConstraint('quote_id'),
        comment='约拍服务报价表',
    )
    op.create_index('idx_yp_quote_demand_status', 'yp_quote', ['demand_id', 'status'])
    op.create_index('idx_yp_quote_receiver_status', 'yp_quote', ['receiver_user_id', 'status'])

    op.create_table(
        'yp_order',
        sa.Column('order_id', sa.BigInteger(), autoincrement=True, nullable=False, comment='订单ID'),
        sa.Column('order_no', sa.String(length=40), nullable=False, comment='订单编号'),
        sa.Column('buyer_user_id', sa.BigInteger(), nullable=False, comment='买方用户ID'),
        sa.Column('seller_user_id', sa.BigInteger(), nullable=False, comment='卖方用户ID'),
        sa.Column('demand_id', sa.BigInteger(), nullable=True, comment='需求ID'),
        sa.Column('quote_id', sa.BigInteger(), nullable=True, comment='报价ID'),
        sa.Column('service_snapshot_json', sa.Text(), nullable=False, comment='服务内容快照JSON'),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False, comment='服务金额'),
        sa.Column('platform_fee', sa.Numeric(12, 2), server_default='0', nullable=False, comment='平台服务费'),
        sa.Column('discount_amount', sa.Numeric(12, 2), server_default='0', nullable=False, comment='优惠金额'),
        sa.Column('payable_amount', sa.Numeric(12, 2), nullable=False, comment='应付金额'),
        sa.Column('paid_amount', sa.Numeric(12, 2), server_default='0', nullable=False, comment='已付金额'),
        sa.Column('shoot_at', sa.DateTime(), nullable=False, comment='拍摄时间'),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, comment='预计服务时长'),
        sa.Column('location_snapshot_json', sa.Text(), nullable=False, comment='地点快照JSON'),
        sa.Column('contact_snapshot_json', sa.Text(), nullable=False, comment='联系人快照JSON'),
        sa.Column('remark', sa.String(length=1000), nullable=True, comment='订单备注'),
        sa.Column('status', sa.String(length=32), server_default='pending_payment', nullable=False, comment='订单状态'),
        sa.Column('payment_status', sa.String(length=20), server_default='unpaid', nullable=False, comment='支付状态'),
        sa.Column('refund_status', sa.String(length=20), server_default='none', nullable=False, comment='退款状态'),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False, comment='乐观锁版本'),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['buyer_user_id'], ['sys_user.user_id'], name='fk_yp_order_buyer'),
        sa.ForeignKeyConstraint(['demand_id'], ['yp_demand.demand_id'], name='fk_yp_order_demand'),
        sa.ForeignKeyConstraint(['quote_id'], ['yp_quote.quote_id'], name='fk_yp_order_quote'),
        sa.ForeignKeyConstraint(['seller_user_id'], ['sys_user.user_id'], name='fk_yp_order_seller'),
        sa.PrimaryKeyConstraint('order_id'),
        sa.UniqueConstraint('order_no', name='uk_yp_order_no'),
        comment='约拍订单表',
    )
    op.create_index('idx_yp_order_buyer_status', 'yp_order', ['buyer_user_id', 'status'])
    op.create_index('idx_yp_order_seller_status', 'yp_order', ['seller_user_id', 'status'])

    op.create_table(
        'yp_order_event',
        sa.Column('event_id', sa.BigInteger(), autoincrement=True, nullable=False, comment='事件ID'),
        sa.Column('order_id', sa.BigInteger(), nullable=False, comment='订单ID'),
        sa.Column('operator_user_id', sa.BigInteger(), nullable=False, comment='操作用户ID'),
        sa.Column('from_status', sa.String(length=32), nullable=True, comment='原状态'),
        sa.Column('to_status', sa.String(length=32), nullable=False, comment='新状态'),
        sa.Column('event_type', sa.String(length=32), nullable=False, comment='事件类型'),
        sa.Column('reason', sa.String(length=500), nullable=True, comment='操作原因'),
        sa.Column('request_id', sa.String(length=64), nullable=False, comment='请求幂等号'),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['operator_user_id'], ['sys_user.user_id'], name='fk_yp_order_event_user'),
        sa.ForeignKeyConstraint(['order_id'], ['yp_order.order_id'], name='fk_yp_order_event_order'),
        sa.PrimaryKeyConstraint('event_id'),
        sa.UniqueConstraint('request_id', name='uk_yp_order_event_request_id'),
        comment='约拍订单状态日志表',
    )
    op.create_index('idx_yp_order_event_order_time', 'yp_order_event', ['order_id', 'create_time'])


def downgrade() -> None:
    op.drop_index('idx_yp_order_event_order_time', table_name='yp_order_event')
    op.drop_table('yp_order_event')
    op.drop_index('idx_yp_order_seller_status', table_name='yp_order')
    op.drop_index('idx_yp_order_buyer_status', table_name='yp_order')
    op.drop_table('yp_order')
    op.drop_index('idx_yp_quote_receiver_status', table_name='yp_quote')
    op.drop_index('idx_yp_quote_demand_status', table_name='yp_quote')
    op.drop_table('yp_quote')
    op.drop_index('idx_yp_application_demand_status', table_name='yp_application')
    op.drop_table('yp_application')
    op.drop_index('idx_yp_demand_owner_status', table_name='yp_demand')
    op.drop_index('idx_yp_demand_city_status_time', table_name='yp_demand')
    op.drop_table('yp_demand')
