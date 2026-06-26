from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.contact import Contact
from app.models.dispatch import Dispatch


@pytest.fixture
async def dispatch(session: AsyncSession) -> Dispatch:
    d = Dispatch(
        idempotency_key='test-key-1',
        message_hash='hash',
        provider='zapi',
        provider_message_id='msg-123',
        phone='5511999999999',
        lid=None,
        status='pending',
    )
    session.add(d)
    await session.commit()
    await session.refresh(d)
    return d


async def test_status_advances_to_received(
    client: AsyncClient, session: AsyncSession, dispatch: Dispatch
):
    payload = {
        'instanceId': 'abc',
        'type': 'MessageStatusCallback',
        'status': 'RECEIVED',
        'ids': ['msg-123'],
    }
    response = await client.post(
        f'/webhooks/zapi/status?token={settings.ZAPI_WEBHOOK_TOKEN}',
        json=payload,
    )
    assert response.status_code == HTTPStatus.OK

    await session.refresh(dispatch)
    assert dispatch.status == 'received'


async def test_status_does_not_regress(
    client: AsyncClient, session: AsyncSession, dispatch: Dispatch
):
    # avança pra read
    dispatch.status = 'read'
    await session.commit()

    # tenta regredir pra received
    payload = {
        'instanceId': 'abc',
        'type': 'MessageStatusCallback',
        'status': 'RECEIVED',
        'ids': ['msg-123'],
    }
    await client.post(
        f'/webhooks/zapi/status?token={settings.ZAPI_WEBHOOK_TOKEN}',
        json=payload,
    )

    await session.refresh(dispatch)
    assert dispatch.status == 'read'  # não regrediu


async def test_lid_updated_on_status(
    client: AsyncClient, session: AsyncSession, dispatch: Dispatch
):

    contact = Contact(
        name='Teste',
        phone='5511999999999',
        lid=None,
    )
    session.add(contact)
    await session.commit()

    payload = {
        'instanceId': 'abc',
        'type': 'MessageStatusCallback',
        'status': 'RECEIVED',
        'ids': ['msg-123'],
        'phone': '213004759113879@lid',
    }
    await client.post(
        f'/webhooks/zapi/status?token={settings.ZAPI_WEBHOOK_TOKEN}',
        json=payload,
    )

    await session.refresh(contact)
    assert contact.lid == '213004759113879@lid'
