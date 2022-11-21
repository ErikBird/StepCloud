from app.tests.utils.user import create_random_customer
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from datetime import datetime
from app.tests.utils.customer_device import create_random_customer_device
from app import sqlmodels
from app.tests.utils.customer_office import create_random_customer_office
from app.tests.utils.gateway import create_random_gateway


async def create_random_device_event(db: AsyncSession) -> sqlmodels.CustomerDevice:
    customer = await create_random_customer(db=db)
    customer_office = await create_random_customer_office(db=db, customer_id=customer.id)
    customer_device = await create_random_customer_device(db=db, customer_office_id=customer_office.id)
    gateway = await create_random_gateway(db=db, customer_office_id=customer_office.id)
    device_event_in = sqlmodels.DeviceEvent(
        event_type=sqlmodels.EventTypeEnum.performed_task,
        gateway_uuid=gateway.uuid, time_recorded=datetime.utcnow(),
        customer_device_id=customer_device.id)
    device_event = await crud.device_event.create(db=db, obj_in=device_event_in)
    return device_event
