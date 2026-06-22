import hashlib
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import logging

from app.models.dispatch import Dispatch
from app.providers.dispatcher import ProviderDispatcher

logger = logging.getLogger(__name__)


class DispatchService:
    def __init__(self, session: AsyncSession, provider_dispatcher: ProviderDispatcher):
        self.session=session
        self.dispatcher=provider_dispatcher

    async def send_to_contact(self, phone: str, lid: str | None, nome: str) -> Dispatch | None:
        message = f"Olá, {nome} tudo bem com você?"
        key = str(uuid.uuid4())
        msg_hash = hashlib.sha256(message.encode()).hexdigest()

        dispatch = Dispatch(
            idempotency_key=key,
            message_hash=msg_hash,
            provider="pending",
            provider_message_id=None,
            phone=phone,
            lid=lid,
            status="pending",
        )
        self.session.add(dispatch)
        try:
            await self.session.flush()
        except IntegrityError:
            logger.info(f"Idempotency key duplicada: {key}")
            return None

        try:
            provider_name, message_id = await self.dispatcher.send_text(phone, lid, message)
            dispatch.provider = provider_name
            dispatch.provider_message_id = message_id
            dispatch.status = "sent"
        except RuntimeError as e:
            dispatch.status = "failed"
            logger.error(f"Falha total ao enviar para {phone}: {e}")

        await self.session.commit()
        return dispatch