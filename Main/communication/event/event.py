
from abc import ABC, abstractmethod

from Main.communication.event.event_type import EventType


class Event(ABC):
    @abstractmethod
    def __init__(self, event_type: EventType, data):
        self.event_type = event_type
        self.data = data

    def get_type(self):
        return self.event_type

    def get_data(self):
        return self.data
