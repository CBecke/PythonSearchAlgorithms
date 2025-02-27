from Main.model.search.data_structure.frontier import Frontier
from Main.model.search.data_structure.node import Node


class Queue(Frontier):
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def pop(self):
        if self.is_empty():
            return None

        popped_node = self.head
        self.head = self.head.next
        # when pop is called on a queue with 1 element, both head and tail should be none
        if self.head is None:
            self.tail = None
        popped_node.next = None   # don't save queue info in popped node
        return popped_node

    def top(self):
        return self.head

    def add(self, node: Node):
        node.next = None
        if self.is_empty():
            self.head = node
            self.tail = node
            return self.tail

        self.tail.next = node
        self.tail = node
        return self.tail

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next




