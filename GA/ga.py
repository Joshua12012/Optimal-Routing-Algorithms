import random
import numpy as np
import datetime
# Parameters
POPULATION_SIZE = 200  # Increased population size
NUM_GENERATIONS = 10
MUTATION_RATE = 0.5 # Further increased mutation rate

# Define waypoints and costs (with bidirectional pairs)
waypoints = ['A', 'B', 'C', 'D', 'E', 'F']
distances = {
    ('A', 'B'): 100, ('B', 'A'): 110,
    ('A', 'C'): 80, ('C', 'A'): 85,
    ('A', 'D'): 120, ('D', 'A'): 125,
    ('A', 'E'): 200, ('E', 'A'): 210,
    ('A', 'F'): 180, ('F', 'A'): 185,
    ('B', 'C'): 90, ('C', 'B'): 95,
    ('B', 'D'): 70, ('D', 'B'): 75,
    ('B', 'E'): 140, ('E', 'B'): 145,
    ('B', 'F'): 130, ('F', 'B'): 135,
    ('C', 'D'): 110, ('D', 'C'): 115,
    ('C', 'E'): 85, ('E', 'C'): 90,
    ('C', 'F'): 150, ('F', 'C'): 155,
    ('D', 'E'): 100, ('E', 'D'): 105,
    ('D', 'F'): 60, ('F', 'D'): 65,
    ('E', 'F'): 95, ('F', 'E'): 100
}


# Fitness function (inverse of distance)
def fitness(route):
    total_distance = 0
    for i in range(len(route) - 1):
        pair = (route[i], route[i + 1])
        if pair in distances:
            total_distance += distances[pair]
        else:
            # Assign a high penalty for missing distances
            total_distance += 1000  # You can adjust this penalty as needed
    
    # Add the distance from the last city back to the first city
    last_pair = (route[-1], route[0])
    if last_pair in distances:
        total_distance += distances[last_pair]
    else:
        total_distance += 1000

    return 1 / total_distance if total_distance > 0 else 0


# Generate initial population
def initial_population():
    population = []
    for _ in range(POPULATION_SIZE):
        route = random.sample(waypoints, len(waypoints))
        population.append(route)
    return population


# Roulette wheel selection
def roulette_wheel_selection(population):
    max_fitness = sum([fitness(individual) for individual in population])
    pick = random.uniform(0, max_fitness)
    current = 0
    for individual in population:
        current += fitness(individual)
        if current > pick:
            return individual


# Uniform crossover for diversity
def ordered_crossover(parent1, parent2):
    size = len(parent1)
    child = [None] * size

    # Choose random start/end points for crossover
    start, end = sorted(random.sample(range(size), 2))

    # Copy the segment from parent1
    child[start:end + 1] = parent1[start:end + 1]

    # Fill the remaining positions with values from parent2
    pointer = end + 1
    for item in parent2:
        if item not in child:
            if pointer >= size:
                pointer = 0
            while child[pointer] is not None:
                pointer += 1
                if pointer >= size:
                    pointer = 0
            child[pointer] = item

    return child


def resolve_duplicates(child, parent1, parent2):
    # Remove duplicates and replace with missing elements
    unique_genes = set(child)
    missing_genes = [gene for gene in parent1 if gene not in unique_genes]
    idx = 0
    for i in range(len(child)):
        if child.count(child[i]) > 1:
            child[i] = missing_genes[idx]
            idx += 1
    return child


# Mutation with shuffling subsections
def enhanced_mutate(route):
    if random.random() < MUTATION_RATE:
        mutation_type = random.choice(['swap', 'insert', 'reverse'])

        if mutation_type == 'swap':
            # Swap two random cities
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]

        elif mutation_type == 'insert':
            # Remove a city and insert it at a random position
            city = route.pop(random.randint(0, len(route) - 1))
            route.insert(random.randint(0, len(route)), city)

        else:  # reverse
            # Reverse a random subsection of the route
            i, j = sorted(random.sample(range(len(route)), 2))
            route[i:j + 1] = reversed(route[i:j + 1])

    return route

# Main GA loop with elitism
# Parameters
POPULATION_SIZE = 300  # Increased population size
NUM_GENERATIONS = 10  # Increased number of generations
MUTATION_RATE = 0.2  # Decreased mutation rate

def genetic_algorithm():
    population = initial_population()

    for generation in range(NUM_GENERATIONS):
        new_population = []

        # Elitism: preserve the best 10% of individuals
        elitism_count = POPULATION_SIZE // 10
        sorted_population = sorted(population, key=lambda x: fitness(x), reverse=True)
        new_population.extend(sorted_population[:elitism_count])

        while len(new_population) < POPULATION_SIZE:
            parent1 = roulette_wheel_selection(population)
            parent2 = roulette_wheel_selection(population)
            child = ordered_crossover(parent1, parent2)
            child = enhanced_mutate(child)
            new_population.append(child)

        population = new_population

        best_route = max(population, key=lambda x: fitness(x))
        print(f"Generation {generation}: Best route {best_route} with fitness {fitness(best_route)}")

    return max(population, key=lambda x: fitness(x))

# Run the genetic algorithm
t1=datetime.datetime.now()
best_route = genetic_algorithm()
print(f"Optimal route found: {best_route}")
print(f"Total distance: {1/fitness(best_route)}")
t2=datetime.datetime.now()
print(f"Time Spent : {t2-t1}")
