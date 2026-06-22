import logging
import secrets
from http import HTTPStatus

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from app.config import settings
from app.dependencies import T_StatusService
from app.providers.status_mapping import normalize_status
from app.schemas.common import ErrorResponse, StatusResponse
from app.schemas.webhooks import WireWebStatusPayload, ZApiStatusPayload

w_router = APIRouter(prefix='/webhooks', tags=['webhooks'])
logger = logging.getLogger(__name__)


def verify_zapi_token(token: str = Query(...)) -> None:
    if not secrets.compare_digest(token, settings.zapi_webhook_token):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'invalid token')


def verify_wireweb_session(
    token: str = Query(...), x_wire_session_id: str = Header(...)
) -> None:
    # ipdb.set_trace()
    if not secrets.compare_digest(token, settings.wireweb_webhook_token):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'invalid token')
    # ipdb.set_trace()
    if not secrets.compare_digest(
        x_wire_session_id, settings.wireweb_session_id
    ):
        raise HTTPException(HTTPStatus.FORBIDDEN, 'unknown session')


@w_router.post(
    '/zapi/status',
    response_model=StatusResponse,
    responses={
        HTTPStatus.UNAUTHORIZED: {'model': ErrorResponse},
        HTTPStatus.UNPROCESSABLE_CONTENT: {'model': ErrorResponse},
    },
    dependencies=[Depends(verify_zapi_token)],
)
async def zapi_status_message_webhook(
    payload: ZApiStatusPayload,
    service: T_StatusService,
):
    status = normalize_status('zapi', payload.status)
    if status is None:
        return StatusResponse(status='ignored')

    await service.update_status('zapi', payload.messageId, status)
    return StatusResponse(status='ok')


@w_router.post(
    '/wireweb/status',
    response_model=StatusResponse,
    responses={
        HTTPStatus.UNAUTHORIZED: {'model': ErrorResponse},
        HTTPStatus.UNPROCESSABLE_CONTENT: {'model': ErrorResponse},
        HTTPStatus.FORBIDDEN: {'model': ErrorResponse},
    },
    dependencies=[Depends(verify_wireweb_session)],
)
async def wireweb_status_message_webhook(
    payload: WireWebStatusPayload,
    service: T_StatusService,
):
    status = normalize_status('wireweb', payload.event)
    if status is None:
        logger.warning('Evento wireweb desconhecido: %s', payload.event)
        return StatusResponse(status='ignored')
    await service.update_status('wireweb', payload.messageId, status)
    return StatusResponse(status='ok')
