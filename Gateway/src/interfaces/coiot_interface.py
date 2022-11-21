from abc import ABC


class CoiotInterface(ABC):
    """
    This Interface provides all tools to use the CoIoT Protocol that are not implemented in the CoAP Interface.
    
    CoIoT is an Extension of the CoAP Protocol. It is created by the manufacturer of the Shelly device family.
    Therefore it is implemented in (all?) Shelly devices and used as the default network protocol.
    https://shelly-api-docs.shelly.cloud/docs/coiot/v1/CoIoT%20for%20Shelly%20devices%20(rev%201.0)%20.pdf
    """

    @staticmethod
    def option_to_type_and_id(option: list):
        """
        Method to extract the device type and the device id from a coap option list if it follows
        the CoIoT Protocol
        :param option: list of all options. All not native CoAP option IDs are encoded as Integer
        :return: the device_type and device_id as encoded in the option if it exists. Otherwise None
        """
        # Check if the CoAP header contains the COIOT_OPTION_BASE which is defined by id 3332
        option_base = [option_entry[3332] for option_entry in option if 3332 in option_entry.keys()]
        if option_base:
            # Decode CoIoT device identification
            device_type, device_id, version = option_base[0].decode('utf-8', "ignore").split('#', 2)
            # Don't pass version since the version decoding is somehow broken and it is not needed up to now
            return device_type, device_id
        else:
            return None, None
