from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base import CRUDBase
from app.sqlmodels.device_event.setting_data import SettingData, SettingDataCreate, SettingDataUpdate
from sqlmodel import select


class CRUDSettingsData(CRUDBase[SettingData, SettingDataCreate, SettingDataUpdate]):
    async def get_by_event_id(self, db: AsyncSession, *, device_event_id: int):
        statement = select(self.model).where(SettingData.event_id == device_event_id)
        query = await db.exec(statement)
        return query.all()


settings_data = CRUDSettingsData(SettingData)
