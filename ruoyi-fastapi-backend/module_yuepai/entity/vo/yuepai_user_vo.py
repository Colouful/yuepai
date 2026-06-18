"""约拍用户VO"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class YuepaiUserQuery(BaseModel):
    """用户查询参数"""
    uid: Optional[str] = Field(None, description='用户UID')
    phone: Optional[str] = Field(None, description='手机号')
    role: Optional[str] = Field(None, description='角色')
    city: Optional[str] = Field(None, description='城市')
    status: Optional[str] = Field(None, description='状态')
    is_verified: Optional[str] = Field(None, description='认证状态')
    page_num: int = Field(1, description='页码')
    page_size: int = Field(20, description='每页数量')


class YuepaiUserVO(BaseModel):
    """用户响应"""
    id: Optional[int] = None
    uid: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    is_verified: Optional[str] = None
    credit_score: Optional[int] = None
    balance: Optional[float] = None
    point_balance: Optional[int] = None
    follower_count: Optional[int] = None
    yuepai_count: Optional[int] = None
    status: Optional[str] = None
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class YuepaiDemandQuery(BaseModel):
    """需求查询参数"""
    demand_no: Optional[str] = None
    type: Optional[str] = None
    city: Optional[str] = None
    status: Optional[str] = None
    audit_status: Optional[str] = None
    keyword: Optional[str] = None
    page_num: int = 1
    page_size: int = 20


class YuepaiDemandVO(BaseModel):
    id: Optional[int] = None
    demand_no: Optional[str] = None
    user_id: Optional[int] = None
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    shooting_type: Optional[str] = None
    shooting_date: Optional[datetime] = None
    city: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    is_mutual: Optional[str] = None
    status: Optional[str] = None
    audit_status: Optional[str] = None
    view_count: Optional[int] = None
    apply_count: Optional[int] = None
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class YuepaiOrderQuery(BaseModel):
    order_no: Optional[str] = None
    status: Optional[str] = None
    page_num: int = 1
    page_size: int = 20


class YuepaiOrderVO(BaseModel):
    id: Optional[int] = None
    order_no: Optional[str] = None
    demand_id: Optional[int] = None
    publisher_id: Optional[int] = None
    photographer_id: Optional[int] = None
    total_amount: Optional[float] = None
    deposit_amount: Optional[float] = None
    platform_fee: Optional[float] = None
    photographer_income: Optional[float] = None
    shooting_date: Optional[datetime] = None
    status: Optional[str] = None
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class YuepaiPostQuery(BaseModel):
    type: Optional[str] = None
    audit_status: Optional[str] = None
    status: Optional[str] = None
    keyword: Optional[str] = None
    page_num: int = 1
    page_size: int = 20


class YuepaiPostVO(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    type: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[list] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    audit_status: Optional[str] = None
    status: Optional[str] = None
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True
