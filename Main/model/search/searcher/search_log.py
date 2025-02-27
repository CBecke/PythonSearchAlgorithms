from copy import deepcopy
from Main.model.search.data_structure.queue import Queue

class SearchLog:
    def __init__(self, generated=None, expanded=None):
        self.generated = generated or Queue() # Queue<set<Node>>
        self.expanded = expanded or Queue() # Queue<Node>

    def add_generated(self, nodes):
        """ logs a deepcopy of the input collection of nodes """
        self.generated.put(deepcopy(nodes))

    def add_expanded(self, node):
        """ logs a deepcopy of the input node """
        self.expanded.put(deepcopy(node))

    def __iter__(self):
        for gen, exp in zip(self.generated, self.expanded):
            yield gen, exp

