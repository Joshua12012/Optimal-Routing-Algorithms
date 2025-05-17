import numpy as np
import matplotlib.pyplot as plt

class AdaptiveACO:
    def __init__(self, n_points, n_ants, alpha, beta, evaporation_rate, improvement_threshold=0.001, max_iterations_without_improvement=20):
        self.n_points = n_points
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.improvement_threshold = improvement_threshold
        self.max_iterations_without_improvement = max_iterations_without_improvement

        self.points = np.random.rand(n_points, 2)  # Randomly generate points
        self.distances = np.linalg.norm(self.points[:, None] - self.points, axis=2)  # Compute distance matrix
        self.pheromones = np.ones((n_points, n_points))  # Initialize pheromones
        self.best_path = None
        self.best_distance = float('inf')

    def run(self):
        print(f"Finding optimal path among all points")
        print(f"{'Iteration':^10}{'Best Distance':^15}{'Best Path':^30}")
        print("-" * 55)

        iterations_without_improvement = 0
        iteration = 0

        while iterations_without_improvement < self.max_iterations_without_improvement:
            iteration += 1
            ant_paths = []
            ant_distances = []

            for _ in range(self.n_ants):
                path = self.construct_path(0)  # Construct path starting from point 0
                distance = self.calculate_distance(path)
                ant_paths.append(path)
                ant_distances.append(distance)

            # Get the best path of this iteration
            best_iteration_path = ant_paths[np.argmin(ant_distances)]
            best_iteration_distance = min(ant_distances)

            # Update best path if improvement is made
            if best_iteration_distance < self.best_distance * (1 - self.improvement_threshold):
                self.best_path = best_iteration_path
                self.best_distance = best_iteration_distance
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1

            self.update_pheromones(ant_paths, ant_distances)

            print(f"{iteration:^10}{self.best_distance:^15.2f}{' -> '.join(map(str, self.best_path)):^30}")
            print("-" * 55)

        print("\nOptimization Complete")
        print(f"Optimal Path: {' -> '.join(map(str, self.best_path))}")
        print(f"Total Distance: {self.best_distance:.2f}")
        self.visualize_result(self.best_path)

    def find_closest_path(self, start):
        """Find the path from the start point to the closest point on the optimal path"""
        if start < 0 or start >= self.n_points:
            raise ValueError(f"Invalid start point. It should be between 0 and {self.n_points-1}.")
        
        print(f"\nFinding path from Point {start} to closest point on the optimal path.")
        closest_point = self.find_closest_point_on_optimal_path(start)
        print(f"Closest point on optimal path: {closest_point}")

        ant_paths = []
        ant_distances = []
        for _ in range(self.n_ants):
            path = self.construct_path(start, closest_point)
            distance = self.calculate_distance(path)
            ant_paths.append(path)
            ant_distances.append(distance)

        best_iteration_path = ant_paths[np.argmin(ant_distances)]
        best_iteration_distance = min(ant_distances)

        print(f"\nOptimal Path from Point {start} to closest point {closest_point}: {' -> '.join(map(str, best_iteration_path))}")
        print(f"Total Distance: {best_iteration_distance:.2f}")
        self.visualize_result(best_iteration_path)

    def construct_path(self, start, end=None):
        """Constructs a path from start to end, or a full path covering all points if no end is given."""
        path = [start]
        while len(path) < self.n_points and (end is None or path[-1] != end):
            next_point = self.choose_next_point(path[-1], path)
            path.append(next_point)

        if end is not None and path[-1] != end:
            path.append(end)  # Ensure the path ends at the given endpoint

        return path

    def choose_next_point(self, current, path):
        """Choose the next point based on pheromones and distances."""
        unvisited = list(set(range(self.n_points)) - set(path))
        if not unvisited:
            return path[0]  # If all points visited, return to start

        pheromone_values = []
        for point in unvisited:
            pheromone = self.pheromones[current, point] ** self.alpha
            distance = (1 / (self.distances[current, point] + 1e-6)) ** self.beta
            pheromone_values.append(pheromone * distance)

        total_pheromone = sum(pheromone_values)
        if total_pheromone == 0:  # Edge case where pheromone values are too small
            probabilities = np.ones(len(unvisited)) / len(unvisited)
        else:
            probabilities = np.array(pheromone_values) / total_pheromone

        return np.random.choice(unvisited, p=probabilities)

    def calculate_distance(self, path):
        """Calculate total distance of a given path."""
        if len(path) < 2:
            return 0  # No distance to compute if fewer than 2 points
        return sum(self.distances[path[i], path[i+1]] for i in range(len(path) - 1))

    def find_closest_point_on_optimal_path(self, start):
        """Find the closest point on the optimal path to the given start point."""
        distances_to_optimal = [self.distances[start, point] for point in self.best_path]
        closest_index = np.argmin(distances_to_optimal)
        return self.best_path[closest_index]

    def update_pheromones(self, ant_paths, ant_distances):
        """Update pheromones after each iteration."""
        self.pheromones *= (1 - self.evaporation_rate)  # Evaporate pheromones
        for path, distance in zip(ant_paths, ant_distances):
            pheromone_deposit = 1 / distance
            for i in range(len(path) - 1):
                self.pheromones[path[i], path[i+1]] += pheromone_deposit
                self.pheromones[path[i+1], path[i]] += pheromone_deposit

    def visualize_result(self, path):
        """Visualize the final result."""
        plt.figure(figsize=(12, 8))

        # Plot all points
        plt.scatter(self.points[:, 0], self.points[:, 1], c='blue', s=50)
        for i, point in enumerate(self.points):
            plt.annotate(f'Point {i}', (point[0], point[1]), xytext=(5, 5), textcoords='offset points')

        # Plot the path
        path_coords = self.points[path]
        plt.plot(path_coords[:, 0], path_coords[:, 1], 'r-', linewidth=2, zorder=4)

        # Plot connections between all points with pheromone levels
        for i in range(self.n_points):
            for j in range(i+1, self.n_points):
                plt.plot([self.points[i, 0], self.points[j, 0]], 
                         [self.points[i, 1], self.points[j, 1]], 
                         'g-', alpha=0.1 + 0.9 * self.pheromones[i, j] / np.max(self.pheromones),
                         linewidth=0.5, zorder=1)

        plt.title("Path Visualization")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

# Example usage
n_points = int(input("Enter the number of points: "))
n_ants = int(input("Enter the number of ants: "))

aco = AdaptiveACO(n_points=n_points, n_ants=n_ants, alpha=1, beta=5, evaporation_rate=0.1)
aco.run()

start_point = int(input(f"Enter a starting point (between 0 and {n_points-1}): "))
aco.find_closest_path(start_point)
