def swipe_grid(grid, direction):
    temp = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    if direction == 'UP':
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * j])

            row = swipe_row(row)

            for j in range(4):
                temp[i + 4 * j] = row[j]

    elif direction == 'DOWN':
        for i in range(4):
            row = []
            for j in range(3, -1, -1):
                row.append(grid[i + 4 * j])
            row = swipe_row(row)
            k = 0
            for j in range(3, -1, -1):
                temp[i + 4 * j] = row[k]
                k += 1

    elif direction == 'LEFT':
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i * 4 + j])
            row = swipe_row(row)
            for j in range(4):
                temp[i * 4 + j] = row[j]

    elif direction == 'RIGHT':
        for i in range(4):
            row = []
            for j in range(3, -1, -1):
                row.append(grid[i * 4 + j])
            row = swipe_row(row)
            k = 0
            for j in range(3, -1, -1):
                temp[4 * i + j] = row[k]
                k += 1
    return temp


def swipe_row(row):
    previous = -1  # previous non-zero element
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:

        if element != 0:
            if previous == -1:
                previous = element
                temp[i] = element
                i += 1
            elif previous == element:
                temp[i - 1] = 2 * element
                previous = -1
            else:
                previous = element
                temp[i] = element
                i += 1
    return temp


def move_possible(grid, direction):
    if grid == swipe_grid(grid, direction):
        return False
    else:
        return True


def empty_tiles_heuristic(grid):
    zeros = 0
    for i in range(16):
        if grid[i] == 0:
            zeros += 1

    return zeros


# Heuristic giving bonus points for maximum value on the board
def max_value_heuristic(grid):
    maximum_value = -1
    for i in range(16):
        maximum_value = max(maximum_value, grid[i])

    return maximum_value


# Heuristic giving bonus points for minimizing differences between adjacent tiles
def smoothness_heuristic(grid):
    smoothness = 0
    for i in range(4):
        current = 0
        while current < 4 and grid[4 * i + current] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[i * 4 + next] == 0:
                next += 1
            if next >= 4:
                break

            current_value = grid[i * 4 + current]
            next_value = grid[i * 4 + next]
            smoothness -= abs(current_value - next_value)

            current = next
            next += 1

    for i in range(4):
        current = 0
        while current < 4 and grid[current * 4 + i] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[4 * next + i]:
                next += 1
            if next >= 4:
                break

            current_value = grid[current * 4 + i]
            next_value = grid[next * 4 + i]
            smoothness -= abs(current_value - next_value)

            current = next
            next += 1

    return smoothness * 10


# Heurisitc giving bonus poitns for monotonic rows of tiles
def monotonicity_heurictic(grid):
    monotonicity_scores = [0, 0, 0, 0]

    # left/right direction
    for i in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and grid[i * 4 + next] == 0:
                next += 1

            if next >= 4:
                next -= 1
            current_value = grid[i * 4 + current]
            next_value = grid[i * 4 + next]

            if current_value > next_value:
                monotonicity_scores[0] += next_value - current_value
            elif next_value > current_value:
                monotonicity_scores[1] += current_value - next_value

            current = next
            next += 1

        # up/down direction
        for i in range(4):
            current = 0
            next = current + 4
            while next < 4:
                while next < 4 and grid[i + 4 * next] == 0:
                    next += 1

                if next >= 4:
                    next -= 1
                current_value = grid[i + 4 * current]
                next_value = grid[i + 4 * next]

                if current_value > next_value:
                    monotonicity_scores[2] += next_value - current_value
                elif next_value > current_value:
                    monotonicity_scores[3] += current_value - next_value
            current = next
            next += 1

    return 20 * max(monotonicity_scores[0], monotonicity_scores[1]) + max(monotonicity_scores[2],
                                                                          monotonicity_scores[3])


# Heuristic giving bonus points for placing tile with maximum value at the corner of the board
def position_of_max_value_heuristic(grid):
    max_value = max_value_heuristic(grid)
    if max_value == grid[0] or max_value == grid[3] or max_value == grid[12] or max_value == grid[15]:
        return 5000
    else:
        return -5000


# Heuristic using weighted grid to determine how many bonus points we are supposed to give
def weighted_tiles_heuristic(grid):
    score_grid = [4 ** 15, 4 ** 14, 4 ** 13, 4 ** 12,
                  4 ** 8, 4 ** 9, 4 ** 10, 4 ** 11,
                  4 ** 7, 4 ** 6, 4 ** 5, 4 ** 4,
                  4 ** 0, 4 ** 1, 4 ** 2, 4 ** 3]

    score = 0
    for i in range(16):
        score += grid[i] * score_grid[i]

    return score


# 1-dim grid!!!
def get_score(grid):
    empty_tiles_score = empty_tiles_heuristic(grid) * 100
    max_value_score = max_value_heuristic(grid) * 4
    smoothness_score = smoothness_heuristic(grid) * 10
    monotonicity_score = monotonicity_heurictic(grid) * 60
    weighted_tiles_score = weighted_tiles_heuristic(grid)

    return smoothness_score + empty_tiles_score + monotonicity_score
