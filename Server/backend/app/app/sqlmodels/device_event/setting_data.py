from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, Column, String, JSON, Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlmodels.device_event import DeviceEvent


# Shared properties
class SettingDataBase(SQLModel):
    # Label which describe the Content of the Event to the user
    label: str = Field(index=True)
    # Payload -> all Settings Data converted into a JSON compatible format
    data: dict = Field(sa_column=Column(JSON))


# Properties to receive via API on creation
class SettingDataCreate(SettingDataBase):
    event_id: Optional[int]


class SettingDataRead(SettingDataBase):
    pass


class SettingDataUpdate(SettingDataBase):
    pass


class SettingData(SettingDataBase, table=True):
    id: int = Field(primary_key=True, index=True)
    # Some ID that identifies the Event at the source
    event_id: int = Field(foreign_key="deviceevent.id")
    event: Optional["DeviceEvent"] = Relationship(back_populates="setting_data")
