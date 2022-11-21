"""
This file contains all Event implementations which are used by the system lifecycle.
Read more about the Lifecycle in the README.
"""

from src.event_bus.helper_classes import Event


class EventBeforeLoad(Event):
    """
    This Event is emitted once the System has started the EventBus.
    """

    def __init__(self):
        super().__init__(name='EventBeforeLoad')


class EventLoaded(Event):
    """
    This Event is emitted after the system has successfully loaded the config.
    """

    def __init__(self):
        super().__init__(name='EventLoaded')


class EventSetupError(Event):
    """
    This Event is emitted if the loading of the System throws an Error.
    """

    def __init__(self):
        super().__init__(name='EventSetupError')


class EventSetupRetry(Event):
    """
    This Event is before the System retries to load the config.
    """

    def __init__(self):
        super().__init__(name='EventSetupRetry')


class EventStart(Event):
    """
    This Event is emitted to start all background processes.
    """

    def __init__(self):
        super().__init__(name='EventStart')


class EventBeforeStop(Event):
    """
    This Event is emitted before the system is stopped to stop all Integrations.
    """

    def __init__(self):
        super().__init__(name='EventBeforeStop')


class EventStop(Event):
    """
    This Event is emitted before the main process is killed.
    """

    def __init__(self):
        super().__init__(name='EventStop')
