# Sudoku Solver using AI Search Algorithms

This repository provides a powerful Sudoku solver implemented using various algorithmic search strategies. The aim is to explore and compare different types of search methods from **uninformed**, **informed**, and **local** search paradigms.

## Prerequisites

Before running this project, make sure you have the following dependencies installed:

- Python 3.x
- NumPy (>= 1.21.0)

You can install the required dependencies using pip:

```bash
pip install numpy
```

Or install all dependencies from the project's setup.py:

```bash
pip install -e .
```

## Overview

The solver supports the following algorithms:

- **Backtracking Search** (Uninformed)
- **Breadth-First Search (BFS)** (Uninformed)
- **Iterative Deepening Search (IDS)** (Uninformed)
- **A\* Search** (Informed)
- **Simulated Annealing** (Local Search)

Each algorithm visualizes the solving process step-by-step and provides detailed **time** and **memory** usage statistics.

## Project Goals

- Solve any valid Sudoku puzzle using AI-based search algorithms  
- Compare algorithm performance in terms of time and space complexity  
- Provide a visual walkthrough of each solving process  
- Offer a flexible environment for experimenting with different approaches  

## Key Features

- Visual representation of each algorithm's solving path  
- Real-time performance metrics (execution time, memory usage)  
- Support for 9x9 standard Sudoku puzzles  
- Modular design for easy expansion or testing with new algorithms  
