import random
from collections import deque

# Parameters
POPULATION_SIZE = 100
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.2
IMPROVEMENT_THRESHOLD = 0.001
MAX_GENERATIONS_WITHOUT_IMPROVEMENT = 50

# Generate waypoints and distances
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

def calculate_total_distance(route):
    total_distance = 0
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        total_distance += distances.get((current_city, next_city), 1000)
    return total_distance

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

def initial_population():
    return [random.sample(waypoints, len(waypoints)) for _ in range(POPULATION_SIZE)]

def tournament_selection(population, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness)

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    
    # Copy a subset from parent1 (slicing is used)
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
    if random.random() < MUTATION_RATE: # this checks whether mutation should be done for each gene of the chromosome
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i] # this swaps the elements in the chromosome (here route is the chromosome)..it can be considered as an arr or list
    return route

def two_opt(route): # 2-opt algo is used to optimize routes by reconnecting and connecting routes to find shortest route
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2): # excludes the 1st and last cities, becoz they are included in the route from first inly
            for j in range(i + 1, len(route)):
                if j - i == 1: continue # this is to check that the adjacent cities are not changed, otherwise the route will change
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1] # stores reversed route in new route
                if calculate_total_distance(new_route) < calculate_total_distance(best): # checks which route is shorter
                    best = new_route  # swaps route if new_route is shorter
                    improved = True
        route = best #initailizes route to best new_route which is shorter
    return best

def genetic_algorithm():
    population = initial_population()
    best_fitness = 0
    best_route = None
    generations_without_improvement = 0
    generation = 0
    
    recent_best_distances = deque(maxlen=5) # double queue can pop elements from both ends,will store only the new elements
    
    while generation < MAX_GENERATIONS:
        population = sorted(population, key=fitness, reverse=True) #stores all of the chromosomes in the population based on fitness level and in desc order so the best routes are placed first
        current_best_route = population[0] 
        current_best_fitness = fitness(current_best_route)
        current_best_distance = calculate_total_distance(current_best_route)
        
        if current_best_fitness > best_fitness: # checks if fitness level has increased or is gen fitness same
            best_fitness = current_best_fitness
            best_route = current_best_route
            generations_without_improvement = 0
            recent_best_distances.append(current_best_distance)
            
            print(f"Generation {generation}: New best route {best_route} with distance {current_best_distance:.2f} and fitness {current_best_fitness:.5f}")
        else:
            generations_without_improvement += 1
        
        if len(recent_best_distances) == recent_best_distances.maxlen: #checks if the recent_best_distance is greater than the already stored best distance
            improvement = (recent_best_distances[0] - current_best_distance) / recent_best_distances[0] # if true then it calcs the improvement value
            if improvement < IMPROVEMENT_THRESHOLD:# it then checks if the improvement has increased or not
                generations_without_improvement += 1
            else:
                generations_without_improvement = 0
        
        if generations_without_improvement >= MAX_GENERATIONS_WITHOUT_IMPROVEMENT: # this checks if the number of generations has crossed the set number without any improvement in the fitness level
            print(f"Terminating: No significant improvement for {MAX_GENERATIONS_WITHOUT_IMPROVEMENT} generations.")
            break
        
        new_population = [current_best_route]  # Elitism: it makes sure that the best route of the current gen is always preserved to the next gen also
        
        while len(new_population) < POPULATION_SIZE: # it performs the GA operations like crossover, mutation, and 2opt algo for further optimization
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