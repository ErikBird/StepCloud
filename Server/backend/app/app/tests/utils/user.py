from typing import Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from httpx import AsyncClient
import logging
from app import crud
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string
from app import sqlmodels
from app.tests.utils.customer import create_random_customer


async def user_authentication_headers(
        *, client: AsyncClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_random_user(db: AsyncSession, customer_id: int = None) -> sqlmodels.User:
    email = random_email()
    password = random_lower_string()
    if not customer_id:
        customer = await create_random_customer(db=db)
        customer_id = customer.id
    user_in = sqlmodels.UserCreate(username=email, email=email, password=password, customer_id=customer_id)
    user = await crud.user.create(db=db, obj_in=user_in)
    return user


async def authentication_token_from_email(
        *, client: AsyncClient, email: str, db: AsyncSession
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user: sqlmodels.User = await crud.user.get_by_email(db=db, email=email)
    customer: sqlmodels.Customer = await crud.customer.get_by_name(db=db, name='Test')
    if not customer:
        customer_in = sqlmodels.CustomerCreate(
            name='Test'
        )
        customer: sqlmodels.Customer = await crud.customer.create(db=db, obj_in=customer_in)
        logging.error(customer)
    if not user:
        user_in_create = sqlmodels.UserCreate(email=email,
                                              password=password,
                                              full_name='Test User',
                                              customer_id=customer.id)

        user: sqlmodels.User = await crud.user.create(db=db, obj_in=user_in_create)
    else:
        # Look at: README.md
        user_in_update = {'password': password}
        user: sqlmodels.User = await crud.user.update(db=db, db_obj=user, obj_in=user_in_update)

    return await user_authentication_headers(client=client, email=email, password=password)
