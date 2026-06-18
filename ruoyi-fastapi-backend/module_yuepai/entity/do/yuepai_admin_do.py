"""约拍管理后台数据模型"""
from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, CHAR, DECIMAL, Text, JSON
from config.database import Base


class YuepaiCertReview(Base):
    """认证审核表"""
    __tablename__ = 'yuepai_cert_review'
    __table_args__ = {'comment': '认证审核表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment='用户ID')
    cert_type = Column(String(20), nullable=False, comment='认证类型')
    real_name = Column(String(50), comment='真实姓名')
    id_card = Column(String(20), comment='身份证号')
    id_card_front = Column(String(500), comment='身份证正面')
    id_card_back = Column(String(500), comment='身份证反面')
    cert_images = Column(JSON, comment='认证材料图片')
    description = Column(String(1000), comment='申请说明')
    status = Column(CHAR(1), nullable=False, server_default='0', comment='状态: 0待审核 1已通过 2已驳回')
    reviewer = Column(String(64), comment='审核人')
    review_time = Column(DateTime, comment='审核时间')
    review_remark = Column(String(500), comment='审核备注')
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class YuepaiAftersale(Base):
    """售后工单表"""
    __tablename__ = 'yuepai_aftersale'
    __table_args__ = {'comment': '售后工单表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticket_no = Column(String(32), unique=True, nullable=False, comment='工单编号')
    order_id = Column(BigInteger, comment='关联订单ID')
    order_no = Column(String(32), comment='关联订单号')
    type = Column(String(20), nullable=False, comment='类型')
    applicant_id = Column(BigInteger, nullable=False, comment='申请人ID')
    respondent_id = Column(BigInteger, comment='被申请人ID')
    amount = Column(DECIMAL(10, 2), comment='涉及金额')
    reason = Column(String(500), nullable=False, comment='原因')
    description = Column(Text, comment='详细描述')
    evidence = Column(JSON, comment='证据材料')
    status = Column(String(20), nullable=False, server_default='pending', comment='状态')
    handler = Column(String(64), comment='处理人')
    handle_time = Column(DateTime, comment='处理时间')
    handle_result = Column(Text, comment='处理结果')
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class YuepaiOperation(Base):
    """运营管理表"""
    __tablename__ = 'yuepai_operation'
    __table_args__ = {'comment': '运营管理表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable=False, comment='类型')
    title = Column(String(200), nullable=False, comment='标题')
    content = Column(Text, comment='内容')
    image = Column(String(500), comment='图片')
    link = Column(String(500), comment='链接')
    config = Column(JSON, comment='扩展配置')
    sort_order = Column(Integer, server_default='0', comment='排序')
    status = Column(CHAR(1), nullable=False, server_default='1', comment='状态')
    view_count = Column(Integer, server_default='0', comment='浏览量')
    start_time = Column(DateTime, comment='开始时间')
    end_time = Column(DateTime, comment='结束时间')
    create_by = Column(String(64), comment='创建人')
    create_time = Column(DateTime, default=datetime.now)
    update_by = Column(String(64), comment='更新人')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class YuepaiRisk(Base):
    """风控记录表"""
    __tablename__ = 'yuepai_risk'
    __table_args__ = {'comment': '风控记录表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable=False, comment='类型')
    target_type = Column(String(20), comment='目标类型')
    target_id = Column(BigInteger, comment='目标ID')
    target_name = Column(String(100), comment='目标名称')
    risk_level = Column(String(10), comment='风险等级')
    risk_score = Column(Integer, comment='风险评分')
    reason = Column(String(500), comment='原因')
    description = Column(Text, comment='详细描述')
    amount = Column(DECIMAL(10, 2), comment='涉及金额')
    block_type = Column(String(20), comment='封禁类型')
    block_days = Column(Integer, comment='封禁天数')
    status = Column(String(20), nullable=False, server_default='pending', comment='状态')
    operator = Column(String(64), comment='操作人')
    operate_time = Column(DateTime, comment='操作时间')
    expire_time = Column(DateTime, comment='过期时间')
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
