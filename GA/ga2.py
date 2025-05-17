import random
from collections import deque

# Parameters
POPULATION_SIZE = 100
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.2
IMPROVEMENT_THRESHOLD = 0.001
MAX_GENERATIONS_WITHOUT_IMPROVEMENT = 50

# Generate waypoints and distances
waypoints = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
distances = {}
for i in range(len(waypoints)):
    for j in range(i+1, len(waypoints)):
        distance = random.randint(50, 200)
        distances[(waypoints[i], waypoints[j])] = distance
        distances[(waypoints[j], waypoints[i])] = distance + random.randint(-20, 20)

def calculate_total_distance(route):
    total_distance = 0
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        total_distance += distances.get((current_city, next_city), 1000)
    return total_distance

def fitness(route):
    return 1 / calculate_total_distance(route)

def initial_population():
    return [random.sample(waypoints, len(waypoints)) for _ in range(POPULATION_SIZE)]

def tournament_selection(population, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness)

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    
    # Copy a subset from parent1
    child[start:end+1] = parent1[start:end+1]
    
    # Fill the remaining positions with cities from parent2
    parent2_index = 0
    for i in range(size):
        if child[i] is None:
            while parent2[parent2_index] in child:
                parent2_index += 1
            child[i] = parent2[parent2_index]
    
    return child

def mutate(route):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

def two_opt(route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]
                if calculate_total_distance(new_route) < calculate_total_distance(best):
                    best = new_route
                    improved = True
        route = best
    return best

def genetic_algorithm():
    population = initial_population()
    best_fitness = 0
    best_route = None
    generations_without_improvement = 0
    generation = 0
    
    recent_best_distances = deque(maxlen=5)
    
    while generation < MAX_GENERATIONS:
        population = sorted(population, key=fitness, reverse=True)
        current_best_route = population[0]
        current_best_fitness = fitness(current_best_route)
        current_best_distance = calculate_total_distance(current_best_route)
        
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_route = current_best_route
            generations_without_improvement = 0
            recent_best_distances.append(current_best_distance)
            
            print(f"Generation {generation}: New best route {best_route} with distance {current_best_distance:.2f}")
        else:
            generations_without_improvement += 1
        
        if len(recent_best_distances) == recent_best_distances.maxlen:
            improvement = (recent_best_distances[0] - current_best_distance) / recent_best_distances[0]
            if improvement < IMPROVEMENT_THRESHOLD:
                generations_without_improvement += 1
            else:
                generations_without_improvement = 0
        
        if generations_without_improvement >= MAX_GENERATIONS_WITHOUT_IMPROVEMENT:
            print(f"Terminating: No significant improvement for {MAX_GENERATIONS_WITHOUT_IMPROVEMENT} generations.")
            break
        
        new_population = [current_best_route]  # Elitism
        
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = ordered_crossover(parent1, parent2)
            child = mutate(child)
            child = two_opt(child)  # Apply local search
            new_population.append(child)
        
        population = new_population
        generation += 1
    
    return best_route, generation

# Run the optimized algorithm
best_route, total_generations = genetic_algorithm()
print(f"Optimal route found: {best_route}")
print(f"Total distance: {calculate_total_distance(best_route):.2f}")
print(f"Total generations: {total_generations}")