import enum
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, Column, String, JSON, Enum
from sqlalchemy.dialects import postgresql  # ARRAY contains requires dialect specific type
import datetime
import sqlmodel
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from .sensor_data import SensorData, SensorDataRead, SensorDataCreate
from .log_data import LogData, LogDataRead, LogDataCreate
from .setting_data import SettingData, SettingDataRead, SettingDataCreate
from .event_type import EventType


class EventTypeEnum(str, enum.Enum):
    settings_changes = "settings_changes"
    performed_task = "performed_task"


# Shared properties
class DeviceEventBase(SQLModel):
    # The gateway that sent the data
    # gateway
    # Interface
    # interface_id
    # The time when the event occurred
    time_recorded: datetime.datetime = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=True),
            nullable=False
        ))


# Properties to receive via API on creation
class DeviceEventCreate(DeviceEventBase):
    event_type: EventTypeEnum
    customer_device_id: int
    gateway_uuid: str
    sensor_data: Optional[list[SensorDataCreate]] = []
    log_data: Optional[list[LogDataCreate]] = []
    setting_data: Optional[list[SettingDataCreate]] = []


# Properties to receive via API on creation
class DeviceEventUpdate(DeviceEventBase):
    event_type: EventTypeEnum


class DeviceEventWithType(DeviceEventBase):
    id: int = Field(primary_key=True, index=True)
    event_type: Optional[EventType]


class DeviceEventWithData(DeviceEventWithType):
    sensor_data: Optional[list[SensorDataRead]] = []
    log_data: Optional[list[LogDataRead]] = []
    setting_data: Optional[list[SettingDataRead]] = []


class DeviceEvent(DeviceEventBase, table=True):
    id: int = Field(primary_key=True, index=True)
    # The device of a customer this Event was emitted by
    customer_device_id: int = Field(foreign_key="customerdevice.id")
    gateway_uuid: str = Field(foreign_key="gateway.uuid")
    sensor_data: Optional[list[SensorData]] = Relationship(back_populates="event")
    log_data: Optional[list[LogData]] = Relationship(back_populates="event")
    setting_data: Optional[list[SettingData]] = Relationship(back_populates="event")
    event_type_id: int = Field(foreign_key="eventtype.id")
    event_type: Optional[EventType] = Relationship()
