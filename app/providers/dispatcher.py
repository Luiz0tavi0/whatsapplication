import logging

import httpx

from app.config import settings
from app.providers.base import WhatsAppProvider
from app.providers.wireweb import WireWebProvider
from app.providers.zapi import ZApiProvider

logger = logging.getLogger(__name__)

PROVIDER_REGISTRY = {'zapi': ZApiProvider, 'wireweb': WireWebProvider}


def build_providers(client: httpx.AsyncClient) -> list[WhatsAppProvider]:
    return [
        PROVIDER_REGISTRY[name](client)
        for name in settings.providers_order
        if name in PROVIDER_REGISTRY
    ]


class ProviderDispatcher:
    def __init__(self, providers: list[WhatsAppProvider]):
        if not providers:
            raise ValueError('Pelo menos um provider é necessário')
        self.providers = providers

    async def send_text(
        self, phone: str, lid: str | None, message: str
    ) -> tuple[str, str]:
        last_error: Exception | None = None
        for provider in self.providers:
            try:
                message_id = await provider.send_text(phone, lid, message)
                return provider.name, message_id
            except Exception as e:
                logger.warning('Falha no provider %s: %s', provider.name, e)
                last_error = e
        raise RuntimeError(
            f'Todos os providers falharam. Último erro: {last_error}'
        )
