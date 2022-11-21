from app.tests.utils.customer_office import create_random_customer_office

from app.tests.utils.user import create_random_customer, create_random_user
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from httpx import AsyncClient
from app.core.security import verify_password
from app import crud, sqlmodels
from app.tests.utils.utils import random_email, random_lower_string
import uuid

pytestmark = pytest.mark.asyncio


async def test_create_gateway(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    uuid_generated_on_the_gateway = str(uuid.uuid4())
    gateway_in = sqlmodels.GatewayCreate(customer_office_id=customer_office.id,
                                         uuid=uuid_generated_on_the_gateway)
    gateway = await crud.gateway.create(db=async_get_db, obj_in=gateway_in)
    assert gateway
    assert gateway.customer_office_id == customer_office.id
    assert gateway.office.id == customer_office.id


async def test_get_gateway_by_uuid(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    uuid_generated_on_the_gateway = str(uuid.uuid4())
    gateway_in = sqlmodels.GatewayCreate(customer_id=customer.id, customer_office_id=customer_office.id,
                                         uuid=uuid_generated_on_the_gateway)
    gateway_create = await crud.gateway.create(db=async_get_db, obj_in=gateway_in)
    gateway = await crud.gateway.get(db=async_get_db, uuid=uuid_generated_on_the_gateway)
    assert gateway
    assert gateway.customer_office_id == customer_office.id
    assert gateway.office.id == customer_office.id
