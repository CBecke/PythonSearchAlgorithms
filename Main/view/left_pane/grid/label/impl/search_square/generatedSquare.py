from Main.view.left_pane.grid.label.impl.emptySquare import EmptySquare
from Main.view.left_pane.grid.label.square import Square


class GeneratedSquare(Square):
    def __init__(self, size):
        super().__init__(size, "darkGray")


    def __repr__(self):
        return "Gen"