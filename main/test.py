# Re-import necessary libraries after execution state reset
import numpy as np
import copy
import random
import math
import pandas as pd
import ace_tools as tools

# Sample Sudoku Puzzle (0 represents an empty cell)
sudoku_puzzle = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])


# Utility function to check if a number can be placed in a given position
def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    # Check column
    if num in board[:, col]:
        return False
    # Check 3x3 subgrid
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True


# Simulated Annealing Sudoku Solver
def simulated_annealing_sudoku_solver(sudoku, initial_temp=1.0, cooling_rate=0.995, min_temp=0.01):
    board = copy.deepcopy(sudoku)

    # Randomly fill the Sudoku board while keeping original clues
    for i in range(9):
        missing_numbers = [num for num in range(1, 10) if num not in board[i]]
        random.shuffle(missing_numbers)
        for j in range(9):
            if board[i, j] == 0:
                board[i, j] = missing_numbers.pop()

    def evaluate(board):
        """ Count the number of conflicts in columns and subgrids """
        score = 0
        for col in range(9):
            score += len(set(board[:, col]))  # Unique numbers in columns

        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                subgrid = board[r:r + 3, c:c + 3].flatten()
                score += len(set(subgrid))  # Unique numbers in 3x3 grid
        return score

    current_temp = initial_temp
    best_board = copy.deepcopy(board)
    best_score = evaluate(best_board)

    max_iterations = 10000  # Large enough to allow proper annealing
    for _ in range(max_iterations):
        if current_temp < min_temp:
            break

        # Select a random row and swap two numbers
        row = random.randint(0, 8)
        cols = [j for j in range(9) if sudoku[row, j] == 0]  # Select non-fixed cells

        if len(cols) > 1:
            c1, c2 = random.sample(cols, 2)
            board[row, c1], board[row, c2] = board[row, c2], board[row, c1]

            new_score = evaluate(board)
            delta = new_score - best_score

            if delta < 0 or math.exp(-delta / current_temp) > random.random():
                best_board = copy.deepcopy(board)
                best_score = new_score
            else:  # Revert swap if not accepted
                board[row, c1], board[row, c2] = board[row, c2], board[row, c1]

        # Cool down temperature
        current_temp *= cooling_rate

        if best_score == 243:  # 243 means a solved Sudoku (no conflicts)
            return best_board

    return None  # No solution found


# Solve the Sudoku using Simulated Annealing
simulated_annealing_solution = simulated_annealing_sudoku_solver(sudoku_puzzle)

# Display the solution
df_simulated_annealing_solution = pd.DataFrame(simulated_annealing_solution)
tools.display_dataframe_to_user(name="Simulated Annealing Sudoku Solution", dataframe=df_simulated_annealing_solution)
