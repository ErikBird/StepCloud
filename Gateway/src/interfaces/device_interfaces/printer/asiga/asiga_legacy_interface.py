import threading
import socket
from datetime import datetime

import requests

from src.constants.const import ProcessMode, UIMessageType
from src.constants.lifecycle_events import EventStart
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import DeviceInterface
from src.interfaces.core_interfaces.sse_adapter import EventSendUIMessage


def get_printer_ini(ip_addr: str) -> dict:
    url = 'http://' + ip_addr + '/printer.ini'
    r = requests.get(url, verify=False, timeout=10)  # 10 seconds
    r.encoding = 'utf-8'
    r.raise_for_status()

    data = r.content.decode("utf-8")
    log_lines = [log_line.split('=') for log_line in data.split('\r\n') if len(log_line.split('=')) > 1]
    log_dict = {}
    for line in log_lines: log_dict[line[0]] = line[1]
    return {'text': data, 'dict': log_dict}


class AsigaObserver(DeviceInterface):
    @property
    def device_type(self):
        return self._model

    def __init__(self, ip_addr):
        self._thread = threading.Thread(target=self._loop)
        self._thread.name = 'AsigaObserver'
        self._thread.daemon = True
        self._host_ip = ip_addr
        self.port = 80
        printer_ini = get_printer_ini(self._host_ip)['dict']
        self.serial_number = printer_ini['Serial Number'].replace('\"', '')
        self._model = printer_ini['Model Type'].replace('\"', '')
        super().__init__(gateway_id=self.serial_number)

    def _loop(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                url = 'http://' + self._host_ip + '/debug?f=1&k=1&n=0'
                s = requests.Session()
                r = s.get(url, stream=True)
                for line in r.iter_lines():
                    if line:
                        log_parts = line.decode("utf-8").split('] ')
                        if len(log_parts) == 3:
                            log_dict = {'time': log_parts[0].replace('[', ''),
                                        'label': log_parts[1].replace('[', ''),
                                        'content': log_parts[2]}
                            if 'Build: Separate' in log_dict['content'] and self.active:
                                ui_message_event = EventSendUIMessage(typ=UIMessageType.UPDATE,
                                                                      name=self.name,
                                                                      message=[int(datetime.now().timestamp()), 1])
                                self.event_bus.emit(event=ui_message_event)
                            elif 'Build: Move down slowly for overdrive' in log_dict['content'] and self.active:
                                ui_message_event = EventSendUIMessage(typ=UIMessageType.UPDATE,
                                                                      name=self.name,
                                                                      message=[int(datetime.now().timestamp()), 0])
                                self.event_bus.emit(event=ui_message_event)
            print('Socket over')

    @subscribe(process_mode=ProcessMode.THREAD, on_event=EventStart)
    def start(self, event=None):
        """
        This method starts the CoAP Thread to listen to continuously listen to the CoAP Socket for messages
        It is started once the EventStart Lifecycle Event is emitted
        """
        self._thread.start()

    @property
    def host_ip(self):
        return self._host_ip
