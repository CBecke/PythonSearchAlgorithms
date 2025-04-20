from Main.model import level_parsing
from Main.model.searchproblem.position_type import PositionType


def test_single_goal():
    # Given a level with initial position (1,1) and goal position (8,6)
    import os
    level_path = r"resources/levels/simple_open.txt"
    # When the level is parsed
    parsed_level = level_parsing.parse_rectangle(level_path)
    # Then the correct grid is returned
    assert parsed_level == [[PositionType.INITIAL, PositionType.EMPTY, PositionType.EMPTY, PositionType.EMPTY],
                           [PositionType.EMPTY,   PositionType.EMPTY, PositionType.EMPTY, PositionType.GOAL]]

def test_three_goals():
    # Given a level with initial position (0,0) and goal positions (0,2), (1,1), and (1,3)
    level_path = r"resources/levels/simple_open_3goals.txt"
    # When the level is parsed
    parsed_level = level_parsing.parse_rectangle(level_path)
    # Then the correct grid is returned
    assert parsed_level == [[PositionType.INITIAL, PositionType.EMPTY, PositionType.GOAL, PositionType.EMPTY],
                           [PositionType.EMPTY, PositionType.GOAL, PositionType.EMPTY, PositionType.GOAL]]

