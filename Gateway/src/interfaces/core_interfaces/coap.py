import threading
import queue
from src.constants.lifecycle_events import EventStart, EventStop
from src.event_bus.decorator import subscribe
import socket
import struct

from src.constants.const import System, ProcessMode
from src.event_bus.helper_classes import Event
from src.interfaces.abstract_interface import SystemInterface


class EventSendCoapMessage(Event):
    """
    This Event can be emitted by Integrations to send a message over the CoAP Multicast Socket.
    """

    def __init__(self, message: bytes):
        super().__init__(name='EventSendCoapMessage')
        self.message = message

    def __str__(self):
        return self.name + ' sends message: ' + str(self.message)


class EventCoapMessageReceived(Event):
    """
    This Event can will be emitted by the CoAP Thread once it received a Message.

    If a Integration wants to receive a CoAP message, it needs to subscribe to this Event.
    """

    def __init__(self, message_id, code, options, payload, ipaddr, token=''):
        super().__init__(name='EventCoapMessageReceived')
        self.message_id = message_id
        self.code = code
        self.options = options
        self.payload = payload
        self.ip = ipaddr
        self.token = token

    def __str__(self):
        return self.name + ' received message with code: ' + str(self.code)


class CoAP(SystemInterface):
    def __init__(self):
        super().__init__('CoAP')
        self._thread = threading.Thread(target=self._loop)
        self._thread.name = 'CoAP'
        self._thread.daemon = True
        self._socket = None
        self.message_queue = queue.Queue()

    def _loop(self):
        """
        This loop is continuously executed while the Tread is active
        It has two Tasks:
        1. Check if it received new UDP Packages
        2. Send messages toward
        Loop which continuously checks for new UDP Packages
        """
        while not self._stop:
            try:
                try:
                    # buffer size is 1024 bytes
                    data, (ipaddr, port) = self._socket.recvfrom(1024)

                except socket.timeout:
                    continue

                message_event = self.create_message_event(data=data, ipaddress=ipaddr)
                self.event_bus.emit(event=message_event)

                try:
                    message = self.message_queue.get(False)
                except queue.Empty:
                    print('Queue empty')
                else:
                    self._socket.sendto(message, (System.COAP_MULTICAST_IP, System.COAP_PORT))

            except Exception as ex:
                self.logger.error(ex)

    @subscribe(process_mode=ProcessMode.THREAD, on_event=EventStart)
    def start(self, event):
        """
        This method starts the CoAP Thread to listen to continuously listen to the CoAP Socket for messages
        It is started once the EventStart Lifecycle Event is emitted
        """
        self.logger.debug('CoAP Socket Started')
        self._init_socket()
        self._thread.start()

    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventSendCoapMessage)
    async def send_message(self, event: EventSendCoapMessage):
        """
        This method enqueues a message to be broadcast over the CoAP Protocol
        You can trigger this method to send a message by emitting a EventSendCoapMessage Event.
        :param event: EventSendCoapMessage containing the message as attribute
        """
        self.logger.debug('Message %s Enqueued' % event.message)
        self.message_queue.put(event.message)

    def _init_socket(self):
        """
        Initializes a UDP Socket to listen for UDP Multicast

        The Socket is used in the Thread loop function to listen for UDP Messages from the CoAP protocol
        """
        # Initialize custom socket
        sock = socket.socket(
            # IPv4 Protocol
            socket.AF_INET,
            # UDP Protocol
            socket.SOCK_DGRAM)
        # Hop restrictions of the network
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # receives ALL multicast groups if bind_ip is empty otherwise only from bind_ip
        sock.bind(('0.0.0.0', System.COAP_PORT))
        # packing IP and 0 into byte vector. 4s = four characters , l = signed long
        mreq = struct.pack("=4sl",
                           socket.inet_aton(System.COAP_MULTICAST_IP),
                           socket.INADDR_ANY)
        # ask the host to join a multicast group defined in mreq
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.settimeout(15)
        self._socket = sock

    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventStop)
    async def close(self):
        """
        This method stops the CoAP Thread and shuts down its UDP Socket
        """
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._stop = True
        except socket.error:
            pass

    def create_message_event(self, data, ipaddress):
        """
        Parse a CoAP message according to the RFC7252 standard.

        The open standard can be found here: https://tools.ietf.org/html/rfc7252#section-3

        The purpose of this method is to extract all information from the message binary with this format:
           0                   1                   2                  3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |Ver| T |  TKL  |      Code     |          Message ID           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |   Token (if any, TKL bytes) ...
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |   Options (if any) ...
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |1 1 1 1 1 1 1 1|    Payload (if any) ...
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        :param ipaddress: the ipaddress from which we received the message
        :param data: Binary in the CoAP message format
        :return: EventCoapMessageReceived Instance with all Attributes
        """
        if len(data) < 4:
            raise Exception('Message to short')

        # Token Length = TKL
        token_length = data[0] & 0b00001111

        if token_length > 8:
            raise Exception('Invalid Token length of received message:', data)

        index_before_payload = data.find(b'\xff')

        code = data[1]
        message_id = data[2:4]
        token = data[4: 4 + token_length]
        options = self.parse_options(data[4 + token_length:index_before_payload])
        payload = data[index_before_payload + 1:]
        event = EventCoapMessageReceived(message_id=message_id, code=code, options=options, payload=payload,
                                         ipaddr=ipaddress, token=token)
        return event

    def parse_options(self, option_binary):
        """
        Parse a CoAP message option content according to the RFC7252 standard.

        The open standard can be found here: https://tools.ietf.org/html/rfc7252#section-3

            0   1   2   3   4   5   6   7
           +---------------+---------------+
           |               |               |
           |  Option Delta | Option Length |   1 byte
           |               |               |
           +---------------+---------------+
           \                               \
           /         Option Delta          /   0-2 bytes
           \          (extended)           \
           +-------------------------------+
           \                               \
           /         Option Length         /   0-2 bytes
           \          (extended)           \
           +-------------------------------+
           \                               \
           /                               /
           \                               \
           /         Option Value          /   0 or more bytes
           \                               \
           /                               /
           \                               \
           +-------------------------------+
        :param option_binary: binary content of the options which is the content after the Token and before the Payload
        :return: A list containing dictionaries with the option name as key and the option value as content
        """
        result = []
        binary_index = 0
        previous_option_id = 0
        while binary_index < len(option_binary):
            option_delta, extended_delta_bytes = self.get_option_delta(option_binary[binary_index:])
            option_length, extended_length_bytes = self.get_length_delta(option_binary[binary_index:])

            start_of_option_value = binary_index + 1 + extended_delta_bytes + extended_length_bytes
            option_value = option_binary[start_of_option_value:]

            option_id = option_delta + previous_option_id
            previous_option_id = option_id

            option_name = self.decode_coap_option_name(option_id)
            option_content = option_value[:option_length]

            result.append({option_name: option_content})

            binary_index = start_of_option_value + option_length

        return result

    def get_option_delta(self, option_binary):
        """
        A implementation of to get the option delta according to RFC7252 standard.
        The first 4-bit unsigned integer represent the delta as long as it is a value
        between 0 and 12. Value 13, 14 and 15 are special delta constructs.

        13:  An 8-bit unsigned integer follows the initial byte and
            indicates the Option Delta minus 13.

        14:  A 16-bit unsigned integer in network byte order follows the
             initial byte and indicates the Option Delta minus 269.

        We do not implement 15 since it is only a reserved marker.

        :param option_binary:
        :return:
        """

        delta = option_binary[0] >> 4
        extended_delta_bytes = 0

        # Special Option Constructs:
        if delta == 13:
            delta = option_binary[1] + 13
            extended_delta_bytes = 1
        elif delta == 14:
            delta = option_binary[1] * 256 + option_binary[2] + 269
            extended_delta_bytes = 2
        return delta, extended_delta_bytes

    def get_length_delta(self, option_binary):
        """
        A implementation of to get the option length according to RFC7252 standard.
        The second 4-bit unsigned integer represent the length as long as it is a value
        between 0 and 12. Value 13, 14 and 15 are special delta constructs.

          13:  An 8-bit unsigned integer precedes the Option Value and
             indicates the Option Length minus 13.

          14:  A 16-bit unsigned integer in network byte order precedes the
             Option Value and indicates the Option Length minus 269.

        We do not implement 15 since it is only a reserved marker.

        :param option_binary:
        :return:
        """
        length = option_binary[0] & 0b00001111
        extended_length_bytes = 0

        # Special Option Constructs:
        if length == 13:
            length = option_binary[1] + 13
            extended_length_bytes = 1
        elif length == 14:
            length = option_binary[1] * 256 + option_binary[2] + 269
            extended_length_bytes = 2
        return length, extended_length_bytes

    def decode_coap_option_name(self, option_id):
        """
        Decode the Names defined by CoAP:
        https://tools.ietf.org/html/rfc7252#section-5.4
        +-----+---+---+---+---+----------------+--------+--------+----------+
           | No. | C | U | N | R | Name           | Format | Length | Default  |
           +-----+---+---+---+---+----------------+--------+--------+----------+
           |   1 | x |   |   | x | If-Match       | opaque | 0-8    | (none)   |
           |   3 | x | x | - |   | Uri-Host       | string | 1-255  | (see     |
           |     |   |   |   |   |                |        |        | below)   |
           |   4 |   |   |   | x | ETag           | opaque | 1-8    | (none)   |
           |   5 | x |   |   |   | If-None-Match  | empty  | 0      | (none)   |
           |   7 | x | x | - |   | Uri-Port       | uint   | 0-2    | (see     |
           |     |   |   |   |   |                |        |        | below)   |
           |   8 |   |   |   | x | Location-Path  | string | 0-255  | (none)   |
           |  11 | x | x | - | x | Uri-Path       | string | 0-255  | (none)   |
           |  12 |   |   |   |   | Content-Format | uint   | 0-2    | (none)   |
           |  14 |   | x | - |   | Max-Age        | uint   | 0-4    | 60       |
           |  15 | x | x | - | x | Uri-Query      | string | 0-255  | (none)   |
           |  17 | x |   |   |   | Accept         | uint   | 0-2    | (none)   |
           |  20 |   |   |   | x | Location-Query | string | 0-255  | (none)   |
           |  35 | x | x | - |   | Proxy-Uri      | string | 1-1034 | (none)   |
           |  39 | x | x | - |   | Proxy-Scheme   | string | 1-255  | (none)   |
           |  60 |   |   | x |   | Size1          | uint   | 0-4    | (none)   |
           +-----+---+---+---+---+----------------+--------+--------+----------+
        Else return the code. Some Protocols like CoIoT have defined their own codes. This can be decoded later on.
        """
        Option_IDs = {
            1: 'If-Match',
            3: 'Uri-Host',
            4: 'ETag',
            5: 'If-None-Match',
            7: 'Uri-Port',
            8: 'Location-Path',
            11: 'Uri-Path',
            12: 'Content-Format',
            14: 'Max-Age',
            15: 'Uri-Query',
            17: 'Accept',
            20: 'Location-Query',
            35: 'Proxy-Uri',
            39: 'Proxy-Scheme',
            60: 'Size1',
        }
        if option_id in Option_IDs:
            return Option_IDs[option_id]
        else:
            return option_id
