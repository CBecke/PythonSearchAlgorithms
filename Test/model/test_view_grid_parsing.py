import sys

from PyQt6.QtWidgets import QApplication

from Main.model import level_parsing
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.position_type import PositionType
from Main.model.view_grid_parsing import parse_view_grid
from Main.view.left_pane.grid.label.impl.agentSquare import AgentSquare
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.impl.goalSquare import GoalSquare
from Main.view.left_pane.grid.label.impl.wallSquare import WallSquare


def test_compound():
    app = QApplication(sys.argv)  # Initialize the PyQt application
    goal = GoalSquare(123)
    agent = AgentSquare(123)
    empty = EmptySquare(123)
    wall = WallSquare(123)
    view_grid = [[goal, agent],
                 [empty, wall]]

    output = parse_view_grid(view_grid)
    expected = [[PositionType.GOAL, PositionType.INITIAL],
                [PositionType.EMPTY, PositionType.WALL]]

    assert output == expected

    app.quit()

