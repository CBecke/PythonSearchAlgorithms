from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class ResetPressedEvent(Event):
    def __init__(self):
        super().__init__(EventType.ResetPressed, None)