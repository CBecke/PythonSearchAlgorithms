from Main.view.left_pane.grid.label.square import Square


class GeneratedSquare(Square):
    def __init__(self, size):
        super().__init__(size, "darkCyan")

    def __repr__(self):
        return "Gen"