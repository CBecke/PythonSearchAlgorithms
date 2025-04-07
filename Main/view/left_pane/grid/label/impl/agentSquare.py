from PyQt6.QtGui import QFont

from Main.view.left_pane.grid.label.square import Square


class AgentSquare(Square):

    def __init__(self, size):
        super().__init__(size, "darkGreen")
        super().setText("A")

    def __repr__(self):
        return "A"