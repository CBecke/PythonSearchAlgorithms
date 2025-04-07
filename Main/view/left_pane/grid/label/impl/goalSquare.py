from PyQt6.QtGui import QFont

from Main.view.left_pane.grid.label.square import Square


class GoalSquare(Square):

    def __init__(self, size):
        super().__init__(size, "darkRed")
        super().setText("G")

    def __repr__(self):
        return "G"