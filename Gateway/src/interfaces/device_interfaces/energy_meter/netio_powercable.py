import time

import requests

from src.constants.const import InterfaceName, SupportedDevice, ProcessMode, StatusEventType, EventTypeEnum
from src.constants.event_collection import StartInterfaceEvent
from src.constants.lifecycle_events import EventStart
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import DeviceInterface
from src.interfaces.core_interfaces.cloud_adapter import EventUploadData
from src.interfaces.core_interfaces.sse_adapter import LoadEvent, StatusEvent
from src.sqlmodels import SensorData, SensorTypeEnum, VisualizationTypeEnum


class NetioPowerCableInterface(DeviceInterface):

    @classmethod
    def init_by_ip(cls, host_ip):
        try:
            r = requests.get(url=f'http://{host_ip}/netio.json')
            mac = r.json()['Agent']['MAC']
            devicename = r.json()['Agent']['DeviceName']
            return cls(gateway_id=mac,  # unique id
                       label=devicename,  # ui name
                       host_ip=host_ip)
        except:
            return None

    def __init__(self, gateway_id: str, label: str, host_ip: str, cloud_id: int = None,
                 device_type: SupportedDevice | None = None):
        super().__init__(gateway_id=gateway_id, label=label,
                         host_ip=host_ip, device_type=device_type,
                         cloud_id=cloud_id)
        self.data = {'time': [],
                     'values': []}
        self.status = StatusEventType.ONLINE

    @property
    def supported_devices(self):
        return [SupportedDevice.NKOptikOtoflashG171, SupportedDevice.Emmi30HC]

    @subscribe(process_mode=ProcessMode.THREAD, on_event=StartInterfaceEvent)
    def start(self, event: StartInterfaceEvent):
        if event.gateway_id == self.gateway_id:
            self.run(event=event)

    @subscribe(process_mode=ProcessMode.THREAD, on_event=EventStart)
    def run(self, event):
        self.logger.info(f'{self.gateway_id} started')
        while True:
            try:
                r = requests.get(url=f'http://{self.host_ip}/netio.json')
                current = r.json()['Outputs'][0]['Current']
                if current > 0:
                    self.data['values'].append(current)
                    self.data['time'].append(current)
                    self.status = StatusEventType.ONLINE
                    load_event = LoadEvent(gateway_id=self.gateway_id, load=current)
                    self.event_bus.emit(load_event)
                    self.logger.debug(f'Load Event {load_event} emitted')
                elif len(self.data['values']) > 0:
                    current_sensor = SensorData(
                        label='current',
                        sensor_type=SensorTypeEnum.timeseries,
                        visualization_type=VisualizationTypeEnum.line,
                        data=self.data
                    )
                    data_event = EventUploadData(cloud_id=self.cloud_id,
                                                 sensor_data=[current_sensor],
                                                 event_type=EventTypeEnum.performed_task)
                    self.event_bus.emit(data_event)
                    status_event = StatusEvent(gateway_id=self.gateway_id,
                                               status=StatusEventType.IDLE)
                    self.event_bus.emit(status_event)
                    self.status = StatusEventType.IDLE
                    self.data = {'time': [],
                                 'values': []}
                time.sleep(5)
            except (requests.ConnectionError, requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):
                status_event = StatusEvent(gateway_id=self.gateway_id,
                                           status=StatusEventType.OFFLINE)
                self.event_bus.emit(status_event)
                self.status = StatusEventType.OFFLINE
            except Exception as e:
                self.logger.error(e)
