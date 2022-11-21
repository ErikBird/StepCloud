from typing import Callable, TypeVar


class Event:
    name = None

    def __init__(self, name):
        self.name = name


class MethodCallback:
    method: Callable = None
    process_mode: int = None

    def __str__(self):
        return str(self.method) + str(self.process_mode)

    def __init__(self, function: Callable, process_mode: int):
        self.method = function
        self.process_mode = process_mode


EventType = TypeVar("EventType", bound=Event)
MethodCallbackType = TypeVar("MethodCallbackType", bound=MethodCallback)
