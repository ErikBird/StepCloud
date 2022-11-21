from src.constants.const import ProcessMode
from src.event_bus.decorator import subscribe
from src.interfaces.abstract_interface import EngineInterface
from src.interfaces.core_interfaces.clock import EventTimeChanged
from src.util.logger import get_logger_system


class Secretary(EngineInterface):

    def __init__(self, name):
        super().__init__(name)
        self.logger = get_logger_system("Secretary")

    @subscribe(on_event=EventTimeChanged, process_mode=ProcessMode.ASYNC)
    async def subscriber(self, event: EventTimeChanged):
        """
        Example Event! This is probably not useful
        Records all TIME_CHANGED events with its corresponding time into the event-log.
        :param event: time of the event
        :return: Writes into the event log
        """
        self.logger.debug('Events.TIME_CHANGED: %s' % str(event.get_time()))
