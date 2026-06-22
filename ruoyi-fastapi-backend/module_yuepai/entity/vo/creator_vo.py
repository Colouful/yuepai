from datetime import date
from decimal import Decimal

from pydantic import Field, field_validator

from module_yuepai.entity.vo.core_vo import CamelModel


class CreatorProfileUpsert(CamelModel):
    role_code: str = Field(min_length=2, max_length=32)
    display_name: str = Field(min_length=2, max_length=50)
    headline: str | None = Field(default=None, max_length=120)
    bio: str | None = Field(default=None, max_length=5000)
    avatar_url: str | None = Field(default=None, max_length=500)
    cover_url: str | None = Field(default=None, max_length=500)
    city_code: str = Field(min_length=2, max_length=20)
    service_cities: list[str] = Field(default_factory=list, max_length=20)
    tags: list[str] = Field(default_factory=list, max_length=20)
    years_experience: int = Field(default=0, ge=0, le=80)
    base_price: Decimal | None = Field(default=None, ge=0, le=9999999)
    accept_mutual: bool = False

    @field_validator('service_cities', 'tags')
    @classmethod
    def normalize_list(cls, value: list[str]) -> list[str]:
        items = [item.strip() for item in value if item and item.strip()]
        return list(dict.fromkeys(items))


class CreatorWorkCreate(CamelModel):
    creator_id: int = Field(ge=1)
    title: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    category: str = Field(min_length=2, max_length=32)
    cover_url: str = Field(min_length=8, max_length=500)
    assets: list[str] = Field(min_length=1, max_length=30)
    tags: list[str] = Field(default_factory=list, max_length=20)
    city_code: str | None = Field(default=None, max_length=20)
    shot_date: date | None = None

    @field_validator('assets', 'tags')
    @classmethod
    def normalize_assets(cls, value: list[str]) -> list[str]:
        items = [item.strip() for item in value if item and item.strip()]
        return list(dict.fromkeys(items))


class ServicePackageCreate(CamelModel):
    creator_id: int = Field(ge=1)
    package_name: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=10, max_length=5000)
    cover_url: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(gt=0, le=9999999)
    duration_minutes: int = Field(ge=30, le=1440)
    original_count: int = Field(default=0, ge=0, le=10000)
    retouched_count: int = Field(default=0, ge=0, le=1000)
    delivery_days: int = Field(default=7, ge=1, le=180)
    revision_count: int = Field(default=1, ge=0, le=20)
    includes: list[str] = Field(default_factory=list, max_length=30)
    excludes: list[str] = Field(default_factory=list, max_length=30)
    addons: list[dict] = Field(default_factory=list, max_length=30)
    booking_notice: str | None = Field(default=None, max_length=3000)
    refund_rule: str | None = Field(default=None, max_length=3000)


class ReviewCreate(CamelModel):
    order_id: int = Field(ge=1)
    rating: int = Field(ge=1, le=5)
    service_rating: int = Field(ge=1, le=5)
    communication_rating: int = Field(ge=1, le=5)
    delivery_rating: int = Field(ge=1, le=5)
    content: str = Field(min_length=5, max_length=1000)
    assets: list[str] = Field(default_factory=list, max_length=9)


class AuditDecision(CamelModel):
    approved: bool
    reason: str | None = Field(default=None, max_length=500)
