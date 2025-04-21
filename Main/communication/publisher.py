
from Main.communication.event.event import Event


class Publisher:
    def __init__(self, listeners=None):
        # listeners is a hashmap from event_type to a set of subscribers
        self.listeners = listeners if listeners is not None else dict()

    def subscribe(self, event_type, subscriber):
        if event_type not in self.listeners:
            self.listeners[event_type] = set()
        self.listeners[event_type].add(subscriber)

    def unsubscribe(self, event_type, subscriber):
        assert subscriber in self.listeners[event_type], "Tried to remove non-existent subscriber"
        self.listeners[event_type].remove(subscriber)

    def notify(self, event: Event):
        for listener in self.listeners[event.get_type()]:
            listener.update_subscriber(event)





