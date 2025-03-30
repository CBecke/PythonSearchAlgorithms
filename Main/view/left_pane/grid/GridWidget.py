from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QGridLayout, QApplication

from Main.model.search.searcher.search_log import SearchLog
from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position_type import PositionType
from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.impl.expandedSquare import ExpandedSquare
from Main.view.left_pane.grid.label.impl.generatedSquare import GeneratedSquare
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
        # make a grid layout with no padding between squares
        self.createGridLayout(rows, cols)
        self.publisher.subscribe(EventType.RadioToggled, self)
        self.publisher.subscribe(EventType.ResetPressed, self)
        self.publisher.subscribe(EventType.StartPressed, self)

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
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if not isinstance(self.grid[row][col], EmptySquare):
                        self.updateSquare(row, col, "empty")
        elif event.get_type() == EventType.StartPressed:
            self.grid_locked = True


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
        if self.currentToggledSquare == "agent" and self.currentAgentPos is not None:
            # turn old agent square into an empty square
            prevAgentX, prevAgentY = self.currentAgentPos
            self.updateSquare(prevAgentX, prevAgentY, "empty")

        self.currentAgentPos = (row, col)
        self.updateSquare(row, col, self.currentToggledSquare)


    def updateSquare(self, row, col, typeTo: str):
        old_widget = self.grid[row][col]
        self.layout.removeWidget(old_widget)
        old_widget.deleteLater()

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

    def render_search(self, log):
        self.grid_locked = True

        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.stop()
            self.search_thread.wait()

        self.search_thread = SearchRendererThread(log, self.speedSlider)
        self.search_thread.render_step.connect(self.handle_render_step)

        self.search_thread.sleep_duration = self.speedSlider.slider.value()
        self.speedSlider.speed_changed.connect(self.search_thread.update_speed)

        self.search_thread.finished.connect(self.render_finished) # TODO: make it update the generated nodes GUI field
        self.search_thread.start()

    def update_thread_speed(self, value):
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.update_speed(value)

    def handle_render_step(self, row, col, render_type_str):
        self.updateSquare(row, col, render_type_str)

    def render_finished(self):
        self.unlock()

    def stop_rendering(self):
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.stop()
            self.search_thread.wait()

    def set_speed_slider(self, speedSlider):
        self.speedSlider = speedSlider
        self.speedSlider.speed_changed.connect(self.update_thread_speed)


# multi-threading with the help of ChatGPT
class SearchRendererThread(QThread):
    render_step = pyqtSignal(int, int, str)
    finished = pyqtSignal()

    def __init__(self, log, speedSlider):
        super().__init__()
        self.log = log
        self.running = True
        self.sleep_duration = 500
        self.speedSlider = speedSlider

    def run(self):
        for node_generated, node_expanded in self.log:
            if not self.running:
                break

            # node_generated is a Node whose value is a set of SearchNode
            for search_node in node_generated.value:
                position = search_node.state
                row, col = position.row, position.column
                self.render_step.emit(row, col, "generated")

            position = node_expanded.value.state
            row, col = position.row, position.column
            self.render_step.emit(row, col, "expanded")

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

