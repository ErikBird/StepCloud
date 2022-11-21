from typing import List
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.crud.base import CRUDBase
from sqlalchemy.orm import selectinload
from app import sqlmodels, crud
from sqlmodel import select


class CRUDDeviceEvent(CRUDBase[sqlmodels.DeviceEvent, sqlmodels.DeviceEventCreate, sqlmodels.DeviceEventUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: sqlmodels.DeviceEventCreate) -> sqlmodels.DeviceEvent:
        event_type = await crud.event_type.get_by_label(db=db, label=obj_in.event_type)
        db_event_obj = sqlmodels.DeviceEvent(
            time_recorded=obj_in.time_recorded,
            customer_device_id=obj_in.customer_device_id,
            gateway_uuid=obj_in.gateway_uuid,
            event_type_id=event_type.id
        )
        event_in_data = jsonable_encoder(obj_in)
        db.add(db_event_obj)
        await db.commit()
        await db.refresh(db_event_obj)

        if "sensor_data" in event_in_data:
            for data_obj_in in event_in_data["sensor_data"]:
                obj_in_sensor_data = sqlmodels.SensorDataCreate(label=data_obj_in['label'],
                                                                data=data_obj_in["data"],
                                                                sensor_type=data_obj_in["sensor_type"],
                                                                visualization_type=data_obj_in["visualization_type"],
                                                                event_id=db_event_obj.id)
                await crud.sensor_data.create(db=db, obj_in=obj_in_sensor_data)

        if "log_data" in event_in_data:
            for data_obj_in in event_in_data["log_data"]:
                obj_in_log_data = sqlmodels.LogDataCreate(label=data_obj_in['label'],
                                                          data=data_obj_in["data"],
                                                          log_type=data_obj_in["log_type"],
                                                          event_id=db_event_obj.id)
                await crud.log_data.create(db=db, obj_in=obj_in_log_data)
        if "setting_data" in event_in_data:
            for data_obj_in in event_in_data["setting_data"]:
                obj_in_settings_data = sqlmodels.SettingDataCreate(label=data_obj_in['label'],
                                                                   data=data_obj_in["data"],
                                                                   event_id=db_event_obj.id)
                await crud.settings_data.create(db=db, obj_in=obj_in_settings_data)
        return db_event_obj

    async def get_multi_by_id(
            self, db: AsyncSession, *, customer_device_id: int, skip: int = 0, limit: int = 100
    ) -> List[sqlmodels.DeviceEventWithData]:
        statement = select(self.model).filter(sqlmodels.DeviceEvent.customer_device_id == customer_device_id).offset(
            skip).limit(limit).options(selectinload('*'))
        query = await db.exec(statement)
        return query.all()

    async def get_by_id(
            self, db: AsyncSession, *, customer_device_id: int, event_id: int
    ) -> sqlmodels.DeviceEventWithData:
        statement = select(self.model).filter(sqlmodels.DeviceEvent.customer_device_id == customer_device_id) \
            .where(sqlmodels.DeviceEvent.id == event_id).options(selectinload('*'))
        query = await db.exec(statement)
        return query.first()

    async def get_last(
            self, db: AsyncSession, *, customer_device_id: int) -> sqlmodels.DeviceEvent:
        statement = select(self.model).filter(sqlmodels.DeviceEvent.customer_device_id == customer_device_id) \
            .order_by(sqlmodels.DeviceEvent.time_recorded.desc()).options(selectinload('*'))
        query = await db.exec(statement)
        return query.first()


device_event = CRUDDeviceEvent(sqlmodels.DeviceEvent)
