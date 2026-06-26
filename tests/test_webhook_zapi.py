from http import HTTPStatus

import ipdb  # noqa: F401
import pytest
from httpx import AsyncClient

from app.config import settings


async def test_unauthorized_invalid_token(client: AsyncClient):
    payload = {'instanceId': 'abc', 'type': 'send'}
    response = await client.post(
        '/webhooks/zapi/status?token=token-invalido', json=payload
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'invalid token'}


async def test_unauthorized_missing_token(client: AsyncClient):
    payload = {'instanceId': 'abc', 'type': 'send'}
    response = await client.post('/webhooks/zapi/status', json=payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('missing_field', ['type', 'instanceId'])
async def test_unprocessable_missing_field(
    missing_field: str, client: AsyncClient
):
    payload = {'type': 'send', 'instanceId': 'abc'}
    del payload[missing_field]
    response = await client.post(
        f'/webhooks/zapi/status?token={settings.ZAPI_WEBHOOK_TOKEN}',
        json=payload,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    errors = response.json()['detail']
    assert errors[0]['loc'][1] == missing_field


async def test_valid_delivery_callback(client: AsyncClient):
    payload = {
        'instanceId': 'abc',
        'type': 'DeliveryCallback',
        'messageId': 'msg-123',
    }
    response = await client.post(
        f'/webhooks/zapi/status?token={settings.ZAPI_WEBHOOK_TOKEN}',
        json=payload,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ok'}


async def test_unknown_status_ignored(client: AsyncClient):
    payload = {
        'instanceId': 'abc',
        'type': 'MessageStatusCallback',
        'status': 'UNKNOWN_STATUS',
        'ids': ['msg-123'],
    }
    response = await client.post(
        f'/webhooks/zapi/status?token={settings.ZAPI_WEBHOOK_TOKEN}',
        json=payload,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ignored'}
