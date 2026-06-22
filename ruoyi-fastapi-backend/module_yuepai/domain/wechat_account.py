from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, String, Text, UniqueConstraint

from config.database import Base


class YpWechatAccount(Base):
    __tablename__ = 'yp_wechat_account'
    __table_args__ = (
        UniqueConstraint('user_id', name='uk_yp_wechat_account_user'),
        UniqueConstraint('subject_hash', name='uk_yp_wechat_account_subject'),
        Index('idx_yp_wechat_union_hash', 'union_hash'),
        {'comment': '微信小程序账号绑定'},
    )

    account_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    subject_hash = Column(String(64), nullable=False)
    subject_secret = Column(Text, nullable=False)
    union_hash = Column(String(64), nullable=True)
    union_secret = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, server_default='active')
    last_login_time = Column(DateTime, nullable=True)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
