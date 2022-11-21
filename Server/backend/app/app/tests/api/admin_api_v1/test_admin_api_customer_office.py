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


async def test_create_customer_office(
        client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    customer = await create_random_customer(db=async_get_db)
    name = random_lower_string()
    data = {"customer_id": customer.id, "name": name}
    r = await client.post(
        f"{settings.ADMIN_API_V1_STR}/customer-office/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    assert int(r.json()['id'])


async def test_get_customer_offices(
        client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)

    r = await client.get(
        f"{settings.ADMIN_API_V1_STR}/customer-office/", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    assert len(r.json()) > 0
