import math
import metrics


def get_move():
    searched_value = node_scores[1]
    children = child_list.get(1, [])

    for index, i in enumerate(children):
        if node_scores.get(i) == searched_value:
            return directions[index]


node_scores = {}
child_list = {}
node_number = 1
state = 0

directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']


def create_expectimax_tree(depth, grid, *parameters):
    global node_scores
    global child_list
    global node_number
    node_scores = {}
    child_list = {}
    node_number = 1

    expectimax(1, grid, 0, depth, *parameters)


def expectimax(node, grid, parent, depth, *parameters):
    global node_scores
    global child_list
    global node_number

    if depth == 0:
        node_scores[node] = metrics.get_score(grid, *parameters)
        return node_scores[node]

    if depth % 2 == 0:  # Maximize player's turn
        alpha = -math.inf
        for i in range(4):
            node_number += 1
            child_list.setdefault(node, []).append(node_number)
            if metrics.move_possible(grid, directions[i]):
                new_grid = metrics.swipe_grid(grid, directions[i])
                alpha = max(alpha, expectimax(node_number, new_grid, node, depth - 1, *parameters))
        node_scores[node] = alpha
        return alpha
    else:  # Random event (tile spawn)
        expected_value = 0
        zeros = [i for i, x in enumerate(grid) if x == 0]

        for i in zeros:
            grid[i] = 2
            expected_value += 0.8 * expectimax(node_number, grid, node, depth - 1, *parameters) # 80% chance 2
            grid[i] = 0

            grid[i] = 4
            expected_value += 0.2 * expectimax(node_number, grid, node, depth - 1, *parameters) # 20% chance 4
            grid[i] = 0

        expected_value /= len(zeros)

        node_scores[node] = expected_value
        return expected_value
