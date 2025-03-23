from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QLabel

from Main.model.searchproblem.position_type import PositionType
from Main.observer_pattern.event.event import Event


class GridLabel(QLabel):
    def __init__(self, size, positionType=PositionType.EMPTY):
        super().__init__()
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.color = GridLabel.getTypeColor(positionType)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self.paint(self.color)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.paint(self.color)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.paint(self.color)
        self.update()

    def paint(self, color):
        #print(f"updating style to {color}")
        self.setStyleSheet(f"background-color: {color}; border: 1px solid gray;")

    def update_subscriber(self, event: Event):
        toggled_radio = event.data
        self.color = GridLabel.getTypeColor(GridLabel.getTextType(toggled_radio))

    @staticmethod
    def getTypeColor(position_type: PositionType):
        colors = {
            PositionType.EMPTY: "white",
            PositionType.WALL: "black",
            PositionType.INITIAL: "darkGreen",
            PositionType.GOAL: "darkRed",
        }
        return colors[position_type]

    @staticmethod
    def getTextType(typeText: str) -> PositionType:
        types = {
            'agent': PositionType.INITIAL,
            'goal': PositionType.GOAL,
            'wall': PositionType.WALL,
            'empty': PositionType.EMPTY,
        }
        return types[typeText]



