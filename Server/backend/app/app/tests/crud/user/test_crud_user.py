from app.tests.utils.user import create_random_customer
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from httpx import AsyncClient
from app import crud
from app.core.security import verify_password
from app.sqlmodels.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
import logging

pytestmark = pytest.mark.asyncio


async def test_create_user(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=email, password=password, customer_id=customer.id, full_name='Random Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


async def test_authenticate_user(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=email, password=password, customer_id=customer.id, full_name='Random Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    authenticated_user = await crud.user.authenticate(db=async_get_db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


async def test_not_authenticate_user(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user = await crud.user.authenticate(db=async_get_db, email=email, password=password)
    assert user is None


async def test_check_if_user_is_active(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=email, password=password, customer_id=customer.id, full_name='Random Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    is_active = await crud.user.is_active(user)
    assert is_active is True


async def test_check_if_user_is_active_inactive(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=email, password=password, disabled=True, customer_id=customer.id,
                         full_name='Random Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    is_active = await crud.user.is_active(user)
    assert is_active


async def test_check_if_user_is_superuser(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=email, password=password, is_superuser=True, customer_id=customer.id,
                         full_name='Random Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    is_superuser = await crud.user.is_superuser(user)
    assert is_superuser is True


async def test_check_if_user_is_superuser_normal_user(async_get_db: AsyncSession) -> None:
    username = random_email()
    password = random_lower_string()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=username, password=password, customer_id=customer.id, full_name='Random Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    is_superuser = await crud.user.is_superuser(user)
    assert is_superuser is False


async def test_get_user(async_get_db: AsyncSession) -> None:
    password = random_lower_string()
    username = random_email()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=username, password=password, is_superuser=True, customer_id=customer.id,
                         full_name='Random Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    user_2 = await crud.user.get(db=async_get_db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


async def test_update_user(async_get_db: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=email, password=password, is_superuser=True, customer_id=customer.id,
                         first_name='Random', last_name='Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    assert user.email is not None
    new_password = random_lower_string()
    # Look at: README.md
    user_in_update = {'password': new_password, 'is_superuser': True}
    await crud.user.update(db=async_get_db, db_obj=user, obj_in=user_in_update)
    user_2 = await crud.user.get(db=async_get_db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)


async def test_update_user_full_name_only(async_get_db: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    customer = await create_random_customer(db=async_get_db)
    user_in = UserCreate(email=email, password=password, is_superuser=True, customer_id=customer.id,
                         first_name='Random', last_name='Name')
    user = await crud.user.create(db=async_get_db, obj_in=user_in)
    assert user.first_name == 'Random'
    assert user.last_name == 'Name'
    new_first_name = "Test"
    new_last_name = "User"
    # Look at: README.md
    user_in_update = {'first_name': new_first_name, 'last_name': new_last_name, 'is_superuser': True}
    await crud.user.update(db=async_get_db, db_obj=user, obj_in=user_in_update)
    user_2 = await crud.user.get(db=async_get_db, id=user.id)
    assert user_2
    assert user_2.first_name == new_first_name
    assert user_2.last_name == new_last_name
