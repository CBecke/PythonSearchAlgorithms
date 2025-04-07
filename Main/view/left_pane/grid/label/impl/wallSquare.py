from PyQt6.QtGui import QFont

from Main.view.left_pane.grid.label.square import Square


class WallSquare(Square):

    def __init__(self, size):
        color = "black"
        super().__init__(size, color)
        super().setText("W")
        self.setStyleSheet(f"background-color: {color}; border: 1px solid gray; color: darkGray;")

    def __repr__(self):
        return "W"