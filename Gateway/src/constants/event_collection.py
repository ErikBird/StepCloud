from src.event_bus.helper_classes import Event


class StartInterfaceEvent(Event):
    """
    This Event is emitted once the System has started the EventBus.
    """

    def __init__(self, gateway_id: str):
        super().__init__(name='StartInterfaceEvent')
        self.gateway_id = gateway_id

    def __str__(self):
        return self.name + ' starts interface with gateway id: ' + str(self.gateway_id)
