from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base import CRUDBase
from app.sqlmodels.device_event.sensor_type import SensorType, SensorTypeCreate, SensorTypeUpdate


class CRUDSensorType(CRUDBase[SensorType, SensorTypeCreate, SensorTypeUpdate]):
    async def get_by_label(self, db: AsyncSession, *, label: str) -> Optional[SensorType]:
        statement = select(SensorType).filter(SensorType.label == label)
        query = await db.exec(statement)
        return query.one_or_none()


sensor_type = CRUDSensorType(SensorType)
