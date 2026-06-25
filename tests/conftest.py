from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app


async def client(session: AsyncSession) -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac
