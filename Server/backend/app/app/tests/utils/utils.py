import random
import string
from typing import Dict

from app.core import security
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.core.config import settings
from datetime import datetime, timedelta
from jose import jwt


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def get_superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert 200 <= r.status_code < 300
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


async def get_normal_user_token_headers(client: AsyncClient) -> Dict[str, str]:
    login_data = {
        "username": settings.EMAIL_TEST_USER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert 200 == r.status_code
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


async def get_gateway_refresh_token_headers(client: AsyncClient, headers: Dict[str, str]) -> Dict[str, str]:
    r = await client.get(
        f"{settings.API_V1_STR}/gateway/{settings.UUID_TEST_GATEWAY}/get-token", headers=headers
    )
    assert 200 <= r.status_code < 300
    tokens = r.json()
    a_token = tokens["refresh_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


async def get_gateway_access_token_headers(client: AsyncClient, headers: Dict[str, str]) -> Dict[str, str]:
    r = await client.get(
        f"{settings.API_V1_STR}/gateway/{settings.UUID_TEST_GATEWAY}/get-token", headers=headers
    )
    assert 200 <= r.status_code < 300
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


async def get_gateway_token(client: AsyncClient, headers: Dict[str, str]) -> Dict[str, str]:
    r = await client.get(
        f"{settings.API_V1_STR}/gateway/{settings.UUID_TEST_GATEWAY}/get-token", headers=headers
    )
    assert 200 <= r.status_code < 300
    tokens = r.json()
    a_token = tokens["access_token"]
    return a_token
