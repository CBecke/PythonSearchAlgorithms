from Main.model.searcher.informed.impl.a_star import AStarSearcher
from Main.model.searcher.informed.impl.best_first_searcher import BestFirstSearcher
from Main.model.searcher.informed.impl.greedy_best_first_searcher import GreedyBestFirstSearcher
from Main.model.searcher.uninformed.impl.breadth_first_searcher import BreadthFirstSearcher
from Main.model.searcher.uninformed.impl.depth_first_searcher import DepthFirstSearcher

algorithms = [BestFirstSearcher(), GreedyBestFirstSearcher(), AStarSearcher(), BreadthFirstSearcher(), DepthFirstSearcher()]

name_to_algorithm = dict()
for algorithm in algorithms:
    name_to_algorithm[algorithm.get_name()] = algorithm