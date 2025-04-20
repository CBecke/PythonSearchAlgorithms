
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton

from Main.communication.event.impl.dimension_apply_pressed import DimensionApplyPressedEvent


class DimensionChoicePane(QWidget):
    def __init__(self, publisher, min_dimension=2, max_dimension=40):
        super().__init__()
        self.publisher = publisher
        self.minDimension = min_dimension
        self.maxDimension = max_dimension

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.description = QLabel("Number of Squares per Axis:")
        self.layout.addWidget(self.description)

        self.dimensionChoice = QLineEdit()
        self.dimensionChoice.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.dimensionChoice.returnPressed.connect(self.update_dimensions)
        self.dimensionChoice.setPlaceholderText(f"Number of squares per row [{self.minDimension}:{self.maxDimension}]")
        self.dimensionChoice.setValidator(QIntValidator()) # make sure only numbers can be written


        self.layout.addWidget(self.dimensionChoice)

        self.button = QPushButton("apply")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.publish_problem_dimensions)

    def publish_problem_dimensions(self):
        n_dimensions = self.dimensionChoice.text()
        if n_dimensions.isnumeric() and self.minDimension <= int(n_dimensions) <= self.maxDimension:
            self.publisher.notify(DimensionApplyPressedEvent(int(n_dimensions)))

    def update_dimensions(self):
        self.publish_problem_dimensions()
        self.dimensionChoice.setText("")
        self.unfocus_lineedit()

    def unfocus_lineedit(self):
        if self.dimensionChoice.hasFocus():
            self.dimensionChoice.clearFocus()

