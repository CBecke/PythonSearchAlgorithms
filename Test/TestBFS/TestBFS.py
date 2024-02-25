import unittest
from Main import LevelParsing
from Main.searchproblem.GridProblem import GridProblem
from Main.algorithms.BFS import BFS
from Main.searchproblem.Position import Position


def isPath(grid_problem, solution):
    for i in range(len(solution)-1):
        current = solution[i]
        next = solution[i+1]
        if (Position.manhattan_distance(current, next) != 1 or grid_problem.is_wall(current)):
            return False

    # test last item
    return not grid_problem.is_wall(solution[-1])



def test_single_goal():
    # given a grid problem
    grid = LevelParsing.parse_rectangle(
        r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\simple_open.txt")
    grid_problem = GridProblem(grid)

    # when breadth-first search is run
    solution = BFS(grid_problem)

    # then a path from the initial state to the goal state is output
    assert len(solution) > 0
    assert isPath(grid_problem, solution)  # TODO: make sure it does not contain walls
    assert grid_problem.is_initial_state(solution[0])
    assert grid_problem.is_goal_state(solution[-1])
    #assert n_generated >= len(solution)
