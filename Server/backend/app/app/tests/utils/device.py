from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.tests.utils.utils import random_lower_string
from app import sqlmodels
import random
from string import ascii_lowercase, digits


def random_identifiers():
    chars = ascii_lowercase + digits
    return list(set([''.join(random.choice(chars) for _ in range(5)) for _ in range(random.randint(1, 10))]))


async def create_random_device_supplier(db: AsyncSession) -> sqlmodels.DeviceSupplier:
    supplier_name = random_lower_string()
    supplier_in = sqlmodels.DeviceSupplierCreate(name=supplier_name)
    supplier = await crud.device_supplier.create(db=db, obj_in=supplier_in)
    return supplier


async def create_random_device(db: AsyncSession) -> sqlmodels.Device:
    supplier = await create_random_device_supplier(db=db)
    device_name = random_lower_string()
    identifiers = random_identifiers()
    device_in = sqlmodels.DeviceCreate(name=device_name,
                                       identifiers=identifiers,
                                       supplier_id=supplier.id)
    device = await crud.device.create_with_identifiers(db=db, obj_in=device_in)
    return device
