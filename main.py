import pygame
import sys

import ai
from board import *
from button import Button
from ai import *

pygame.init()

# podstawowe parametry
width = 400
height = 500
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font(pygame.font.get_default_font(), 18)
title_font = pygame.font.Font(pygame.font.get_default_font(), 60)

bg = (238, 228, 218)
board = Board(0)


# wyswietlanie napisow w manu glownym
def draw_main_menu():
    title = title_font.render('2048', True, 'black')
    title_rect = title.get_rect()
    title_rect.center = (width // 2, 50)
    text1 = font.render('One player mode', True, 'black')
    text2 = font.render('Two players mode', True, 'black')
    screen.blit(title, title_rect)
    screen.blit(text1, (30, 250))
    screen.blit(text2, (215, 250))


# funkcja sterujaca gra w trybie jednoosobowym
def single_player():
    game_over = False
    spawn_new = True
    init_count = 0
    direction = ''

    run_game = True
    while run_game:
        timer.tick(fps)
        screen.fill('gray')
        board.draw_board(width, height, screen)
        board.draw_pieces(width, screen)

        # gdy nacisiniemy przycisk "main menu", przerwij gre
        if main_menu_button.draw(screen):
            run_game = False
            board.score = 0

        # ruch komputera - generowanie nowego pola
        if spawn_new or init_count < 2:
            init_count += 1
            game_over = board.random_piece()
            spawn_new = False
            ai.create_minimax_tree(2, board.board_values)
            direction = get_move()

        # wczytanie i wykonanie ruchu gracza
        if direction != '':
            board.take_turn(direction)
            direction = ''
            spawn_new = True

        if game_over:
            board.draw_game_over(screen)

        # zapamietywanie wprowadzonego ruchu przez gracza
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'

        pygame.display.flip()


# funkcja obslugujaca tryb gry dla dwoch graczy
# def multi_player():
#     game_over = False
#     spawn_new = False
#     spawn_initial_pieces = True
#     direction = ''
#     board.score = 0
#
#     run_game = True
#     while run_game:
#         timer.tick(fps)
#         screen.fill('gray')
#         board.draw_board(width, height, screen)
#         board.draw_pieces(width, screen)
#
#         if main_menu_button.draw(screen):
#             run_game = False
#             board.score = 0
#
#         if spawn_initial_pieces:
#             board.random_piece()
#             board.random_piece()
#             spawn_initial_pieces = False
#
#         if spawn_new:  # ruch gracza sterujacego mysza
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     sys.exit()
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     x, y = pygame.mouse.get_pos()
#                     if event.button == 1:  # kliknieto lewy przycisk myszy
#                         if board.check_place(x, y, 2):
#                             board.check_game_over()
#                             spawn_new = False
#                     elif event.button == 3:  # kliknieto prawy przycisk myszy
#                         if board.check_place(x, y, 4):
#                             board.check_game_over()
#                             spawn_new = False
#
#         if direction != '':
#             board.take_turn(direction)
#             direction = ''
#             spawn_new = True
#
#         if game_over:
#             board.draw_game_over(screen)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_UP:
#                     direction = 'UP'
#                 elif event.key == pygame.K_RIGHT:
#                     direction = 'RIGHT'
#                 elif event.key == pygame.K_DOWN:
#                     direction = 'DOWN'
#                 elif event.key == pygame.K_LEFT:
#                     direction = 'LEFT'
#
#         pygame.display.flip()


# wczytanie przyciskow i umieszczenie ich w oknie
start_img = pygame.image.load('button_start.png').convert_alpha()
main_menu_img = pygame.image.load('button_main-menu.png').convert_alpha()
single_player_button = Button(50, 300, start_img, 0.8)
multi_player_button = Button(235, 300, start_img, 0.8)
main_menu_button = Button(200, height - 75, main_menu_img, 0.7)

# glowna petla programu
run = True
while run:
    screen.fill(bg)
    draw_main_menu()
    if single_player_button.draw(screen):
        board.clear_board_values()
        single_player()
    if multi_player_button.draw(screen):
        board.clear_board_values()
        multi_player()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
