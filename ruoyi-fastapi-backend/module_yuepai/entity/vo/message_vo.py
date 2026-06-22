from typing import Literal

from pydantic import Field, model_validator

from module_yuepai.entity.vo.core_vo import CamelModel


class ConversationCreate(CamelModel):
    target_user_id: int = Field(ge=1)
    creator_id: int | None = Field(default=None, ge=1)
    order_id: int | None = Field(default=None, ge=1)


class MessageCreate(CamelModel):
    client_message_id: str = Field(min_length=16, max_length=64)
    message_type: Literal['text', 'image', 'quote', 'order'] = 'text'
    text: str | None = Field(default=None, max_length=2000)
    payload: dict = Field(default_factory=dict)

    @model_validator(mode='after')
    def validate_content(self):
        if self.message_type == 'text' and not (self.text or '').strip():
            raise ValueError('文本消息不能为空')
        if self.message_type == 'image' and not self.payload.get('url'):
            raise ValueError('图片消息缺少图片地址')
        return self
