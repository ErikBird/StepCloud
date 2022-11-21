from typing import Dict
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.sqlmodels import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


async def test_get_users_superuser_me(
        client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.API_V1_STR}/customers/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


async def test_get_users_normal_user_me(
        client: AsyncClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.API_V1_STR}/customers/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER
