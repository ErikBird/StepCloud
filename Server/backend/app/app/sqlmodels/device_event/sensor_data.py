import enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Column, String, JSON, Enum
from sqlalchemy.dialects import postgresql  # ARRAY contains requires dialect specific type
import datetime
from typing import TYPE_CHECKING
from .visualization_type import VisualizationType
from .sensor_type import SensorType

if TYPE_CHECKING:
    from .device_event import DeviceEvent


class SensorTypeEnum(str, enum.Enum):
    timeseries = "timeseries"
    singular = "singular"


class VisualizationTypeEnum(str, enum.Enum):
    default = "default"
    scatter = "scatter"
    line = "line"
    bar = "bar"


# Shared properties
class SensorDataBase(SQLModel):
    # Label which describe the Content of the Event to the user
    label: str = Field(index=True)
    # Payload -> all Settings Data converted into a JSON compatible format
    data: dict = Field(sa_column=Column(JSON))
    # The unit of measurement of the content
    unit: Optional[str]


# Properties to receive via API on creation
class SensorDataCreate(SensorDataBase):
    sensor_type: SensorTypeEnum
    visualization_type: VisualizationTypeEnum
    event_id: Optional[int]


class SensorDataUpdate(SensorDataBase):
    sensor_type: SensorTypeEnum
    visualization_type: VisualizationTypeEnum


class SensorDataRead(SensorDataBase):
    id: int  # To iterate over the entries in the frontend
    label: str = Field(index=True)
    # Payload -> all Settings Data converted into a JSON compatible format
    data: dict = Field(sa_column=Column(JSON))
    # Some ID that identifies the Event at the source
    event_id: int = Field(foreign_key="DeviceEvent.id")
    # The unit of measurement of the content
    unit: Optional[str]
    sensor_type: Optional[SensorType]
    visualization_type: Optional[VisualizationType]


class SensorData(SensorDataBase, table=True):
    id: int = Field(primary_key=True, index=True)
    # Some ID that identifies the Event at the source
    event_id: int = Field(foreign_key="deviceevent.id")
    event: Optional["DeviceEvent"] = Relationship(back_populates="sensor_data")
    # The type of Log this Event contains
    sensor_type_id: int = Field(foreign_key="sensortype.id")
    sensor_type: Optional[SensorType] = Relationship()
    # The preferred type of visualization for this data in the frontend
    visualization_type_id: int = Field(foreign_key="visualizationtype.id")
    visualization_type: Optional[VisualizationType] = Relationship()
