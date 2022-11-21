import logging
from typing import Dict
import pytest
from httpx import AsyncClient
from app import crud
from app.core.config import settings
from app.sqlmodels import UserCreate
from app.tests.utils.utils import random_email, random_lower_string
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


async def test_create_user_existing_username(
        client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    c = await client.get(
        f"{settings.ADMIN_API_V1_STR}/customers/", headers=superuser_token_headers,
    )
    assert 200 <= c.status_code < 300
    customer = c.json()[0]
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, customer_id=customer["id"], first_name='Random',
                         last_name='Name')
    await crud.user.create(db=async_get_db, obj_in=user_in)
    data = {"email": username, "password": password, "customer_id": customer["id"], 'first_name': 'Random',
            'last_name': 'Name'}
    r = await client.post(
        f"{settings.ADMIN_API_V1_STR}/customers/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


async def test_create_user_by_normal_user(
        client: AsyncClient, normal_user_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str]
) -> None:
    c = await client.get(
        f"{settings.ADMIN_API_V1_STR}/customers/", headers=superuser_token_headers,
    )
    assert 200 <= c.status_code < 300
    customer = c.json()[0]
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password, "customer_id": customer["id"], 'first_name': 'Random',
            'last_name': 'Name'}
    r = await client.post(
        f"{settings.ADMIN_API_V1_STR}/customers/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code >= 400


async def test_retrieve_users(
        client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    r = await client.get(
        f"{settings.ADMIN_API_V1_STR}/customers/", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    customer = r.json()[0]

    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, customer_id=customer["id"], first_name='random',
                         last_name='Name')
    await crud.user.create(db=async_get_db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2, customer_id=customer["id"], first_name='random',
                          last_name='Name')
    await crud.user.create(db=async_get_db, obj_in=user_in2)

    r = await client.get(f"{settings.ADMIN_API_V1_STR}/customers/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item


async def test_create_user_new_email(
        client: AsyncClient, async_get_db: AsyncSession,
        superuser_token_headers: dict,
) -> None:
    assert settings.TESTING is True
    r = await client.get(
        f"{settings.ADMIN_API_V1_STR}/customers/",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    customer = r.json()[0]
    mail = random_email()
    first_name = random_lower_string()
    last_name = random_lower_string()
    password = random_lower_string()
    data = {"email": mail, "password": password, "customer_id": customer["id"], 'first_name': first_name,
            'last_name': last_name}
    r = await client.post(
        f"{settings.ADMIN_API_V1_STR}/customers/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300

    created_user = r.json()
    user = await crud.user.get_by_email(db=async_get_db, email=mail)
    assert user
    assert user.email == created_user["email"]
