from abc import ABC, abstractmethod

from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType


class Publisher():
    def __init__(self, listeners=None):
        # listeners is a hashmap from event_type to a set of subscribers
        self.listeners = listeners if listeners is not None else dict()

    def subscribe(self, event_type, subscriber):
        if event_type not in self.listeners:
            self.listeners[event_type] = set()
        self.listeners[event_type].add(subscriber)

    def unsubscribe(self, event_type, subscriber):
        self.listeners[event_type].remove(subscriber)

    def notify(self, event_type: EventType, event: Event):
        for listener in self.listeners[event_type]:
            listener.update_subscriber(event)





