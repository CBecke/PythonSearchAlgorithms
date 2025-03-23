from Main.observer_pattern.event.dimension_apply_pressed import DimensionApplyPressedEvent
from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType
from Main.observer_pattern.subscriber import Subscriber


class Controller(Subscriber):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.event_map = {
            EventType.DimensionApplyPressed: self.updateDimensions
        }

    def update_subscriber(self, event: Event):
        self.event_map[event.get_type()](event)

    def updateDimensions(self, event: DimensionApplyPressedEvent):
        representation = event.get_data()
        self.model.get_problem().update_state(representation)
        self.view.update_problem(self.model.get_problem())


