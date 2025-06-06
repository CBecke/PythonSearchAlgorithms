from Main.communication.publisher import Publisher
from Main.model.searchproblem.grid_problem import GridProblem
from Main.model import level_parsing
from Main.model.searchproblem import position

def test_initialization():
    level_path = r"resources/levels/simple_open_3goals.txt"
    parsed_level = level_parsing.parse_rectangle(level_path)
    gp = GridProblem(parsed_level, Publisher())

    goal_states = {position.Position(1, 1),
                   position.Position(0, 2),
                   position.Position(1, 3)}

    assert (gp.find_initial_state() == position.Position(0, 0) and
            gp.find_goal_states() == goal_states)