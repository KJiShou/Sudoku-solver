import random
import math
import numpy as np
from copy import deepcopy

class SimulatedAnnealingSudoku:
    def __init__(self, board, initial_temp=1.0, cooling_rate=0.995, max_iter=10000):
        self.board = np.array(board)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.max_iter = max_iter
        self.fixed_positions = self.get_fixed_positions()
        self.process = []  # Store solving steps

    def get_fixed_positions(self):
        """Find fixed (given) numbers in the Sudoku grid."""
        return [(r, c) for r in range(9) for c in range(9) if self.board[r][c] != 0]

    def generate_random_solution(self):
        """Fill each row randomly while keeping fixed numbers."""
        for r in range(9):
            missing_numbers = list(set(range(1, 10)) - set(self.board[r]))  # Find missing numbers in row
            empty_positions = [c for c in range(9) if (r, c) not in self.fixed_positions]
            random.shuffle(missing_numbers)  # Randomize missing numbers
            for c, num in zip(empty_positions, missing_numbers):
                self.board[r][c] = num

    def calculate_cost(self):
        """Calculate conflicts in columns and 3x3 subgrids."""
        cost = 0
        # Check column conflicts
        for c in range(9):
            col_values = [self.board[r][c] for r in range(9)]
            cost += 9 - len(set(col_values))  # Count duplicate numbers

        # Check 3x3 subgrid conflicts
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                subgrid_values = [self.board[r][c] for r in range(box_r, box_r + 3) 
                                                   for c in range(box_c, box_c + 3)]
                cost += 9 - len(set(subgrid_values))  # Count duplicate numbers

        return cost

    def swap_random_cells(self):
        """Swap two non-fixed numbers within the same row."""
        row = random.randint(0, 8)
        non_fixed_cells = [c for c in range(9) if (row, c) not in self.fixed_positions]
        if len(non_fixed_cells) < 2:
            return
        c1, c2 = random.sample(non_fixed_cells, 2)
        self.board[row][c1], self.board[row][c2] = self.board[row][c2], self.board[row][c1]

    def solve(self):
        """Solve Sudoku using Simulated Annealing while recording steps."""
        self.generate_random_solution()
        temp = self.initial_temp
        current_cost = self.calculate_cost()
        self.process.append(deepcopy(self.board))  # Store initial board

        for iteration in range(self.max_iter):
            if current_cost == 0:
                print(f"Solved in {iteration} iterations!")
                return True

            # Make a move
            old_board = self.board.copy()
            self.swap_random_cells()
            new_cost = self.calculate_cost()

            # Accept move if better, or with some probability if worse
            if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temp):
                current_cost = new_cost
                self.process.append(deepcopy(self.board))  # Store board state after valid change
            else:
                self.board = old_board  # Revert move

            # Cool down the temperature
            temp *= self.cooling_rate

            # Stop if temperature is very low
            if temp < 0.001:
                print(f"Failed after {iteration} iterations.")
                return False

        print("Failed to find a solution.")
        return False

    def print_board(self):
        """Print the Sudoku board with separators for better visualization."""
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print("-" * 21)  # Horizontal separator every 3 rows

            row_str = ""
            for j, num in enumerate(row):
                if j % 3 == 0 and j != 0:
                    row_str += " | "  # Vertical separator every 3 columns
                row_str += str(num) if num != 0 else "."
                row_str += " "

            print(row_str.strip())
        print()

    def print_process(self):
        """Print all recorded solving steps, even if it fails, with separators."""
        print(f"\nTotal Steps Recorded: {len(self.process)}\n")
        for step_index, step in enumerate(self.process):
            print(f"Step {step_index + 1}:")
            for i, row in enumerate(step):
                if i % 3 == 0 and i != 0:
                    print("-" * 21)

                row_str = ""
                for j, num in enumerate(row):
                    if j % 3 == 0 and j != 0:
                        row_str += " | "
                    row_str += str(num) if num != 0 else "."
                    row_str += " "

                print(row_str.strip())
            print("------")


# Test Sudoku Board (0 represents empty cells)
initial_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = SimulatedAnnealingSudoku(initial_board)
print("Initial Sudoku Board:")
solver.print_board()

if solver.solve():
    print("\nSolved Sudoku Board:")
else:
    print("\nSolver failed to find a solution.")

solver.print_board()  # Show final board (whether solved or not)
solver.print_process()  # Print all steps (even on failure)
