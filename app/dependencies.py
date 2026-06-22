from typing import Annotated, AsyncGenerator

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.providers.dispatcher import ProviderDispatcher, build_providers
from app.services.dispatch_service import DispatchService
from app.services.status_service import StatusService

T_DBSession = Annotated[AsyncSession, Depends(get_session)]


def get_status_service(
    session: T_DBSession,
) -> StatusService:
    return StatusService(session)


T_StatusService = Annotated[StatusService, Depends(get_status_service)]


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(timeout=10) as client:
        yield client


T_HttpClient = Annotated[httpx.AsyncClient, Depends(get_http_client)]


def get_provider_dispatcher(client: T_HttpClient) -> ProviderDispatcher:
    return ProviderDispatcher(build_providers(client))


T_Dispatcher = Annotated[ProviderDispatcher, Depends(get_provider_dispatcher)]


def get_dispatch_service(
    session: T_DBSession,
    dispatcher: T_Dispatcher,
) -> DispatchService:
    return DispatchService(session, dispatcher)


T_DispatchService = Annotated[DispatchService, Depends(get_dispatch_service)]
