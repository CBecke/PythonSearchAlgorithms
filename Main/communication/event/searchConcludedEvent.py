from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class SearchConcludedEvent(Event):
    def __init__(self, n_generated):
        super().__init__(EventType.SearchConcluded, n_generated)
