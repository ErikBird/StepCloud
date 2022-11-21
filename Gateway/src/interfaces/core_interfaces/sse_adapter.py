import json
import queue
from src.constants.const import ProcessMode, StatusEventType, SSEEventType
from src.event_bus.decorator import subscribe
from src.event_bus.helper_classes import Event
from src.interfaces.abstract_interface import SystemInterface
from src.util.singleton import Singleton


class StatusEvent(Event):
    def __init__(self, gateway_id, status: StatusEventType):
        super().__init__(name='StatusEvent')
        self.typ = SSEEventType.STATUS
        self.data = status
        self.gateway_id = gateway_id

    @property
    def json(self):
        return json.dumps({'gateway_id': self.gateway_id, 'typ': self.typ, 'data': self.data})

    def __str__(self):
        return self.typ + ' with data ' + str(self.data)


class ProgressEvent(Event):
    def __init__(self, gateway_id, current: int, total: int):
        super().__init__(name='ProgressEvent')
        self.typ = SSEEventType.PROGRESS
        self.data = {'current': current, 'total': total}
        self.gateway_id = gateway_id

    @property
    def json(self):
        return json.dumps({'gateway_id': self.gateway_id, 'typ': self.typ, 'data': self.data})

    def __str__(self):
        return self.typ + ' with data ' + str(self.data)


class LoadEvent(Event):
    def __init__(self, gateway_id, load: float):
        super().__init__(name='ProgressEvent')
        self.typ = SSEEventType.LOAD
        self.data = load
        self.gateway_id = gateway_id

    @property
    def json(self):
        return json.dumps({'gateway_id': self.gateway_id, 'typ': self.typ, 'data': self.data})

    def __str__(self):
        return self.typ + ' with data ' + str(self.data)


@Singleton
class EventQueue:
    """
    """

    def __init__(self):
        self.q = queue.Queue()

    def add(self, data: str):
        self.q.put(data)

    def stream(self):
        while True:
            yield self.q.get()


class EventStreamAdapter(SystemInterface):
    """

    """

    def __init__(self):
        super().__init__('EventStreamAdapter')
        self.event_queue = EventQueue.instance()

    @subscribe(process_mode=ProcessMode.CALL, on_event=[StatusEvent, ProgressEvent, LoadEvent])
    def send_messages(self, event):
        self.event_queue.add(event.json)
