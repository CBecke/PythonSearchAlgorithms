import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QApplication


class SpeedSliderPane(QWidget):
    speed_changed = pyqtSignal(int)

    def __init__(self, minValue, maxValue):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.description = QLabel("Speed:")
        self.layout.addWidget(self.description)

        self.minimum = minValue
        self.maximum = maxValue

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(minValue, maxValue)
        self.slider.setValue((minValue+maxValue)//2)
        self.slider.valueChanged.connect(self.emit_speed)
        self.layout.addWidget(self.slider)

    def emit_speed(self, value):
        self.speed_changed.emit(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpeedSliderPane(minValue = 0, maxValue = 100)
    window.show()
    sys.exit(app.exec())

