from abc import abstractmethod
from Main.search.data_structure.node import Node


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
    def add(self, node: Node):
        pass