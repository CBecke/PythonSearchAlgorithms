from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication



class GridWidget(QWidget):
    def __init__(self, widgetWidth, widgetHeight, rows=20, cols=20):
        super().__init__()

        self.rows = rows
        self.cols = cols

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

        # make a grid layout with no padding between squares
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        cellWidth = widgetWidth // self.cols
        cellHeight = widgetHeight // self.rows

        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                label.setFixedSize(cellWidth, cellHeight)
                label.setStyleSheet("background-color: white; border: 1px solid gray;")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.layout.addWidget(label, row, col)
                self.grid[row][col] = label


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Create and show grid
    window = GridWidget(250, 250, rows=10, cols=10)
    window.show()

    sys.exit(app.exec())

