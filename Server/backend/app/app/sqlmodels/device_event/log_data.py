import enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Column, String, JSON, Enum
from sqlalchemy.dialects import postgresql  # ARRAY contains requires dialect specific type
import datetime
from typing import TYPE_CHECKING
from .log_type import LogType

if TYPE_CHECKING:
    from .device_event import DeviceEvent


class LogTypeEnum(str, enum.Enum):
    error = "error"
    debug = "debug"
    build = "build"


# Shared properties
class LogDataBase(SQLModel):
    # Label which describe the Content of the Event to the user
    label: str = Field(index=True)
    # Payload -> all Settings Data converted into a JSON compatible format
    data: dict = Field(sa_column=Column(JSON))


# Properties to receive via API on creation
class LogDataCreate(LogDataBase):
    log_type: LogTypeEnum
    event_id: Optional[int]


class LogDataUpdate(LogDataBase):
    log_type: LogTypeEnum


class LogDataRead(LogDataBase):
    log_type: Optional[LogType]


class LogData(LogDataBase, table=True):
    id: int = Field(primary_key=True, index=True)
    # Some ID that identifies the Event at the source
    event_id: int = Field(foreign_key="deviceevent.id")
    event: Optional["DeviceEvent"] = Relationship(back_populates="log_data")
    # The type of Log this Event contains
    log_type_id: int = Field(foreign_key="logtype.id")
    log_type: Optional[LogType] = Relationship()
