import logging
from typing import Dict
import pytest
from app.tests.utils.customer_office import create_random_customer_office

from app.tests.utils.customer import create_random_customer
from httpx import AsyncClient
from app import crud
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


async def test_update_customer_office_not_owner(
        client: AsyncClient, normal_user_token_headers: dict, async_get_db: AsyncSession
) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    name = random_lower_string()
    data = {"id": customer_office.id, "customer_id": customer.id, "name": name}
    r = await client.put(
        f"{settings.API_V1_STR}/customer-office/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 400 <= r.status_code < 500


async def test_update_customer_office(
        client: AsyncClient, normal_user_token_headers: dict, async_get_db: AsyncSession
) -> None:
    u = await client.get(
        f"{settings.API_V1_STR}/customers/users/me", headers=normal_user_token_headers,
    )
    assert 200 <= u.status_code < 300
    user = u.json()
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=user['customer']['id'])
    name = random_lower_string()
    data = {"id": customer_office.id, "customer_id": user['customer']['id'], "name": name}
    r = await client.put(
        f"{settings.API_V1_STR}/customer-office/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    assert int(r.json()['id'])
