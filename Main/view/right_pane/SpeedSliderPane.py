import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QApplication


class SpeedSliderPane(QWidget):
    def __init__(self, minValue, maxValue, initalValue = None):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.description = QLabel("Speed:")
        self.layout.addWidget(self.description)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(minValue, maxValue)
        self.slider.setValue((minValue+maxValue)//2)
        self.layout.addWidget(self.slider)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpeedSliderPane(minValue = 0, maxValue = 100)
    window.show()
    sys.exit(app.exec())

