from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event import EventType


class DimensionApplyPressedEvent(Event):
    def __init__(self, data):
        assert isinstance(data, int)

        super().__init__(EventType.DimensionApplyPressed, data)

