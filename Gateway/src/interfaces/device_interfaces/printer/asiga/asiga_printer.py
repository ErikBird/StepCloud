import re
import time
from typing import List

import requests

from src.constants.const import InterfaceName, SupportedDevice, ProcessMode, StatusEventType, EventTypeEnum
from src.constants.event_collection import StartInterfaceEvent
from src.constants.lifecycle_events import EventStart
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import DeviceInterface
from src.interfaces.core_interfaces.cloud_adapter import EventUploadData
from src.interfaces.core_interfaces.sse_adapter import StatusEvent, LoadEvent, ProgressEvent
from src.sqlmodels import SensorData, SensorTypeEnum, VisualizationTypeEnum, LogData, LogTypeEnum


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


class AsigaPrinterInterface(DeviceInterface):
    @classmethod
    def init_by_ip(cls, host_ip):
        try:
            return cls(host_ip=host_ip)
        except:
            return None

    def __init__(self, host_ip: str, gateway_id=None, label=None, cloud_id: int = None, device_type=None):
        self._device_name = device_type
        if not label or not gateway_id:
            printer_ini = get_printer_ini(host_ip)['dict']
            self._serial_number = printer_ini['Serial Number'].replace('\"', '')
            self._device_name = printer_ini['Model Type'].replace('\"', '')
            if not label:
                label = printer_ini['Network Name'].replace('\"', '')
            if not gateway_id:
                gateway_id = self._serial_number
        super().__init__(gateway_id=gateway_id, label=label,
                         host_ip=host_ip, cloud_id=cloud_id, device_type=self._device_name)
        self.seperation_weight = {'time': [],
                                  'values': []}
        self.debug_log = {'time': [],
                          'label': [],
                          'content': []}
        self.status = StatusEventType.ONLINE

    @property
    def supported_devices(self) -> List[SupportedDevice]:
        return [self._device_name]

    @subscribe(process_mode=ProcessMode.THREAD, on_event=StartInterfaceEvent)
    def start(self, event: StartInterfaceEvent):
        if event.gateway_id == self.gateway_id:
            self.run(event=event)

    @subscribe(process_mode=ProcessMode.THREAD, on_event=EventStart)
    def run(self, event):
        self.logger.info(f'{self.gateway_id} started')
        while True:
            try:
                url = f'http://{self._host_ip}/debug?f=1&k=1&n=0'
                s = requests.Session()
                r = s.get(url, stream=True)
                for line in r.iter_lines():
                    if line:

                        log_parts = line.decode("utf-8").split('] ')
                        if len(log_parts) == 3:
                            log_dict = {'time': log_parts[0].replace('[', ''),
                                        'label': log_parts[1].replace('[', ''),
                                        'content': log_parts[2]}
                            if 'Separation weight limit:' in log_dict['content']:
                                data = re.findall("\d*\.?\d* kg$", log_dict['content'])
                                if len(data) > 0:
                                    weight = float(data[0].replace(" kg", ""))

                                    self.seperation_weight['values'].append(weight)
                                    self.seperation_weight['time'].append(log_dict['time'])

                                    self.debug_log['time'].append(log_dict['time'])
                                    self.debug_log['label'].append(log_dict['label'])
                                    self.debug_log['content'].append(log_dict['content'])

                                    load_event = LoadEvent(gateway_id=self.gateway_id, load=weight)
                                    self.event_bus.emit(load_event)
                                    self.logger.debug(f'Load Event {load_event} emitted')
                            elif 'ExposeOn Slice' in log_dict['content']:
                                data = re.findall("\d+", log_dict['content'])
                                if len(data) == 2:
                                    current, total = data[0], data[1]
                                    progress_event = ProgressEvent(gateway_id=self.gateway_id,
                                                                   current=current,
                                                                   total=total)
                                    self.event_bus.emit(progress_event)
                                    self.logger.debug(f'Progress Event {progress_event} emitted')
                            elif 'Build: Pause' in log_dict['content']:
                                status_event = StatusEvent(gateway_id=self.gateway_id,
                                                           status=StatusEventType.IDLE)
                                self.event_bus.emit(status_event)
                            elif 'Finished' in log_dict['content']:
                                status_event = StatusEvent(gateway_id=self.gateway_id,
                                                           status=StatusEventType.IDLE)
                                self.event_bus.emit(status_event)
                                weight_sensor = SensorData(
                                    label='seperation_weight',
                                    sensor_type=SensorTypeEnum.timeseries,
                                    unit='kg',
                                    visualization_type=VisualizationTypeEnum.line,
                                    data=self.seperation_weight
                                )
                                debug_log = LogData(label='Debug Log', log_type=LogTypeEnum.debug,
                                                    data=self.debug_log)
                                build_log = LogData(label='Build Log', log_type=LogTypeEnum.build,
                                                    data=self.get_last_build_log())
                                data_event = EventUploadData(cloud_id=self.cloud_id,
                                                             sensor_data=[weight_sensor],
                                                             log_data=[debug_log, build_log],
                                                             event_type=EventTypeEnum.performed_task)
                                self.event_bus.emit(data_event)

                                self.logger.debug(f'EventUploadData Event {EventUploadData} emitted')
                                self.seperation_weight = {'time': [],
                                                          'values': []}
                                self.debug_log = {'time': [],
                                                  'label': [],
                                                  'content': []}
                        else:
                            self.logger.debug(
                                f'Line does not fit the structure: [time] [label] [content]: {line}')


            except (requests.ConnectionError, requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):
                status_event = StatusEvent(gateway_id=self.gateway_id,
                                           status=StatusEventType.OFFLINE)
                self.event_bus.emit(status_event)
                self.status = StatusEventType.OFFLINE
                time.sleep(10)

            except Exception as e:
                self.logger.error(e)

    def get_last_build_log(self):
        r = requests.get(url=f'http://{self._host_ip}/BuildLog.ini')
        log_stack = []
        for index, line in enumerate(r.iter_lines(delimiter='\n', decode_unicode=True)):
            if '[Build ' in line:
                log_stack = []
            else:
                log_stack.append(line)
        return {'content': log_stack}
