import random
import math
import numpy as np
from copy import deepcopy
from main.KongJiShou_TanZhongYen_NgZheWei_CheaHongJun_TeohYongMing import sudoku_function as sf  # Contains helper methods like printing board and animation


class SimulatedAnnealingSudoku:
    """
    Sudoku solver using the Simulated Annealing algorithm.
    The class initializes with a Sudoku board, and attempts to find a valid solution
    by minimizing a cost function through probabilistic search.
    """

    def __init__(self, board, initial_temp=1.0, cooling_rate=0.995, max_iter=10000):
        """
        Initialize the solver with the given board and parameters.
        :param board: 2D list representing the Sudoku puzzle
        :param initial_temp: Starting temperature for annealing
        :param cooling_rate: How quickly the temperature decreases
        :param max_iter: Maximum iterations per SA cycle
        """
        self.board = np.array(board)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.max_iter = max_iter
        self.fixed_positions = self.get_fixed_positions()
        self.process = []  # Store solving steps
        self.status_message = ""
        self.final_iteration = 0

    def get_fixed_positions(self):
        """
        Return a list of (row, col) positions where the initial values are fixed (non-zero).
        """
        return [(r, c) for r in range(9) for c in range(9) if self.board[r][c] != 0]

    def generate_random_solution(self):
        """
        Fill each row randomly with missing digits without changing fixed cells.
        This creates a complete initial candidate solution.
        """
        for r in range(9):
            missing_numbers = list(set(range(1, 10)) - set(self.board[r]))
            empty_positions = [c for c in range(9) if (r, c) not in self.fixed_positions]
            random.shuffle(missing_numbers)
            for c, num in zip(empty_positions, missing_numbers):
                self.board[r][c] = num

    def calculate_cost(self):
        """
        Compute the cost of the current board:
        - Penalty is based on repeated values in columns and 3x3 subgrids.
        - Lower cost means closer to a valid solution.
        """
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
        """
        Swap two non-fixed cells in a randomly selected row to explore new configurations.
        """
        row = random.randint(0, 8)
        non_fixed_cells = [c for c in range(9) if (row, c) not in self.fixed_positions]
        if len(non_fixed_cells) < 2:
            return
        c1, c2 = random.sample(non_fixed_cells, 2)
        self.board[row][c1], self.board[row][c2] = self.board[row][c2], self.board[row][c1]

    @staticmethod
    def is_valid_solution(board):
        """
        Check if the board is a complete and valid Sudoku solution.
        """
        for i in range(9):
            row = board[i, :]
            col = board[:, i]
            if len(set(row)) != 9 or len(set(col)) != 9:
                return False

        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                subgrid = board[r:r + 3, c:c + 3].flatten()
                if len(set(subgrid)) != 9:
                    return False

        return True

    def solve(self):
        """
        Perform the Simulated Annealing algorithm:
        - Try to minimize the board cost.
        - Accept worse solutions probabilistically.
        - Stop when a valid solution is found or the iteration limit is reached.
        :return: True if a valid solution is found, else False
        """
        total_iterations = 0
        max_total_iterations = 100_000
        best_board = None
        best_cost = float("inf")
        best_process = []

        while total_iterations < max_total_iterations:
            self.generate_random_solution()
            temp = self.initial_temp
            current_cost = self.calculate_cost()
            current_process = [deepcopy(self.board)]

            for iteration in range(self.max_iter):
                total_iterations += 1

                if current_cost < best_cost:
                    best_cost = current_cost
                    best_board = deepcopy(self.board)
                    best_process = deepcopy(current_process)

                    if best_cost == 0 and self.is_valid_solution(best_board):
                        self.status_message = f"Solved in {total_iterations} total iterations!"
                        self.board = best_board
                        self.process = best_process
                        self.final_iteration = total_iterations
                        return True

                old_board = self.board.copy()
                self.swap_random_cells()
                new_cost = self.calculate_cost()

                # Metropolis criterion for simulated annealing
                if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temp):
                    current_cost = new_cost
                    current_process.append(deepcopy(self.board))
                else:
                    self.board = old_board

                temp *= self.cooling_rate
                if temp < 0.001:
                    break

        # Final fallback if no perfect solution found
        if best_board is not None and self.is_valid_solution(best_board):
            self.status_message = f"Could not find perfect solution, but returning best valid attempt (cost {best_cost})"
            self.board = best_board
            self.process = best_process
            self.final_iteration = total_iterations
            return True
        else:
            self.status_message = f"Could not fully solve. Best cost = {best_cost} after {total_iterations} iterations."
            self.board = None  # Force menu to treat as failure
            return False

    def print_board(self):
        """
        Print the current board using the helper function.
        """
        sf.print_board(self.board)

    def print_process(self):
        """
        Display the step-by-step solving process using the helper function.
        """
        sf.show_procedure(self.process)


def compare_boards(board1, board2):
    """
    Compare two 9x9 Sudoku boards.
    :return: True if the boards are identical.
    """
    return np.array_equal(np.array(board1), np.array(board2))


def closeness_score(board1, board2):
    """
    Calculate how many cells match between two Sudoku boards.
    :return: Number of matching cells, and the percentage match.
    """
    b1 = np.array(board1)
    b2 = np.array(board2)
    matches = np.sum(b1 == b2)
    percentage = (matches / 81) * 100
    return matches, round(percentage, 2)


if __name__ == "__main__":
    """
    Example usage of SimulatedAnnealingSudoku.
    Loads a puzzle, solves it, prints the process, and evaluates closeness to known solution.
    """
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

    solver = SimulatedAnnealingSudoku(initial_board)
    print("Initial Sudoku Board:")
    solver.print_board()

    success = solver.solve()

    solver.print_process()

    print("\nFinal Sudoku Board:")
    solver.print_board()
    print(solver.status_message)

    if compare_boards(solver.board, correct_board):
        print("Final board matches the known correct solution.")
    else:
        print("Final board does NOT match the known correct solution.")

    matches, percentage = closeness_score(solver.board, correct_board)
    print(f"Closeness to correct answer: {matches}/81 cells correct ({percentage}%)")
