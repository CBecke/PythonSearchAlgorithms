from Main.view.left_pane.grid.label.square import Square



class ExpandedSquare(Square):
    def __init__(self, size, color):
        if color is None:
            color = "black"
        super().__init__(size, color)


    def __repr__(self):
        return "Exp"