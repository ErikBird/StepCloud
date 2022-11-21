import functools
from .helper_classes import MethodCallback, Event
from typing import Type
from ..constants.const import ProcessMode
from .event_bus import EventBus


def subscribe(on_event: Type[Event] | list[Type[Event]], process_mode: int = ProcessMode.ASYNC):
    """
    This decorator subscribes the decorated method to the given Event on the EventBus

    The decorator (all methods around the wrapper) are executed once the object is instantiated somewhere in the code.
    This makes the decorator approach very convenient since we never have to explicitly call to subscribe the method
    :param on_event: EventClass of the Event
    :param process_mode: ProcessMode Variable of the desired method execution mode
    :return: Decorated method
    """
    bus_instance = EventBus.instance()

    def real_decorator(function):
        if isinstance(on_event, list):
            for event in on_event:
                bus_instance.add_event(event_name=event.__name__,
                                       method_callback=MethodCallback(function=function, process_mode=process_mode))
        else:
            bus_instance.add_event(event_name=on_event.__name__,
                                   method_callback=MethodCallback(function=function, process_mode=process_mode))

        # The function @functools.wraps(function) helps to identify the decorated function at runtime
        # Without the decorator, the __name__ attribute shows only the wrapper and not the real function
        # With the decorator, we can identify the function at runtime as the original function
        # This is used in the event_bus to identify if methods are the same
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            return function(self, *args, **kwargs)

        return wrapper

    return real_decorator
