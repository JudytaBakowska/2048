from board import *
from ai import *

board = Board(0)

def single_player(num_games):
    for _ in range(num_games):
        game_over = False
        spawn_new = True
        init_count = 0
        direction = ''

        run_game = True
        while run_game:

            # ruch komputera - generowanie nowego pola
            if spawn_new or init_count < 2:
                init_count += 1
                game_over = board.random_piece()
                spawn_new = False
                create_minimax_tree(2, board.board_values, 0.8)
                direction = get_move()

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
                return



if __name__ == "__main__":
    num_games = int(input("Enter number of games to play automatically: "))
    actual_game = 0
    run = True
    while run:
        if actual_game < num_games:
            actual_game %= num_games
            actual_game += 1
            board.clear_board_values()
            single_player(num_games)
            board.score = 0
        else:
            break