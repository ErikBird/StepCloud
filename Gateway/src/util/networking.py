import socket
import sys


def get_network_interface_ip_address():
    """
    Get the IP address of the current network interface.
    :return: The IP address.
    """
    if not sys.flags.dev_mode:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    else:
        return "0.0.0.0:7353"
