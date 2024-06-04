import random

import metrics


class Board:
    def __init__(self, score=0):
        self.grid = [0 for _ in range(16)]
        self.score = [score]

    def swipe_grid(self, direction):
        self.grid = metrics.swipe_grid(self.grid, direction, self.score)

    def random_piece(self):
        if 0 in self.grid:
            while True:
                pos = random.randint(0, 15)
                if self.grid[pos] == 0:
                    if random.randint(0, 9) < 2:  # 20% chance for value '4'
                        self.grid[pos] = 4
                    else:
                        self.grid[pos] = 2
                    return

    def clear_grid(self):
        self.grid = [0 for _ in range(16)]

    def game_over(self):

        if 0 in self.grid:
            return False

        # checking rows
        for i in range(3):
            for j in range(4):
                if self.grid[i + j * 4] == self.grid[i + 1 + j * 4]:
                    return False

        for i in range(4):
            for j in range(3):
                if self.grid[i + j * 4] == self.grid[i + (j + 1) * 4]:
                    return False

        return True

    def move_possible(self, direction):
        return metrics.move_possible(self.grid, direction)

    def print_grid(self):
        for i in range(4):
            for j in range(4):
                print(self.grid[i * 4 + j], " ", end="")
            print()
        print()

    def max_tile(self):
        return max(self.grid)
