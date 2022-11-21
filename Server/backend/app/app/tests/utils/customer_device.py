from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.tests.utils.utils import random_lower_string
from app.tests.utils.device import create_random_device
from app.tests.utils.user import create_random_customer
from app.tests.utils.customer_office import create_random_customer_office
from app import sqlmodels
from tests.utils.gateway import create_random_gateway


async def create_random_customer_device(db: AsyncSession, customer_id: int = None,
                                        customer_office_id: int = None, gateway_id=None) -> sqlmodels.CustomerDevice:
    device = await create_random_device(db=db)
    if not customer_id:
        customer = await create_random_customer(db=db)
        customer_id = customer.id
    if not customer_office_id:
        customer_office = await create_random_customer_office(db=db, customer_id=customer_id)
        customer_office_id = customer_office.id
    if not gateway_id:
        gateway = await create_random_gateway(db=db, customer_office_id=customer_office_id)
        gateway_id = gateway.uuid
    customer_device_name = random_lower_string()
    customer_device_in = sqlmodels.CustomerDevice(gateway_id=gateway_id,
                                                  device_id=device.id,
                                                  label=customer_device_name,
                                                  customer_office_id=customer_office_id,
                                                  interface_name='interface_name')
    customer_device = await crud.customer_device.create(db=db, obj_in=customer_device_in)
    return customer_device
