import enum

from pydantic import validator
from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional


class SensorTypeEnum(str, enum.Enum):
    timeseries = "timeseries"
    singular = "singular"


class VisualizationTypeEnum(str, enum.Enum):
    default = "default"
    scatter = "scatter"
    line = "line"
    bar = "bar"


# Shared properties
class SensorData(SQLModel):
    # Label which describe the Content of the Event to the user
    label: str = Field(index=True)
    # Payload -> all Settings Data converted into a JSON compatible format
    data: dict = Field(default={}, sa_column=Column(JSON))
    # The unit of measurement of the content
    unit: Optional[str]
    sensor_type: SensorTypeEnum
    visualization_type: VisualizationTypeEnum

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True
