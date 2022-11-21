from typing import Optional

from sqlmodel import SQLModel, Field


class CustomerDevice(SQLModel, table=True):
    gateway_id: str = Field(primary_key=True)
    cloud_id: Optional[str]
    network_ip: Optional[str]
    registration_code: Optional[str]
    serial_number: Optional[str]
    cloud_id: Optional[str]
    device_type: str
    interface_name: str
    label: Optional[str]
