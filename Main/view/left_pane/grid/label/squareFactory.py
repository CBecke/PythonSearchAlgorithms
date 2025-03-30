from Main.view.left_pane.grid.label.impl.agentSquare import AgentSquare
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.impl.expandedSquare import ExpandedSquare
from Main.view.left_pane.grid.label.impl.generatedSquare import GeneratedSquare
from Main.view.left_pane.grid.label.impl.goalSquare import GoalSquare
from Main.view.left_pane.grid.label.impl.wallSquare import WallSquare


class SquareFactory:

    def make(string, squareSize):
        match string:
            case "agent":
                return AgentSquare(squareSize)
            case "goal":
                return GoalSquare(squareSize)
            case "wall":
                return WallSquare(squareSize)
            case "empty":
                return EmptySquare(squareSize)
            case "generated":
                return GeneratedSquare(squareSize)
            case "expanded":
                return ExpandedSquare(squareSize)
            case _:
                raise ValueError
                