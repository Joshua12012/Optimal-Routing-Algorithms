import random

# Parameters
POPULATION_SIZE = 10
NUM_GENERATIONS = 10
MUTATION_RATE = 0.2

# Generate waypoints and distances
waypoints = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
distances = {}
for i in range(len(waypoints)):
    for j in range(i+1, len(waypoints)):
        distance = random.randint(50, 200)
        distances[(waypoints[i], waypoints[j])] = distance
        distances[(waypoints[j], waypoints[i])] = distance + random.randint(-20, 20)

# Ensure all waypoints are connected
for i in range(len(waypoints)):
    next_point = waypoints[(i+1) % len(waypoints)]
    distances[(waypoints[i], next_point)] = random.randint(30, 100)
    distances[(next_point, waypoints[i])] = distances[(waypoints[i], next_point)] + random.randint(-10, 10)

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

def genetic_algorithm():
    population = initial_population()
    best_fitness = 0
    
    for generation in range(NUM_GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        
        if fitness(population[0]) > best_fitness:
            best_fitness = fitness(population[0])
        
        new_population = population[:2]  # Elitism
        
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = ordered_crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        
        population = new_population
        
        best_route = population[0]
        print(f"Generation {generation}: Best route {best_route} with distance {calculate_total_distance(best_route):.2f}")
    
    return population[0]

# Run the algorithm
best_route = genetic_algorithm()
print(f"Optimal route found: {best_route}")
print(f"Total distance: {calculate_total_distance(best_route):.2f}")

