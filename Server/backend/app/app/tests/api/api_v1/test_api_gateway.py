import logging
import uuid
from typing import Dict
import pytest

from app.core import security

from app.tests.utils.customer_office import create_random_customer_office

from app.tests.utils.customer import create_random_customer
from httpx import AsyncClient
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, sqlmodels

pytestmark = pytest.mark.asyncio


async def test_create_gateway(
        client: AsyncClient, normal_user_token_headers: dict, async_get_db: AsyncSession
) -> None:
    u = await client.get(
        f"{settings.API_V1_STR}/customers/users/me", headers=normal_user_token_headers,
    )
    assert 200 <= u.status_code < 300
    user = u.json()
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=user['customer']['id'])
    uuid_generated_on_the_gateway = str(uuid.uuid4())
    serial_number = random_lower_string()
    data = {"uuid": uuid_generated_on_the_gateway, "customer_office_id": customer_office.id,
            "serial_number": serial_number}
    r = await client.post(
        f"{settings.API_V1_STR}/gateway/create",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= u.status_code < 300
    created_gateway = r.json()
    assert 'access_token' in created_gateway.keys()
    assert 'refresh_token' in created_gateway.keys()

    payload = security.decode_token(created_gateway['access_token'])
    access_token_uuid = payload['sub']
    gateway = await crud.gateway.get(db=async_get_db, uuid=access_token_uuid)
    assert gateway


async def test_get_gateway_tokens(
        client: AsyncClient, normal_user_token_headers: dict, async_get_db: AsyncSession
) -> None:
    u = await client.get(
        f"{settings.API_V1_STR}/customers/users/me", headers=normal_user_token_headers,
    )
    assert 200 <= u.status_code < 300
    user = u.json()
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=user['customer']['id'])
    uuid_generated_on_the_gateway = str(uuid.uuid4())
    gateway_in = sqlmodels.GatewayCreate(customer_office_id=customer_office.id,
                                         uuid=uuid_generated_on_the_gateway)
    gateway = await crud.gateway.create(db=async_get_db, obj_in=gateway_in)
    r = await client.get(
        f"{settings.API_V1_STR}/gateway/{uuid_generated_on_the_gateway}/get-token",
        headers=normal_user_token_headers,
    )
    assert 200 <= u.status_code < 300
    created_gateway = r.json()
    assert 'access_token' in created_gateway.keys()
    assert 'refresh_token' in created_gateway.keys()

    payload = security.decode_token(created_gateway['access_token'])
    access_token_uuid = payload['sub']
    gateway = await crud.gateway.get(db=async_get_db, uuid=access_token_uuid)
    assert gateway


async def test_get_my_gateways(
        client: AsyncClient, normal_user_token_headers: dict, async_get_db: AsyncSession
) -> None:
    u = await client.get(
        f"{settings.API_V1_STR}/customers/users/me", headers=normal_user_token_headers,
    )
    assert 200 <= u.status_code < 300
    user = u.json()
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=user['customer']['id'])
    uuid_generated_on_the_gateway = str(uuid.uuid4())
    gateway_in = sqlmodels.GatewayCreate(customer_office_id=customer_office.id,
                                         uuid=uuid_generated_on_the_gateway)
    gateway = await crud.gateway.create(db=async_get_db, obj_in=gateway_in)
    r = await client.get(
        f"{settings.API_V1_STR}/gateway/me",
        headers=normal_user_token_headers,
    )
    my_gateways = r.json()
    assert 200 <= u.status_code < 300
    assert len(my_gateways) > 0
