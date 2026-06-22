from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint

from config.database import Base


class YpQuote(Base):
    __tablename__ = 'yp_quote'
    __table_args__ = (
        Index('idx_yp_quote_demand_status', 'demand_id', 'status'),
        Index('idx_yp_quote_receiver_status', 'receiver_user_id', 'status'),
        {'comment': '约拍服务报价表'},
    )

    quote_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='报价ID')
    demand_id = Column(BigInteger, ForeignKey('yp_demand.demand_id'), nullable=True, comment='需求ID')
    application_id = Column(BigInteger, ForeignKey('yp_application.application_id'), nullable=True, comment='报名ID')
    sender_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False, comment='报价方用户ID')
    receiver_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False, comment='接收方用户ID')
    amount = Column(Numeric(12, 2), nullable=False, comment='报价总额')
    fee_breakdown_json = Column(Text, nullable=False, comment='费用明细JSON')
    service_snapshot_json = Column(Text, nullable=False, comment='服务内容快照JSON')
    remark = Column(String(1000), nullable=True, comment='补充说明')
    expires_at = Column(DateTime, nullable=False, comment='报价失效时间')
    status = Column(String(20), nullable=False, server_default='pending', comment='报价状态')
    parent_quote_id = Column(BigInteger, nullable=True, comment='原报价ID')
    version = Column(Integer, nullable=False, server_default='1', comment='乐观锁版本')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class YpOrder(Base):
    __tablename__ = 'yp_order'
    __table_args__ = (
        UniqueConstraint('order_no', name='uk_yp_order_no'),
        Index('idx_yp_order_buyer_status', 'buyer_user_id', 'status'),
        Index('idx_yp_order_seller_status', 'seller_user_id', 'status'),
        {'comment': '约拍订单表'},
    )

    order_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='订单ID')
    order_no = Column(String(40), nullable=False, comment='订单编号')
    buyer_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False, comment='买方用户ID')
    seller_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False, comment='卖方用户ID')
    demand_id = Column(BigInteger, ForeignKey('yp_demand.demand_id'), nullable=True, comment='需求ID')
    quote_id = Column(BigInteger, ForeignKey('yp_quote.quote_id'), nullable=True, comment='报价ID')
    service_snapshot_json = Column(Text, nullable=False, comment='服务内容快照JSON')
    amount = Column(Numeric(12, 2), nullable=False, comment='服务金额')
    platform_fee = Column(Numeric(12, 2), nullable=False, server_default='0', comment='平台服务费')
    discount_amount = Column(Numeric(12, 2), nullable=False, server_default='0', comment='优惠金额')
    payable_amount = Column(Numeric(12, 2), nullable=False, comment='应付金额')
    paid_amount = Column(Numeric(12, 2), nullable=False, server_default='0', comment='已付金额')
    shoot_at = Column(DateTime, nullable=False, comment='拍摄时间')
    duration_minutes = Column(Integer, nullable=False, comment='预计服务时长')
    location_snapshot_json = Column(Text, nullable=False, comment='地点快照JSON')
    contact_snapshot_json = Column(Text, nullable=False, comment='联系人快照JSON')
    remark = Column(String(1000), nullable=True, comment='订单备注')
    status = Column(String(32), nullable=False, server_default='pending_payment', comment='订单状态')
    payment_status = Column(String(20), nullable=False, server_default='unpaid', comment='支付状态')
    refund_status = Column(String(20), nullable=False, server_default='none', comment='退款状态')
    version = Column(Integer, nullable=False, server_default='1', comment='乐观锁版本')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class YpOrderEvent(Base):
    __tablename__ = 'yp_order_event'
    __table_args__ = (
        Index('idx_yp_order_event_order_time', 'order_id', 'create_time'),
        UniqueConstraint('request_id', name='uk_yp_order_event_request_id'),
        {'comment': '约拍订单状态日志表'},
    )

    event_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='事件ID')
    order_id = Column(BigInteger, ForeignKey('yp_order.order_id'), nullable=False, comment='订单ID')
    operator_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False, comment='操作用户ID')
    from_status = Column(String(32), nullable=True, comment='原状态')
    to_status = Column(String(32), nullable=False, comment='新状态')
    event_type = Column(String(32), nullable=False, comment='事件类型')
    reason = Column(String(500), nullable=True, comment='操作原因')
    request_id = Column(String(64), nullable=False, comment='请求幂等号')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
