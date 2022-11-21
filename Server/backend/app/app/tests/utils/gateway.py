import uuid

from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app import sqlmodels
from .customer_office import create_random_customer_office
from .user import create_random_customer


async def create_random_gateway(db: AsyncSession, customer_id: int = None,
                                customer_office_id: int = None) -> sqlmodels.Gateway:
    if not customer_id:
        customer = await create_random_customer(db=db)
        customer_id = customer.id
    if not customer_office_id:
        customer_office = await create_random_customer_office(db=db, customer_id=customer_id)
        customer_office_id = customer_office.id
    uuid_generated_on_the_gateway = str(uuid.uuid4())
    gateway_in = sqlmodels.GatewayCreate(customer_office_id=customer_office_id, uuid=uuid_generated_on_the_gateway)
    gateway = await crud.gateway.create(db=db, obj_in=gateway_in)
    return gateway
