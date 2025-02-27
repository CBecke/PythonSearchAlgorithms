from abc import abstractmethod, ABC

from Main.model.search.searcher.AlgorithmDescription import AlgorithmDescription
from Main.model.search.searcher.logged_searcher import LoggedSearcher
from Main.model.search.searcher.search_log import SearchLog
from Main.model.search.data_structure.node import Node
from Main.model.search.data_structure.priority_queue import PriorityQueue
from Main.model.searchproblem.search_problem import SearchProblem


class InformedSearcher(LoggedSearcher, AlgorithmDescription, ABC):

    @abstractmethod
    def f(self, problem: SearchProblem, current: Node):
        """ The heuristic function of the search """
        pass

    def logged_search(self, problem: SearchProblem, log = None) -> SearchLog:
        log = log or SearchLog()
        position = problem.find_initial_state()
        node = Node(position, None, None, 0)
        frontier = PriorityQueue(problem, self.f)
        frontier.add(node)
        reached = {node.state: node.path_cost}

        while not frontier.is_empty():
            node = frontier.pop()
            log.add_expanded(node)
            if problem.is_goal_state(node.state):
                return log

            for child in self.expand(problem, node):
                s = child.state
                generated = set()
                if s not in reached or child.path_cost < reached[s]:
                    generated.add(child)
                    reached[s] = child.path_cost
                    frontier.add(child)

                log.add_generated(generated)
        return SearchLog() # return an empty log if the search fails

    @staticmethod
    def expand(problem: SearchProblem, node: Node):
        s = node.state
        for action in problem.actions(s):
            resulting_state = problem.result(s, action)
            cost = node.path_cost + problem.action_cost(s, action)
            yield Node(resulting_state, node, action, cost)