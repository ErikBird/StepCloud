import os
from typing import Dict, Generator, AsyncGenerator

from app.core import security
from asgi_lifespan import LifespanManager

from app.db.session import engine_async, async_session
from httpx import AsyncClient
import pytest
import asyncio
from app.core.config import settings
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import \
    get_superuser_token_headers, get_gateway_access_token_headers, get_gateway_token, get_gateway_refresh_token_headers, \
    get_normal_user_token_headers
import pytest_asyncio
from sqlmodel import SQLModel
from app.db.init_db import init_db
import logging
from app.main import app
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine
from app.api import deps
from datetime import datetime, timedelta


async def override_get_db():
    mydb = AsyncSession(
        bind=engine_async,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    try:
        yield mydb
    finally:
        await mydb.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(async_get_db: AsyncSession) -> None:
    try:
        # Try to create session to check if DB is awake
        async with engine_async.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
        await init_db(db=async_get_db)
        await async_get_db.execute("SELECT 1")
        yield
    except Exception as e:
        raise e


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_get_db(event_loop) -> AsyncGenerator:
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def client(setup_db) -> AsyncClient:
    async with LifespanManager(app):
        app.dependency_overrides[deps.async_get_db] = override_get_db
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac


@pytest_asyncio.fixture()
async def superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    headers = await get_superuser_token_headers(client)
    return headers


@pytest_asyncio.fixture()
async def normal_user_token_headers(client: AsyncClient) -> Dict[str, str]:
    headers = await get_normal_user_token_headers(client)
    return headers


@pytest_asyncio.fixture()
async def gateway_access_token_headers(client: AsyncClient, normal_user_token_headers: Dict[str, str]) -> Dict[
    str, str]:
    headers = await get_gateway_access_token_headers(client, headers=normal_user_token_headers)
    return headers


@pytest_asyncio.fixture()
async def gateway_refresh_token_headers(client: AsyncClient, normal_user_token_headers: Dict[str, str]) -> Dict[
    str, str]:
    headers = await get_gateway_refresh_token_headers(client, headers=normal_user_token_headers)
    return headers


@pytest_asyncio.fixture()
async def gateway_token(client: AsyncClient, normal_user_token_headers: Dict[str, str]) -> Dict[str, str]:
    token = await get_gateway_token(client, headers=normal_user_token_headers)
    return token


@pytest_asyncio.fixture()
async def gateway_token_header_expired() -> Dict[str, str]:
    # Access Token with a negative time delta (results in a timestamp in the past) of one minute
    a_token = security.create_access_token(settings.UUID_TEST_GATEWAY, expires_delta=-timedelta(minutes=1))
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
