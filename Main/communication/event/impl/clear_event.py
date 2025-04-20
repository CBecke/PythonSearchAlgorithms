from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class ClearGridEvent(Event):
    def __init__(self):
        super().__init__(EventType.ClearGridPressed, None)