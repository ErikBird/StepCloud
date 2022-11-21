from typing import List
from src.constants.const import SupportedDevice, ProcessMode
from src.constants.lifecycle_events import EventStop
from abc import ABC, abstractmethod
from src.event_bus.helper_classes import Event
from src import sqlmodels
from src.event_bus.decorator import subscribe
from src.event_bus.event_bus import EventBus
from src.util.logger import get_logger


class EngineInterface(ABC):
    """
    Generic Class of a EngineInterface.

    This class should be inherited to create a higher level Interface.
    """

    def __init__(self, gateway_id):
        # The Gateway ID should Identify the Interface Uniquely
        self._gateway_id: str = gateway_id
        # The Interface Label should Label the Interface such that a user can recognize it.
        # It should be unique, however the recognizablility is more important than a proven uniqueness.
        # Therefore, sometimes the label converges from the name for a better ux
        self._label: str = gateway_id
        # The stop variable should be checked in the implementation of loops to abort if the Interface should be stopped
        self._stop = False
        # The EventBus reference can be used to emit Events
        self.event_bus = EventBus.instance()
        self.logger = get_logger(gateway_id)

    @property
    def gateway_id(self) -> str:
        return self._gateway_id

    @property
    def label(self) -> str:
        return self._label

    def register(self):
        """
        This method registers the Interface on the EventBus.

        The Interface Methods are only triggered by the Events if the Interface is registered.
        """
        EventBus.instance().register(subscriber=self, gateway_id=self._gateway_id)

    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventStop)
    def stop(self):
        """
        The stop method sets the stop variable to True

        This should stop a looping processes of a higher level Interface
        """
        self._stop = True


class SystemInterface(EngineInterface):
    @property
    def communicating(self):
        return False


class DeviceInterface(EngineInterface):
    """
    This class represents all Interfaces which gather Data for a Production Step.
    It should NOT be implemented by system background interfaces.
    """

    # The general name of the interface
    interface_name: str

    def __init__(self, gateway_id: str, label: str, host_ip: str, device_type: str = None, cloud_id=None):
        super().__init__(gateway_id)
        self._label: str = label
        self._host_ip: str = host_ip
        # The device type this Interface should represent
        self._device_type: str = device_type
        self._registration_code: str = ''
        self._serial_number: str = ''
        # Cloud ID is the same as the customer_device_id on the cloud
        # indicates weather the cloud knows this device
        self._cloud_id: int = cloud_id

    @classmethod
    @abstractmethod
    def init_by_ip(cls, host_ip):
        pass

    @property
    def host_ip(self):
        """
        Returns IP without Protocol
        """
        ip = self._host_ip.replace('http://', '').replace('https://', '')
        return ip

    def set_cloud_id(self, cloud_id: int):
        self._cloud_id = cloud_id

    @property
    def device_type(self):
        return self._device_type

    @property
    def cloud_id(self):
        return self._cloud_id

    def set_device_type(self, device_type: SupportedDevice):
        self._device_type = device_type

    def get_device_representation(self) -> sqlmodels.CustomerDevice:
        return sqlmodels.CustomerDevice(
            network_ip=self.host_ip,
            registration_code=self._registration_code,
            serial_number=self._serial_number,
            device_type=self._device_type,
            gateway_id=self._gateway_id,
            label=self._label,
            interface_name=self.interface_name,
            cloud_id=self._cloud_id
        )

    @property
    @abstractmethod
    def supported_devices(self) -> List[SupportedDevice]:
        # The devices that can be monitored with this Interface
        pass

    @property
    def interface_name(self) -> str:
        return type(self).__name__


class EventDiscoverInterfaces(Event):
    """
    This Event can be emitted by Integrations to send a message over the CoAP Multicast Socket.
    """

    def __init__(self):
        super().__init__(name='EventDiscoverInterfaces')

    def __str__(self):
        return self.name


class DiscoveryInterface(SystemInterface):
    """
    This class enables the
    """

    def __init__(self, gateway_id):
        # The Gateway ID should Identify the Interface Uniquely
        super().__init__(gateway_id)

    @abstractmethod
    def search(self, event):
        pass
