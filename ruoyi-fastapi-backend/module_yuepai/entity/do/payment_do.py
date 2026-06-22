from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint

from config.database import Base


class YpPayment(Base):
    __tablename__ = 'yp_payment'
    __table_args__ = (
        UniqueConstraint('payment_no', name='uk_yp_payment_no'),
        UniqueConstraint('request_id', name='uk_yp_payment_request_id'),
        Index('idx_yp_payment_order_status', 'order_id', 'status'),
        {'comment': '约拍支付单'},
    )

    payment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    payment_no = Column(String(40), nullable=False)
    order_id = Column(BigInteger, ForeignKey('yp_order.order_id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    provider = Column(String(20), nullable=False, server_default='wechat')
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(8), nullable=False, server_default='CNY')
    status = Column(String(20), nullable=False, server_default='created')
    request_id = Column(String(64), nullable=False)
    provider_transaction_id = Column(String(64), nullable=True)
    prepay_id = Column(String(128), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    failure_code = Column(String(64), nullable=True)
    failure_message = Column(String(500), nullable=True)
    version = Column(Integer, nullable=False, server_default='1')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class YpPaymentEvent(Base):
    __tablename__ = 'yp_payment_event'
    __table_args__ = (
        UniqueConstraint('provider_event_id', name='uk_yp_payment_event_provider_id'),
        Index('idx_yp_payment_event_payment_time', 'payment_id', 'create_time'),
        {'comment': '支付回调事件'},
    )

    event_id = Column(BigInteger, primary_key=True, autoincrement=True)
    payment_id = Column(BigInteger, ForeignKey('yp_payment.payment_id'), nullable=True)
    provider_event_id = Column(String(128), nullable=False)
    event_type = Column(String(64), nullable=False)
    payload_digest = Column(String(64), nullable=False)
    process_status = Column(String(20), nullable=False, server_default='received')
    error_message = Column(String(500), nullable=True)
    processed_at = Column(DateTime, nullable=True)
    create_time = Column(DateTime, nullable=False, default=datetime.now)


class YpRefund(Base):
    __tablename__ = 'yp_refund'
    __table_args__ = (
        UniqueConstraint('refund_no', name='uk_yp_refund_no'),
        UniqueConstraint('request_id', name='uk_yp_refund_request_id'),
        Index('idx_yp_refund_order_status', 'order_id', 'status'),
        {'comment': '约拍退款单'},
    )

    refund_id = Column(BigInteger, primary_key=True, autoincrement=True)
    refund_no = Column(String(40), nullable=False)
    order_id = Column(BigInteger, ForeignKey('yp_order.order_id'), nullable=False)
    payment_id = Column(BigInteger, ForeignKey('yp_payment.payment_id'), nullable=False)
    applicant_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    reason = Column(String(500), nullable=False)
    status = Column(String(20), nullable=False, server_default='requested')
    request_id = Column(String(64), nullable=False)
    provider_refund_id = Column(String(64), nullable=True)
    evidence_json = Column(Text, nullable=True)
    version = Column(Integer, nullable=False, server_default='1')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
