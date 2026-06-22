from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint

from config.database import Base


class YpConversation(Base):
    __tablename__ = 'yp_conversation'
    __table_args__ = (
        UniqueConstraint('user_low_id', 'user_high_id', name='uk_yp_conversation_user_pair'),
        Index('idx_yp_conversation_last_time', 'last_message_time'),
        {'comment': '用户私聊会话'},
    )

    conversation_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_low_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    user_high_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    creator_id = Column(BigInteger, ForeignKey('yp_creator_profile.creator_id'), nullable=True)
    order_id = Column(BigInteger, ForeignKey('yp_order.order_id'), nullable=True)
    last_message_id = Column(BigInteger, nullable=True)
    last_message_preview = Column(String(200), nullable=True)
    last_message_time = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, server_default='active')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class YpConversationMember(Base):
    __tablename__ = 'yp_conversation_member'
    __table_args__ = (
        UniqueConstraint('conversation_id', 'user_id', name='uk_yp_conversation_member'),
        Index('idx_yp_member_user_unread', 'user_id', 'unread_count'),
        {'comment': '会话成员状态'},
    )

    member_id = Column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id = Column(BigInteger, ForeignKey('yp_conversation.conversation_id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    unread_count = Column(Integer, nullable=False, server_default='0')
    last_read_message_id = Column(BigInteger, nullable=True)
    muted = Column(Integer, nullable=False, server_default='0')
    status = Column(String(20), nullable=False, server_default='active')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class YpMessage(Base):
    __tablename__ = 'yp_message'
    __table_args__ = (
        UniqueConstraint('sender_user_id', 'client_message_id', name='uk_yp_message_sender_client'),
        Index('idx_yp_message_conversation_id', 'conversation_id', 'message_id'),
        {'comment': '会话消息'},
    )

    message_id = Column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id = Column(BigInteger, ForeignKey('yp_conversation.conversation_id'), nullable=False)
    sender_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    message_type = Column(String(20), nullable=False, server_default='text')
    text_content = Column(Text, nullable=True)
    payload_json = Column(Text, nullable=True)
    client_message_id = Column(String(64), nullable=False)
    status = Column(String(20), nullable=False, server_default='sent')
    recalled_at = Column(DateTime, nullable=True)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
