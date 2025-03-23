from Main.view.left_pane.grid.label.square import Square


class WallSquare(Square):

    def __init__(self, size):
        super().__init__(size, "black")

    def __repr__(self):
        return "W"