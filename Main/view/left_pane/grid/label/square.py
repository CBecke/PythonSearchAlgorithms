
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QLabel

from Main.model.searchproblem.position_type import PositionType
from Main.observer_pattern.event.event import Event


class Square(QLabel):
    def __init__(self, size, color):
        super().__init__()
        self.setFixedSize(size, size)
        self.color = color

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self.setStyleSheet(f"background-color: {color}; border: 1px solid gray;")

        # make Square transparent so that the containing GridWidget can accept the MouseEvent instead
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    """
    def update_subscriber(self, event: Event):
        toggled_radio = event.data
        self.color = Square.getTypeColor(Square.getTextType(toggled_radio))
    """




