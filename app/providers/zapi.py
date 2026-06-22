import httpx

from app.config import settings
from app.providers.base import WhatsAppProvider


class ZApiProvider(WhatsAppProvider):
    name = 'zapi'
    supports_lid = True
    base_url = settings.zapi_base_url

    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.url = (
            f'{self.base_url}instances/{settings.zapi_instance}'
            f'/token/{settings.zapi_token}/send-text'
        )
        self.headers = (
            {'Client-Token': settings.zapi_client_token}
            if settings.zapi_client_token
            else {}
        )

    async def _send_text(self, recipient: str, message: str) -> str:
        resp = await self.client.post(
            self.url,
            json={'phone': recipient, 'message': message},
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()['messageId']
