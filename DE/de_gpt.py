import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
N_PORTS = 10
POP_SIZE = 50
N_GENERATIONS = 100
F = 0.8  # Differential weight
CR = 0.7  # Crossover rate

# --- Generate Random Distances ---
np.random.seed(0)  # For reproducibility
distances = np.random.randint(10, 100, size=(N_PORTS, N_PORTS))
np.fill_diagonal(distances, 0)
distances = (distances + distances.T) / 2  # Make symmetric

# --- Fitness Function ---
def fitness(solution):
    solution = solution.astype(int)  # Ensure integer indices
    return sum(distances[solution[i], solution[(i + 1) % N_PORTS]] for i in range(N_PORTS))

# --- Initialize Population ---
def initialize_population():
    return [np.random.permutation(N_PORTS).astype(int) for _ in range(POP_SIZE)]

# --- Mutation ---
def mutate(target, population):
    indices = np.random.choice(range(POP_SIZE), 3, replace=False)
    a, b, c = [population[i].astype(int) for i in indices]
    mutant = np.copy(target).astype(float)  # Convert to float for arithmetic
    
    # Perform mutation
    for i in range(N_PORTS):
        if np.random.rand() < CR:
            j = indices[0]
            mutant[i] = population[j][i] + F * (population[indices[1]][i] - population[indices[2]][i])
    
    # Ensure valid permutation
    return create_valid_permutation(mutant)

def create_valid_permutation(mutant):
    # Convert to ranks to create a valid permutation
    return np.argsort(mutant).astype(int)

# --- Run Differential Evolution ---
def differential_evolution():
    population = initialize_population()
    best_solution = None
    best_fitness = float('inf')
    
    for generation in range(N_GENERATIONS):
        new_population = []
        
        for i in range(POP_SIZE):
            target = population[i]
            trial = mutate(target, population)
            
            trial_fit = fitness(trial)
            target_fit = fitness(target)
            
            if trial_fit < target_fit:
                new_population.append(trial)
            else:
                new_population.append(target)
        
        population = new_population
        current_best = min(population, key=fitness)
        current_fitness = fitness(current_best)
        
        if current_fitness < best_fitness:
            best_fitness = current_fitness
            best_solution = current_best.copy()
            
        print(f"Generation {generation + 1}: Best fitness = {best_fitness:.2f}")
    
    return best_solution, best_fitness

# --- Visualization ---
def visualize_de(best_solution):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    port_locations = np.random.rand(N_PORTS, 2)
    ax.scatter(port_locations[:, 0], port_locations[:, 1], s=100, c='blue')
    
    for i, loc in enumerate(port_locations):
        ax.annotate(f'Port {i}', (loc[0], loc[1]), xytext=(5, 5), textcoords='offset points')
    
    # Plot best path
    best_solution = best_solution.astype(int)  # Ensure integer indices
    x = port_locations[best_solution, 0]
    y = port_locations[best_solution, 1]
    ax.plot(np.append(x, x[0]), np.append(y, y[0]), 'r-', linewidth=2, label='Best Path')
    
    ax.set_title('Differential Evolution for TSP')
    ax.legend()
    plt.show()

# --- Run the DE Algorithm ---
best_solution, best_fitness = differential_evolution()
print(f"\nOptimal route found: {best_solution}")
print(f"Total distance: {best_fitness:.2f}")

# --- Visualize the Best Solution ---
visualize_de(best_solution)
