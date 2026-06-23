import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import Contact
from app.models.dispatch import Dispatch
from app.services.status_transition import is_valid_transition

logger = logging.getLogger(__name__)


class StatusService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_status(
        self,
        provider: str,
        provider_message_id: str,
        new_status: str,
        lid: str | None = None,
    ) -> bool:
        result = await self.session.execute(
            select(Dispatch).where(
                Dispatch.provider == provider,
                Dispatch.provider_message_id == provider_message_id,
            )
        )
        dispatch = result.scalar_one_or_none()
        if dispatch is None:
            logger.warning(
                f'Dispatch não encontrado: {provider}/{provider_message_id}'
            )
            return False

        if not is_valid_transition(dispatch.status, new_status):
            logger.info(
                f'Transição ignorada: {dispatch.status} -> {new_status}'
            )
            return False

        dispatch.status = new_status

        if lid and '@lid' in lid:
            result = await self.session.execute(
                select(Contact).where(
                    Contact.phone == dispatch.phone, Contact.lid.is_(None)
                )
            )
            contact = result.scalar_one_or_none()
            if contact:
                contact.lid = lid

        await self.session.commit()
        return True

    # async def update_status(
    #     self, provider: str, provider_message_id: str, new_status: str
    # ) -> bool:
    #     result = await self.session.execute(
    #         select(Dispatch).where(
    #             Dispatch.provider == provider,
    #             Dispatch.provider_message_id == provider_message_id,
    #         )
    #     )
    #     dispatch = result.scalar_one_or_none()
    #     # ipdb.set_trace()
    #     if dispatch is None:
    #         logger.warning(
    #             f'Dispatch não encontrado: {provider}/{provider_message_id}'
    #         )
    #         return False

    #     if not is_valid_transition(dispatch.status, new_status):
    #         logger.info(
    #             f'Transição ignorada: {dispatch.status} -> {new_status}'
    #         )
    #         return False

    #     dispatch.status = new_status
    #     await self.session.commit()
    #     return True
