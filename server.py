from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.webhooks import w_router

http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client  # noqa: PLW0603
    async with httpx.AsyncClient(timeout=10) as client:
        http_client = client
        yield
    http_client = None


app = FastAPI(title='WA Status Receiver', lifespan=lifespan)


app.include_router(w_router)
