from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QRadioButton


class DrawChoiceButton(QRadioButton):
    def __init__(self, name, connected_key):
        super().__init__(name)
        self.connected_key = connected_key

