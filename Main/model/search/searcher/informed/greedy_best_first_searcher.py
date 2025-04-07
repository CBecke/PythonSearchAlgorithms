from Main.model.search.searcher.informed.best_first_searcher import BestFirstSearcher
from Main.model.searchproblem.search_node import SearchNode
from Main.model.search.searcher.informed.informed_searcher import InformedSearcher
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_problem import SearchProblem


class GreedyBestFirstSearcher(BestFirstSearcher):

    def f(self, problem: SearchProblem, current: SearchNode):
        minimum_manhattan_dist = 1000000

        for goal in problem.find_goal_states():
            current_manhattan_dist = Position.manhattan_distance(current.state, goal)
            if current_manhattan_dist < minimum_manhattan_dist:
                minimum_manhattan_dist = current_manhattan_dist

        assert minimum_manhattan_dist >= 0, "incorrect manhattan distance"
        return minimum_manhattan_dist


    @staticmethod
    def get_name():
        return "Greedy Best-First Search"

    @staticmethod
    def get_description():
        return "Greedy Best-first search is an informed search algorithm. It expands generated nodes based on an evaluation function f(n). The generated node n with the lowest f(n) value is expanded next. In this implementation, f(n) is the wall-agnostic Manhattan distance from n to the nearest goal. "

    def should_generate(self, child, reached, position):
        return position not in reached