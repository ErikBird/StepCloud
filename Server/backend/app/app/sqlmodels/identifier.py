from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint
from typing import TYPE_CHECKING


class IdentifierBase(SQLModel):
    expression: str = Field(primary_key=True, index=True)


class IdentifierCreate(IdentifierBase):
    device_id: int = Field(foreign_key="device.id")


class IdentifierUpdate(IdentifierBase):
    device_id: int = Field(foreign_key="device.id")


class IdentifierRead(IdentifierBase):
    pass


from .device import Device, DeviceRead


class Identifier(IdentifierBase, table=True):
    device_id: int = Field(foreign_key="device.id")
    device: Device = Relationship(back_populates="identifiers",
                                  sa_relationship_kwargs={
                                      "lazy": "selectin"})


class IdentifierReadWithDevices(IdentifierRead):
    device: DeviceRead = None
