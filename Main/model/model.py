from Main.model.searchproblem.position_type import PositionType
from Main.model.searchproblem.search_problem import SearchProblem


class Model:
    def __init__(self, problem: SearchProblem):
        self.problem = problem

    def get_problem(self) -> SearchProblem:
        return self.problem

    def is_valid_problem(self, grid_problem_grid):
        agent_count = 0
        for row in range(len(grid_problem_grid)):
            for col in range(len(grid_problem_grid[row])):
                if grid_problem_grid[row][col] == PositionType.INITIAL.value:
                    agent_count += 1

        return agent_count == 1