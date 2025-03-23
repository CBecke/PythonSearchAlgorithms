from Main.model.searchproblem.search_problem import SearchProblem


class Model:
    def __init__(self, problem: SearchProblem):
        self.problem = problem

    def get_problem(self) -> SearchProblem:
        return self.problem