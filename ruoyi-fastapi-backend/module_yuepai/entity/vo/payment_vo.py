from decimal import Decimal

from pydantic import Field

from module_yuepai.entity.vo.core_vo import CamelModel


class PaymentPrepareRequest(CamelModel):
    request_id: str = Field(min_length=16, max_length=64)
    payer_openid: str = Field(min_length=8, max_length=128)


class RefundCreateRequest(CamelModel):
    request_id: str = Field(min_length=16, max_length=64)
    amount: Decimal = Field(gt=0, le=9999999)
    reason: str = Field(min_length=4, max_length=500)
    evidence: list[str] = Field(default_factory=list, max_length=20)
