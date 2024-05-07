import ai
from board import *
import evolutionary_algorithm

board = Board(0)

def single_player(num_games, weights):
    for _ in range(num_games):
        game_over = False
        spawn_new = True
        init_count = 0
        direction = ''

        run_game = True
        while run_game:
            # ruch komputera-generowanie nowego pola
            if spawn_new or init_count < 2:
                init_count += 1
                game_over = board.random_piece()
                spawn_new = False
                ai.create_minimax_tree(2, board.board_values, weights)
                direction = ai.get_move()

            # wczytanie i wykonanie ruchu gracza
            if direction != '':
                board.take_turn(direction)
                direction = ''
                spawn_new = True

            if game_over:
                print("Final board: ")
                for row in board.board_values:
                    print(row)
                print(f"Points: {board.score}\n")
                return board.score


if __name__ == "__main__":
    best_weights_result = evolutionary_algorithm.algorithm(pop_size=5, num_generations=1, num_games=2, mutation_rate=0.1)
    print("Best weights:", best_weights_result)
