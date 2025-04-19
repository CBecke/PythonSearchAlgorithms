from Main.model.searcher.informed.a_star import AStarSearcher
from Main.model.searcher.informed.best_first_searcher import BestFirstSearcher
from Main.model.searcher.informed.greedy_best_first_searcher import GreedyBestFirstSearcher
from Main.model.searcher.uninformed.breadth_first_searcher import BreadthFirstSearcher
from Main.model.searcher.uninformed.depth_first_searcher import DepthFirstSearcher

algorithms = [BestFirstSearcher(), GreedyBestFirstSearcher(), AStarSearcher(), BreadthFirstSearcher(), DepthFirstSearcher()]

name_to_algorithm = dict()
for algorithm in algorithms:
    name_to_algorithm[algorithm.get_name()] = algorithm