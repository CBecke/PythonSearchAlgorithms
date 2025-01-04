from Main import LevelParsing
from Main.searchproblem.PositionType import PositionType


def test_single_goal():
    # Given a level with initial position (1,1) and goal position (8,6)
    levelPath = r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\simple_open.txt"
    # When the level is parsed
    parsedLevel = LevelParsing.parse_rectangle(levelPath)
    # Then the correct grid is returned
    assert parsedLevel == [[PositionType.INITIAL.value, PositionType.EMPTY.value, PositionType.EMPTY.value, PositionType.EMPTY.value],
                           [PositionType.EMPTY.value,   PositionType.EMPTY.value, PositionType.EMPTY.value, PositionType.GOAL.value]]

def test_three_goals():
    # Given a level with initial position (0,0) and goal positions (0,2), (1,1), and (1,3)
    levelPath = r"C:\Users\chris\PycharmProjects\SearchAlgorithms\Test\resources\levels\simple_open_3agents.txt"
    # When the level is parsed
    parsedLevel = LevelParsing.parse_rectangle(levelPath)
    # Then the correct grid is returned
    assert parsedLevel == [[PositionType.INITIAL.value, PositionType.EMPTY.value, PositionType.GOAL.value, PositionType.EMPTY.value],
                           [PositionType.EMPTY.value, PositionType.GOAL.value, PositionType.EMPTY.value, PositionType.GOAL.value]]

