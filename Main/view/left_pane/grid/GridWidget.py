from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QGridLayout, QApplication

from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position_type import PositionType
from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType
from Main.view.left_pane.grid.label.impl.agentSquare import AgentSquare
from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.squareFactory import SquareFactory


class GridWidget(QWidget):
    def __init__(self, widgetWidth, widgetHeight, state, publisher):
        super().__init__()
        self.publisher = publisher
        rows = len(state)
        cols = len(state[0])
        self.widgetWidth = widgetWidth
        self.widgetHeight = widgetHeight
        self.squareLength = self.widgetWidth // max(rows, cols)

        self.currentToggledSquare = "agent"
        self.currentAgentPos = None

        # grid to hold squares [labels]
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        # make a grid layout with no padding between squares
        self.createGridLayout(rows, cols)
        self.publisher.subscribe(EventType.RadioToggled, self)

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
        self.currentToggledSquare = event.data

    def mouseMoveEvent(self, event: QMouseEvent):
        self.mouseUpdate(event)

    def mousePressEvent(self, event: QMouseEvent):
        self.mouseUpdate(event)

    def mouseUpdate(self, event: QMouseEvent):
        # TODO: debug why program crashes when clicking and hovering outside of the grid while drawing agent.
        col, row = self.getSquareIndices(event)
        # only allow a single agent on the grid
        currentSquare = self.grid[row][col]
        if isinstance(currentSquare, AgentSquare):
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

        new_widget = SquareFactory.make(typeTo, self.squareLength)
        self.layout.addWidget(new_widget, row, col)
        self.grid[row][col] = new_widget

    def getSquareIndices(self, event: QMouseEvent):
        x = event.pos().x() // self.squareLength
        y = event.pos().y() // self.squareLength
        return x, y

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Create and show grid
    grid = [[PositionType.EMPTY for _ in range(10)] for _ in range(10)]
    problem = GridProblem(grid)
    window = GridWidget(250, 250, problem.get_state())
    window.show()

    sys.exit(app.exec())

