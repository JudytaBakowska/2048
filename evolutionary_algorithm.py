# Funkcja generująca losową populację
import random
from main_no_GUI import board, single_player

def generate_population(pop_size):
    population = []
    for _ in range(pop_size):
        weights = [random.random() for _ in range(5)]  # Losowe wagi dla każdej heurystyki
        population.append(weights)
    return population

# Funkcja oceniająca populację na podstawie wyników
def evaluate_population(population, num_games):
    scores = []
    for weights in population:
        board.clear_board_values()
        total_score = single_player(num_games, weights)
        board.score = 0
        avg_score = total_score / num_games
        scores.append((weights, avg_score))
    return scores


# Funkcja selekcji osobników do reprodukcji
def select_parents(scores, num_parents):
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [x[0] for x in sorted_scores[:num_parents]]


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
                offspring[i][j] = random.random()
    return offspring


def algorithm(pop_size, num_generations, num_games, mutation_rate):
    population = generate_population(pop_size)
    best_weights = None
    for gen in range(num_generations):
        print(f"Generation {gen + 1}")
        scores = evaluate_population(population, num_games)
        parents = select_parents(scores, pop_size // 2)
        offspring = crossover(parents, pop_size - len(parents))
        offspring = mutate(offspring, mutation_rate)
        population = parents + offspring
        best_weights = max(scores, key=lambda x: x[1] if x[1] is not None else float('-inf'))[0]

    return best_weights
