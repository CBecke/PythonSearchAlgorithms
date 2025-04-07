from abc import ABC, abstractmethod

from Main.communication.event.event import Event


class Subscriber(ABC):

    @abstractmethod
    def update_subscriber(self, event: Event):
        pass