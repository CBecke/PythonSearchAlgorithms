from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class OptionsPane(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.startBtn = QPushButton('Start')
        self.stopBtn = QPushButton('Stop')
        self.saveBtn = QPushButton('Save')

        self.layout.addWidget(self.startBtn)
        self.layout.addWidget(self.stopBtn)
        self.layout.addWidget(self.saveBtn)