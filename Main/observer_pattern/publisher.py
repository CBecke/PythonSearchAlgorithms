from abc import ABC, abstractmethod

class Publisher():
    def __init__(self, listeners=None):
        self.listeners = listeners if listeners is not None else dict()

    def subscribe(self, subscriber):
        self.listeners.add(subscriber)

    def unsubscribe(self, subscriber):
        self.listeners.remove(subscriber)

    def notify(self, event_type, data):
        for listener in self.listeners[event_type]:
            listener.update(data)





