from abc import abstractmethod
from Main.model.searchproblem.search_node import SearchNode


class Frontier:

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def top(self):
        pass

    @abstractmethod
    def add(self, node: SearchNode):
        pass

    @abstractmethod
    def clear(self):
        pass