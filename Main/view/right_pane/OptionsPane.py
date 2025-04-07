from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from Main.communication.event.StartPressedEvent import StartPressedEvent
from Main.communication.event.clear_event import ClearGridEvent


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

        self.startBtn.clicked.connect(self.startAction)
        self.clearBtn.clicked.connect(self.clearAction)

    def startAction(self):
        event = StartPressedEvent()
        self.publisher.notify(event.get_type(), event)

    def clearAction(self):
        event = ClearGridEvent()
        self.publisher.notify(event.get_type(), event)