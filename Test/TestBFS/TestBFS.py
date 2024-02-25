
import unittest
from Main import LevelParsing
from Main.searchproblem.GridProblem import GridProblem
from Main.algorithms.BFS import BFS


def isPath(solution):
    return False


class TestBFS(unittest.TestCase):
    def test_single_goal(self):
        # given a grid problem
        grid = LevelParsing.parse_rectangle(r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\simple_open.txt")
        gridProblem = GridProblem(grid)

        # when breadth-first search is run
        (solution, n_generated) = BFS(gridProblem)

        # then a path from the initial state to the goal state is output
        self.assertGreater(len(solution), 0)
        self.assertTrue(isPath(solution))
        self.assertTrue(gridProblem.isInitialPosition(solution[0]))
        self.assertTrue(gridProblem.isGoal(solution[-1]))
        self.assertGreaterEqual(n_generated, len(solution))