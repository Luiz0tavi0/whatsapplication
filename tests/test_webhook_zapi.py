import ipdb
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def must_be_raise_exception_unauthorized(client: AsyncClient):
    response = await client.post('/webhooks/zapi/status')
    ipdb.set_trace()
