import random
import uuid

from src.interfaces.abstract_interface import SystemInterface
import socket
import threading
from email.utils import formatdate
from src.constants.const import System, ProcessMode
from src.constants.lifecycle_events import EventStart, EventStop
from src.event_bus.decorator import subscribe
from src.util.networking import get_network_interface_ip_address


class SSDPServer(SystemInterface):
    """
    A implementation of a SSDP server.
    The Server listens for this device type and responds accordingly.

    This implementation does not implement the specs of ssdp precisely
    http://www.upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.1.pdf

    Differences:
    - the location does not point to the XML document about the device but only sends the ip
    - the server name does not follow the advised naming convention
    - our own device identifier is not a defined upnp device

    We differentiate from the spec because we don't seek compatibility with Upnp Protocols
    The differences make it easier to connect the gateway to clients.
    """
    known = {}

    def __init__(self):
        super().__init__('SSDPServer')
        self._thread = threading.Thread(target=self._loop)
        self._thread.name = 'SSDPServer'
        self._thread.daemon = True
        self._socket = None
        # ST: The search target of this service
        self.st: str = System.NAME.lower().replace(' ', ':')
        # USN: The unique service name to identify this device.
        self.usn: str = 'uuid:{}::{}'.format(uuid.uuid4(), self.st)
        # LOCATION: The location URL to allow the original transmitting device to gain more information about the
        # discovered device.
        self.location: str = f'{get_network_interface_ip_address()}'
        # SERVER: The server system information value providing information in the following format: [OS-Name] UPnP/[
        # Version] [Product-Name]/[Product-Version].
        self.server: str = System.NAME
        # A value to determine for how long the message is valid
        self.cache_control: str = 'max-age=1800'
        self.host = None

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
        sock.bind(('0.0.0.0', System.SSDP_PORT))
        # create multicast group network information
        addr = socket.inet_aton(System.SSDP_ADDR)
        interface = socket.inet_aton('0.0.0.0')
        # ask the host to join a multicast group
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, addr + interface)
        sock.settimeout(1)
        self._socket = sock

    def _loop(self):
        while not self._stop:
            try:
                try:
                    # buffer size is 1024 bytes
                    data, (ipaddr, port) = self._socket.recvfrom(1024)

                except socket.timeout:
                    continue

                self.datagram_received(data=data, host=ipaddr, port=port)
            except Exception as ex:
                self.logger.error(ex)

        self.shutdown()

    @subscribe(process_mode=ProcessMode.THREAD, on_event=EventStart)
    def start(self, event):
        """
        This method starts the SSDP Thread to listen to continuously listen to the SSDP Socket for messages
        It is started once the EventStart Lifecycle Event is emitted
        """
        self.logger.info(self.gateway_id + ' started with st: ' + self.st)
        self._init_socket()
        self._thread.start()

    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventStop)
    async def shutdown(self):
        # for st in self.known:
        #    if self.known[st]['MANIFESTATION'] == 'local':
        #        print('self.do_byebye(st)')
        self._stop = True
        self._socket.shutdown(socket.SHUT_RDWR)

    def datagram_received(self, data, host, port):
        """Handle a received multicast datagram."""

        try:
            header, payload = data.decode().split('\r\n\r\n')[:2]
        except ValueError as err:
            self.logger.error(err)
            return

        lines = header.split('\r\n')
        cmd = lines[0].split(' ')
        lines = map(lambda x: x.replace(': ', ':', 1), lines[1:])
        lines = filter(lambda x: len(x) > 0, lines)

        headers = [x.split(':', 1) for x in lines]
        headers = dict(map(lambda x: (x[0].lower(), x[1]), headers))

        if cmd[0] == 'M-SEARCH' and cmd[1] == '*':

            # SSDP discovery
            self.discovery_request(headers, (host, port))
        elif cmd[0] == 'NOTIFY' and cmd[1] == '*':
            # SSDP presence
            self.logger.debug('NOTIFY *')
        else:
            self.logger.warning('Unknown SSDP command %s %s' % (cmd[0], cmd[1]))

    def send_it(self, response, destination, delay, usn):
        self.logger.debug('send discovery response delayed by %ds for %s to %r' % (delay, usn, destination))
        try:
            self._socket.sendto(response.encode(), destination)
        except (AttributeError, socket.error) as msg:
            self.logger.warning("failure sending out byebye notification: %r" % msg)

    def discovery_request(self, headers, host_port):
        """Process a discovery request.  The response must be sent to
        the address specified by (host, port)."""

        (host, port) = host_port
        self.logger.info(self.st)
        if self.st == headers['st'] or headers['st'] == 'ssdp:all':
            response = ['HTTP/1.1 200 OK',
                        'CACHE-CONTROL: %s' % self.cache_control,
                        'ST: %s' % self.st,
                        'USN: %s' % self.usn,
                        'EXT: %s' % '',
                        'SERVER: %s' % self.server,
                        'LOCATION: %s' % self.location,
                        'DATE: %s' % formatdate(timeval=None, localtime=False, usegmt=True)]

            response.extend(('', ''))
            import sys
            self.logger.info(sys.flags.dev_mode)
            self.logger.info(response)
            delay = random.randint(0, int(headers['mx']))
            self.logger.info('Respond to discovery request')
            self.send_it('\r\n'.join(response), (host, port), delay, self.usn)

#:27:09,679 — SSDPServer — DEBUG — with headers: {'host': '239.255.255.250:1900', 'location': 'http://192.168.178.1:49000/MediaServerDevDesc.xml', 'server': 'FRITZ!Box 6490 Cable (lgi) UPnP/1.0 AVM FRITZ!Box 6490 Cable (lgi) 141.07.29', 'cache-control': 'max-age=1800', 'nt': 'urn:avm.de:service:AVM_ServerStatus:1', 'nts': 'ssdp:alive', 'usn': 'uuid:fa095ecc-e13e-40e7-8e6c-ccce1ea62917::urn:avm.de:service:AVM_ServerStatus:1'}.
