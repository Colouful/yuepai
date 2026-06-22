from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class DemandCreate(CamelModel):
    title: str = Field(min_length=4, max_length=80)
    description: str = Field(min_length=20, max_length=5000)
    demand_type: str = Field(min_length=2, max_length=32)
    city_code: str = Field(min_length=2, max_length=20)
    location_name: str | None = Field(default=None, max_length=160)
    shoot_at: datetime
    duration_minutes: int = Field(default=120, ge=30, le=1440)
    roles: list[str] = Field(min_length=1, max_length=8)
    reference_assets: list[str] = Field(default_factory=list, max_length=12)
    budget_type: Literal['fixed', 'range', 'quote', 'mutual', 'free', 'negotiable']
    budget_min: Decimal | None = Field(default=None, ge=0, le=9999999)
    budget_max: Decimal | None = Field(default=None, ge=0, le=9999999)
    applicant_limit: int = Field(default=20, ge=1, le=200)
    application_deadline: datetime

    @field_validator('roles')
    @classmethod
    def validate_roles(cls, value: list[str]) -> list[str]:
        roles = [item.strip() for item in value if item.strip()]
        if not roles:
            raise ValueError('至少选择一个招募角色')
        return list(dict.fromkeys(roles))

    @model_validator(mode='after')
    def validate_business_rules(self):
        now = datetime.now(self.shoot_at.tzinfo) if self.shoot_at.tzinfo else datetime.now()
        if self.shoot_at <= now:
            raise ValueError('拍摄时间必须晚于当前时间')
        if self.application_deadline >= self.shoot_at:
            raise ValueError('报名截止时间必须早于拍摄时间')
        if self.budget_type == 'fixed' and self.budget_min is None:
            raise ValueError('固定预算必须填写金额')
        if self.budget_type == 'range':
            if self.budget_min is None or self.budget_max is None:
                raise ValueError('预算区间必须填写最低和最高金额')
            if self.budget_min > self.budget_max:
                raise ValueError('最低预算不能高于最高预算')
        return self


class DemandResponse(CamelModel):
    demand_id: int
    owner_user_id: int
    title: str
    description: str
    demand_type: str
    city_code: str
    location_name: str | None
    shoot_at: datetime
    duration_minutes: int
    roles: list[str]
    reference_assets: list[str]
    budget_type: str
    budget_min: Decimal | None
    budget_max: Decimal | None
    applicant_limit: int
    application_deadline: datetime
    audit_status: str
    status: str
    version: int
    create_time: datetime
    update_time: datetime


class ApplicationCreate(CamelModel):
    role_code: str = Field(min_length=2, max_length=32)
    introduction: str = Field(min_length=10, max_length=500)
    quote_amount: Decimal | None = Field(default=None, ge=0, le=9999999)
    portfolio_assets: list[str] = Field(default_factory=list, max_length=20)


class ApplicationResponse(CamelModel):
    application_id: int
    demand_id: int
    applicant_user_id: int
    role_code: str
    introduction: str
    quote_amount: Decimal | None
    portfolio_assets: list[str]
    status: str
    reject_reason: str | None
    version: int
    create_time: datetime
    update_time: datetime


class QuoteCreate(CamelModel):
    demand_id: int | None = None
    application_id: int | None = None
    receiver_user_id: int
    amount: Decimal = Field(gt=0, le=9999999)
    fee_breakdown: dict[str, Decimal]
    service_snapshot: dict
    remark: str | None = Field(default=None, max_length=1000)
    expires_at: datetime

    @model_validator(mode='after')
    def validate_quote(self):
        now = datetime.now(self.expires_at.tzinfo) if self.expires_at.tzinfo else datetime.now()
        if self.expires_at <= now:
            raise ValueError('报价有效期必须晚于当前时间')
        if not self.fee_breakdown:
            raise ValueError('报价必须包含费用明细')
        total = sum(self.fee_breakdown.values(), Decimal('0'))
        if total != self.amount:
            raise ValueError('费用明细合计必须等于报价总额')
        return self


class QuoteResponse(CamelModel):
    quote_id: int
    demand_id: int | None
    application_id: int | None
    sender_user_id: int
    receiver_user_id: int
    amount: Decimal
    fee_breakdown: dict
    service_snapshot: dict
    remark: str | None
    expires_at: datetime
    status: str
    version: int
    create_time: datetime
    update_time: datetime


class QuoteAccept(CamelModel):
    request_id: str = Field(min_length=16, max_length=64)
    shoot_at: datetime
    duration_minutes: int = Field(ge=30, le=1440)
    location_snapshot: dict
    contact_snapshot: dict
    remark: str | None = Field(default=None, max_length=1000)


class OrderTransition(CamelModel):
    to_status: str = Field(min_length=3, max_length=32)
    request_id: str = Field(min_length=16, max_length=64)
    reason: str | None = Field(default=None, max_length=500)
    expected_version: int = Field(ge=1)


class OrderResponse(CamelModel):
    order_id: int
    order_no: str
    buyer_user_id: int
    seller_user_id: int
    demand_id: int | None
    quote_id: int | None
    service_snapshot: dict
    amount: Decimal
    platform_fee: Decimal
    discount_amount: Decimal
    payable_amount: Decimal
    paid_amount: Decimal
    shoot_at: datetime
    duration_minutes: int
    location_snapshot: dict
    contact_snapshot: dict
    remark: str | None
    status: str
    payment_status: str
    refund_status: str
    version: int
    create_time: datetime
    update_time: datetime
