from Main.model.searchproblem.search_problem import SearchProblem


class Model:
    def __init__(self, problem: SearchProblem):
        self.problem = problem

    def get_problem(self) -> SearchProblem:
        return self.problem

    def is_valid_problem(self, grid_problem_grid):
        # TODO: complete. Should actually probably be a static method in search_problem (and then implemented in grid_problem)
        # problem should have exactly one agent and at least one goal
        return True