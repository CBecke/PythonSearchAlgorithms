from Main.datastructures.Queue import Queue
from Main.searchproblem.GridProblem import GridProblem


def get_solution_path(predecessors, goal):
    """
    :param predecessors: Dictionary with Positions as keys and values. The value is the position that generated the key.
    :param goal: The goal state in the found solution
    :return: A list of Positions forming a path with the initial state at the head, and the goal state in the rear.
    """
    solution = []
    current = goal
    while current:
        solution.append(current)
        current = predecessors[current]

    solution.reverse()
    return solution


def BFS(grid_problem: GridProblem):
    initial_position = grid_problem.initial_state

    visited = {initial_position}
    predecessors = dict()
    predecessors[initial_position] = None

    # queue will contain doubles: the position as well as the node that generated the current one
    queue = Queue([initial_position])

    while not queue.is_empty():
        current_position = queue.pop()

        for action in grid_problem.actions(current_position):
            neighbor = grid_problem.result(current_position, action)

            if grid_problem.is_goal_state(neighbor):
                predecessors[neighbor] = current_position
                return get_solution_path(predecessors, neighbor)

            if neighbor not in visited:
                predecessors[neighbor] = current_position
                visited.add(neighbor)
                queue.push(neighbor)

    return []
