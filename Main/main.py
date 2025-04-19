import sys

from PyQt6.QtWidgets import QApplication

from Main.controller.controller import Controller
from Main.model.model import Model
from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position_type import PositionType
from Main.communication.event.event_type import EventType
from Main.communication.publisher import Publisher
from Main.view.search_window import SearchWindow


def main():
    publisher = Publisher()

    grid_length = 3
    state = [[PositionType.EMPTY for _ in range(grid_length)] for _ in range(grid_length)]
    problem = GridProblem(state, publisher)

    app = QApplication([])
    view = SearchWindow(publisher, problem.get_state())
    view.show()
    model = Model(problem)
    controller = Controller(model, view, publisher)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()