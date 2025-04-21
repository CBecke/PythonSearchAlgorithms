from typing import Collection

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QGridLayout

from Main.model.data_structure.node import Node
from Main.model.data_structure.queue import Queue
from Main.model.searcher.informed.impl.best_first_searcher import BestFirstSearcher
from Main.model.searcher.search_log import SearchLog
from Main.model.searchproblem import grid_problem
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_problem import SearchProblem
from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType
from Main.communication.event.impl.search_concluded_event import SearchConcludedEvent
from Main.view.left_pane.grid.label.impl.agentSquare import AgentSquare
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.impl.goalSquare import GoalSquare
from Main.view.left_pane.grid.label.impl.search_square.expandedSquare import ExpandedSquare
from Main.view.left_pane.grid.label.impl.search_square.generatedSquare import GeneratedSquare
from Main.view.left_pane.grid.label.impl.wallSquare import WallSquare
from Main.view.left_pane.grid.label.squareFactory import SquareFactory


class GridWidget(QWidget):
    def __init__(self, widget_width, widget_height, state, publisher, current_toggled_square="agent"):
        super().__init__()
        self.publisher = publisher
        self.publisher.subscribe(EventType.RadioToggled, self)
        self.publisher.subscribe(EventType.ResetPressed, self)
        self.publisher.subscribe(EventType.ClearGridPressed, self)

        self.speedSlider = None
        rows = len(state)
        cols = len(state[0])
        self.widgetWidth = widget_width
        self.widgetHeight = widget_height
        self.squareLength = self.widgetWidth // max(rows, cols)

        self.currentToggledSquare = current_toggled_square
        self.currentAgentPos = None
        self.grid_locked = False
        self.search_thread = None

        # grid to hold squares [labels]
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        # for each square state the color it has as rgb string based on its distance to the closest goal
        self.distance_color_grid = [[None for _ in range(cols)] for _ in range(rows)]

        # make a grid layout with no padding between squares
        self.create_grid_layout(rows, cols)

    def create_grid_layout(self, n_rows, n_cols):
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.grid = [[None for _ in range(n_cols)] for _ in range(n_rows)]
        for row in range(n_rows):
            for col in range(n_cols):
                label = EmptySquare(self.squareLength)
                self.layout.addWidget(label, row, col)
                self.grid[row][col] = label


    def update_subscriber(self, event: Event):
        # This is the currently chosen radio button
        if event.get_type() == EventType.RadioToggled:
            self.currentToggledSquare = event.data
        elif event.get_type() == EventType.ResetPressed:
            self.stop_rendering()
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if not isinstance(self.grid[row][col], EmptySquare):
                        self.update_square(row, col, "empty")

        elif event.get_type() == EventType.ClearGridPressed:
            self.stop_rendering()

            self.clear_search_squares()


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.grid_locked or self.currentToggledSquare == "agent": # only allow one agent; agents are made by clicking and not moved click
            return
        col, row = self.get_square_indices(event)
        if not (0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])): # stay within grid
            return
        self.update_square(row, col, self.currentToggledSquare)

    def mousePressEvent(self, event: QMouseEvent):
        if self.grid_locked:
            return
        col, row = self.get_square_indices(event)

        # only allow a single agent on the grid
        if self.currentToggledSquare == "agent":
            if self.currentAgentPos is not None:
                # turn old agent square into an empty square
                prev_agent_x, prev_agent_y = self.currentAgentPos
                self.update_square(prev_agent_x, prev_agent_y, "empty")
            self.currentAgentPos = (row, col)

        self.update_square(row, col, self.currentToggledSquare)


    def update_square(self, row, col, type_to: str):
        old_widget = self.grid[row][col]
        if old_widget:
            self.layout.removeWidget(old_widget)
            old_widget.deleteLater()

        if type_to == "expanded":
            new_widget = ExpandedSquare(self.squareLength, self.distance_color_grid[row][col])
        else:
            new_widget = SquareFactory.make(type_to, self.squareLength)
        self.layout.addWidget(new_widget, row, col)
        self.grid[row][col] = new_widget

    def get_square_indices(self, event: QMouseEvent):
        x = event.pos().x() // self.squareLength
        y = event.pos().y() // self.squareLength
        return x, y

    def get_grid(self):
        return self.grid

    def unlock(self):
        self.grid_locked = False

    def render_search(self, log: SearchLog):
        self.grid_locked = True

        # stop any previous timer
        if getattr(self, "timer", None):
            self.timer.stop()

        self.clear_search_squares()

        self.step_iter = iter(log)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.render_step)
        self.timer.setInterval(self.slider_to_interval(self.speedSlider.slider.value()))
        self.timer.start()

        self.speedSlider.speed_changed.connect(
            lambda v: self.timer.setInterval(self.slider_to_interval(v))
        )
        self.publisher.notify(SearchConcludedEvent(log.n_generated()))

    def render_step(self):
        try:
            generated_set_node, expanded_node = next(self.step_iter)
        except StopIteration:
            self.timer.stop()
            self.unlock()
            return

        position = expanded_node.value.state
        row, col = position.row, position.column
        if not isinstance(self.grid[row][col], AgentSquare) and not isinstance(self.grid[row][col], GoalSquare):
            self.update_square(row, col, "expanded")

        for search_node in generated_set_node.value:
            position = search_node.state
            row, col = position.row, position.column
            if not isinstance(self.grid[row][col], AgentSquare) and not isinstance(self.grid[row][col], GoalSquare):
                self.update_square(row, col, "generated")

    def stop_rendering(self):
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()
        self.step_iter = iter([])
        self.unlock()

    def slider_to_interval(self, slider_value):
        min_val = self.speedSlider.minimum
        max_val = self.speedSlider.maximum
        return max(min_val, max_val-slider_value+min_val)

    def set_speed_slider(self, speed_slider):
        self.speedSlider = speed_slider

    def update_color_map(self, problem: SearchProblem):
        assert isinstance(problem, grid_problem.GridProblem), "the current update_color_map assumes 1) no negative cost cycles and 2) a 2d array structure - which is true for GridProblem"
        goal_distance_grid = self.goal_distances(problem)

        # when there are no goals or solution, a grid full of None is returned
        log = BestFirstSearcher().logged_search(problem)
        if len(problem.find_goal_states()) == 0 or not problem.is_goal_state(log.expanded.tail.value.state):
            self.distance_color_grid = goal_distance_grid
            return

        (min_value, max_value) = self.distance_grid_min_max(goal_distance_grid)
        n_colors = max_value - min_value + 1
        max_color_value = 255
        color_step = 255 / n_colors
        blue = 0
        for row in range(len(goal_distance_grid)):
            for col in range(len(goal_distance_grid[row])):
                distance = goal_distance_grid[row][col]
                if distance is None:
                    continue
                red = round(color_step * distance)
                green = max_color_value - round(color_step * distance)
                goal_distance_grid[row][col] = f"rgb({red}, {green}, {blue})"
        self.distance_color_grid = goal_distance_grid


    def goal_distances(self, problem: SearchProblem):
        goals = problem.find_goal_states()
        problem_grid = problem.to_array()
        assert not isinstance(problem_grid[0][0], Collection), "assumes two-dimensional non-empty search problem"
        # Do BFS to determine distances
        distance_grid = [[None for _ in range(len(problem_grid[row]))] for row in range(len(problem_grid))]
        queue = Queue()
        for position in goals:
            distance_grid[position.row][position.column] = 0
            queue.add(Node(position))

        while not queue.is_empty():
            current = queue.pop()
            row, col = current.value.row, current.value.column
            current_value = distance_grid[row][col]
            assert current_value is not None, "current value should always be filled"

            potential_neighbors = [Position(row, col - 1), Position(row, col + 1), Position(row - 1, col), Position(row + 1, col)]
            potential_new_value = current_value + 1
            for neighbor in potential_neighbors:
                neighbor_row, neighbor_col = neighbor.row, neighbor.column
                if not (0 <= neighbor_row < len(distance_grid) and 0 <= neighbor_col < len(distance_grid[neighbor_row])):
                    continue

                neighbor_value = distance_grid[neighbor_row][neighbor_col]
                if (neighbor_value is None or neighbor_value > potential_new_value) and not isinstance(self.grid[neighbor_row][neighbor_col], WallSquare):
                    distance_grid[neighbor_row][neighbor_col] = potential_new_value
                    queue.add(Node(neighbor))

        return distance_grid

    def distance_grid_min_max(self, grid):
        assert not isinstance(grid[0][0], Collection), "assumes two-dimensional non-empty search problem"
        min_value = None
        max_value = None
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                value = grid[row][col]
                if value is None:
                    continue
                min_value = min(min_value, value) if min_value is not None else value
                max_value = max(max_value, value) if max_value is not None else value
        return min_value, max_value

    def clear_search_squares(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                current = self.grid[row][col]
                if isinstance(current, GeneratedSquare) or isinstance(current, ExpandedSquare):
                    self.update_square(row, col, "empty")

