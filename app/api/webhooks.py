import logging
import secrets
from http import HTTPStatus

from config import settings
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.providers.status_mapping import normalize_status
from app.services.status_service import StatusService

w_router = APIRouter(prefix='webhooks', tags=['webhooks'])
logger = logging.getLogger(__name__)


def get_status_service(
    session: AsyncSession = Depends(get_session),
) -> StatusService:
    return StatusService(session)


def verify_zapi_token(token: str = Query(...)) -> None:
    if not secrets.compare_digest(token, settings.zapi_webhook_token):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'invalid token')


def verify_wireweb_session(
    token: str = Query(...), x_wire_session_id: str = Header(...)
) -> None:
    if not secrets.compare_digest(token, settings.wireweb_webhook_token):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'invalid token')
    if not secrets.compare_digest(
        x_wire_session_id, settings.wireweb_session_id
    ):
        raise HTTPException(HTTPStatus.FORBIDDEN, 'unknown session')


@w_router.post('/', dependencies=[Depends(verify_zapi_token)])
async def zapi_status_message_webhook(
    payload: dict, service: StatusService = Depends(get_status_service)
):
    status = normalize_status('zapi', payload['status'])
    if status is None:
        return {'status': 'ignored'}
    await service.update_status('zapi', payload['messageId'], status)
    return {'status': 'ok'}


@w_router.post('/', dependencies=[Depends(verify_wireweb_session)])
async def wireweb_status_message_webhook(
    payload: dict, service: StatusService = Depends(get_status_service)
):
    status = normalize_status('wireweb', payload['event'])
    if status is None:
        logger.warning('Evento wireweb desconhecido: %s', payload['event'])
        return {'status': 'ignored'}
    await service.update_status('wireweb', payload['messageId'], status)
    return {'status': 'ok'}
