from app.tests.utils.user import create_random_customer
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app import sqlmodels


async def create_random_customer_office(db: AsyncSession, customer_id: int = None) -> sqlmodels.CustomerOffice:
    if not customer_id:
        customer = await create_random_customer(db=db)
        customer_id = customer.id
    customer_office_in = sqlmodels.CustomerOfficeCreate(customer_id=customer_id)
    customer_office = await crud.customer_office.create(db=db, obj_in=customer_office_in)
    return customer_office
