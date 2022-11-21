from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device


# Shared properties
class DeviceSupplierBase(SQLModel):
    name: str = Field(index=True)


# Properties to receive via API on creation
class DeviceSupplierCreate(DeviceSupplierBase):
    pass


# Properties to receive via API on creation
class DeviceSupplierUpdate(DeviceSupplierBase):
    pass


class DeviceSupplierRead(DeviceSupplierBase):
    pass


class DeviceSupplier(DeviceSupplierBase, table=True):
    id: int = Field(primary_key=True, index=True)
    devices: Optional[List["Device"]] = Relationship(back_populates="supplier")
