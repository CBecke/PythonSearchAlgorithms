
### Examples based on https://realpython.com/python-pyqt-gui-calculator/#:~:text=PyQt%20is%20a%20Python%20binding,and%20many%20other%20powerful%20features.

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QFormLayout,
    QLineEdit, QDialog, QVBoxLayout, QDialogButtonBox, QMainWindow, QToolBar, QStatusBar,
)

"""
# Hello world text GUI
app = QApplication([])
window = QWidget()
window.setWindowTitle('PyQt App')
window.setGeometry(1000, 400, 280, 80)
helloMsg = QLabel('<h1>Hello, World!</h1>', parent=window)
helloMsg.move(60, 15)

window.show()
sys.exit(app.exec())
"""

"""
# 3 horizontal buttons
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('QHBoxLayout')

layout = QHBoxLayout()
window.setLayout(layout)
layout.addWidget(QPushButton('left'))
layout.addWidget(QPushButton('center'))
layout.addWidget(QPushButton('right'))

window.show()
sys.exit(app.exec())
"""

"""
# grid layout
app = QApplication([])
window = QWidget()
window.setWindowTitle('QGridLayout')

layout = QGridLayout()
window.setLayout(layout)
layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)
layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)
layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)
layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)
layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)
layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)
layout.addWidget(QPushButton("Button (2, 0)"), 2, 0)
layout.addWidget(
    QPushButton("Button (2, 1) + 2 Columns Span"), 2, 1, 1, 2
)

window.show()
sys.exit(app.exec())
"""

"""
# form layout example
app = QApplication([])
window = QWidget()
window.setWindowTitle("QFormLayout")

layout = QFormLayout()
layout.addRow("Name:", QLineEdit())
layout.addRow("Age:", QLineEdit())
layout.addRow("Job:", QLineEdit())
layout.addRow("Hobbies:", QLineEdit())
window.setLayout(layout)

window.show()
sys.exit(app.exec())
"""

"""
# dialog window (a "pop-up" type window which is slightly simply than the main window)
class Window(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QDialog")
        dialogLayout = QVBoxLayout()

        formLayout = QFormLayout()
        formLayout.addRow("Name:", QLineEdit())
        formLayout.addRow("Age:", QLineEdit())
        formLayout.addRow("Job:", QLineEdit())
        formLayout.addRow("Hobbies:", QLineEdit())
        dialogLayout.addLayout(formLayout)
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        dialogLayout.addWidget(buttons)
        self.setLayout(dialogLayout)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
"""

"""
# main window application
class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
"""

"""
# defining event behavior
def greet(name):
    if msgLabel.text():
        msgLabel.setText("")
    else:
        msgLabel.setText(f"Hello, {name}")

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Signals and slots")
layout = QVBoxLayout()

button = QPushButton("Greet")
button.clicked.connect(lambda: greet("World!"))

layout.addWidget(button)
msgLabel = QLabel("")
layout.addWidget(msgLabel)
window.setLayout(layout)
window.show()
sys.exit(app.exec())
"""

from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class GridWidget(QWidget):
    def __init__(self, rows=10, cols=10, cell_size=40):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

        # Set up the layout
        self.layout = QGridLayout()
        self.layout.setSpacing(0)  # No spacing between cells
        self.layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.setLayout(self.layout)

        # Create grid of labels
        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                label.setFixedSize(cell_size, cell_size)
                label.setStyleSheet("background-color: white; border: 1px solid gray;")  # Default color
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text (if needed)
                self.layout.addWidget(label, row, col)
                self.grid[row][col] = label

    def update_cell(self, row, col, color):
        """Updates a cell's color dynamically."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col].setStyleSheet(f"background-color: {color}; border: 1px solid gray;")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Create and show grid
    window = GridWidget(rows=10, cols=10, cell_size=20)
    window.show()

    # Example usage: Change a cell color after a short delay
    from PyQt6.QtCore import QTimer


    def demo():
        window.update_cell(2, 3, "red")  # Example update


    QTimer.singleShot(1000, demo)  # Update after 1 second

    sys.exit(app.exec())




