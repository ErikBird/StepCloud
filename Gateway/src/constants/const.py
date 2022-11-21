"""
This file contains all constants of the system.

If multiple constants are used by multiple Integrations, it is advised to to have its own class for simplicity.
"""
import logging
import os
from enum import Enum
from src import sqlmodels


class System(object):
    """
    These constants are used to configure the system or Integrations.
    The first word should describe the system part, the constant belongs to.
    """
    NAME = 'StepCloud Gateway'
    STDOUT_LOG_LEVEL = logging.DEBUG
    SOFTWARE_VERSION = "0.0.1"
    HARDWARE_VERSION = "0.0.1"
    UUID: sqlmodels.UUID
    AUTH_TOKEN: sqlmodels.AuthTokens
    SQLITE_FILE_PATH = "database.db"
    CLI_PID_FILE_PATH = os.path.abspath(os.getcwd()) + "/engine.pid"
    LOGGING_PATH_ERROR = os.path.abspath(os.getcwd()) + "/logs/error.log"
    CLOCK_TIMER_INTERVAL = 30  # seconds
    COAP_MULTICAST_IP = "224.0.1.187"
    COAP_PORT = 5683
    SSDP_PORT = 1900
    SSDP_ADDR = '239.255.255.250'


class ProcessMode(int, Enum):
    """
    These constants are used to determine in which process mode the event_bus will start a event callback function.
    """
    CALL = 0
    ASYNC = 1
    PROCESS = 2
    THREAD = 3


class EventTypeEnum(str, Enum):
    settings_changes = "settings_changes"
    performed_task = "performed_task"


class RequestedType(str, Enum):
    GET = 'get'
    POST = 'post'


class SSEEventType(str, Enum):
    STATUS = 'status'
    PROGRESS = 'progress'
    LOAD = 'load'


class StatusEventType(str, Enum):
    ONLINE = 'online'
    IDLE = 'idle'
    OFFLINE = 'offline'


class InterfaceName(str, Enum):
    """
    These constants need to be the same Names as the .png pictures in the public/device_interfaces/ folder on the UI Client
    """
    NetioPowerCable = 'NetioPowerCable'
    AsigaPrinter = 'AsigaPrinter'


class SupportedDevice(str, Enum):
    """
    These constants need to correspond to the names of the devices on the cloud and their identifiers
    """
    NKOptikOtoflashG171 = 'Otoflash G171'
    Emmi30HC = 'Emmi-30 HC'
    AsigaMaxUV385 = 'MAX UV385'
    AsigaMaxMini = 'MAX Mini'
    AsigaPro2UV385 = 'PRO 2 UV385'
    AsigaMaxUV365 = 'MAX UV365'
    AsigaPro4KUV385 = 'PRO 4K UV385'
