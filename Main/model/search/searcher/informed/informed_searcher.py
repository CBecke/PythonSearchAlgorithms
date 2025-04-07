from abc import abstractmethod, ABC

from Main.model.search.data_structure.node import Node
from Main.model.search.searcher.algorithm_description import AlgorithmDescription
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
                position = child.state
                if self.should_generate(child, reached, position):
                    generated.add(child)
                    reached[position] = child.path_cost
                    frontier.add(child)

            log.add_generated(generated)
        return log # returns the log even whe the search fails (in which case the tail of log.expanded is not a goal)

    def should_generate(self, child, reached, position):
        return position not in reached or child.path_cost < reached[position]

    @staticmethod
    def expand(problem: SearchProblem, parent: SearchNode):
        s = parent.state
        for action in problem.actions(s):
            resulting_state = problem.result(s, action)
            cost = parent.path_cost + problem.action_cost(s, action)
            yield SearchNode(resulting_state, parent, action, cost)