from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QGridLayout, QApplication

from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position_type import PositionType
from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.squareFactory import SquareFactory


class GridWidget(QWidget):
    def __init__(self, widgetWidth, widgetHeight, state, publisher, currentToggledSquare="agent"):
        super().__init__()
        self.publisher = publisher
        rows = len(state)
        cols = len(state[0])
        self.widgetWidth = widgetWidth
        self.widgetHeight = widgetHeight
        self.squareLength = self.widgetWidth // max(rows, cols)

        self.currentToggledSquare = currentToggledSquare
        self.currentAgentPos = None

        # grid to hold squares [labels]
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        # make a grid layout with no padding between squares
        self.createGridLayout(rows, cols)
        self.publisher.subscribe(EventType.RadioToggled, self)
        self.publisher.subscribe(EventType.ResetPressed, self)

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

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.currentToggledSquare == "agent": # only allow one agent; agents are made by clicking and not moved click
            return
        col, row = self.getSquareIndices(event)
        if row >= len(self.grid) or col >= len(self.grid[row]): # stay within grid
            return
        self.updateSquare(row, col, self.currentToggledSquare)

    def mousePressEvent(self, event: QMouseEvent):
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

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Create and show grid
    grid = [[PositionType.EMPTY for _ in range(10)] for _ in range(10)]
    problem = GridProblem(grid)
    window = GridWidget(250, 250, problem.get_state())
    window.show()

    sys.exit(app.exec())

