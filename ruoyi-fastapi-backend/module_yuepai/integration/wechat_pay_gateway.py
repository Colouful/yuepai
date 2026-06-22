from __future__ import annotations

import base64
import json
import secrets
import time
from pathlib import Path
from typing import Any

import httpx
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from module_yuepai.config.payment_config import WechatPayConfig, WechatPaySettings


class WechatPayGatewayError(RuntimeError):
    pass


class WechatPayGateway:
    def __init__(self, settings: WechatPaySettings | None = None) -> None:
        self.settings = settings or WechatPayConfig
        self.settings.validate_runtime()
        private_key_bytes = Path(self.settings.yuepai_wechat_pay_private_key_path).read_bytes()
        self.private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
        cert_bytes = Path(self.settings.yuepai_wechat_pay_platform_cert_path).read_bytes()
        self.platform_cert = x509.load_pem_x509_certificate(cert_bytes)

    async def prepare_jsapi(self, *, payment_no: str, description: str, amount_fen: int, payer_openid: str, expires_at: str) -> dict[str, Any]:
        if amount_fen <= 0:
            raise WechatPayGatewayError('支付金额必须大于零')
        payload = {
            'appid': self.settings.yuepai_wechat_pay_app_id,
            'mchid': self.settings.yuepai_wechat_pay_mch_id,
            'description': description[:127],
            'out_trade_no': payment_no,
            'time_expire': expires_at,
            'notify_url': self.settings.yuepai_wechat_pay_notify_url,
            'amount': {'total': amount_fen, 'currency': 'CNY'},
            'payer': {'openid': payer_openid},
        }
        path = '/v3/pay/transactions/jsapi'
        body = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
        headers = self._authorization_headers('POST', path, body)
        async with httpx.AsyncClient(base_url=self.settings.yuepai_wechat_pay_base_url, timeout=15) as client:
            response = await client.post(path, content=body.encode(), headers=headers)
        if response.status_code != 200:
            raise WechatPayGatewayError(self._provider_error(response))
        data = response.json()
        prepay_id = data.get('prepay_id')
        if not prepay_id:
            raise WechatPayGatewayError('微信支付未返回 prepay_id')
        return {'prepayId': prepay_id, 'invokeParams': self._mini_program_invoke_params(prepay_id)}

    async def request_refund(self, *, payment_no: str, refund_no: str, total_fen: int, refund_fen: int, reason: str) -> dict[str, Any]:
        if refund_fen <= 0 or refund_fen > total_fen:
            raise WechatPayGatewayError('退款金额无效')
        payload = {
            'out_trade_no': payment_no,
            'out_refund_no': refund_no,
            'reason': reason[:80],
            'notify_url': self.settings.yuepai_wechat_refund_notify_url,
            'amount': {'refund': refund_fen, 'total': total_fen, 'currency': 'CNY'},
        }
        path = '/v3/refund/domestic/refunds'
        body = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
        headers = self._authorization_headers('POST', path, body)
        async with httpx.AsyncClient(base_url=self.settings.yuepai_wechat_pay_base_url, timeout=15) as client:
            response = await client.post(path, content=body.encode(), headers=headers)
        if response.status_code not in {200, 201}:
            raise WechatPayGatewayError(self._provider_error(response))
        return response.json()

    def verify_and_decrypt_notification(self, *, body: bytes, timestamp: str, nonce: str, signature: str) -> dict[str, Any]:
        message = f'{timestamp}\n{nonce}\n{body.decode()}\n'.encode()
        try:
            self.platform_cert.public_key().verify(base64.b64decode(signature), message, padding.PKCS1v15(), hashes.SHA256())
        except Exception as exc:
            raise WechatPayGatewayError('微信支付回调签名验证失败') from exc
        envelope = json.loads(body)
        resource = envelope.get('resource') or {}
        required = ('ciphertext', 'nonce', 'associated_data')
        if any(resource.get(name) is None for name in required):
            raise WechatPayGatewayError('微信支付回调资源字段不完整')
        try:
            plaintext = AESGCM(self.settings.yuepai_wechat_pay_api_v3_key.encode()).decrypt(
                resource['nonce'].encode(),
                base64.b64decode(resource['ciphertext']),
                resource['associated_data'].encode(),
            )
            data = json.loads(plaintext)
        except Exception as exc:
            raise WechatPayGatewayError('微信支付回调解密失败') from exc
        return {'event': envelope, 'resource': data}

    def _authorization_headers(self, method: str, path: str, body: str) -> dict[str, str]:
        timestamp = str(int(time.time()))
        nonce = secrets.token_hex(16)
        message = f'{method}\n{path}\n{timestamp}\n{nonce}\n{body}\n'.encode()
        signature = base64.b64encode(self.private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())).decode()
        token = (
            'WECHATPAY2-SHA256-RSA2048 '
            f'mchid="{self.settings.yuepai_wechat_pay_mch_id}",'
            f'nonce_str="{nonce}",signature="{signature}",'
            f'timestamp="{timestamp}",serial_no="{self.settings.yuepai_wechat_pay_serial_no}"'
        )
        return {'Authorization': token, 'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': '91YuepaiPro/1.0'}

    def _mini_program_invoke_params(self, prepay_id: str) -> dict[str, str]:
        timestamp = str(int(time.time()))
        nonce = secrets.token_hex(16)
        package_value = f'prepay_id={prepay_id}'
        message = f'{self.settings.yuepai_wechat_pay_app_id}\n{timestamp}\n{nonce}\n{package_value}\n'.encode()
        pay_sign = base64.b64encode(self.private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())).decode()
        return {'timeStamp': timestamp, 'nonceStr': nonce, 'package': package_value, 'signType': 'RSA', 'paySign': pay_sign}

    @staticmethod
    def _provider_error(response: httpx.Response) -> str:
        try:
            data = response.json()
            code = data.get('code') or response.status_code
            message = data.get('message') or response.text
            return f'微信支付请求失败[{code}]：{message}'
        except Exception:
            return f'微信支付请求失败[{response.status_code}]'
