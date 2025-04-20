from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class StateUpdateEvent(Event):
    def __init__(self, data):
        super().__init__(EventType.StateUpdate, data)
