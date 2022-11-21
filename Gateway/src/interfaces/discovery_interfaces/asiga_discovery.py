from src.constants.const import ProcessMode
from src.constants.lifecycle_events import EventStart
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import EventDiscoverInterfaces
from src.interfaces.abstract_interface import DiscoveryInterface
from src.interfaces.device_interfaces.printer.asiga.asiga_printer import AsigaPrinterInterface
import socket


class AsigaDiscovery(DiscoveryInterface):
    def __init__(self):
        super().__init__('AsigaDiscovery')
        self.sock = None
        self.ASIGA_PORT = 42511
        self.ASIGA_LISTEN_PORT = 44873
        self.ASIGA_ADDR = '192.168.0.255'
        self.search()

    def init_socket(self):
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
        sock.bind(('0.0.0.0', self.ASIGA_LISTEN_PORT))
        # create multicast group network information
        addr = socket.inet_aton(self.ASIGA_ADDR)
        interface = socket.inet_aton('0.0.0.0')
        # ask the host to join a multicast group
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, addr + interface)
        sock.settimeout(1)
        self.sock = sock

    @subscribe(process_mode=ProcessMode.THREAD, on_event=EventStart)
    def run(self, event):
        self.init_socket()
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                host_ip = addr[0]  # ip, port
                asiga_interface = AsigaPrinterInterface(host_ip=host_ip)
                self.event_bus.introduce(interface=asiga_interface)
            except socket.timeout:
                continue
        self.shutdown()

    @subscribe(process_mode=ProcessMode.CALL, on_event=EventDiscoverInterfaces)
    def search(self, event=None):
        try:
            self.sock.sendto(bytes.fromhex("0a"), (self.ASIGA_ADDR, self.ASIGA_PORT))
            self.logger.info("Search for ASIGA devices")
        except (AttributeError, socket.error) as msg:
            self.logger.warning("failure sending out byebye notification: %r" % msg)
