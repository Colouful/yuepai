from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint

from config.database import Base


class YpDelivery(Base):
    __tablename__ = 'yp_delivery'
    __table_args__ = (
        UniqueConstraint('order_id', 'delivery_version', name='uk_yp_delivery_order_version'),
        UniqueConstraint('request_id', name='uk_yp_delivery_request_id'),
        Index('idx_yp_delivery_order_status', 'order_id', 'status'),
        {'comment': '约拍作品交付版本'},
    )

    delivery_id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey('yp_order.order_id'), nullable=False)
    uploader_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    delivery_version = Column(Integer, nullable=False)
    original_assets_json = Column(Text, nullable=True)
    retouched_assets_json = Column(Text, nullable=False)
    note = Column(String(1000), nullable=True)
    status = Column(String(24), nullable=False, server_default='submitted')
    revision_reason = Column(String(1000), nullable=True)
    request_id = Column(String(64), nullable=False)
    submitted_at = Column(DateTime, nullable=False, default=datetime.now)
    accepted_at = Column(DateTime, nullable=True)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
