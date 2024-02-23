

def parseRectangle(level):
    """
    Takes the path of a level as input and returns a 2d-list of int representing the level.
    In the representation, "0" is an empty square, "1" is a wall, "2" is the starting position,
    and "3" is a goal position.
    """

    charMappings = {
        ' ': 0,
        '+': 1,
        'i': 2,
        'g': 3
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
