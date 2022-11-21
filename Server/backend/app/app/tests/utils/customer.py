from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.tests.utils.utils import random_lower_string
from app import sqlmodels


async def create_random_customer(db: AsyncSession) -> sqlmodels.Customer:
    customer_name = random_lower_string()
    customer_in = sqlmodels.CustomerCreate(name=customer_name, contract_level=1)
    customer = await crud.customer.create(db=db, obj_in=customer_in)
    return customer
