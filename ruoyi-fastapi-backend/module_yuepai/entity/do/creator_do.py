from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)

from config.database import Base


class YpCreatorProfile(Base):
    __tablename__ = 'yp_creator_profile'
    __table_args__ = (
        UniqueConstraint('user_id', 'role_code', name='uk_yp_creator_user_role'),
        Index('idx_yp_creator_role_city_status', 'role_code', 'city_code', 'status'),
        Index('idx_yp_creator_rating_orders', 'rating', 'completed_orders'),
        {'comment': '约拍创作者多身份资料'},
    )

    creator_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    role_code = Column(String(32), nullable=False)
    display_name = Column(String(50), nullable=False)
    headline = Column(String(120), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    cover_url = Column(String(500), nullable=True)
    city_code = Column(String(20), nullable=False)
    service_city_json = Column(Text, nullable=True)
    tags_json = Column(Text, nullable=True)
    years_experience = Column(Integer, nullable=False, server_default='0')
    base_price = Column(Numeric(12, 2), nullable=True)
    response_rate = Column(Integer, nullable=False, server_default='0')
    completed_orders = Column(Integer, nullable=False, server_default='0')
    rating = Column(Numeric(3, 2), nullable=False, server_default='0')
    review_count = Column(Integer, nullable=False, server_default='0')
    follower_count = Column(Integer, nullable=False, server_default='0')
    accept_mutual = Column(Boolean, nullable=False, server_default='0')
    certification_status = Column(String(20), nullable=False, server_default='pending')
    status = Column(String(20), nullable=False, server_default='draft')
    version = Column(Integer, nullable=False, server_default='1')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class YpCreatorWork(Base):
    __tablename__ = 'yp_creator_work'
    __table_args__ = (
        Index('idx_yp_work_creator_status', 'creator_id', 'status'),
        Index('idx_yp_work_category_status', 'category', 'status'),
        Index('idx_yp_work_popularity', 'favorite_count', 'view_count'),
        {'comment': '创作者作品'},
    )

    work_id = Column(BigInteger, primary_key=True, autoincrement=True)
    creator_id = Column(BigInteger, ForeignKey('yp_creator_profile.creator_id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(32), nullable=False)
    cover_url = Column(String(500), nullable=False)
    assets_json = Column(Text, nullable=False)
    tags_json = Column(Text, nullable=True)
    city_code = Column(String(20), nullable=True)
    shot_date = Column(Date, nullable=True)
    favorite_count = Column(Integer, nullable=False, server_default='0')
    view_count = Column(Integer, nullable=False, server_default='0')
    audit_status = Column(String(20), nullable=False, server_default='pending')
    status = Column(String(20), nullable=False, server_default='draft')
    version = Column(Integer, nullable=False, server_default='1')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class YpServicePackage(Base):
    __tablename__ = 'yp_service_package'
    __table_args__ = (
        Index('idx_yp_package_creator_status', 'creator_id', 'status'),
        Index('idx_yp_package_price', 'price'),
        {'comment': '创作者服务套餐'},
    )

    package_id = Column(BigInteger, primary_key=True, autoincrement=True)
    creator_id = Column(BigInteger, ForeignKey('yp_creator_profile.creator_id'), nullable=False)
    package_name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    cover_url = Column(String(500), nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    original_count = Column(Integer, nullable=False, server_default='0')
    retouched_count = Column(Integer, nullable=False, server_default='0')
    delivery_days = Column(Integer, nullable=False, server_default='7')
    revision_count = Column(Integer, nullable=False, server_default='1')
    includes_json = Column(Text, nullable=True)
    excludes_json = Column(Text, nullable=True)
    addons_json = Column(Text, nullable=True)
    booking_notice = Column(Text, nullable=True)
    refund_rule = Column(Text, nullable=True)
    audit_status = Column(String(20), nullable=False, server_default='pending')
    status = Column(String(20), nullable=False, server_default='draft')
    version = Column(Integer, nullable=False, server_default='1')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class YpCreatorReview(Base):
    __tablename__ = 'yp_creator_review'
    __table_args__ = (
        UniqueConstraint('order_id', name='uk_yp_review_order'),
        Index('idx_yp_review_creator_status', 'creator_id', 'status'),
        {'comment': '订单创作者评价'},
    )

    review_id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey('yp_order.order_id'), nullable=False)
    creator_id = Column(BigInteger, ForeignKey('yp_creator_profile.creator_id'), nullable=False)
    reviewer_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    rating = Column(Integer, nullable=False)
    service_rating = Column(Integer, nullable=False)
    communication_rating = Column(Integer, nullable=False)
    delivery_rating = Column(Integer, nullable=False)
    content = Column(String(1000), nullable=False)
    assets_json = Column(Text, nullable=True)
    creator_reply = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, server_default='published')
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class YpCreatorFollow(Base):
    __tablename__ = 'yp_creator_follow'
    __table_args__ = (
        UniqueConstraint('follower_user_id', 'creator_id', name='uk_yp_follow_user_creator'),
        Index('idx_yp_follow_creator_time', 'creator_id', 'create_time'),
        {'comment': '用户关注创作者'},
    )

    follow_id = Column(BigInteger, primary_key=True, autoincrement=True)
    follower_user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    creator_id = Column(BigInteger, ForeignKey('yp_creator_profile.creator_id'), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now)


class YpWorkFavorite(Base):
    __tablename__ = 'yp_work_favorite'
    __table_args__ = (
        UniqueConstraint('user_id', 'work_id', name='uk_yp_favorite_user_work'),
        Index('idx_yp_favorite_work_time', 'work_id', 'create_time'),
        {'comment': '用户收藏作品'},
    )

    favorite_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=False)
    work_id = Column(BigInteger, ForeignKey('yp_creator_work.work_id'), nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.now)
