from fastapi import APIRouter

w_router = APIRouter(prefix="webhooks", tags=['webhooks'])


@w_router.post('/')
async def zapi_status_message_webhook(payload: dict):
    ...

@w_router.post('/')
async def wireweb_status_message_webhook(payload: dict):
    ...
