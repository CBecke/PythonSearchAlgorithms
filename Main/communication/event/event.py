
from abc import ABC, abstractmethod

from Main.communication.event.event_type import EventType


class Event(ABC):
    @abstractmethod
    def __init__(self, type: EventType, data):
        self.type = type
        self.data = data

    def get_type(self):
        return self.type

    def get_data(self):
        return self.data
