from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class HeuristicUpdateEvent(Event):
    # heuristic function is a lambda / mapping function
    def __init__(self, heuristic_function):
        super().__init__(EventType.HeuristicUpdate, heuristic_function)