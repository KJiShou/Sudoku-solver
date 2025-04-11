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
        self.status_message = ""
        self.final_iteration = 0

    def get_fixed_positions(self):
        return [(r, c) for r in range(9) for c in range(9) if self.board[r][c] != 0]

    def generate_random_solution(self):
        for r in range(9):
            missing_numbers = list(set(range(1, 10)) - set(self.board[r]))
            empty_positions = [c for c in range(9) if (r, c) not in self.fixed_positions]
            random.shuffle(missing_numbers)
            for c, num in zip(empty_positions, missing_numbers):
                self.board[r][c] = num

    def calculate_cost(self):
        cost = 0
        for c in range(9):
            col_values = [self.board[r][c] for r in range(9)]
            cost += 9 - len(set(col_values))
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                subgrid_values = [self.board[r][c] for r in range(box_r, box_r + 3)
                                                   for c in range(box_c, box_c + 3)]
                cost += 9 - len(set(subgrid_values))
        return cost

    def swap_random_cells(self):
        row = random.randint(0, 8)
        non_fixed_cells = [c for c in range(9) if (row, c) not in self.fixed_positions]
        if len(non_fixed_cells) < 2:
            return
        c1, c2 = random.sample(non_fixed_cells, 2)
        self.board[row][c1], self.board[row][c2] = self.board[row][c2], self.board[row][c1]

    def solve(self):
        self.generate_random_solution()
        temp = self.initial_temp
        current_cost = self.calculate_cost()
        self.process.append(deepcopy(self.board))

        for iteration in range(self.max_iter):
            if current_cost == 0:
                self.status_message = f"Solved in {iteration} iterations!"
                self.final_iteration = iteration
                return True

            old_board = self.board.copy()
            self.swap_random_cells()
            new_cost = self.calculate_cost()

            if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temp):
                current_cost = new_cost
                self.process.append(deepcopy(self.board))
            else:
                self.board = old_board

            temp *= self.cooling_rate
            if temp < 0.001:
                self.status_message = f"Failed after {iteration} iterations."
                self.final_iteration = iteration
                return False

        self.status_message = f"Failed after {self.max_iter} iterations."
        self.final_iteration = self.max_iter
        return False

    def print_board(self):
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            row_str = ""
            for j, num in enumerate(row):
                if j % 3 == 0 and j != 0:
                    row_str += " | "
                row_str += str(num) if num != 0 else "."
                row_str += " "
            print(row_str.strip())
        print()

    def print_process(self):
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


def compare_boards(board1, board2):
    """Compare two 9x9 Sudoku boards. Return True if identical."""
    return np.array_equal(np.array(board1), np.array(board2))

def closeness_score(board1, board2):
    """Return the number of matching cells and percentage similarity."""
    b1 = np.array(board1)
    b2 = np.array(board2)
    matches = np.sum(b1 == b2)
    percentage = (matches / 81) * 100
    return matches, round(percentage, 2)


# Initial Sudoku Board
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

# Known correct solution to validate against
correct_board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

# Solve using SA
solver = SimulatedAnnealingSudoku(initial_board)
print("Initial Sudoku Board:")
solver.print_board()

success = solver.solve()

# Always show step history
solver.print_process()

# Then show final result + validation
print("\nFinal Sudoku Board:")
solver.print_board()
print(solver.status_message)

# Validation only if solve was successful
if success:
    if compare_boards(solver.board, correct_board):
        print("Final board matches the known correct solution.")
    else:
        print("Final board does NOT match the known correct solution.")

    matches, percentage = closeness_score(solver.board, correct_board)
    print("Closeness to correct answer: {matches}/81 cells correct ({percentage}%)")
