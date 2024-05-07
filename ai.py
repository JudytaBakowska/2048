import math
from heuristics import *

node_scores = [0 for _ in range(50000)]
child_list = [[0 for _ in range(0)] for _ in range(50000)]

node_number = 1
directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']


def create_minimax_tree(depth, board_values, weights):
    global node_scores
    global child_list
    global node_number
    node_scores = [0 for _ in range(50000)]
    child_list = [[0 for _ in range(0)] for y in range(50000)]
    node_number = 1
    grid = [element for row in board_values for element in row]  # zamieniamy na 1-dim

    alpha_beta_pruning(1, grid, 0, depth, -math.inf, math.inf, weights)


def alpha_beta_pruning(node, grid, parent, depth, alpha, beta, weights):
    global node_scores
    global child_list
    global node_number
    if depth == 0:
        node_scores[node] = get_score(grid, weights)
        return node_scores[node]

    #player's turn - moze zmienic potem?
    if depth % 2 == 0:
        for i in range(4):
            node_number += 1
            child_list[node].append(node_number)
            if move_possible(grid, directions[i]):
                alpha = max(alpha, alpha_beta_pruning(node_number, swipe_grid(grid, directions[i]), node, depth-1, alpha, beta, weights))
            if alpha >= beta:
                break
        node_scores[node] = alpha
        return alpha

    #the turn of computer
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
            grid_table_scores.append(get_score(i, weights))

        for i in range(4):
            minimum_score = min(grid_table_scores)
            index = grid_table_scores.index(minimum_score)

            node_number += 1
            child_list[node].append(node_number)
            beta = min(beta, alpha_beta_pruning(node_number, grid_table[index], node, depth-1, alpha, beta, weights))

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

