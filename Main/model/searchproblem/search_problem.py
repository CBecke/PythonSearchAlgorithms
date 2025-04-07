
from abc import ABC, abstractmethod

class SearchProblem(ABC):

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
        :return: The numeric cost of applying action a in state_from, resulting in state_to.
        """
        pass

    @abstractmethod
    def find_initial_state(self):
        pass

    @abstractmethod
    def find_goal_states(self):
        pass

    @abstractmethod
    def is_initial_state(self, state):
        pass

    @abstractmethod
    def is_goal_state(self, state):
        pass

    @abstractmethod
    def update_state(self, representation):
        pass

    @abstractmethod
    def get_state(self):
        pass

    def to_array(self):
        pass