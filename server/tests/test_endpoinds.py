from pytest import mark

from .contests import async_client

from ..db import (
    db_manager,
    Link,
    select
)


@mark.asyncio
async def test_register_success(async_client):
    user_data = {
        "name": "testuser",
        "password": "password123"
    }
    response = await async_client.post("/auth/register", json=user_data)
    assert response.status == 201


@mark.asyncio
async def test_login_success(async_client):
    user_data = {
        "name": "loginuser",
        "password": "password123"
    }
    await async_client.post("/auth/register", json=user_data)
    
    login_data = {
        "name": "loginuser",
        "password": "password123"
    }

    response = await async_client.post("/auth/token", data=login_data)
    assert response.status == 200


@mark.asyncio
async def test_login_invalid_password(async_client):
    login_data = {
        "name": "loginuser",
        "password": "cxvlkjsfsdlk"
    }

    response = await async_client.post("/auth/token", data=login_data)
    assert response.status == 401


@mark.asyncio
async def test_link(async_client):
        async with async_client.get(f'/links/37489237598476945367') as response:
            assert response.status == 404