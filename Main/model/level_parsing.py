import os

from Main.model.searchproblem.position_type import PositionType

def parse_rectangle(level):
    """
    Takes the path of a level as input and returns a 2d-list of int representing the level.
    In the representation, "0" is an empty square, "1" is a wall, "2" is the starting position,
    and "3" is a goal position.
    """

    char_mappings = {
        ' ': PositionType.EMPTY,
        '+': PositionType.WALL,
        'i': PositionType.INITIAL,
        'g': PositionType.GOAL,

    }

    print("\n\n___" + os.getcwd() + "___\n\n")
    with open(level, 'r') as file:
        parsed_level = []
        lines = file.readlines()[1:-1]   # skip walls; they are redundant
        for line in lines:
            current_line = []
            for char in line[1:-2]:      # skip walls and ending new line
                current_line.append(char_mappings[char])
            parsed_level.append(current_line)

    return parsed_level