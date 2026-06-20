import asyncio
import hashlib
import logging
import uuid

import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import async_session
from app.models import Contact, Dispatch
from app.providers.dispatcher import ProviderDispatcher, build_providers

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)


async def get_contacts(limit: int = 3) -> list[Contact]:
    async with async_session() as session:
        result = await session.execute(select(Contact).limit(limit))
        return list(result.scalars().all())


async def dispatch_one(
    session, dispatcher: ProviderDispatcher, contact: Contact
) -> None:
    message = f'Olá, {contact.nome} tudo bem com você?'
    key = str(uuid.uuid4())
    msg_hash = hashlib.sha256(message.encode()).hexdigest()

    dispatch = Dispatch(
        idempotency_key=key,
        message_hash=msg_hash,
        provider='pending',
        phone=contact.telefone,
        lid=contact.lid,
        status='pending',
    )
    session.add(dispatch)
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        logger.info('Idempotency key duplicada, pulando: %s', key)
        return

    try:
        provider_name, message_id = await dispatcher.send_text(
            contact.telefone, contact.lid, message
        )
        dispatch.provider = provider_name
        dispatch.provider_message_id = message_id
        dispatch.status = 'sent'
        logger.info(
            'Enviado via %s para %s (id=%s)',
            provider_name,
            contact.telefone,
            message_id,
        )
    except RuntimeError as e:
        dispatch.status = 'failed'
        logger.error('Falha total ao enviar para %s: %s', contact.telefone, e)

    await session.commit()


async def main() -> None:
    contacts = await get_contacts(limit=3)
    if not contacts:
        logger.warning('Nenhum contato encontrado.')
        return

    logger.info('Encontrados %d contato(s).', len(contacts))

    async with httpx.AsyncClient(timeout=10) as client:
        dispatcher = ProviderDispatcher(build_providers(client))
        async with async_session() as session:
            for contact in contacts:
                await dispatch_one(session, dispatcher, contact)


if __name__ == '__main__':
    asyncio.run(main())
