from Main.model.level_parsing import parse_rectangle
from Main.model.searchproblem.position_type import PositionType
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_problem import SearchProblem

from enum import Enum, auto


# Put here instead of inside GridProblem to avoid writing "GridProblem.[...]" every time
class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class GridProblem(SearchProblem):
    """
    Defines a 2d grid problem where the state is represented by the (row, col)-position of the agent. (0,0) is the top
    left position [note that the encapsulating wall in the txt input is not part of the grid]. (0,1) is thus the
    1st (top) row and 2nd column from the left.
    """

    def __init__(self, grid):
        self.grid = grid
        self.initial_state = self.find_initial_state()
        self.goal_states = self.find_goal_states()

        self.action_mapping = {
            Action.UP: lambda state: Position(state.row - 1, state.column),
            Action.DOWN: lambda state: Position(state.row + 1, state.column),
            Action.LEFT: lambda state: Position(state.row, state.column - 1),
            Action.RIGHT: lambda state: Position(state.row, state.column + 1)
        }

    def get_state(self):
        return self.grid

    def actions(self, state):
        """
        :return: The set of actions which leave the agent within the bounds of the grid
        """
        actions = set()
        if state.column < len(self.grid[state.row]) - 1 and not self.is_wall(self.result(state, Action.RIGHT)):
            actions.add(Action.RIGHT)
        if state.row > 0 and not self.is_wall(self.result(state, Action.UP)):
            actions.add(Action.UP)
        if state.row < len(self.grid) - 1 and not self.is_wall(self.result(state, Action.DOWN)):
            actions.add(Action.DOWN)
        if state.column > 0 and not self.is_wall(self.result(state, Action.LEFT)):
            actions.add(Action.LEFT)
        return actions

    def result(self, state, action):
        return self.action_mapping[action](state)

    def action_cost(self, state_from, action):
        return 1

    def is_initial_state(self, state):
        return state is not None and self.initial_state == state

    def is_goal_state(self, state):
        return state in self.goal_states

    def get(self, state):
        return self.grid[state.row][state.column]

    def is_wall(self, state):
        return self.get(state) == PositionType.WALL.value

    def find_initial_state(self):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.get(Position(row, column)) == PositionType.INITIAL.value:
                    return Position(row, column)

    def find_goal_states(self):
        goals = set()
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.get(Position(row, column)) == PositionType.GOAL.value:
                    goals.add(Position(row, column))
        return goals

    def update_state(self, representation):
        """ accepts either a string which can be parsed into a grid, or an int representing the number of squares per
            axis"""
        if isinstance(representation, int):
            self.grid = [[PositionType.EMPTY for col in range(representation)] for row in range(representation)]
        elif isinstance(representation, str):
            self.grid = parse_rectangle(representation)

        # given the "actual" grid problem: list[list[PositionType.value:int]]. Must be non-empty.
        elif isinstance(representation, list) and isinstance(representation[0], list) and isinstance(representation[0][0], int):
            self.grid = representation
        else:
            raise ValueError("invalid input type")
        return self.grid


