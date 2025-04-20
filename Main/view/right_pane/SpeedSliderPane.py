import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QApplication

class SpeedSliderPane(QWidget):
    speed_changed = pyqtSignal(int)

    def __init__(self, min_speed, max_speed):
        super().__init__()
        self.minimum = min_speed
        self.maximum = max_speed

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.description = QLabel("Speed:")
        self.layout.addWidget(self.description)



        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(self.minimum, self.maximum)
        self.slider.setValue((self.minimum+self.maximum)//2)
        self.slider.valueChanged.connect(self.emit_speed)
        self.layout.addWidget(self.slider)

    def emit_speed(self, value):
        self.speed_changed.emit(value)

