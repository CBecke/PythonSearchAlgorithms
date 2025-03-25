import sys

from PyQt6.QtWidgets import QApplication

from Main.controller.controller import Controller
from Main.model.model import Model
from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position_type import PositionType
from Main.observer_pattern.event.dimension_apply_pressed import DimensionApplyPressedEvent
from Main.observer_pattern.event.event_type import EventType
from Main.observer_pattern.publisher import Publisher
from Main.view.search_window import SearchWindow


def main():

    state = [[PositionType.EMPTY for _ in range(10)] for _ in range(10)]
    problem = GridProblem(state)

    publisher = Publisher()

    app = QApplication([])
    view = SearchWindow(publisher, problem.get_state())
    view.show()
    model = Model(problem)
    controller = Controller(model, view)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()