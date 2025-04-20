program = """
print("first")

from Main.model.searchproblem.position import Position
from Main.model.searchproblem.search_node import SearchNode
from Main.model.searchproblem.search_problem import SearchProblem

def h(problem: SearchProblem, current: SearchNode) -> float | int:
    minimum_manhattan_dist = 1000000

    for goal in problem.find_goal_states():
        current_manhattan_dist = Position.manhattan_distance(current.state, goal)
        if current_manhattan_dist < minimum_manhattan_dist:
            minimum_manhattan_dist = current_manhattan_dist

    assert minimum_manhattan_dist >= 0, "incorrect manhattan distance"
    return minimum_manhattan_dist

print("second")

from Main.communication.publisher import Publisher
from Main.model.searchproblem.grid_problem import GridProblem
from Main.model.searchproblem.position import Position
from Main.model.searchproblem.position_type import PositionType
from Main.model.searchproblem.search_node import SearchNode

state = [[PositionType.INITIAL, PositionType.EMPTY, PositionType.EMPTY],
         [PositionType.EMPTY, PositionType.WALL, PositionType.EMPTY],
         [PositionType.EMPTY, PositionType.EMPTY, PositionType.GOAL]]

current = SearchNode(Position(0, 0), None, None, 0)
problem = GridProblem(state, Publisher())

print("third")

h(problem, current)

print("fourth")
"""

if __name__ == '__main__':
    exec(program)
    print("hi")