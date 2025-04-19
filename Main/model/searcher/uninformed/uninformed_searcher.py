from abc import ABC, abstractmethod

from Main.model.data_structure.node import Node
from Main.model.searcher.algorithm_description import AlgorithmDescription
from Main.model.searcher.logged_searcher import LoggedSearcher
from Main.model.searcher.search_log import SearchLog
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_node import SearchNode
from Main.model.searchproblem.search_problem import SearchProblem


class UninformedSearcher(LoggedSearcher, AlgorithmDescription, ABC):

    @abstractmethod
    def __init__(self, frontier):
        self.frontier = frontier


    def logged_search(self, problem: SearchProblem, log=None) -> SearchLog:
        log = log or SearchLog()
        initial_position = problem.find_initial_state()
        self.frontier.clear()
        self.frontier.add(Node(initial_position))
        reached = {initial_position}
        while not self.frontier.is_empty():
            position = self.frontier.pop().value
            log.add_expanded(Node(SearchNode(position, None, None, 1)))

            generated = set()
            for child_position in self.expand(problem, position):
                if problem.is_goal_state(child_position):
                    return log

                if child_position not in reached:
                    reached.add(child_position)
                    self.frontier.add(Node(child_position))
                    generated.add(SearchNode(child_position, position, None,
                                             1))  # abusing that it's a GridProblem where all actions have cost = 1.

            log.add_generated(generated)

        return log  # no solution was found

    @staticmethod
    def expand(problem: SearchProblem, state_from: Position):
        for action in problem.actions(state_from):
            yield problem.result(state_from, action)
