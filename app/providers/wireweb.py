import httpx

from app.config import settings
from app.providers.base import WhatsAppProvider


class WireWebProvider(WhatsAppProvider):
    name = 'wireweb'
    supports_lid = False
    base_url = settings.WIREWEB_BASE_URL

    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.url = f'{self.base_url}/api/v1/messages'
        self.headers = {'Authorization': f'Bearer {settings.WIREWEB_API_KEY}'}

    async def _send_text(self, recipient: str, message: str) -> str:
        resp = await self.client.post(
            self.url,
            json={
                'sessionId': settings.WIREWEB_SESSION_ID,
                'to': recipient,
                'text': message,
            },
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()['messageId']
