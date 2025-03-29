from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from Main.observer_pattern.event.StartPressedEvent import StartPressedEvent


class OptionsPane(QWidget):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.startBtn = QPushButton('Start')
        self.stopBtn = QPushButton('Stop')
        self.saveBtn = QPushButton('Save')

        self.layout.addWidget(self.startBtn)
        self.layout.addWidget(self.stopBtn)
        self.layout.addWidget(self.saveBtn)

        self.startBtn.clicked.connect(self.startAction)

    def startAction(self):
        event = StartPressedEvent()
        self.publisher.notify(event.get_type(), event)
