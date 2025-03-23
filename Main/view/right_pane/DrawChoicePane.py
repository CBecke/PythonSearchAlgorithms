import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication, QPushButton, QGridLayout, QRadioButton, \
    QVBoxLayout

from Main.observer_pattern.event.event_type import EventType
from Main.observer_pattern.event.radio_toggled_event import RadioToggledEvent


class DrawChoicePane(QWidget):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.description = QLabel("Draw:")
        self.description.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.description)

        self.createButtons()

    def createButtons(self):
        self.radioAgent = QRadioButton("Agent")
        self.radioWall = QRadioButton("Wall")
        self.radioGoal = QRadioButton("Goal")
        self.radioEmpty = QRadioButton("Empty")

        self.buttons = [self.radioAgent, self.radioWall, self.radioGoal, self.radioEmpty]
        self.radioAgent.setChecked(True)

        radioLayout = QHBoxLayout()
        for btn in self.buttons:
            btn.toggled.connect(self.onClicked)
            radioLayout.addWidget(btn)

        self.publisher.notify(EventType.RadioToggled, RadioToggledEvent(self.radioAgent.text()))

        outerLayout = QVBoxLayout()
        resetButton = QPushButton("Reset")
        outerLayout.addLayout(radioLayout)
        outerLayout.addSpacing(30)
        outerLayout.addWidget(resetButton)

        self.layout.addLayout(outerLayout)

    def onClicked(self):
        button = self.sender()
        if button.isChecked():
            self.publisher.notify(EventType.RadioToggled, RadioToggledEvent(button.text()))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawChoicePane()
    window.show()
    sys.exit(app.exec())
