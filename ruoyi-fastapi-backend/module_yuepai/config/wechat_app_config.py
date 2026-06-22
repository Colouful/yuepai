import base64

from pydantic_settings import BaseSettings, SettingsConfigDict


class WechatAppSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    yuepai_wechat_app_id: str = ''
    yuepai_wechat_app_secret: str = ''
    yuepai_identity_encryption_key: str = ''
    yuepai_wechat_api_base_url: str = 'https://api.weixin.qq.com'

    def encryption_key(self) -> bytes:
        if not self.yuepai_identity_encryption_key:
            raise RuntimeError('YUEPAI_IDENTITY_ENCRYPTION_KEY 未配置')
        try:
            key = base64.urlsafe_b64decode(self.yuepai_identity_encryption_key.encode())
        except Exception as exc:
            raise RuntimeError('身份加密密钥不是有效的 URL-safe Base64') from exc
        if len(key) != 32:
            raise RuntimeError('身份加密密钥解码后必须为 32 字节')
        return key

    def validate_runtime(self) -> None:
        missing = []
        if not self.yuepai_wechat_app_id.strip():
            missing.append('YUEPAI_WECHAT_APP_ID')
        if not self.yuepai_wechat_app_secret.strip():
            missing.append('YUEPAI_WECHAT_APP_SECRET')
        if missing:
            raise RuntimeError(f'微信小程序缺少配置：{", ".join(missing)}')
        self.encryption_key()


WechatAppConfig = WechatAppSettings()
