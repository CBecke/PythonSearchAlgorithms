from Main.model.data_structure.queue import Queue
from Main.model.searcher.algorithm_description import AlgorithmDescription
from Main.model.searcher.logged_searcher import LoggedSearcher
from Main.model.searcher.uninformed.uninformed_searcher import UninformedSearcher


class BreadthFirstSearcher(UninformedSearcher, LoggedSearcher, AlgorithmDescription):

    def __init__(self):
        super().__init__(Queue())

    @staticmethod
    def get_name() -> str:
        return "Breadth-First"

    @staticmethod
    def get_description() -> str:
        return ("Breadth-First Search (BFS) is an uninformed search algorithm. It expands generated nodes based on a"
                + "FIFO queue. With uniform cost, it finds optimal solutions. It has a high memory usage however.")
