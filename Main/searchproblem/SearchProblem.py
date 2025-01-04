
from abc import ABC, abstractmethod

class SearchProblem(ABC):
    def __init__(self):
        self.initial_state = None
        self.goal_states = []
        self.solution = []

    @abstractmethod
    def actions(self, state):
        """
        :return: a set of actions that can be executed in state, namely the actions applicable
        in the state.
        """
        pass

    @abstractmethod
    def result(self, state, action):
        """
        :return: The state that results from doing action a in state s if a is applicable in s,
        and None otherwise.
        """
        pass

    @abstractmethod
    def action_cost(self, state_from, action):
        """
        :return: The numeric cost of applying action a in stateFrom to reach stateTo.
        """

    @abstractmethod
    def find_initial_state(self):
        pass

    @abstractmethod
    def find_goal_states(self):
        pass

    def is_initial_state(self, state):
        return state is not None and self.initial_state == state

    def is_goal_state(self, state):
        return state in self.goal_states

