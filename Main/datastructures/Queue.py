from Main.datastructures.Node import Node


class Queue:
    def __init__(self, elements=None):
        """
        :param items: a list of items to be inserted. The first item will be put at the front of the queue and hence
        be popped first.
        """
        if elements is None:
            elements = []

        self.size = 0
        self.head = None
        self.tail = None
        for element in elements:
            self.push(element)

    def push(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            self.tail.previous = new_node
            new_node.next = self.tail
        self.tail = new_node
        self.size += 1

    def pop(self):
        if self.head is None:
            return None

        value = self.head.value
        self.head = self.head.previous
        self.size -= 1
        return value

    def is_empty(self):
        return self.size == 0
