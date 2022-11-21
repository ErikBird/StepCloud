from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, sqlmodels
from app.core.config import settings


async def init_user(db: AsyncSession) -> None:
    customer = await crud.customer.get_by_name(db, name='AMIRA')
    if not customer:
        customer_in = sqlmodels.customer.CustomerCreate(
            name='AMIRA',
            contract_level=0,
        )
        customer = await crud.customer.create(db, obj_in=customer_in)
    user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = sqlmodels.user.UserCreate(
            first_name="Armin",
            last_name="Administrator",
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            customer_id=customer.id
        )
        await crud.user.create(db, obj_in=user_in)
    user = await crud.user.get_by_email(db, email=settings.EMAIL_TEST_USER)
    if not user:
        user_in = sqlmodels.user.UserCreate(
            first_name="Normal",
            last_name="User",
            email=settings.EMAIL_TEST_USER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=False,
            customer_id=customer.id
        )
        await crud.user.create(db=db, obj_in=user_in)
    customer_office = await crud.customer_office.get_by_customer_id(db, customer_id=customer.id)
    if len(customer_office) > 0:
        customer_office = customer_office[0]
    else:
        customer_office_in = sqlmodels.customer_office.CustomerOfficeCreate(
            customer_id=customer.id
        )
        customer_office = await crud.customer_office.create(db=db, obj_in=customer_office_in)
    gateway = await crud.gateway.get(db=db, uuid=settings.UUID_TEST_GATEWAY)
    if not gateway:
        gateway_in = sqlmodels.GatewayCreate(customer_id=customer.id, customer_office_id=customer_office.id,
                                             uuid=settings.UUID_TEST_GATEWAY)
        await crud.gateway.create(db=db, obj_in=gateway_in)
