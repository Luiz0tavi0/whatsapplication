from app.config import settings
from app.dependencies import T_HttpClient
from app.providers.base import WhatsAppProvider


class WireWebProvider(WhatsAppProvider):
    name = 'wireweb'
    supports_lid = False
    base_url = settings.wireweb_base_url

    def __init__(self, client: T_HttpClient):
        self.client = client
        self.url = f'{self.base_url}/api/v1/messages'
        self.headers = {'Authorization': f'Bearer {settings.wireweb_api_key}'}

    async def _send_text(self, recipient: str, message: str) -> str:
        resp = await self.client.post(
            self.url,
            json={
                'sessionId': settings.wireweb_session_id,
                'to': recipient,
                'text': message,
            },
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()['messageId']
