from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication

from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position_type import PositionType
from Main.observer_pattern.event.event import Event
from Main.observer_pattern.event.event_type import EventType
from Main.view.left_pane.grid.gridLabel import GridLabel


class GridWidget(QWidget):
    def __init__(self, widgetWidth, widgetHeight, state, publisher):
        super().__init__()
        self.publisher = publisher
        rows = len(state)
        cols = len(state[0])
        self.widgetWidth = widgetWidth
        self.widgetHeight = widgetHeight
        self.squareLength = self.widgetWidth // max(rows, cols)

        # grid to hold squares [labels]
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        # make a grid layout with no padding between squares
        self.createGridLayout(rows, cols)

    def createGridLayout(self, nRows, nCols):
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.grid = [[None for _ in range(nCols)] for _ in range(nRows)]

        for row in range(nRows):
            for col in range(nCols):
                label = GridLabel(self.squareLength)
                self.publisher.subscribe(EventType.RadioToggled, label)
                self.layout.addWidget(label, row, col)
                self.grid[row][col] = label


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Create and show grid
    grid = [[PositionType.EMPTY for _ in range(10)] for _ in range(10)]
    problem = GridProblem(grid)
    window = GridWidget(250, 250, problem.get_state())
    window.show()

    sys.exit(app.exec())

