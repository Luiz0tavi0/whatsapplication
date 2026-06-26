from http import HTTPStatus

import ipdb  # noqa: F401
import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.mark.asyncio
async def test_must_be_raise_exception_unauthorized(client: AsyncClient):
    payload = {'instanceId': 'aasdasdasd5a4sd5a', 'type': 'send'}
    response = await client.post(
        '/webhooks/zapi/status?token=token-invalido', json=payload
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'invalid token'}


@pytest.mark.parametrize('missing_field', ['type', 'instanceId'])
@pytest.mark.asyncio
async def test_must_be_raise_unprocessable_content(
    missing_field: str, client: AsyncClient
):
    payload = {'type': 'send', 'instanceId': 'aweasdadsadadsa'}
    del payload[missing_field]
    response = await client.post(
        f'/webhooks/zapi/status?token={settings.ZAPI_WEBHOOK_TOKEN}',
        json=payload,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    # ipdb.set_trace()
    errors = response.json()['detail']
    assert errors[0]['loc'][1] == missing_field


# instanceId: str
# type: str
# status: Optional[str] = None
# phone: Optional[str] = None
# messageId: Optional[str] = None
# ids: Optional[list[str]] = None
