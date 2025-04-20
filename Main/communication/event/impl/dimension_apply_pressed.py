from Main.communication.event.event import Event
from Main.communication.event.event import EventType


class DimensionApplyPressedEvent(Event):
    def __init__(self, data):
        assert isinstance(data, int)

        super().__init__(EventType.DimensionApplyPressed, data)

