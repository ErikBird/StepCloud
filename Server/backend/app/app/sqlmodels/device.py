from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint
from typing import TYPE_CHECKING


# Shared properties
class DeviceBase(SQLModel):
    name: str = Field(index=True)
    image_path: str = 'default.png'
    supplier_id: int = Field(foreign_key="devicesupplier.id")


# Properties to receive via API on creation
class DeviceCreate(DeviceBase):
    # Overrides Base Class Identifier since Relatioinshio does not work yet with async sqlmodel
    identifiers: Optional[List[str]]


# Properties to receive via API on creation
class DeviceUpdate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: int


class Device(DeviceBase, table=True):
    id: int = Field(primary_key=True, index=True)
    supplier: Optional["DeviceSupplier"] = Relationship(back_populates="devices")
    identifiers: Optional[List["Identifier"]] = Relationship(back_populates="device")


from .identifier import IdentifierRead
from .device_supplier import DeviceSupplierRead


class DeviceReadWithSupplier(DeviceRead):
    supplier: Optional[DeviceSupplierRead] = None


class DeviceReadWithRelationships(DeviceRead):
    supplier: Optional[DeviceSupplierRead] = None
    identifiers: Optional[List[IdentifierRead]] = []
