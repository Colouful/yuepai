from pydantic_settings import BaseSettings, SettingsConfigDict

from config.env import AppConfig, DataBaseConfig, JwtConfig


_DEFAULT_JWT_SECRET = 'b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55'
_DEFAULT_DB_PASSWORDS = {'', 'mysqlroot', 'root', 'password', '123456'}


class YuepaiProductionSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    yuepai_payment_enabled: bool = False
    yuepai_wechat_pay_app_id: str = ''
    yuepai_wechat_pay_mch_id: str = ''
    yuepai_wechat_pay_serial_no: str = ''
    yuepai_wechat_pay_api_v3_key: str = ''
    yuepai_wechat_pay_private_key_path: str = ''
    yuepai_storage_provider: str = 'local'
    yuepai_storage_bucket: str = ''
    yuepai_storage_endpoint: str = ''
    yuepai_sms_provider: str = 'disabled'
    yuepai_content_moderation_provider: str = 'disabled'


YuepaiProductionConfig = YuepaiProductionSettings()


def validate_yuepai_production_readiness() -> None:
    if AppConfig.app_env.lower() not in {'prod', 'production'}:
        return

    errors: list[str] = []
    if JwtConfig.jwt_secret_key == _DEFAULT_JWT_SECRET or len(JwtConfig.jwt_secret_key) < 32:
        errors.append('JWT_SECRET_KEY 必须替换为至少 32 位的生产密钥')
    if DataBaseConfig.db_password.lower() in _DEFAULT_DB_PASSWORDS:
        errors.append('DB_PASSWORD 不得使用空值或默认弱密码')
    if AppConfig.app_demo_mode:
        errors.append('APP_DEMO_MODE 在生产环境必须关闭')
    if AppConfig.app_reload:
        errors.append('APP_RELOAD 在生产环境必须关闭')
    if AppConfig.app_root_path in {'', '/dev-api'}:
        errors.append('APP_ROOT_PATH 必须配置为生产 API 前缀')

    payment = YuepaiProductionConfig
    if not payment.yuepai_payment_enabled:
        errors.append('YUEPAI_PAYMENT_ENABLED 必须开启，禁止使用模拟支付')
    else:
        required_payment = {
            'YUEPAI_WECHAT_PAY_APP_ID': payment.yuepai_wechat_pay_app_id,
            'YUEPAI_WECHAT_PAY_MCH_ID': payment.yuepai_wechat_pay_mch_id,
            'YUEPAI_WECHAT_PAY_SERIAL_NO': payment.yuepai_wechat_pay_serial_no,
            'YUEPAI_WECHAT_PAY_API_V3_KEY': payment.yuepai_wechat_pay_api_v3_key,
            'YUEPAI_WECHAT_PAY_PRIVATE_KEY_PATH': payment.yuepai_wechat_pay_private_key_path,
        }
        errors.extend(f'{name} 未配置' for name, value in required_payment.items() if not value.strip())

    if payment.yuepai_storage_provider.lower() == 'local':
        errors.append('生产环境必须配置对象存储，YUEPAI_STORAGE_PROVIDER 不得为 local')
    if not payment.yuepai_storage_bucket.strip():
        errors.append('YUEPAI_STORAGE_BUCKET 未配置')
    if not payment.yuepai_storage_endpoint.strip():
        errors.append('YUEPAI_STORAGE_ENDPOINT 未配置')
    if payment.yuepai_sms_provider.lower() == 'disabled':
        errors.append('YUEPAI_SMS_PROVIDER 未配置，手机号登录和安全通知不可用')
    if payment.yuepai_content_moderation_provider.lower() == 'disabled':
        errors.append('YUEPAI_CONTENT_MODERATION_PROVIDER 未配置，内容不可安全上线')

    if errors:
        details = '\n'.join(f'- {item}' for item in errors)
        raise RuntimeError(f'91约拍Pro 生产启动检查失败：\n{details}')
