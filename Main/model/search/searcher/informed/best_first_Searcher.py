from Main.model.search.data_structure.node import Node
from Main.model.search.searcher.informed.informed_searcher import InformedSearcher
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_problem import SearchProblem


class BestFirstSearcher(InformedSearcher):

    def f(self, problem: SearchProblem, current: Node):
        minimum_manhattan_dist = 1000000

        for goal in problem.find_goal_states():
            current_manhattan_dist = Position.manhattan_distance(current.state, goal)
            if current_manhattan_dist < minimum_manhattan_dist:
                minimum_manhattan_dist = current_manhattan_dist

        assert minimum_manhattan_dist != 1000000, "No goals in problem"
        assert minimum_manhattan_dist >= 0, "incorrect manhattan distance"
        return minimum_manhattan_dist



    @staticmethod
    def get_name():
        return "Best-First Search"

    @staticmethod
    def get_description():
        return "Best-first search is an informed search algorithm which, which greedily expanding the generated node with minimum value of the evaluation function f(n). In this case, f(n) is Manhattan distance from n to the nearest goal."