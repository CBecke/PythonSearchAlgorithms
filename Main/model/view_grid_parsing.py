from Main.model.searchproblem.position import Position
from Main.model.searchproblem.position_type import PositionType
from Main.view.left_pane.grid.label.impl.agentSquare import AgentSquare
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.impl.expandedSquare import ExpandedSquare
from Main.view.left_pane.grid.label.impl.generatedSquare import GeneratedSquare
from Main.view.left_pane.grid.label.impl.goalSquare import GoalSquare
from Main.view.left_pane.grid.label.impl.wallSquare import WallSquare
from Main.view.left_pane.grid.label.square import Square


def parse_view_grid(view_grid: list[list[Square]]) -> list[list[int]]:

    square_mappings = {
        EmptySquare: PositionType.EMPTY.value,
        WallSquare: PositionType.WALL.value,
        AgentSquare: PositionType.INITIAL.value,
        GoalSquare: PositionType.GOAL.value,
        GeneratedSquare: PositionType.EMPTY.value,
        ExpandedSquare: PositionType.EMPTY.value,
    }
    parsed_grid = []
    for row in view_grid:
        current_row = []
        for square in row:
            current_row.append(square_mappings[square.__class__])
        parsed_grid.append(current_row)

    return parsed_grid
