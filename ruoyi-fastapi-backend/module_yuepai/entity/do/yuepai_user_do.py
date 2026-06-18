"""约拍用户扩展模型"""
from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, CHAR, DECIMAL, JSON
from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil


class YuepaiUser(Base):
    """约拍用户表"""
    __tablename__ = 'yuepai_user'
    __table_args__ = {'comment': '约拍用户扩展表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    sys_user_id = Column(BigInteger, nullable=False, comment='关联RuoYi系统用户ID')
    uid = Column(String(32), unique=True, nullable=False, comment='约拍用户UID')
    phone = Column(String(20), nullable=True, comment='手机号')
    phone_hash = Column(String(64), unique=True, nullable=True, comment='手机号哈希')
    wechat_openid = Column(String(64), unique=True, nullable=True, comment='微信OpenID')
    role = Column(String(20), nullable=False, server_default='user', comment='角色: user/model/photographer/makeup/merchant')
    city = Column(String(50), nullable=True, comment='城市')
    bio = Column(String(500), nullable=True, comment='简介')
    is_verified = Column(CHAR(1), nullable=True, server_default='0', comment='实名认证: 0否 1是')
    is_professional = Column(CHAR(1), nullable=True, server_default='0', comment='专业认证')
    credit_score = Column(Integer, nullable=True, server_default='100', comment='信用分')
    balance = Column(DECIMAL(10, 2), nullable=True, server_default='0', comment='账户余额')
    point_balance = Column(Integer, nullable=True, server_default='0', comment='积分余额')
    follower_count = Column(Integer, nullable=True, server_default='0', comment='粉丝数')
    yuepai_count = Column(Integer, nullable=True, server_default='0', comment='约拍次数')
    status = Column(CHAR(1), nullable=True, server_default='0', comment='状态: 0正常 1禁用')
    del_flag = Column(CHAR(1), nullable=True, server_default='0', comment='删除标志')
    create_by = Column(String(64), nullable=True, server_default="''")
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    update_by = Column(String(64), nullable=True, server_default="''")
    update_time = Column(DateTime, nullable=True, default=datetime.now)
    remark = Column(String(500), nullable=True)


class YuepaiDemand(Base):
    """约拍需求表"""
    __tablename__ = 'yuepai_demand'
    __table_args__ = {'comment': '约拍需求表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    demand_no = Column(String(32), unique=True, nullable=False, comment='需求编号')
    user_id = Column(BigInteger, nullable=False, comment='发布者ID')
    type = Column(String(20), nullable=False, comment='类型: seek_photographer/seek_model/seek_makeup/mutual')
    title = Column(String(100), nullable=False, comment='标题')
    description = Column(String(2000), nullable=False, comment='描述')
    shooting_type = Column(String(30), nullable=False, comment='拍摄类型')
    shooting_date = Column(DateTime, nullable=False, comment='拍摄日期')
    city = Column(String(50), nullable=False, comment='城市')
    budget_min = Column(DECIMAL(10, 2), nullable=True, server_default='0', comment='预算下限')
    budget_max = Column(DECIMAL(10, 2), nullable=True, server_default='0', comment='预算上限')
    is_mutual = Column(CHAR(1), nullable=True, server_default='0', comment='是否互勉')
    reference_images = Column(JSON, nullable=True, comment='参考图片')
    status = Column(CHAR(1), nullable=True, server_default='0', comment='状态: 0关闭 1开放 2进行中 3已完成')
    view_count = Column(Integer, nullable=True, server_default='0', comment='浏览数')
    apply_count = Column(Integer, nullable=True, server_default='0', comment='申请数')
    audit_status = Column(CHAR(1), nullable=True, server_default='0', comment='审核状态: 0待审 1通过 2拒绝')
    del_flag = Column(CHAR(1), nullable=True, server_default='0')
    create_by = Column(String(64), nullable=True, server_default="''")
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    update_by = Column(String(64), nullable=True, server_default="''")
    update_time = Column(DateTime, nullable=True, default=datetime.now)


class YuepaiOrder(Base):
    """约拍订单表"""
    __tablename__ = 'yuepai_order'
    __table_args__ = {'comment': '约拍订单表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    order_no = Column(String(32), unique=True, nullable=False, comment='订单编号')
    demand_id = Column(BigInteger, nullable=False, comment='需求ID')
    publisher_id = Column(BigInteger, nullable=False, comment='需求方ID')
    photographer_id = Column(BigInteger, nullable=False, comment='摄影师ID')
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment='总金额')
    deposit_amount = Column(DECIMAL(10, 2), nullable=False, comment='定金')
    final_amount = Column(DECIMAL(10, 2), nullable=True, comment='尾款')
    platform_fee = Column(DECIMAL(10, 2), nullable=True, server_default='0', comment='平台佣金')
    photographer_income = Column(DECIMAL(10, 2), nullable=True, server_default='0', comment='摄影师收入')
    shooting_date = Column(DateTime, nullable=False, comment='拍摄日期')
    status = Column(CHAR(1), nullable=True, server_default='0', comment='状态: 0待付定金 1已付 2拍摄中 3待付尾款 4已完成 5已取消 6退款中')
    del_flag = Column(CHAR(1), nullable=True, server_default='0')
    create_by = Column(String(64), nullable=True, server_default="''")
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    update_by = Column(String(64), nullable=True, server_default="''")
    update_time = Column(DateTime, nullable=True, default=datetime.now)


class YuepaiPayment(Base):
    """支付记录表"""
    __tablename__ = 'yuepai_payment'
    __table_args__ = {'comment': '支付记录表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    payment_no = Column(String(64), unique=True, nullable=False, comment='支付流水号')
    order_id = Column(BigInteger, nullable=False, comment='订单ID')
    user_id = Column(BigInteger, nullable=False, comment='用户ID')
    type = Column(Integer, nullable=False, comment='类型: 1定金 2尾款 3充值 4会员')
    amount = Column(DECIMAL(10, 2), nullable=False, comment='金额')
    channel = Column(String(20), nullable=False, comment='支付渠道')
    status = Column(Integer, nullable=True, server_default='0', comment='状态: 0待支付 1成功 2失败 3已退款')
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    update_time = Column(DateTime, nullable=True, default=datetime.now)


class YuepaiPost(Base):
    """作品动态表"""
    __tablename__ = 'yuepai_post'
    __table_args__ = {'comment': '作品动态表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    user_id = Column(BigInteger, nullable=False, comment='作者ID')
    type = Column(String(20), nullable=True, server_default='work', comment='类型: work/dynamic')
    title = Column(String(100), nullable=True, comment='标题')
    content = Column(String(2000), nullable=True, comment='内容')
    images = Column(JSON, nullable=False, comment='图片列表')
    like_count = Column(Integer, nullable=True, server_default='0')
    comment_count = Column(Integer, nullable=True, server_default='0')
    view_count = Column(Integer, nullable=True, server_default='0')
    audit_status = Column(CHAR(1), nullable=True, server_default='0', comment='审核: 0待审 1通过 2拒绝')
    status = Column(CHAR(1), nullable=True, server_default='0', comment='状态: 0正常 1下架')
    del_flag = Column(CHAR(1), nullable=True, server_default='0')
    create_by = Column(String(64), nullable=True, server_default="''")
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    update_by = Column(String(64), nullable=True, server_default="''")
    update_time = Column(DateTime, nullable=True, default=datetime.now)


class YuepaiPointRecord(Base):
    """积分记录表"""
    __tablename__ = 'yuepai_point_record'
    __table_args__ = {'comment': '积分记录表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    user_id = Column(BigInteger, nullable=False, comment='用户ID')
    type = Column(String(30), nullable=False, comment='类型')
    amount = Column(Integer, nullable=False, comment='积分数量')
    balance = Column(Integer, nullable=False, comment='变动后余额')
    description = Column(String(200), nullable=True, comment='描述')
    create_time = Column(DateTime, nullable=True, default=datetime.now)


class YuepaiMember(Base):
    """会员表"""
    __tablename__ = 'yuepai_member'
    __table_args__ = {'comment': '会员表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    user_id = Column(BigInteger, unique=True, nullable=False, comment='用户ID')
    level = Column(Integer, nullable=True, server_default='0', comment='等级: 0普通 1银卡 2金卡 3钻石')
    started_at = Column(DateTime, nullable=True, comment='开始时间')
    expired_at = Column(DateTime, nullable=True, comment='过期时间')
    total_paid = Column(DECIMAL(10, 2), nullable=True, server_default='0', comment='累计付费')
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    update_time = Column(DateTime, nullable=True, default=datetime.now)
