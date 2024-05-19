import random
from board import *
import algorithm
import numpy as np
import os


def generate_random_population(pop_size):
    population = []
    for _ in range(pop_size):
        # dodalem tutaj zaokraglenie do 6 cyfr zeby wygodniej sie nam testowalo
        weights = [round(random.random(),6) for _ in range(5)]  # Losowe wagi dla każdej heurystyki
        population.append(weights)
    return tuple(population)


# Funkcja oceniająca populację na podstawie wyników
def evaluate_population(population, num_games):
    scores = []

    for parameters in population:
        score_sum = 0
        for _ in range(num_games):
            score_sum += play_single_game(*parameters)

        avg_score = score_sum // num_games
        scores.append((parameters, avg_score))

    return scores


# Funkcja selekcji osobników do reprodukcji
def select_parents(scores, num_parents):
    # total_sum = sum(scores)
    total_sum = sum(x[1] for x in scores)

    weights_of_score = [x[1] / total_sum for x in scores]

    drawn_parents_unique = []

    only_scores = [score[1] for score in scores]

    # Continue drawing until we have exactly 'num_parents' unique values
    while len(drawn_parents_unique) < num_parents:
        # Draw a number based on the weights

        drawn_number = random.choices(only_scores, weights=weights_of_score)[0]
        # If the drawn number is not already in the list, add it
        if drawn_number not in drawn_parents_unique:
            drawn_parents_unique.append(drawn_number)

    parents = [parameters[0] for parameters in scores if parameters[1] in drawn_parents_unique]
    return parents


# Funkcja krzyżowania osobników
def crossover(parents, offspring_size):
    offspring = []
    for _ in range(offspring_size):
        parent1, parent2 = random.sample(parents, 2)
        child = [random.choice(gene_pair) for gene_pair in zip(parent1, parent2)]
        offspring.append(child)
    return offspring


# Funkcja mutacji osobników
def mutate(offspring, mutation_rate):
    for i in range(len(offspring)):
        for j in range(len(offspring[i])):
            if random.random() < mutation_rate:
                offspring[i][j] = round(random.random(),6)
    return offspring


def genetic_algorithm(pop_size, num_generations, num_games, mutation_rate, save_results):
    population = generate_random_population(pop_size)
    file_num = return_file_number()
    best_weights = None
    for gen in range(num_generations):
        print(f"Generation {gen + 1}")
        scores = evaluate_population(population, num_games)
        parents = select_parents(scores, pop_size // 2)
        offspring = crossover(parents, pop_size - len(parents))
        offspring = mutate(offspring, mutation_rate)

        only_scores = [score[1] for score in scores]

        if save_results:
            save_to_file(file_num, gen+1, population, only_scores)

        population = parents + offspring
        best_weights = max(scores, key=lambda x: x[1] if x[1] is not None else float('-inf'))[0]
        print("Mean score: ", np.mean(only_scores))

    return best_weights


def play_single_game(*params):
    board = Board()
    game_over = False

    # generating two blocks at the beginning
    for _ in range(2):
        board.random_piece()

    while not game_over:
        algorithm.create_minimax_tree(2, board.grid, *params)
        direction = algorithm.get_move()
        board.swipe_grid(direction)
        board.random_piece()
        game_over = board.game_over()

    return board.score[0]


def return_file_number():
    counter = 1
    while os.path.exists(f"results{counter}.txt"):
        counter += 1

    return counter


def save_to_file(file_num, generation, population, scores):
    filename = f"results{file_num}.txt"

    with open(filename, "a") as file:
        file.write(f"{generation},{population},{scores}\n") # dodac najwiekszy kafelek

