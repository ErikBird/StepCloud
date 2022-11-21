from app.tests.utils.user import create_random_customer
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from httpx import AsyncClient
from app.core.security import verify_password
from app import crud, sqlmodels
from app.tests.utils.utils import random_email, random_lower_string
import logging

pytestmark = pytest.mark.asyncio


async def test_create_customer(async_get_db: AsyncSession) -> None:
    customer_name = random_lower_string()
    customer_in = sqlmodels.CustomerCreate(name=customer_name, contract_level=1)
    customer = await crud.customer.create(db=async_get_db, obj_in=customer_in)
    assert customer
    assert customer.name == customer_name
    assert int(customer.id)


async def test_get_customer_by_name(async_get_db: AsyncSession) -> None:
    customer_name = random_lower_string()
    customer_in = sqlmodels.CustomerCreate(name=customer_name, contract_level=1)
    customer = await crud.customer.create(db=async_get_db, obj_in=customer_in)
    assert customer

    customer2 = await crud.customer.get_by_name(db=async_get_db, name=customer_name)
    assert customer2
    assert customer2.name == customer_name
    assert customer2.id == customer.id


async def test_create_customer_default_contract_level(async_get_db: AsyncSession) -> None:
    customer_name = random_lower_string()
    customer_in = sqlmodels.CustomerCreate(name=customer_name)
    customer = await crud.customer.create(db=async_get_db, obj_in=customer_in)
    assert customer
    assert customer.contract_level == 1
