from datetime import datetime
import time
from src.constants.const import System, ProcessMode
from src.event_bus.helper_classes import Event
from src.event_bus.decorator import subscribe
from src.constants.lifecycle_events import EventStart
from src.interfaces.abstract_interface import SystemInterface


class EventTimeChanged(Event):
    """
    This Event is emitted every CLOCK_TIMER_INTERVAL Seconds.
    It always carries the time of emission. This gives Interfaces the possibility to fire on a desired time.
    """

    def __init__(self):
        super().__init__(name='EventTimeChanged')
        self.time = datetime.now()

    def __str__(self):
        return self.name + ' at ' + str(self.time)

    def get_time(self):
        return self.time


class Clock(SystemInterface):
    """
    The Clock is an Interface which emits an Event every couple of seconds.
    """

    def __init__(self):
        super().__init__('Clock')

    @subscribe(process_mode=ProcessMode.THREAD, on_event=EventStart)
    def run(self, event):
        """
        The Process emits the EventTimeChanged every TIMER_INTERVAL Seconds
        """
        self.logger.debug('Clock Started')
        while True:
            # check every second if a Event should be emitted
            while True:
                time.sleep(1)
                if self._stop or datetime.now().second % System.CLOCK_TIMER_INTERVAL == 0:
                    break
            # Stop infinite loop if Thread should stop
            if self._stop:
                break
            event_now = EventTimeChanged()
            self.event_bus.emit(event=event_now)
