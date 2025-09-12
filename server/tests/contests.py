from aiohttp import ClientSession

from pytest_asyncio import fixture

from .. import API_URL

@fixture
async def async_client():
    async with ClientSession('http://127.0.0.1:8000') as session:
        yield session