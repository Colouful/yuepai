import httpx

from module_yuepai.config.wechat_app_config import WechatAppConfig


class MiniProgramClientError(RuntimeError):
    pass


async def exchange_login_code(code: str) -> tuple[str, str | None]:
    WechatAppConfig.validate_runtime()
    params = {
        'appid': WechatAppConfig.yuepai_wechat_app_id,
        'secret': WechatAppConfig.yuepai_wechat_app_secret,
        'js_code': code,
        'grant_type': 'authorization_code',
    }
    async with httpx.AsyncClient(base_url=WechatAppConfig.yuepai_wechat_api_base_url, timeout=10) as client:
        response = await client.get('/sns/jscode2session', params=params)
    data = response.json()
    if response.status_code != 200 or data.get('errcode'):
        raise MiniProgramClientError(f"小程序账号交换失败：{data.get('errmsg') or response.status_code}")
    subject = str(data.get('openid') or '')
    if not subject:
        raise MiniProgramClientError('小程序账号交换未返回账号标识')
    union = str(data.get('unionid')) if data.get('unionid') else None
    return subject, union
