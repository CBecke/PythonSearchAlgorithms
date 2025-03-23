from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication

from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.position_type import PositionType


class GridWidget(QWidget):
    def __init__(self, widgetWidth, widgetHeight, state):
        super().__init__()

        rows = len(state)
        cols = len(state[0])
        self.widgetWidth = widgetWidth
        self.widgetHeight = widgetHeight
        self.squareLength = self.widgetWidth // max(rows, cols)

        # grid to hold squares [labels]
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        # make a grid layout with no padding between squares
        self.createGridLayout(rows, cols)

    def make_square(self, position_type: PositionType):
        label = QLabel()
        label.setFixedSize(self.squareLength, self.squareLength)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color = self.get_square_color(position_type)
        label.setStyleSheet(f"background-color: {color}; border: 1px solid gray;")
        
        return label


    @staticmethod
    def get_square_color(position_type:PositionType):
        colors = {
            PositionType.EMPTY: "white",
            PositionType.WALL: "black",
            PositionType.INITIAL: "darkGreen",
            PositionType.GOAL: "darkRed",
        }
        return colors[position_type]

    def createGridLayout(self, nRows, nCols):
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.grid = [[None for _ in range(nCols)] for _ in range(nRows)]

        for row in range(nRows):
            for col in range(nCols):
                label = self.make_square(PositionType.EMPTY)
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

