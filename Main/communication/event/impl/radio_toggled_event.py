from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class RadioToggledEvent(Event):
    def __init__(self, data):
        assert isinstance(data, str)
        data = data.lower()
        assert data in ['agent', 'wall', 'goal', 'empty']
        super().__init__(EventType.RadioToggled, data)