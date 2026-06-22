from pydantic import Field

from module_yuepai.entity.vo.core_vo import CamelModel


class DeliverySubmit(CamelModel):
    request_id: str = Field(min_length=16, max_length=64)
    expected_order_version: int = Field(ge=1)
    original_assets: list[str] = Field(default_factory=list, max_length=500)
    retouched_assets: list[str] = Field(min_length=1, max_length=200)
    note: str | None = Field(default=None, max_length=1000)


class DeliveryDecision(CamelModel):
    request_id: str = Field(min_length=16, max_length=64)
    expected_order_version: int = Field(ge=1)
    accepted: bool
    reason: str | None = Field(default=None, max_length=1000)
