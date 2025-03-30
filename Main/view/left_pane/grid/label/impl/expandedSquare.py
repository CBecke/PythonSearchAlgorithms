from Main.view.left_pane.grid.label.square import Square


class ExpandedSquare(Square):

    def __init__(self, size):
        super().__init__(size, "darkBlue")

    def __repr__(self):
        return "Exp"