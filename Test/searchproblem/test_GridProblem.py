from Main import LevelParsing
from Main.PositionType import PositionType
from Main.searchproblem.GridProblem import GridProblem, Action
from Main.searchproblem.Position import Position


def test_actions_open():
    file_location = r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\open_3x3.txt"
    grid = LevelParsing.parse_rectangle(file_location)
    grid_problem = GridProblem(grid)

    topleft = Position(0, 0)
    bottomright = Position(2, 2)
    middle = Position(1, 1)

    assert grid_problem.actions(topleft) == {Action.DOWN, Action.RIGHT}
    assert grid_problem.actions(bottomright) == {Action.LEFT, Action.UP}
    assert grid_problem.actions(middle) == {Action.DOWN, Action.RIGHT, Action.LEFT, Action.UP}


def test_actions_closed():
    file_location = r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\closed_unsolvable.txt"
    grid = LevelParsing.parse_rectangle(file_location)
    grid_problem = GridProblem(grid)

    assert len(grid_problem.actions(grid_problem.initial_state)) == 0


def test_result():
    state = Position(1,1)
    file_location = r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\open_3x3.txt"
    grid = LevelParsing.parse_rectangle(file_location)
    grid_problem = GridProblem(grid)

    assert grid_problem.result(state, Action.UP) == Position(0,1)
    assert grid_problem.result(state, Action.DOWN) == Position(2,1)
    assert grid_problem.result(state, Action.LEFT) == Position(1,0)
    assert grid_problem.result(state, Action.RIGHT) == Position(1,2)

def test_find_goal_states():
    file_location = r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\simple_open_3agents.txt"
    grid = LevelParsing.parse_rectangle(file_location)
    grid_problem = GridProblem(grid)

    goal_states = grid_problem.find_goal_states()
    assert len(goal_states) == 3
    for state in goal_states:
        assert grid_problem.get(state) == PositionType.GOAL.value