from app.tests.utils.customer_office import create_random_customer_office

from app.tests.utils.user import create_random_customer, create_random_user
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from httpx import AsyncClient
from app.core.security import verify_password
from app import crud, sqlmodels
from app.tests.utils.utils import random_email, random_lower_string
import logging

pytestmark = pytest.mark.asyncio


async def test_create_customer_office(async_get_db: AsyncSession) -> None:
    name = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    customer_office_in = sqlmodels.CustomerOfficeCreate(customer_id=customer.id, name=name)
    customer_office = await crud.customer_office.create(db=async_get_db, obj_in=customer_office_in)
    assert customer_office.name == name
    assert int(customer_office.id)


async def test_create_customer_office_missing_customer_id(async_get_db: AsyncSession) -> None:
    name = random_lower_string()
    with pytest.raises(Exception):
        customer_office_in = sqlmodels.CustomerOfficeCreate(name=name)


async def test_update_customer_office(async_get_db: AsyncSession) -> None:
    name = 'Random'
    customer = await create_random_customer(db=async_get_db)
    customer_office_in = sqlmodels.CustomerOfficeCreate(customer_id=customer.id, name=name)
    customer_office = await crud.customer_office.create(db=async_get_db, obj_in=customer_office_in)
    assert customer_office.name == name
    assert int(customer_office.id)

    name2 = 'Random2'
    # Look at: README.md
    customer_office_update = {'id': customer_office.id, 'name': name2}
    customer_office2 = await crud.customer_office.update(db=async_get_db, db_obj=customer_office,
                                                         obj_in=customer_office_update)
    assert customer_office2.name == name2
    assert int(customer_office2.id)


async def test_get_customer_office(async_get_db: AsyncSession) -> None:
    name = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    customer_office_in = sqlmodels.CustomerOfficeCreate(customer_id=customer.id, name=name)
    customer_office = await crud.customer_office.create(db=async_get_db, obj_in=customer_office_in)
    assert customer_office.name == name
    assert int(customer_office.id)

    customer_office_2 = await crud.customer_office.get(db=async_get_db, id=customer_office.id)
    assert customer_office_2
    assert customer_office_2.name == name
    assert customer_office_2.id == customer_office.id


async def test_get_customer_office(async_get_db: AsyncSession) -> None:
    name = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    customer_office_in = sqlmodels.CustomerOfficeCreate(customer_id=customer.id, name=name)
    customer_office = await crud.customer_office.create(db=async_get_db, obj_in=customer_office_in)
    assert customer_office.name == name
    assert int(customer_office.id)

    customer_office_2 = await crud.customer_office.get(db=async_get_db, id=customer_office.id)
    assert customer_office_2
    assert customer_office_2.name == name
    assert customer_office_2.id == customer_office.id


async def test_get_customer_office_in_user(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    user = await create_random_user(db=async_get_db, customer_id=customer.id)
    user_query = await crud.user.get(id=user.id, db=async_get_db)

    assert customer_office in user_query.customer.offices
