from app.tests.utils.customer_device import create_random_customer_device
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from app import sqlmodels, crud
from app.tests.utils.utils import random_lower_string
from app.tests.utils.device import create_random_device
from app.tests.utils.user import create_random_customer
from app.tests.utils.customer_office import create_random_customer_office

pytestmark = pytest.mark.asyncio


async def test_create_customer_device(async_get_db: AsyncSession) -> None:
    device = await create_random_device(db=async_get_db)
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    customer_name = random_lower_string()
    customer_device_in = sqlmodels.CustomerDevice(gateway_name=customer_name,
                                                  device_id=device.id,
                                                  label=customer_name,
                                                  customer_id=customer.id,
                                                  customer_office_id=customer_office.id)
    customer_device = await crud.customer_device.create(db=async_get_db, obj_in=customer_device_in)
    assert customer_device
    assert int(customer_device.id)
    assert customer_device.gateway_name == customer_name
    assert customer_device.label == customer_name
    assert customer_device.serial_number is None
    assert customer_device.network_ip is None
    assert customer_device.registration_code is None


async def test_get_customer_device_by_customer(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    await create_random_customer_device(db=async_get_db, customer_id=customer.id)

    customer_devices = await crud.customer_device.get_multi_by_customer(db=async_get_db, customer_id=customer.id)
    customer_offices = await crud.customer_office.get_by_customer_id(db=async_get_db, customer_id=customer.id)
    office_ids = [office.id for office in customer_offices]

    assert list(customer_devices)
    for customer_device in customer_devices:
        assert customer_device.customer_office_id in office_ids
