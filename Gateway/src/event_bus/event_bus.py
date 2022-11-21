import asyncio
from collections import defaultdict
import multiprocessing
import threading

from .helper_classes import EventType, MethodCallbackType
from src.util.singleton import *
from ..constants.const import ProcessMode


@Singleton
class EventBus:
    """
    A class to provide a EventBus with multiple Process execution possibilities

    The bus basically keeps track of all registered event subscribers and calls them if an event is emitted on the bus.
    This function call can then be executed as async function, thread or process.

    For aesthetic purposes I want to provide a possibility to subscribe to an event with a python decorator.
    However this raised the problem that a decorator doesn't know its context while it is called.
    Therefore you not only have to decorate the method which should subscribe to an Event
    but also have to register its class on the EventBus.
    This has the advantage that you can have a different Event behaviour in different instances of a class
    (like unsubscribing only one instance).
    """

    def __init__(self):
        # A list of all processes started from this class
        self.processes = []
        # Registry to map Method Callback (containing callback-function and the mode to process it) to Events
        self.__events = defaultdict(list)
        # Registry of all active Interface Objects that can subscribe to Events/ which subscriptions can be triggered
        # gateway_id -> subscriber
        self.__subscribers = {}
        self.__available = {}

    @property
    def available_interfaces(self):
        """
        Property for returning all registered subscribers
        :return: Events and their respective subscribers
        """
        return self.__available

    def introduce(self, interface: object):
        from ..interfaces.abstract_interface import DeviceInterface
        if isinstance(interface, DeviceInterface):
            self.__available[interface.gateway_id] = interface
        else:
            raise Exception('Only DeviceInterfaces should be introduced!')

    def activate(self, gateway_id):
        if gateway_id not in self.__available.keys():
            return None
        else:
            self.__subscribers[gateway_id] = self.__available[gateway_id]
            del self.__available[gateway_id]

            return self.__subscribers[gateway_id]

    @property
    def events(self):
        """
        Property for returning events and their respective subscribers
        :return: Events and their respective subscribers
        """
        return self.__events

    @property
    def subscribers(self):
        """
        Property for returning all registered subscribers
        :return: Events and their respective subscribers
        """
        return self.__subscribers

    @staticmethod
    def test_method_origin(test_object: object, method: callable):
        """
        Tests if the a method belongs to a given object

        The issue with implementing this method was that python objects don't carry a lot of information.
        For example usually a object cannot retrieve its module (folder structure where it was defined).
        But methods and function contain this information.
        Furthermore, objects can retrieve all their attributes (methods and class variables).
        Therefore to test if a method belongs to a object,
        we first try to receive the same method from the object.
        If such a method exist in the object, we compare their origin to check if they are really the same.

        It is farly common to compare only the name in python (for backwards compatibility?)
        since the other attributes have been added in later python 3 versions.
        This felt very error prone.
        Comparing the module and qualifier are very robust indicators of method similarity in my opinion.
        :param test_object: Object which might have implemented the method
        :param method: method we want to test the object on
        :return: True if the method originated from object else False
        """
        name_of_the_known_method = method.__name__
        # get the method of the instance by the name if possible
        object_method = getattr(test_object, name_of_the_known_method, None)

        if not object_method:
            # False if a method with the same name does not exist in the object
            return False

        # Check qualifier which is basically class_name.function_name
        same_qualifier = object_method.__qualname__ == method.__qualname__
        # Check name of module in which their classes were defined like root_name.folder_name.class_name
        same_module = object_method.__module__ == method.__module__
        # Test if it is actually a function.
        is_method = callable(object_method)
        # Assume that they are the same methods thus have the same origin (class) if all checks are passed
        return is_method and same_qualifier and same_module

    def add_event(self, event_name: str, method_callback: MethodCallbackType):
        """
        Method for subscribing a method to an event
        :param event_name: EventClass to subscribe to
        :param method_callback: MethodCallbackClass containing the callback method and its ProcessMode
        """
        self.__events[event_name].append(method_callback)

    def register(self, subscriber: object, gateway_id: str):
        """
        Method to register a class instance to the event bus.

        Only registered objects and its methods will be considered in a Event emission
        :param subscriber: Object which wants to be registered
        :param gateway_id: Gateway ID of the object
        """
        if gateway_id not in self.__subscribers.keys():
            self.__subscribers[gateway_id] = subscriber

    def unregister(self, gateway_id: str):
        """
        Unregisters a registered object from the EventBus if it exist.

        Unregistered objects will not be triggered based on Events anymore.
        :param gateway_id: Gateway ID of the object with which it was registered
        """
        del self.subscribers[gateway_id]

    def emit(self, event: EventType):
        """
        Method for emitting an event.

        Only registered objects and its methods will be considered in a Event emission.
        This method calls a method if it subscribed to the given Event and its object (Interface) is registered

        The method iterates through all registered objects and all methods which subscribed to the given Event
        Each time it tests if a method belongs to a object and trigger them if they match
        :param event: EventClass which represents the Event
        :return: calls a method if the emitted event has a registered subscriber
        """
        event_callbacks = self.__events[event.name]
        if not event_callbacks:
            return None
        # list command needs to make a copy bc the subscriber dict can change during execution
        for subscriber in list(self.__subscribers.values()):
            for callback in event_callbacks:
                if self.test_method_origin(test_object=subscriber, method=callback.method):
                    self.call(process_mode=callback.process_mode,
                              method=callback.method,
                              subscriber=subscriber,
                              event=event)

    def call(self, process_mode: int, method: callable, subscriber: object, event: EventType):
        """
        Calls a method from a given object to be executed in a given process mode

        :param process_mode: ProcessMode Variable representing the mode the method should be executed as
        :param method: method to be triggered
        :param subscriber: object of the method
        :param event: EventClass, the method got called by
        :return: Starts the process
        """
        if process_mode == ProcessMode.CALL:
            method(subscriber, event)
        elif process_mode == ProcessMode.ASYNC:
            asyncio.run(method(subscriber, event))
        elif process_mode == ProcessMode.THREAD:
            t = threading.Thread(target=method, args=(subscriber, event,))
            t.daemon = True
            t.start()
        elif process_mode == ProcessMode.PROCESS:
            p = multiprocessing.Process(target=method, args=(subscriber, event,))
            self.processes.append(p)
            p.start()

    def stop(self):
        """
        Stops all Threads and Background processes which have been started by the EventBus
        """
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        for p in self.processes:
            p.terminate()
            p.join()
