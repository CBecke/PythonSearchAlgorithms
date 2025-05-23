from Main.model.view_grid_parsing import parse_view_grid
from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class Controller:
    def __init__(self, model, view, publisher):
        self.model = model
        self.view = view
        self.publisher = publisher
        publisher.subscribe(EventType.StartPressed, self)
        publisher.subscribe(EventType.StateUpdate, self)

        self.event_map = {
            EventType.StartPressed: self.start_algorithm,
            EventType.StateUpdate: self.forward_state_update
        }

    def update_subscriber(self, event: Event):
        if event.get_type() == EventType.StartPressed:
            self.start_algorithm()
        elif event.get_type() == EventType.StateUpdate:
            self.forward_state_update(event)
        else:
            raise Exception("Invalid event type")


    def start_algorithm(self):
        """ Fetches the view's grid, converts it to the model's expected problem, and conducts a search """
        grid_representation = self.view.get_grid_representation()
        grid_problem_grid = parse_view_grid(grid_representation)
        if not self.model.is_valid_problem(grid_problem_grid):
            return

        self.model.get_problem().update_state(grid_problem_grid)
        searcher = self.view.get_searcher()
        search_log = searcher.logged_search(self.model.get_problem())
        self.view.render_search(search_log)

    def forward_state_update(self, state_update: Event):
        problem = state_update.data
        self.view.update_color_map(problem)

        




