import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class SimpleACO:
    def __init__(self, n_ports, n_ships, n_iterations, evaporation_rate):
        self.n_ports = n_ports
        self.n_ships = n_ships
        self.n_iterations = n_iterations
        self.evaporation_rate = evaporation_rate
        
        # Generate random port locations
        self.ports = np.random.rand(n_ports, 2)
        
        # Calculate distances between ports
        self.distances = np.linalg.norm(self.ports[:, None] - self.ports, axis=2)
        
        # Initialize pheromones
        self.pheromones = np.ones_like(self.distances)
        
        # Initialize ships at random ports
        self.ships = np.random.randint(0, n_ports, n_ships)
        
        self.best_path = None
        self.best_distance = float('inf')

    def move_ships(self):
        for i in range(self.n_ships):
            current_port = self.ships[i]
            next_port = self.choose_next_port(current_port)
            self.ships[i] = next_port
            
            # Update pheromones
            self.pheromones[current_port, next_port] += 1 / self.distances[current_port, next_port]
            self.pheromones[next_port, current_port] = self.pheromones[current_port, next_port]

    def choose_next_port(self, current_port):
        probabilities = self.pheromones[current_port] / self.distances[current_port]
        probabilities[current_port] = 0  # Can't stay in the same port
        return np.random.choice(self.n_ports, p=probabilities/sum(probabilities))

    def evaporate_pheromones(self):
        self.pheromones *= (1 - self.evaporation_rate)

    def update_best_path(self):
        for ship in range(self.n_ships):
            path = [self.ships[ship]]
            for _ in range(self.n_ports - 1):
                path.append(self.choose_next_port(path[-1]))
            distance = sum(self.distances[path[i], path[i+1]] for i in range(self.n_ports - 1))
            if distance < self.best_distance:
                self.best_path = path
                self.best_distance = distance

def animate(i):
    aco.move_ships()
    aco.evaporate_pheromones()
    aco.update_best_path()
    
    # Clear the plot
    plt.clf()
    
    # Plot ports
    plt.scatter(aco.ports[:, 0], aco.ports[:, 1], c='blue', s=100, zorder=2)
    for j, port in enumerate(aco.ports):
        plt.annotate(f'Port {j}', (port[0], port[1]), xytext=(5, 5), textcoords='offset points')
    
    # Plot pheromones
    for i in range(aco.n_ports):
        for j in range(i+1, aco.n_ports):
            plt.plot([aco.ports[i, 0], aco.ports[j, 0]], 
                     [aco.ports[i, 1], aco.ports[j, 1]], 
                     'g-', alpha=aco.pheromones[i, j] / np.max(aco.pheromones), 
                     linewidth=1, zorder=1)
    
    # Plot ships
    plt.scatter(aco.ports[aco.ships, 0], aco.ports[aco.ships, 1], c='red', s=50, zorder=3)
    
    # Plot best path
    if aco.best_path:
        best_path = np.array(aco.best_path)
        plt.plot(aco.ports[best_path, 0], aco.ports[best_path, 1], 'r--', linewidth=2, zorder=4)
    
    plt.title(f'Iteration {i+1}, Best Distance: {aco.best_distance:.2f}')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

# Create ACO instance
aco = SimpleACO(n_ports=10, n_ships=5, n_iterations=100, evaporation_rate=0.1)

# Create animation
fig = plt.figure(figsize=(10, 8))
anim = FuncAnimation(fig, animate, frames=aco.n_iterations, interval=200, repeat=False)
plt.show()