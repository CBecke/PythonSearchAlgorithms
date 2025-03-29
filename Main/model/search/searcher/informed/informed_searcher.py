from abc import abstractmethod, ABC

from Main.model.search.data_structure.node import Node
from Main.model.search.searcher.AlgorithmDescription import AlgorithmDescription
from Main.model.search.searcher.logged_searcher import LoggedSearcher
from Main.model.search.searcher.search_log import SearchLog
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_node import SearchNode
from Main.model.search.data_structure.priority_queue import PriorityQueue
from Main.model.searchproblem.search_problem import SearchProblem


class InformedSearcher(LoggedSearcher, AlgorithmDescription, ABC):

    @abstractmethod
    def f(self, problem: SearchProblem, current: SearchNode):
        """ The heuristic function of the search """
        pass

    def logged_search(self, problem: SearchProblem, log = None) -> SearchLog:
        log = log or SearchLog()
        position = problem.find_initial_state()
        state_node = SearchNode(position, None, None, 0)
        frontier = PriorityQueue(problem, self.f)
        frontier.add(state_node)
        reached = {state_node.state: state_node.path_cost}

        while not frontier.is_empty():
            state_node = frontier.pop()
            log.add_expanded(Node(state_node))
            if problem.is_goal_state(state_node.state):
                return log

            generated = set()
            for child in self.expand(problem, state_node):
                s = child.state
                if s not in reached or child.path_cost < reached[s]:
                    generated.add(Node(child))
                    reached[s] = child.path_cost
                    frontier.add(child)

            log.add_generated(generated)
        return SearchLog() # return an empty log if the search fails

    @staticmethod
    def expand(problem: SearchProblem, node: SearchNode):
        s = node.state
        for action in problem.actions(s):
            resulting_state = problem.result(s, action)
            cost = node.path_cost + problem.action_cost(s, action)
            yield SearchNode(resulting_state, node, action, cost)