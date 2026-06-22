"""create conversation and message tables

Revision ID: yp_message_0005
Revises: yp_creator_social_0004
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'yp_message_0005'
down_revision: str | None = 'yp_creator_social_0004'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'yp_conversation',
        sa.Column('conversation_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_low_id', sa.BigInteger(), nullable=False),
        sa.Column('user_high_id', sa.BigInteger(), nullable=False),
        sa.Column('creator_id', sa.BigInteger(), nullable=True),
        sa.Column('order_id', sa.BigInteger(), nullable=True),
        sa.Column('last_message_id', sa.BigInteger(), nullable=True),
        sa.Column('last_message_preview', sa.String(200), nullable=True),
        sa.Column('last_message_time', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(20), server_default='active', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_low_id'], ['sys_user.user_id'], name='fk_yp_conversation_low'),
        sa.ForeignKeyConstraint(['user_high_id'], ['sys_user.user_id'], name='fk_yp_conversation_high'),
        sa.ForeignKeyConstraint(['creator_id'], ['yp_creator_profile.creator_id'], name='fk_yp_conversation_creator'),
        sa.ForeignKeyConstraint(['order_id'], ['yp_order.order_id'], name='fk_yp_conversation_order'),
        sa.PrimaryKeyConstraint('conversation_id'),
        sa.UniqueConstraint('user_low_id', 'user_high_id', name='uk_yp_conversation_user_pair'),
        comment='用户私聊会话',
    )
    op.create_index('idx_yp_conversation_last_time', 'yp_conversation', ['last_message_time'])

    op.create_table(
        'yp_conversation_member',
        sa.Column('member_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('conversation_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('unread_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_read_message_id', sa.BigInteger(), nullable=True),
        sa.Column('muted', sa.Integer(), server_default='0', nullable=False),
        sa.Column('status', sa.String(20), server_default='active', nullable=False),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('update_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['yp_conversation.conversation_id'], name='fk_yp_member_conversation'),
        sa.ForeignKeyConstraint(['user_id'], ['sys_user.user_id'], name='fk_yp_member_user'),
        sa.PrimaryKeyConstraint('member_id'),
        sa.UniqueConstraint('conversation_id', 'user_id', name='uk_yp_conversation_member'),
        comment='会话成员状态',
    )
    op.create_index('idx_yp_member_user_unread', 'yp_conversation_member', ['user_id', 'unread_count'])

    op.create_table(
        'yp_message',
        sa.Column('message_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('conversation_id', sa.BigInteger(), nullable=False),
        sa.Column('sender_user_id', sa.BigInteger(), nullable=False),
        sa.Column('message_type', sa.String(20), server_default='text', nullable=False),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('payload_json', sa.Text(), nullable=True),
        sa.Column('client_message_id', sa.String(64), nullable=False),
        sa.Column('status', sa.String(20), server_default='sent', nullable=False),
        sa.Column('recalled_at', sa.DateTime(), nullable=True),
        sa.Column('create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['yp_conversation.conversation_id'], name='fk_yp_message_conversation'),
        sa.ForeignKeyConstraint(['sender_user_id'], ['sys_user.user_id'], name='fk_yp_message_sender'),
        sa.PrimaryKeyConstraint('message_id'),
        sa.UniqueConstraint('sender_user_id', 'client_message_id', name='uk_yp_message_sender_client'),
        comment='会话消息',
    )
    op.create_index('idx_yp_message_conversation_id', 'yp_message', ['conversation_id', 'message_id'])


def downgrade() -> None:
    op.drop_index('idx_yp_message_conversation_id', table_name='yp_message')
    op.drop_table('yp_message')
    op.drop_index('idx_yp_member_user_unread', table_name='yp_conversation_member')
    op.drop_table('yp_conversation_member')
    op.drop_index('idx_yp_conversation_last_time', table_name='yp_conversation')
    op.drop_table('yp_conversation')
