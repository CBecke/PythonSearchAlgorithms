import sys

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication, QLineEdit, QPushButton

from Main.communication.event.dimension_apply_pressed import DimensionApplyPressedEvent
from Main.communication.publisher import Publisher
from Main.communication.event.event_type import EventType as ET


class DimensionChoiceWidget(QWidget):
    def __init__(self, publisher, minDimension=2, maxDimension=40):
        super().__init__()
        self.publisher = publisher
        self.minDimension = minDimension
        self.maxDimension = maxDimension

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.description = QLabel("Number of Squares per Axis:")
        self.layout.addWidget(self.description)

        self.dimensionChoice = QLineEdit()
        self.layout.addWidget(self.dimensionChoice)
        self.dimensionChoice.setPlaceholderText(f"#squares [{self.minDimension}:{self.maxDimension}]")

        self.button = QPushButton("apply")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.publishProblemDimensions)

    def publishProblemDimensions(self):
        nDimensions = self.dimensionChoice.text()
        if nDimensions.isnumeric() and self.minDimension <= int(nDimensions) <= self.maxDimension:
            event = DimensionApplyPressedEvent(int(nDimensions))
            self.publisher.notify(event.get_type(), event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DimensionChoiceWidget(Publisher())
    window.show()
    sys.exit(app.exec())
