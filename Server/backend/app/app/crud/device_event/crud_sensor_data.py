from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base import CRUDBase
from app import sqlmodels, crud
from sqlmodel import select


class CRUDSensorData(CRUDBase[sqlmodels.SensorData, sqlmodels.SensorDataCreate, sqlmodels.SensorDataUpdate]):
    async def get_by_event_id(self, db: AsyncSession, *, device_event_id: int) -> sqlmodels.SensorData:
        statement = select(self.model).where(sqlmodels.SensorData.event_id == device_event_id)
        query = await db.exec(statement)
        return query.all()

    async def create(self, db: AsyncSession, *, obj_in: sqlmodels.SensorDataCreate) -> sqlmodels.SensorData:
        sensor_type = await crud.sensor_type.get_by_label(db=db, label=obj_in.sensor_type)
        visualization_type = await crud.visualization_type.get_by_label(db=db, label=obj_in.visualization_type)
        db_obj = sqlmodels.SensorData(label=obj_in.label,
                                      data=obj_in.data,
                                      event_id=obj_in.event_id,
                                      visualization_type_id=visualization_type.id,
                                      sensor_type_id=sensor_type.id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


sensor_data = CRUDSensorData(sqlmodels.SensorData)
