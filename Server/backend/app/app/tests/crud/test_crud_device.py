from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from app import sqlmodels, crud
from app.tests.utils.utils import random_lower_string
from app.tests.utils.device import create_random_device_supplier, random_identifiers

pytestmark = pytest.mark.asyncio


async def test_create_device_supplier(async_get_db: AsyncSession) -> None:
    supplier_name = random_lower_string()
    supplier_in = sqlmodels.DeviceSupplierCreate(name=supplier_name)
    supplier = await crud.device_supplier.create(db=async_get_db, obj_in=supplier_in)
    assert supplier
    assert int(supplier.id)
    assert supplier.name == supplier_name


async def test_create_device(async_get_db: AsyncSession) -> None:
    supplier = await create_random_device_supplier(db=async_get_db)
    device_name = random_lower_string()
    identifiers = random_identifiers()
    device_in = sqlmodels.DeviceCreate(name=device_name,
                                       identifiers=identifiers,
                                       supplier_id=supplier.id)
    device = await crud.device.create_with_identifiers(db=async_get_db, obj_in=device_in)
    assert device
    assert int(device.id)
    assert device.name == device_name
    assert device.supplier_id == supplier.id
