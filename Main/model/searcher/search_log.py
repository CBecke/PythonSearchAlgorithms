from copy import deepcopy

from Main.model.data_structure.node import Node
from Main.model.data_structure.queue import Queue

class SearchLog:
    def __init__(self, generated=None, expanded=None):
        self.generated = generated or Queue() # Queue<set<Node>>
        self.expanded = expanded or Queue() # Queue<Node>

    def add_generated(self, nodes_set: set[Node]):
        """ logs a deepcopy of the input collection of nodes """
        self.generated.add(Node(deepcopy(nodes_set)))

    def add_expanded(self, node: Node):
        """ logs a deepcopy of the input node """
        self.expanded.add(deepcopy(node))

    def __iter__(self):
        assert (len(self.generated) == len(self.expanded) or len(self.expanded) - len(self.generated) == 1), "the generated and expanded queues must be equal length, or differ by 1 (for eager goal state test)"
        if len(self.expanded) - len(self.generated) == 1:
            self.generated.add(Node(set()))

        for node_generated, node_expanded in zip(self.generated, self.expanded):
            yield node_generated, node_expanded


    def n_expanded(self):
        return len(self.expanded)

    def n_generated(self):
        count = 0
        current = self.generated.head
        while current is not None:
            count += len(current.value)
            current = current.next

        return count




