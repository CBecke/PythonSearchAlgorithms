import sys

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication, QLineEdit, QPushButton


class DimensionChoiceWidget(QWidget):
    def __init__(self, publisher, minRows=2, maxRows=40, minCols=2, maxCols=40):
        super().__init__()
        self.publisher = publisher
        self.minRows = minRows
        self.maxRows = maxRows
        self.minCols = minCols
        self.maxCols = maxCols

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.description = QLabel("Grid Dimensions:")
        self.layout.addWidget(self.description)

        self.rowChoice = QLineEdit()
        self.layout.addWidget(self.rowChoice)
        self.columnChoice = QLineEdit()
        self.layout.addWidget(self.columnChoice)
        self.rowChoice.setPlaceholderText(f"#rows [{self.minRows}:{self.maxRows}]")
        self.columnChoice.setPlaceholderText(f"#cols [{self.minCols}:{self.maxCols}]")

        self.button = QPushButton("apply")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.publishProblemDimensions())

    def publishProblemDimensions(self):
        nRows = self.rowChoice.text()
        nCols = self.columnChoice.text()
        if (nRows.isnumeric() and self.minRows <= int(nRows) <= self.maxRows and
                nCols.isnumeric() and self.minCols <= int(nCols) <= self.maxCols):
            self.publisher.notify("problemDimensionsModifyEvent", {"rows": int(nRows), "columns": int(nCols)})



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DimensionChoiceWidget()
    window.show()
    sys.exit(app.exec())
