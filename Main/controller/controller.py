from Main.model.search.searcher.informed.best_first_Searcher import BestFirstSearcher
from Main.model.view_grid_parsing import parse_view_grid
from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType
from Main.observer_pattern.subscriber import Subscriber


class Controller(Subscriber):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.event_map = {
            EventType.StartPressed: self.startAlgorithm,
        }

    def update_subscriber(self, event: Event):
        self.event_map[event.get_type()](event)

    def startAlgorithm(self, event: Event):
        grid_representation = self.view.get_grid_representation()
        grid_problem_grid = parse_view_grid(grid_representation)
        if not self.model.is_valid_problem(grid_problem_grid):
            return

        self.model.get_problem().update_state(grid_problem_grid)
        searcher = BestFirstSearcher()
        search_log = searcher.logged_search(self.model.get_problem())
        self.view.render_search(search_log)


        self.view.unlock_grid()
        




