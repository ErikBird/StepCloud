from src.constants.const import ProcessMode
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import SystemInterface
from src.interfaces.coiot_interface import CoiotInterface
from src.interfaces.core_interfaces.coap import EventSendCoapMessage, EventCoapMessageReceived
from src.interfaces.device_interfaces.energy_meter.shelly_plug_s import ShellyPlugSEnergyMeterInterface

InterfaceByType = {
    **dict.fromkeys(['SHPLG-S', 'SHPLG-1', 'SHPLG2-1', 'SHPLG-U1'], ShellyPlugSEnergyMeterInterface)
}


class CoiotDiscovery(CoiotInterface, SystemInterface):
    """
    The CoiotDiscovery Interface monitors all network devices which are communicating in the local network over CoAP
    according to the CoIoT protocol.
    The Interface registers unseen devices to the EventBus.
    Therefore the EventBus always knows all devices in the network.
    """

    def __init__(self):
        super().__init__('CoIoTDiscovery')

    @subscribe(process_mode=ProcessMode.CALL, on_event=EventCoapMessageReceived)
    def on_coiot_event(self, event: EventCoapMessageReceived):
        """
        Method to subscribe on all CoAP Messages and check if their senders are already registered in the system.
        If they are not known, the appropriate Interface is created and registered on the Eventbus.
        :param event: Any EventCoapMessageReceived Event
        """
        # The message option can identify the sender of a CoIoT conform message
        device_type, device_id = self.option_to_type_and_id(event.options)
        if device_type:
            # Code 30 is defined to send a new Status in the CoIoT Protocol
            if event.code == 30:
                if device_id not in self.event_bus.subscribers.keys():
                    interface_class = InterfaceByType[device_type]
                    interface = interface_class(device_id=device_id, ip_addr=event.ip)
                    interface.register()
                    self.event_bus.emit(event)

    def send_discover(self):
        """
        Give the Task to multicast a GET request for the device description according to the CoIoT protocol

        All devices which listen to CoAP in the CoIoT protocol should respond to the uri query '/cit/d'
        with their device description. The description is send with the CoAP Code 69.

        We don't listen for messages with this code yet bc. we have no "unknown" sensors where we need to get
        the attribute information from the sensor.

        Example Payload for the request:
        b'{"blk":[{"I":0,"D":"Relay0"}],"sen":[{"I":111,"T":"W","R":"0/2500","L":0},
        {"I":112,"T":"Switch","R":"0/1","L":0}],
        "act":[{"I":211,"D":"Switch","L":0,"P":[{"I":2011,"D":"ToState","R":"0/1"}]}]}'
        :return: Gives the EventBus the task to emit a CoAP GET Message
        """
        msg = b'/cit/s'
        coap_message_event = EventSendCoapMessage(message=msg)
        self.event_bus.emit(event=coap_message_event)
