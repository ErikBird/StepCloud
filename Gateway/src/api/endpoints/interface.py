from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src import sqlmodels
from src.api.deps import get_session
from src.constants.const import System
from src.constants.event_collection import StartInterfaceEvent
from src.event_bus.event_bus import EventBus
from src.interface_manager import InterfaceManager, get_interface_by_interface_name
from src.interfaces import device_interfaces
from src.interfaces.abstract_interface import EventDiscoverInterfaces

router = APIRouter()


@router.get("/manual/all", response_model=List[sqlmodels.ManualInterface])
async def all_manual_interfaces():
    interface_name = [{'interface_name': device_interface.__qualname__} for device_interface in
                      device_interfaces.__all__]
    return interface_name


@router.get("/discovery/all", response_model=List[sqlmodels.Interface])
async def discover_all_interfaces():
    bus = EventBus.instance()
    bus.emit(EventDiscoverInterfaces())
    # All matching interfaces should have implemented DeviceInterface
    available_interfaces = [{'gateway_id': interface.gateway_id,
                             'label': interface.label,
                             'interface_name': interface.interface_name,
                             'ip': interface.host_ip,
                             'supported_devices': interface.supported_devices}
                            for interface in bus.available_interfaces.values() if
                            interface.gateway_id not in bus.subscribers.keys()]
    return available_interfaces


@router.post("/introduce/{interface_name}/{network_ip}", response_model=sqlmodels.Interface)
async def configure_interface(interface_name: str, network_ip: str, session: Session = Depends(get_session)):
    interface_class = get_interface_by_interface_name(interface_name)
    if not interface_class:
        raise HTTPException(
            status_code=404, detail="The interface with this name can not be found!"
        )
    interface = interface_class.init_by_ip(network_ip)
    if not interface:
        raise HTTPException(
            status_code=400, detail="The interface could not be initialized by ip!"
        )
    bus = EventBus.instance()
    bus.introduce(interface=interface)
    return {'gateway_id': interface.gateway_id,
            'label': interface.label,
            'interface_name': interface.interface_name,
            'ip': interface.host_ip,
            'supported_devices': interface.supported_devices}


@router.post("/{gateway_id}/serve/{device_type}")
async def configure_interface(gateway_id: str, device_type: str, session: Session = Depends(get_session)):
    bus = EventBus.instance()
    # Transfer Interface from available to registered interfaces on event bus
    interface = bus.activate(gateway_id)
    # Make sure the interface existed in the first place
    if not interface:
        raise HTTPException(
            status_code=404, detail="The interface with this gateway_id is not available!"
        )
    # Configure the interface with the selected device_type
    interface.set_device_type(device_type)
    # Start the interface
    start_event = StartInterfaceEvent(gateway_id=interface.gateway_id)
    bus.emit(start_event)
    # Save the interface on the cloud and in the database
    if await InterfaceManager().save_device_interface(interface=interface, db=session):
        return True
    else:
        raise HTTPException(
            status_code=400, detail="Server is offline"
        )
