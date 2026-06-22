from pydantic import Field

from module_yuepai.entity.vo.core_vo import CamelModel


class SecurePaymentPrepare(CamelModel):
    request_id: str = Field(min_length=16, max_length=64)
