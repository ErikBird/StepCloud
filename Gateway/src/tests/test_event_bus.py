import pytest

from src.constants.lifecycle_events import EventBeforeLoad
from src.event_bus.event_bus import EventBus
from src.interface_manager import InterfaceManager
from src.interfaces.device_interfaces.energy_meter.netio_powercable import NetioPowerCableInterface

pytestmark = pytest.mark.asyncio


async def test_activate_interface():
    bus = EventBus.instance()
    InterfaceManager().register()
    bus.emit(event=EventBeforeLoad())
    interface_name = 'interface_name'
    netio_interface = NetioPowerCableInterface(name='sadasd',  # unique id
                                               label='interface_name',  # ui name
                                               host_ip='0.0.0.0')

    bus.introduce(interface=netio_interface, interface_name=interface_name)
    interface = bus.activate(interface_name)
    assert interface is not None
