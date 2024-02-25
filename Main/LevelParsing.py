
from Main.searchproblem.PositionType import PositionType

def parse_rectangle(level):
    """
    Takes the path of a level as input and returns a 2d-list of int representing the level.
    In the representation, "0" is an empty square, "1" is a wall, "2" is the starting position,
    and "3" is a goal position.
    """

    charMappings = {
        ' ': PositionType.EMPTY.value,
        '+': PositionType.WALL.value,
        'i': PositionType.INITIAL.value,
        'g': PositionType.GOAL.value
    }

    file = open(level, 'r')
    parsedLevel = []

    lines = file.readlines()[1:-1]   # skip walls; they are redundant
    for line in lines:
        currentLine = []
        for char in line[1:-2]:      # skip walls and ending new line
            currentLine.append(charMappings[char])
        parsedLevel.append(currentLine)

    file.close()
    return parsedLevel
