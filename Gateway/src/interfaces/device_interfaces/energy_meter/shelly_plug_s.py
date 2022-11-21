from datetime import datetime
import json
from src.constants.const import ProcessMode, UIMessageType
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import CommunicationInterface
from src.interfaces.coiot_interface import CoiotInterface
from src.interfaces.core_interfaces.coap import EventCoapMessageReceived
from src.interfaces.core_interfaces.sse_adapter import EventSendUIMessage
from src.util.logger import get_logger_system


class ShellyPlugSEnergyMeterInterface(CoiotInterface, CommunicationInterface):
    """
    This Interface monitors messages from a Shelly Plug S over the CoIoT Protocol.
    It keeps track of its energy meter status and completely disregards the switch functionality bc we don't need them.
    """

    @property
    def device_type(self):
        return self._device_type

    def __init__(self, device_id, ip_addr, status=None):
        super().__init__(name=device_id)
        self.ip = ip_addr
        self._device_type = 'SHPLG-S'
        self.unit = 'Watt'
        # The range the status can be in
        self.range = "0/2500"
        # The sensor id is extracted from other python libraries and my own shelly adapter.
        # https://github.com/StyraHem/pyShelly/blob/master/pyShelly/powermeter.py
        # It seems like it is always the same but I have no official documentation for that.
        self.sensor_ids = [111, 4101, 4102, 4105]
        self.status = status
        # The status history without the current Status. List of Dict(time, Status)
        self.history = []
        self.last_updated = datetime.now()
        self.logger = get_logger_system(device_id)

    @property
    def host_ip(self):
        return self.ip

    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventCoapMessageReceived)
    async def on_coap_event(self, event: EventCoapMessageReceived):
        """
        This method observes all messages which are received on the CoAP protocol.
        For each message, it checks whether it belongs to this interface.
        If it is indeed a status message for this interface, it updates its status according to the message.
        :param event: A EventCoapMessageReceived Event which is emitted by the coap Thread.
        """
        # Code 30 is defined to send a new Status
        if event.code == 30:
            data = json.loads(event.payload.decode())
            # Get Generic sensor values
            sensor_values = data['G']
            # Extract the sensor Value according to the CoIoT Protocol for a device status
            value = next((sensor_value[2] for sensor_value in sensor_values if sensor_value[1] in self.sensor_ids),
                         None)
            self.update_status(value)

    def update_status(self, new_status: float):
        """
        This method updates the object status and makes sure that the object history is correct
        :param new_status: Status to be updated.
        """
        if self.active:
            self.history.append({'time': self.last_updated, 'status': self.status})
            self.status = new_status
            self.last_updated = datetime.now()
            self.logger.debug('New Status: %s' % self.status)
            ui_message_event = EventSendUIMessage(typ=UIMessageType.UPDATE,
                                                  name=self.name,
                                                  message=[int(self.last_updated.timestamp()), self.status])
            self.event_bus.emit(event=ui_message_event)
        else:
            print(self.name + 'inactive')
