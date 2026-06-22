from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint

from config.database import Base


class YpDemand(Base):
    __tablename__ = 'yp_demand'
    __table_args__ = (
        Index('idx_yp_demand_city_status_time', 'city_code', 'status', 'shoot_at'),
        Index('idx_yp_demand_owner_status', 'owner_user_id', 'status'),
        {'comment': '约拍需求表'},
    )

    demand_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='需求ID')
    owner_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False, comment='发布用户ID')
    title = Column(String(80), nullable=False, comment='需求标题')
    description = Column(Text, nullable=False, comment='需求描述')
    demand_type = Column(String(32), nullable=False, comment='约拍类型')
    city_code = Column(String(20), nullable=False, comment='城市编码')
    location_name = Column(String(160), nullable=True, comment='地点名称')
    shoot_at = Column(DateTime, nullable=False, comment='拍摄开始时间')
    duration_minutes = Column(Integer, nullable=False, server_default='120', comment='预计时长')
    roles_json = Column(Text, nullable=False, comment='招募角色JSON')
    reference_assets_json = Column(Text, nullable=True, comment='参考图JSON')
    budget_type = Column(String(20), nullable=False, comment='预算类型')
    budget_min = Column(Numeric(12, 2), nullable=True, comment='最低预算')
    budget_max = Column(Numeric(12, 2), nullable=True, comment='最高预算')
    applicant_limit = Column(Integer, nullable=False, server_default='20', comment='报名人数上限')
    application_deadline = Column(DateTime, nullable=False, comment='报名截止时间')
    audit_status = Column(String(16), nullable=False, server_default='pending', comment='审核状态')
    status = Column(String(16), nullable=False, server_default='draft', comment='业务状态')
    version = Column(Integer, nullable=False, server_default='1', comment='乐观锁版本')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class YpApplication(Base):
    __tablename__ = 'yp_application'
    __table_args__ = (
        UniqueConstraint('demand_id', 'applicant_user_id', 'role_code', name='uk_yp_application_demand_user_role'),
        Index('idx_yp_application_demand_status', 'demand_id', 'status'),
        {'comment': '约拍需求报名表'},
    )

    application_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='报名ID')
    demand_id = Column(BigInteger, ForeignKey('yp_demand.demand_id'), nullable=False, comment='需求ID')
    applicant_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False, comment='报名用户ID')
    role_code = Column(String(32), nullable=False, comment='报名身份')
    introduction = Column(String(500), nullable=False, comment='报名说明')
    quote_amount = Column(Numeric(12, 2), nullable=True, comment='报名报价')
    portfolio_assets_json = Column(Text, nullable=True, comment='作品资料JSON')
    status = Column(String(20), nullable=False, server_default='pending', comment='报名状态')
    reject_reason = Column(String(500), nullable=True, comment='未入选原因')
    version = Column(Integer, nullable=False, server_default='1', comment='乐观锁版本')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
