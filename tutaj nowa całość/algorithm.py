import math

import metrics

# node_scores = {}
# child_list = {}
# node_number = 0

node_scores = [0 for _ in range(50000)]
child_list = [[0 for _ in range(0)] for _ in range(50000)]
node_number = 1

directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']


def create_minimax_tree(depth, grid, *parameters):
    global node_scores
    global child_list
    global node_number
    node_scores = {}
    child_list = {}
    node_number = 1

    node_scores = [0 for _ in range(50000)]
    child_list = [[0 for _ in range(0)] for _ in range(50000)]
    node_number = 1

    alpha_beta_pruning(1, grid, 0, depth, -math.inf, math.inf, *parameters)

    # expectiminimax(1, grid, 0, depth, *parameters)


def expectiminimax(node, grid, parent, depth, *parameters):
    global node_scores
    global child_list
    global node_number

    print(f"Node: {node}, Depth: {depth}, Grid: {grid}")

    if depth == 0:
        score = metrics.get_score(grid, *parameters)
        node_scores[node] = score
        return score

    if node not in child_list:
        child_list[node] = []

    if depth % 2 == 0:  # Player's turn
        max_value = -math.inf
        for direction in directions:
            if metrics.move_possible(grid, direction):
                new_grid = metrics.swipe_grid(grid, direction)
                node_number += 1
                child_list[node].append(node_number)
                max_value = max(max_value, expectiminimax(node_number, new_grid, node, depth - 1, *parameters))
        node_scores[node] = max_value
        return max_value

    else:  # Random tile spawning
        zeros = [i for i in range(16) if grid[i] == 0]
        if not zeros:
            print("NOT ZEROS")
            return metrics.get_score(grid, *parameters)

        expected_value = 0
        num_zeros = len(zeros)
        for zero in zeros:
            # Spawn '2' with probability 0.9
            grid_copy2 = grid[:]
            grid_copy2[zero] = 2
            node_number += 1
            child_list[node].append(node_number)
            expected_value += 0.9 * expectiminimax(node_number, grid_copy2, node, depth - 1, *parameters)

            # Spawn '4' with probability 0.1
            grid_copy4 = grid[:]
            grid_copy4[zero] = 4
            node_number += 1
            child_list[node].append(node_number)
            expected_value += 0.1 * expectiminimax(node_number, grid_copy4, node, depth - 1, *parameters)

        expected_value /= num_zeros
        node_scores[node] = expected_value
        return expected_value


def alpha_beta_pruning(node, grid, parent, depth, alpha, beta, *parameters):
    global node_scores
    global child_list
    global node_number
    if depth == 0:
        node_scores[node] = metrics.get_score(grid, *parameters)
        return node_scores[node]

    # move performing
    if depth % 2 == 0:
        for i in range(4):
            node_number += 1
            child_list[node].append(node_number)
            if metrics.move_possible(grid, directions[i]):
                new_grid = metrics.swipe_grid(grid, directions[i])
                alpha = max(alpha, alpha_beta_pruning(node_number, new_grid, node, depth - 1, alpha, beta, *parameters))
            if alpha >= beta:
                break
        node_scores[node] = alpha
        return alpha

    # spawning random tile
    else:
        zeros = []

        for i in range(16):
            if grid[i] == 0:
                zeros.append(i)

        grid_table = [[0 for _ in range(16)] for _ in range(0)]
        grid_table_scores = []

        for i in zeros:
            grid[i] = 2
            grid_table.append(grid)
            grid[i] = 0

        for i in zeros:
            grid[i] = 4
            grid_table.append(grid)
            grid[i] = 0

        for i in grid_table:
            grid_table_scores.append(metrics.get_score(i, *parameters))

        for i in range(4):
            minimum_score = min(grid_table_scores)
            index = grid_table_scores.index(minimum_score)

            node_number += 1
            child_list[node].append(node_number)
            beta = min(beta,
                       alpha_beta_pruning(node_number, grid_table[index], node, depth - 1, alpha, beta, *parameters))

            if beta <= alpha:
                break

            grid_table_scores[index] = math.inf

        node_scores[node] = beta
        return beta


def get_move():
    searched_value = node_scores[1]

    for index, i in enumerate(child_list[1]):
        if node_scores[i] == searched_value:
            return directions[index]
