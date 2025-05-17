# 🚢 Metaheuristic Algorithms for Route Optimization

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20+-green.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-orange.svg)](https://matplotlib.org/)

This repository contains implementations of various metaheuristic algorithms for solving route optimization problems, specifically the Traveling Salesman Problem (TSP) and its variants.

## 📋 Table of Contents
- [Overview](#overview)
- [Algorithms](#algorithms)
- [Installation](#installation)
- [Usage](#usage)
- [Example Results](#example-results)
- [Comparison](#comparison)
- [Contributing](#contributing)

## 🔍 Overview

Route optimization is a critical problem in logistics, transportation, and many other fields. These algorithms help find optimal or near-optimal solutions to complex routing problems that cannot be solved efficiently using exact methods.

## 🧠 Algorithms

### 🐜 Adaptive Ant Colony Optimization (ACO)
`aco_gpt.py` implements an adaptive version of the Ant Colony Optimization algorithm.

Key features:
- Randomly generates points in a 2D space
- Constructs paths using pheromone-based probabilistic selection
- Visualizes results with pheromone strength displayed
- Finds the closest path from any point to the optimal route

### 🧬 Genetic Algorithm (GA)
Multiple implementations are provided with different features:

#### Basic GA (`ga1.py`)
- Uses tournament selection
- Implements ordered crossover
- Simple mutation operator

#### Advanced GA with Two-Opt (`ga2.py`, `exp.py`)
- Adds Two-Opt local search optimization
- Early termination based on improvement threshold
- Handles asymmetric distances

#### Experimental GA (`ga.py`)
- Uses randomly generated waypoints
- Supports bidirectional pairs with different costs

### 🔄 Differential Evolution (DE)
`de_gpt.py` implements a Differential Evolution algorithm for TSP.

Key features:
- Parameter-based mutation strategy
- Efficient population management
- Visualization of best solution

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/metaheuristic-route-optimization.git
cd metaheuristic-route-optimization

# Install requirements
pip install numpy matplotlib
```

## 🚀 Usage

### Ant Colony Optimization
```bash
python aco_gpt.py
```
You'll be prompted to enter:
- Number of points
- Number of ants
- Starting point (to find path to the optimal route)

### Genetic Algorithm
```bash
python exp.py
```
The algorithm will run with the predefined waypoints and parameters.

### Differential Evolution
```bash
python de_gpt.py
```
The algorithm will run with the default parameters and show the best route visualization.

## 📊 Example Results

For the Ant Colony Optimization:
```
Finding optimal path among all points
Iteration  Best Distance      Best Path
-------------------------------------------------------
    1         2.34          0 -> 3 -> 1 -> 2 -> 4
-------------------------------------------------------
    ...
    10        1.87          0 -> 4 -> 1 -> 3 -> 2
-------------------------------------------------------

Optimization Complete
Optimal Path: 0 -> 4 -> 1 -> 3 -> 2
Total Distance: 1.87
```

## 📈 Comparison

| Algorithm | Advantages | Disadvantages | Best Use Case |
|-----------|------------|---------------|--------------|
| ACO | Works well with dynamic problems | Parameter tuning can be complex | Problems with changing environments |
| GA | Simple to implement | May converge to local optima | Problems with complex constraints |
| DE | Good global search capability | Slower convergence | Problems requiring high precision |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
