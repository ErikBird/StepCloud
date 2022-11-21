from typing import Dict
import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from app import crud
from app.core.config import settings
import logging

from app.tests.utils.customer_device import create_random_customer_device

pytestmark = pytest.mark.asyncio


async def test_token(
        client: AsyncClient, gateway_access_token_headers: Dict[str, str]) -> None:
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/test-token",
                          headers=gateway_access_token_headers)
    device_event = r.json()
    assert 200 <= r.status_code < 300
    assert str(device_event['uuid'])


async def test_expired_access_token(client: AsyncClient, gateway_token_header_expired: Dict[str, str]):
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/test-token",
                          headers=gateway_token_header_expired)
    device_event = r.json()
    assert r.status_code == 403


async def test_access_token_refresh(client: AsyncClient, gateway_refresh_token_headers: Dict[str, str],
                                    async_get_db: AsyncSession) -> None:
    # Use refresh-token to get new access-token
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/refresh",
                          headers=gateway_refresh_token_headers)
    assert 200 <= r.status_code < 300
    # test received access-token
    access_token = r.json()['access_token']
    headers = {"Authorization": f"Bearer {access_token}"}
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/test-token",
                          headers=headers)
    token = r.json()
    assert 200 <= r.status_code < 300
    assert str(token['uuid'])
