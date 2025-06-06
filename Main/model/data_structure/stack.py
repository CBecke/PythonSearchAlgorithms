from Main.model.data_structure.frontier import Frontier
from Main.model.searchproblem.search_node import SearchNode


class Stack(Frontier):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def pop(self):
        if self.is_empty():
            return None
        popped_node = self.head
        self.head = self.head.next
        popped_node.next = None # don't save stack info in popped node
        return popped_node

    def top(self):
        return self.head

    def add(self, node: SearchNode):
        if self.is_empty():
            node.next = None
        else:
            node.next = self.head
        self.head = node
        return self.head

    def clear(self):
        while not self.is_empty():
            self.pop()