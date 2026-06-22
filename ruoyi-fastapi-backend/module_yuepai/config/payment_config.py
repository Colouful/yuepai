from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class WechatPaySettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    yuepai_payment_enabled: bool = False
    yuepai_wechat_pay_app_id: str = ''
    yuepai_wechat_pay_mch_id: str = ''
    yuepai_wechat_pay_serial_no: str = ''
    yuepai_wechat_pay_api_v3_key: str = ''
    yuepai_wechat_pay_private_key_path: str = ''
    yuepai_wechat_pay_platform_cert_path: str = ''
    yuepai_wechat_pay_notify_url: str = ''
    yuepai_wechat_pay_base_url: str = 'https://api.mch.weixin.qq.com'

    def validate_runtime(self) -> None:
        if not self.yuepai_payment_enabled:
            raise RuntimeError('微信支付未启用')
        required = {
            'YUEPAI_WECHAT_PAY_APP_ID': self.yuepai_wechat_pay_app_id,
            'YUEPAI_WECHAT_PAY_MCH_ID': self.yuepai_wechat_pay_mch_id,
            'YUEPAI_WECHAT_PAY_SERIAL_NO': self.yuepai_wechat_pay_serial_no,
            'YUEPAI_WECHAT_PAY_API_V3_KEY': self.yuepai_wechat_pay_api_v3_key,
            'YUEPAI_WECHAT_PAY_PRIVATE_KEY_PATH': self.yuepai_wechat_pay_private_key_path,
            'YUEPAI_WECHAT_PAY_PLATFORM_CERT_PATH': self.yuepai_wechat_pay_platform_cert_path,
            'YUEPAI_WECHAT_PAY_NOTIFY_URL': self.yuepai_wechat_pay_notify_url,
        }
        missing = [name for name, value in required.items() if not value.strip()]
        if missing:
            raise RuntimeError(f'微信支付缺少配置：{", ".join(missing)}')
        if len(self.yuepai_wechat_pay_api_v3_key.encode()) != 32:
            raise RuntimeError('YUEPAI_WECHAT_PAY_API_V3_KEY 必须为 32 字节')
        if not self.yuepai_wechat_pay_notify_url.startswith('https://'):
            raise RuntimeError('微信支付回调地址必须使用 HTTPS')
        for path_value, label in (
            (self.yuepai_wechat_pay_private_key_path, '商户私钥'),
            (self.yuepai_wechat_pay_platform_cert_path, '微信支付平台证书'),
        ):
            path = Path(path_value)
            if not path.is_file():
                raise RuntimeError(f'{label}文件不存在：{path}')


WechatPayConfig = WechatPaySettings()
