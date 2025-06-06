
from enum import Enum, auto

class EventType(Enum):
    DimensionApplyPressed = auto(),
    RadioToggled = auto(),
    ResetPressed = auto(),
    StartPressed = auto(),
    SearchConcluded = auto(),
    StateUpdate = auto(),
    ClearGridPressed = auto(),
    HeuristicUpdate = auto(),

