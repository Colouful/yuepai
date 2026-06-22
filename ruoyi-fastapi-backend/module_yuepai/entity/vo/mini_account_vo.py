from pydantic import Field

from module_yuepai.entity.vo.core_vo import CamelModel


class MiniAccountBind(CamelModel):
    login_code: str = Field(min_length=5, max_length=256)
