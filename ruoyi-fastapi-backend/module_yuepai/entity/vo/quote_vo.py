from pydantic import Field

from module_yuepai.entity.vo.core_vo import CamelModel


class QuoteStatusAction(CamelModel):
    expected_version: int = Field(ge=1)
    reason: str | None = Field(default=None, max_length=500)
