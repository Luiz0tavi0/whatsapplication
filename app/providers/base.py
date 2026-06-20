from abc import ABC, abstractmethod
from http import HTTPStatus

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

RETRYABLE = (
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
)


def _retryable(exc: BaseException) -> bool:
    if isinstance(exc, RETRYABLE):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR
    return False


class WhatsAppProvider(ABC):
    name: str
    supports_lid: bool = False

    @abstractmethod
    async def _send_text(self, recipient: str, message: str) -> str: ...

    def resolve_recipient(self, phone: str, lid: str | None) -> str:
        return lid if (self.supports_lid and lid) else phone

    @retry(
        retry=retry_if_exception(_retryable),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    async def send_text(
        self, phone: str, lid: str | None, message: str
    ) -> str:
        recipient = self.resolve_recipient(phone, lid)
        return await self._send_text(recipient, message)
