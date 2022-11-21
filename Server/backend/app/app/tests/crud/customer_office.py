from app.tests.utils.customer_device import create_random_customer_device
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from app import sqlmodels, crud
from app.tests.utils.utils import random_lower_string
from app.tests.utils.device import create_random_device
from app.tests.utils.user import create_random_customer
from app.tests.utils.customer_office import create_random_customer_office

pytestmark = pytest.mark.asyncio


async def test_get_customer_office_by_customer(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    customer_offices = await crud.customer_office.get_by_customer_id(db=async_get_db, customer_id=customer.id)
    for office in customer_offices:
        assert office.customer_id == customer.id
