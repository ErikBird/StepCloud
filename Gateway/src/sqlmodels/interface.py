from typing import List, Optional
from sqlmodel import SQLModel


class Interface(SQLModel):
    gateway_id: str
    label: str
    interface_name: str
    ip: str
    supported_devices: List[str]


class ManualInterface(SQLModel):
    interface_name: str
