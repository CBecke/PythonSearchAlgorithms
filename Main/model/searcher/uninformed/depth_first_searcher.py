from Main.model.data_structure.stack import Stack
from Main.model.searcher.algorithm_description import AlgorithmDescription
from Main.model.searcher.logged_searcher import LoggedSearcher
from Main.model.searcher.uninformed.uninformed_searcher import UninformedSearcher


class DepthFirstSearcher(UninformedSearcher, LoggedSearcher, AlgorithmDescription):
    def __init__(self):
        super().__init__(Stack())

    @staticmethod
    def get_name() -> str:
        return "Depth-First"

    @staticmethod
    def get_description() -> str:
        return ("Depth-first search (DFS) is an uninformed search algorithm. It expands generated nodes based on a "
                + "LIFO queue (stack). It is not guaranteed to find optimal solutions, but it uses far less memory "
                + "than BFS. Whereas DFS is often implemented as a tree-search, meaning it does not keep track of cycles "
                + ", this implementation does use a \"reached\" set to avoid cycles. It is thereby complete on finite"
                +  "search problems.")