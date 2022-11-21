import time

from sqlmodel import Session

from src import crud
from src.constants.const import ProcessMode, RequestedType
from src.constants.lifecycle_events import EventBeforeLoad
from src.db.session import engine
from src.event_bus.decorator import subscribe
from src.event_bus.event_bus import EventBus
from src.interfaces.abstract_interface import SystemInterface, DeviceInterface
from src.interfaces import core_interfaces, discovery_interfaces, device_interfaces
from src.interfaces.core_interfaces.cloud_adapter import CloudAdapter


def get_interface_by_interface_name(interface_name):
    for device_interface in device_interfaces.__all__:
        # During the creation, the interface_name origin is from type(self).__name__
        # But it appears to be the same as __qualname__ without initialization
        if interface_name == device_interface.__qualname__:
            return device_interface
    return None


class InterfaceManager(SystemInterface):
    def __init__(self):
        super().__init__("InterfaceManager")

    @subscribe(process_mode=ProcessMode.CALL, on_event=EventBeforeLoad)
    def register_system_interfaces(self, event):
        for core_interface in core_interfaces.__all__:
            interface = core_interface()
            self.logger.info('Register CoreInterface: ' + str(interface.gateway_id))
            interface.register()
        # shelly_discovery
        # shelly_discovery = CoiotDiscovery()
        # shelly_discovery.register()
        # network adapter
        # network_adapter.register()

    @subscribe(process_mode=ProcessMode.CALL, on_event=EventBeforeLoad)
    def register_discovery_interfaces(self, event):
        for discovery_interface in discovery_interfaces.__all__:
            interface = discovery_interface()
            self.logger.info('Register DiscoveryInterface: ' + str(interface.gateway_id))
            interface.register()

    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventBeforeLoad)
    async def restore_initialized_interfaces(self, event: None):
        await self.load_device_interfaces_database()
        await self.load_device_interfaces_cloud()

    async def save_device_interface(self, interface: DeviceInterface, db: Session):
        cloud_adapter = CloudAdapter()
        # If cloud ID does not exist, create on cloud
        # Cloud ID indicates weather the cloud knows this device
        r = await cloud_adapter.request(method=RequestedType.POST, url='/gateway/api/v1/customer-device/create',
                                        data=interface.get_device_representation())
        if r.status_code != 200:
            return False
        interface.set_cloud_id(cloud_id=r.json()['id'])
        try:
            crud.customer_device.create(interface.get_device_representation(), db=db)
        except Exception as e:
            self.logger.error(e)
        return True

    async def load_device_interfaces_database(self):
        with Session(engine) as session:
            stored_devices = crud.customer_device.get_all(db=session)
            for device_info in stored_devices:
                try:
                    device_interface = get_interface_by_interface_name(interface_name=device_info.interface_name)

                    interface = device_interface(gateway_id=device_info.gateway_id, label=device_info.label,
                                                 host_ip=device_info.network_ip, device_type=device_info.device_type,
                                                 cloud_id=device_info.cloud_id)
                    self.logger.info(
                        'Loaded from Database and Registered DeviceInterface: ' + str(interface.gateway_id))
                    interface.register()
                except Exception as e:
                    self.logger.error(e)

    async def load_device_interfaces_cloud(self):
        cloud_devices = await CloudAdapter().get_customer_devices()
        for cloud_device in cloud_devices:
            if cloud_device['gateway_id'] not in EventBus.instance().subscribers.keys():
                try:
                    device_interface = get_interface_by_interface_name(interface_name=cloud_device['interface_name'])
                    # Device Label is missing during this creation
                    interface = device_interface(gateway_id=cloud_device['gateway_id'], label=cloud_device['label'],
                                                 host_ip=cloud_device['network_ip'],
                                                 device_type=cloud_device['device']['name'],
                                                 cloud_id=cloud_device['id'])
                    self.logger.info('Loaded from Cloud and Registered DeviceInterface: ' + str(interface.gateway_id))
                    interface.register()
                    with Session(engine) as session:
                        await self.save_device_interface(interface, db=session)
                except Exception as e:
                    self.logger.error(e)


"""
    @property
    def available(self):
        return self.__interface_available

    @property
    def not_initialized(self):

        initialized_interfaces = EventBus.instance().subscribers.values()
        return self.__interface_available not in initialized_interfaces

    def add(self, interface: object, interface_name: str):

        self.__interface_available[interface_name] = interface
"""
