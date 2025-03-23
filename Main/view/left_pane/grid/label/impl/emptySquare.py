from Main.view.left_pane.grid.label.square import Square


class EmptySquare(Square):

    def __init__(self, size):
        super().__init__(size, "white")

    def __repr__(self):
        return "E"