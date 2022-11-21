from sqlmodel.ext.asyncio.session import AsyncSession
from .init_data.default_entries import init_default_entries
from .init_data.devices import init_devices
from .init_data.user_accounts import init_user


async def init_db(db: AsyncSession) -> None:
    await init_default_entries(db)
    await init_devices(db)
    await init_user(db)
