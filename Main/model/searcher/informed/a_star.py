from Main.model.searcher.informed.informed_searcher import InformedSearcher
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_node import SearchNode
from Main.model.searchproblem.search_problem import SearchProblem

def manhattan_distance(problem: SearchProblem, current: SearchNode):
    minimum_manhattan_dist = 1000000

    for goal in problem.find_goal_states():
        current_manhattan_dist = Position.manhattan_distance(current.state, goal)
        if current_manhattan_dist < minimum_manhattan_dist:
            minimum_manhattan_dist = current_manhattan_dist

    assert minimum_manhattan_dist >= 0, "incorrect manhattan distance"
    return minimum_manhattan_dist

class AStarSearcher(InformedSearcher):
    def __init__(self, heuristic_function=manhattan_distance):
        super().__init__()
        self.heuristic_function = heuristic_function

    def f(self, problem: SearchProblem, current: SearchNode):
        assert current.path_cost >= 0
        return current.path_cost + self.heuristic_function(problem, current)

    def set_heuristic(self, function):
        self.heuristic_function = function

    @staticmethod
    def get_name() -> str:
        return "A*"

    @staticmethod
    def get_description() -> str:
        return ("A* is an informed search algorithm that expanded generated nodes based on an evaluation function " +
                "f(n) = g(n) + h(n), where g(n) is the cost to reach node n, and h(n) is the estimated goal distance " +
                "from n to the nearest goal. The generated node with the lowest f(n) value is expanded next. A* is " +
                "both complete and optimal if the heuristic is admissible.")