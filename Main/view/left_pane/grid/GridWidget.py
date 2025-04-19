from typing import Collection

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QGridLayout, QApplication

from Main.model.data_structure.node import Node
from Main.model.data_structure.queue import Queue
from Main.model.searcher.informed.best_first_searcher import BestFirstSearcher
from Main.model.searcher.search_log import SearchLog
from Main.model.searchproblem import grid_problem
from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.position_type import PositionType
from Main.model.searchproblem.search_problem import SearchProblem
from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType
from Main.communication.event.searchConcludedEvent import SearchConcludedEvent
from Main.view.left_pane.grid.label.impl.agentSquare import AgentSquare
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.impl.search_square.expandedSquare import ExpandedSquare
from Main.view.left_pane.grid.label.impl.goalSquare import GoalSquare
from Main.view.left_pane.grid.label.impl.search_square.generatedSquare import GeneratedSquare
from Main.view.left_pane.grid.label.impl.wallSquare import WallSquare
from Main.view.left_pane.grid.label.squareFactory import SquareFactory


class GridWidget(QWidget):
    def __init__(self, widgetWidth, widgetHeight, state, publisher, currentToggledSquare="agent"):
        super().__init__()
        self.publisher = publisher
        self.speedSlider = None
        rows = len(state)
        cols = len(state[0])
        self.widgetWidth = widgetWidth
        self.widgetHeight = widgetHeight
        self.squareLength = self.widgetWidth // max(rows, cols)

        self.currentToggledSquare = currentToggledSquare
        self.currentAgentPos = None
        self.grid_locked = False
        self.search_thread = None

        # grid to hold squares [labels]
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        # for each square state the color it has as rgb string based on its distance to the closest goal
        self.distance_color_grid = [[None for _ in range(cols)] for _ in range(rows)]

        # make a grid layout with no padding between squares
        self.createGridLayout(rows, cols)
        self.publisher.subscribe(EventType.RadioToggled, self)
        self.publisher.subscribe(EventType.ResetPressed, self)
        self.publisher.subscribe(EventType.ClearGridPressed, self)

    def createGridLayout(self, nRows, nCols):
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.grid = [[None for _ in range(nCols)] for _ in range(nRows)]
        for row in range(nRows):
            for col in range(nCols):
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
                        self.updateSquare(row, col, "empty")

        elif event.get_type() == EventType.ClearGridPressed:
            if self.search_thread and self.search_thread.isRunning():
                self.search_thread.stop()
                self.search_thread.wait()

            self.clear_search_squares()


    def mouseMoveEvent(self, event: QMouseEvent):
        if self.grid_locked or self.currentToggledSquare == "agent": # only allow one agent; agents are made by clicking and not moved click
            return
        col, row = self.getSquareIndices(event)
        if not (0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])): # stay within grid
            return
        self.updateSquare(row, col, self.currentToggledSquare)

    def mousePressEvent(self, event: QMouseEvent):
        if self.grid_locked:
            return
        col, row = self.getSquareIndices(event)
        # only allow a single agent on the grid
        currentSquare = self.grid[row][col]
        if self.currentToggledSquare == "agent":
            if self.currentAgentPos is not None:
                # turn old agent square into an empty square
                prevAgentX, prevAgentY = self.currentAgentPos
                self.updateSquare(prevAgentX, prevAgentY, "empty")
            self.currentAgentPos = (row, col)

        self.updateSquare(row, col, self.currentToggledSquare)


    def updateSquare(self, row, col, typeTo: str):
        old_widget = self.grid[row][col]
        self.layout.removeWidget(old_widget)
        old_widget.deleteLater()

        if typeTo == "expanded":
            color = self.distance_color_grid[row][col]
            if color is None:
                color = "darkBlue"
            new_widget = ExpandedSquare(self.squareLength, self.distance_color_grid[row][col])
        else:
            new_widget = SquareFactory.make(typeTo, self.squareLength)
        self.layout.addWidget(new_widget, row, col)
        self.grid[row][col] = new_widget

    def getSquareIndices(self, event: QMouseEvent):
        x = event.pos().x() // self.squareLength
        y = event.pos().y() // self.squareLength
        return x, y

    def get_grid(self):
        return self.grid

    def unlock(self):
        self.grid_locked = False

    def render_search(self, log: SearchLog):
        self.grid_locked = True

        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.stop()
            self.search_thread.wait()

        self.clear_search_squares()

        self.search_thread = SearchRendererThread(log, self.speedSlider)
        self.search_thread.render_step.connect(self.handle_render_step)
        self.speedSlider.speed_changed.connect(self.search_thread.update_speed)

        self.search_thread.finished.connect(self.render_finished)
        self.search_thread.start()
        event = SearchConcludedEvent(log.n_generated())
        self.publisher.notify(event.get_type(), event)

    def update_thread_speed(self, value):
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.update_speed(value)

    def handle_render_step(self, row, col, render_type_str):
        square = self.grid[row][col]
        if not isinstance(square, AgentSquare) and not isinstance(square, GoalSquare):
            self.updateSquare(row, col, render_type_str)

    def render_finished(self):
        self.unlock()

    def stop_rendering(self):
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.stop()
            self.search_thread.wait()
            self.unlock()

    def set_speed_slider(self, speedSlider):
        self.speedSlider = speedSlider
        self.speedSlider.speed_changed.connect(self.update_thread_speed)

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
        distance_grid = [[None for col in range(len(problem_grid[row]))] for row in range(len(problem_grid))]
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
                    self.updateSquare(row, col, "empty")


# multi-threading with the help of ChatGPT
class SearchRendererThread(QThread):
    render_step = pyqtSignal(int, int, str)
    finished = pyqtSignal()

    def __init__(self, log, speedSlider):
        super().__init__()
        self.log = log
        self.running = True
        self.speedSlider = speedSlider
        self.update_speed(self.speedSlider.slider.value())

    def run(self):
        for node_generated, node_expanded in self.log:
            if not self.running:
                break

            position = node_expanded.value.state
            row, col = position.row, position.column
            self.render_step.emit(row, col, "expanded")

            # node_generated is a Node whose value is a set of SearchNode
            for search_node in node_generated.value:
                position = search_node.state
                row, col = position.row, position.column
                self.render_step.emit(row, col, "generated")

            self.msleep(self.sleep_duration)


        self.finished.emit()

    def stop(self):
        self.running = False

    def update_speed(self, value):
        min_val = self.speedSlider.minimum
        max_val = self.speedSlider.maximum
        self.sleep_duration = max(min_val, max_val - value + min_val)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Create and show grid
    grid = [[PositionType.EMPTY for _ in range(10)] for _ in range(10)]
    problem = GridProblem(grid)
    window = GridWidget(250, 250, problem.get_state())
    window.show()

    sys.exit(app.exec())

