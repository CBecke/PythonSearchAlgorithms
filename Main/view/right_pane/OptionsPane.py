from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from Main.communication.event.impl.start_pressed_event import StartPressedEvent
from Main.communication.event.impl.clear_event import ClearGridEvent


class OptionsPane(QWidget):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.startBtn = QPushButton('Start')
        self.clearBtn = QPushButton('Clear Search')

        self.layout.addWidget(self.startBtn)
        self.layout.addWidget(self.clearBtn)

        self.startBtn.clicked.connect(self.start_action)
        self.clearBtn.clicked.connect(self.clear_action)

    def start_action(self):
        self.publisher.notify(StartPressedEvent())

    def clear_action(self):
        self.publisher.notify(ClearGridEvent())
