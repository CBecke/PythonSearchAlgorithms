
class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return f'({self.row}, {self.column})'

    def __eq__(self, other):
        return (self.row, self.column) == (other.row, other.column)

    def __hash__(self):
        return hash((self.row, self.column))

    @staticmethod
    def manhattan_distance(position1, position2):
        return abs(position1.row - position2.row) + abs(position1.column - position2.column)