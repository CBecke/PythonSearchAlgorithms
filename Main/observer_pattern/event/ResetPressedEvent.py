from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType


class ResetPressedEvent(Event):
    def __init__(self):
        super().__init__(EventType.ResetPressed, None)