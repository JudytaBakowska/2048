import pygame
import random

pygame.init()

colors = {0: (204, 192, 179),
                       2: (238, 228, 218),
                       4: (237, 224, 200),
                       8: (242, 177, 121),
                       16: (245, 149, 99),
                       32: (246, 124, 95),
                       64: (246, 94, 59),
                       128: (237, 207, 114),
                       256: (237, 204, 97),
                       512: (237, 200, 80),
                       1024: (237, 197, 63),
                       2048: (237, 194, 46),
                       'light text': (249, 246, 242),
                       'dark text': (119, 110, 101),
                       'other': (0, 0, 0),
                       'bg': (187, 173, 160)}
font = pygame.font.Font(pygame.font.get_default_font(), 24)
title_font = pygame.font.Font(pygame.font.get_default_font(), 60)

class Board:
    def __init__(self, score):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        self.score = score
        self.tiles_coordinates = [[(0, 0) for _ in range(4)] for _ in range(4)]
        self.block_size = 0

    def draw_board(self, width, height, screen):
        # global colors
        pygame.draw.rect(screen, colors['bg'], [0, 0, height - 100, width], 0, 20)
        score_text = font.render(f'Score: {self.score}', True, 'black')
        screen.blit(score_text, (10, height - 90))

    def random_piece(self):
        if any(0 in row for row in self.board_values):
            placed = False
            while not placed:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
                if self.board_values[row][col] == 0:
                    if random.randint(0, 9) < 2:  # 20% szans na pojawienie sie 4
                        self.board_values[row][col] = 4
                    else:
                        self.board_values[row][col] = 2
                    placed = True
            return False
        return self.check_game_over()

    def clear_board_values(self):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]

    def check_game_over(self):
        for row in self.board_values:
            for col in range(len(row) - 1):
                if row[col] == row[col + 1]:
                    return False
        for col in range(len(self.board_values[0])):
            for row in range(len(self.board_values) - 1):
                if self.board_values[row][col] == self.board_values[row + 1][col]:
                    return False
        return True

    def draw_pieces(self, width, screen):
        for i in range(len(self.board_values)):
            for j in range(len(self.board_values[0])):
                value = self.board_values[i][j]
                if value > 8:
                    value_color = colors['light text']  # dla ciemnych klockow uzywamy jasnej czcionki
                else:
                    value_color = colors['dark text']
                if value <= 2048:
                    color = colors[value]
                else:
                    color = colors['other']
                space = (width * 0.25) / 5  # przestrzen pomiedzy klockami
                block = (width * 0.75) / 4  # szerokosc klocka
                self.block_size = block
                left = j * (block + space) + space  # koordynaty lewej granicy klocka
                up = i * (block + space) + space  # koordynaty gornej granicy klocka

                self.tiles_coordinates[i][j] = (left, up)  # potrzebne do sprawdzania, jaki klocek zostal klikniety (tryb multiplayer)
                pygame.draw.rect(screen, color, [left, up, block, block], 0, 5)

                if value > 0:  # dla wartosci 0 nie wyswietlamy tekstu
                    value_len = len(str(value))
                    value_font = pygame.font.Font(pygame.font.get_default_font(),
                                                  48 - (5 * value_len))  # zmniejszanie czcionki wraz z dlugoscia tekstu
                    value_text = value_font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(
                        center=(j * (block + space) + block / 2 + space, i * (
                                    block + space) + block / 2 + space))  # wyliczanie pozycji tekstu kazdego klocka (jego srodek)
                    screen.blit(value_text, text_rect)

    # funkcja sprawdza czy klikniete pole (tryb multiplayer) jest wolne - jesli tak, pojawia sie tam nowy klocek
    def check_place(self, x, y, value):
        for i in range(len(self.board_values)):
            for j in range(len(self.board_values[0])):
                if self.tiles_coordinates[i][j][0] <= x <= self.tiles_coordinates[i][j][0] + self.block_size \
                        and self.tiles_coordinates[i][j][1] <= y <= self.tiles_coordinates[i][j][1] + self.block_size:
                    if self.board_values[i][j] == 0:
                        self.board_values[i][j] = value
                        return True
                    else:
                        return False
        return False

    # przesuwanie klockow w gore
    def move_up(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(1, 4):
            for j in range(4):
                shift = 0
                for k in range(i):
                    if self.board_values[k][j] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i - shift][j] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if i - shift - 1 >= 0 and self.board_values[i - shift - 1][j] == self.board_values[i - shift][j] \
                        and not merged[i - shift - 1][j] and not merged[i - shift][j]:
                    self.board_values[i - shift - 1][j] *= 2
                    self.score += self.board_values[i - shift - 1][j]
                    self.board_values[i - shift][j] = 0
                    merged[i - shift - 1][j] = True

    # przesuwanie klockow w dol
    def move_down(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(2, -1, -1):
            for j in range(4):
                shift = 0
                for k in range(i + 1, 4):
                    if self.board_values[k][j] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i + shift][j] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if i + shift + 1 <= 3 and self.board_values[i + shift + 1][j] == self.board_values[i + shift][j] \
                        and not merged[i + shift + 1][j] and not merged[i + shift][j]:
                    self.board_values[i + shift + 1][j] *= 2
                    self.score += self.board_values[i + shift + 1][j]
                    self.board_values[i + shift][j] = 0
                    merged[i + shift + 1][j] = True

    # przesuwanie klockow w prawo
    def move_right(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(2, -1, -1):
                shift = 0
                for k in range(j + 1, 4):
                    if self.board_values[i][k] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i][j + shift] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if j + shift + 1 <= 3 and self.board_values[i][j + shift + 1] == self.board_values[i][j + shift] \
                        and not merged[i][j + shift + 1] and not merged[i][j + shift]:
                    self.board_values[i][j + shift + 1] *= 2
                    self.score += self.board_values[i][j + shift + 1]
                    self.board_values[i][j + shift] = 0
                    merged[i][j + shift + 1] = True

    # przesuwanie klockow w lewo
    def move_left(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(1, 4):
                shift = 0
                for k in range(j):
                    if self.board_values[i][k] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i][j - shift] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if j - shift - 1 >= 0 and self.board_values[i][j - shift - 1] == self.board_values[i][j - shift] \
                        and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    self.board_values[i][j - shift - 1] *= 2
                    self.score += self.board_values[i][j - shift - 1]
                    self.board_values[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    # wywolywanie odpowiedniej funkcji przesuniecia w zaleznosci od ruchu gracza
    def take_turn(self, direction):
        if direction == 'UP':
            self.move_up()
        elif direction == 'RIGHT':
            self.move_right()
        elif direction == 'DOWN':
            self.move_down()
        elif direction == 'LEFT':
            self.move_left()

    # wyswietlanie komunikatu o zakonczeniu gry
    def draw_game_over(self, screen):
        pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
        game_over_text = font.render('GAME OVER', True, 'white')
        screen.blit(game_over_text, (130, 65))
