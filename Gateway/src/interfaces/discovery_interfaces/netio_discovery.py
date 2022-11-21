from src.constants.const import ProcessMode
from src.constants.lifecycle_events import EventStart
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import EventDiscoverInterfaces
from src.interfaces.abstract_interface import DiscoveryInterface
from src.interfaces.device_interfaces.energy_meter.netio_powercable import NetioPowerCableInterface
import socket


class NetioDiscovery(DiscoveryInterface):
    def __init__(self):
        super().__init__('NetioDiscovery')
        self.sock = None
        self.NETIO_PORT = 62386
        self.NETIO_ADDR = '255.255.255.255'
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
        sock.bind(('0.0.0.0', self.NETIO_PORT))
        # create multicast group network information
        addr = socket.inet_aton(self.NETIO_ADDR)
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
                device_info = self.parseDeviceInfo(data)
                self.logger.info(f"Device discovered: {device_info['devicename']}")
                ip = device_info['ip']
                mac = device_info['mac']
                devicename = device_info['devicename']
                netio_interface = NetioPowerCableInterface(gateway_id=mac,  # unique id
                                                           label=devicename,  # ui name
                                                           host_ip=ip)
                self.event_bus.introduce(interface=netio_interface)
                self.logger.info(f"NETIO device {devicename} found and introduced as NetioPowerCableInterface")
            except socket.timeout:
                continue

    def parseDeviceInfo(self, data):
        """
        Parse NETIO Device information from data payload
        """
        binarydata = bytearray(data)

        if binarydata[0] != 2:
            self.logger.error("Data are not valid")
            return
        else:
            pass

        i = 3
        params = []
        datalen = len(binarydata)
        while i < datalen - 1:
            param = {'DATA': []}
            param['FTYPE'] = binarydata[i]
            i += 1
            paramlen = binarydata[i]
            i += 1
            if (i + paramlen) < len(binarydata):
                for j in range(0, paramlen):
                    param['DATA'].append(binarydata[i + j])
            i += paramlen
            params.append(param)

        device = {}

        for item in params:

            if item.get('FTYPE') == 0x01:  # FIRMWARE_VERSION
                device['fwversion'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x02:  # MAC
                device['mac'] = ':'.join(format(i, '02x') for i in item.get('DATA')).upper()
                continue
            if item.get('FTYPE') == 0x03:  # IP
                device['ip'] = '.'.join(str(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x04:  # NETMASK
                device['mask'] = '.'.join(str(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x05:  # HOSTNAME
                device['hostname'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x06:  # DHCP
                continue
            if item.get('FTYPE') == 0x07:  # SETUP_STATE
                continue
            if item.get('FTYPE') == 0x08:  # RESULT
                continue
            if item.get('FTYPE') == 0x09:  # PRODUCT
                device['model'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0a:  # MANUFACTURER
                device['manufacturer'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0b:  # PLATFORM
                device['platform'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0c:  # VARIANT
                device['hostname'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0d:  # TIMEOUT
                continue
            if item.get('FTYPE') == 0x0e:  # GATEWAY
                continue
            if item.get('FTYPE') == 0x0f:  # DNS
                continue
            if item.get('FTYPE') == 0x12:  # PRETTY_PLATFORM_NAME
                device['platformname'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x13:  # DEVICE_NAME
                device['devicename'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
        return device

    @subscribe(process_mode=ProcessMode.CALL, on_event=EventDiscoverInterfaces)
    def search(self, event=None):
        try:
            self.sock.sendto(bytes.fromhex("01ec00"), ('255.255.255.255', 62387))
            self.logger.info("Search for NETIO devices")
        except (AttributeError, socket.error) as msg:
            self.logger.warning("failure with error %r" % msg)
