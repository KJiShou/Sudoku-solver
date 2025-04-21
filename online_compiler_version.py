import time
import tracemalloc
import threading
import numpy as np
from copy import deepcopy
from collections import deque
import random
import math
import heapq

# Global flag for animation
solving = True

def as_is_valid(board, row, col, num):
    """
    Check if placing `num` at (row, col) is valid under Sudoku rules.
    """
    if num in board[row]:  # Row check
        return False
    for i in range(9):  # Column check
        if board[i][col] == num:
            return False
    # Box check
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def is_valid(board: list, num: int, row: int, col: int) -> bool:
    """
        Check if placing 'num' at position (row, col) is valid
        according to Sudoku rules (row, column, and 3x3 grid).
    """
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def as_find_empty(board):
    """
    Find the empty cell with the fewest valid candidate numbers (MRV heuristic).
    """
    min_options = float('inf')
    best_empty = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                options = 0
                for num in range(1, 10):
                    if as_is_valid(board, row, col, num):
                        options += 1
                if options < min_options:
                    min_options = options
                    best_empty = (row, col)
    return best_empty

def find_empty(board):
    """
    Find the first empty cell in the Sudoku board.
    Returns a tuple (row, col) if found, or None if the board is full.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def dfs(board, depth, max_depth, process, depth_log):
    """
    Perform Depth-First Search with a depth limit.
    If a solution is found within the current depth, return True.
    Logs each step and depth for visualization.
    """
    if depth > max_depth:
        return False

    empty = find_empty(board)
    if not empty:
        return True  # Puzzle is solved

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            process.append(deepcopy(board))
            depth_log.append(depth + 1)

            if dfs(board, depth + 1, max_depth, process, depth_log):
                return True

            board[row][col] = 0  # Backtrack if not successful

    return False


def iterative_deepening(board):
    """
    Solve the Sudoku using Iterative Deepening Search.
    Starts with a shallow depth and increases it until a solution is found.
    Logs the solving process and depth levels.
    """
    process = []
    depth_log = []

    empty_cells = sum(row.count(0) for row in board)
    for max_depth in range(empty_cells, 81):  # 81 is the max number of empty moves
        copied_board = deepcopy(board)
        process.append(deepcopy(board))
        depth_log.append(0)
        if dfs(copied_board, 0, max_depth, process, depth_log):
            return copied_board, process, depth_log
    return None, process, depth_log

# Backtracking Search
def solve_sudoku_with_logging(board):
    """
    Solve the given Sudoku board using the backtracking algorithm.
    Logs each step into 'process' and records recursion depth in 'depth_log'.
    """
    process = []
    depth_log = []

    board_copy = deepcopy(board)
    process.append(deepcopy(board_copy))  # Initial state, depth 0
    depth_log.append(0)

    def backtrack(board, depth):
        """
        Recursive helper function for backtracking.
        """
        empty = find_empty(board)
        if not empty:
            return True  # Puzzle solved

        row, col = empty
        for num in range(1, 10):
            if is_valid(board, num, row, col):
                board[row][col] = num
                process.append(deepcopy(board))
                depth_log.append(depth + 1)

                if backtrack(board, depth + 1):
                    return True

                board[row][col] = 0  # Undo move
                process.append(deepcopy(board))  # Log backtrack
                depth_log.append(depth + 1)
        return False

    solved = backtrack(board_copy, 0)
    return (board_copy if solved else None), process, depth_log

# Breadth First Search
# --------------------------------------------
# Find first empty cell in board (returns tuple or None)
# --------------------------------------------
def find_empty_cell(board):
    """
    Return the position (row, col) of the first empty cell (value = 0).
    If the board is full, return None.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None
# --------------------------------------------
# Breadth-First Search (BFS) Sudoku Solver
# --------------------------------------------
def bfs_sudoku_solver(board):
    """
    Solve the Sudoku puzzle using Breadth-First Search (BFS).
    Returns the solved board (if found), all intermediate boards (path_list),
    and their respective breadth levels (breadth_levels).
    """
    queue = deque([(board, 0)])  # Start queue with initial board and level 0
    path_list = []               # Store all visited board states
    breadth_levels = []          # Corresponding breadth levels (steps)

    while queue:
        current_board, breadth = queue.popleft()

        path_list.append(deepcopy(current_board))
        breadth_levels.append(breadth)

        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board, path_list, breadth_levels  # Solved

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, num, row, col):
                new_board = deepcopy(current_board)
                new_board[row][col] = num
                queue.append((new_board, breadth + 1))

    return None, path_list, breadth_levels  # No solution found

# A* Search
def heuristic(board):
    """
    Heuristic function: returns number of violations in the board.
    Violations = repeated numbers in rows, columns, and boxes.
    """
    violations = 0

    # Row violations
    for row in board:
        seen = set()
        for num in row:
            if num != 0 and num in seen:
                violations += 1
            seen.add(num)

    # Column violations
    for col in range(9):
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != 0 and num in seen:
                violations += 1
            seen.add(num)

    # Box violations
    for block_row in range(3):
        for block_col in range(3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    num = board[3 * block_row + i][3 * block_col + j]
                    if num != 0 and num in seen:
                        violations += 1
                    seen.add(num)
    return violations


# ======== A* Sudoku Solver ========

def solve_sudoku_a_star(initial_board, show_steps=False):
    """
    Solve Sudoku using A* search algorithm with heuristic guidance.
    Returns:
        - final board
        - list of visited boards (process path)
        - None (placeholder for compatibility)
    """

    open_list = [(heuristic(initial_board), 0, deepcopy(initial_board), [deepcopy(initial_board)])]
    closed_set = set()

    while open_list:
        f, g, current_board, path = heapq.heappop(open_list)
        board_tuple = tuple(map(tuple, current_board))

        if board_tuple in closed_set:
            continue
        closed_set.add(board_tuple)

        if heuristic(current_board) == 0 and as_find_empty(current_board) is None:
            return current_board, path, None

        empty_cell = as_find_empty(current_board)
        if empty_cell is None:
            return current_board, path, None

        row, col = empty_cell
        for num in range(1, 10):
            if as_is_valid(current_board, row, col, num):
                new_board = deepcopy(current_board)
                new_board[row][col] = num
                h = heuristic(new_board)
                new_path = deepcopy(path)
                new_path.append(deepcopy(new_board))
                heapq.heappush(open_list, (g + 1 + h, g + 1, new_board, new_path))

    return None, path, None

# Simulated Annealing
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
        print_board(self.board)

    def print_process(self):
        """
        Display the step-by-step solving process using the helper function.
        """
        show_procedure(self.process)

def print_board(board):
    """
        Print a Sudoku board in formatted 9x9 layout.
    """
    if board is None:
        print("Cannot Find the result!")
        return
    for row in range(9):
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")
            val = board[row][col]
            print(f" {val if val != 0 else ' '} ", end="")
        print()
        if row % 3 == 2 and row != 8:
            print("- " * 17)
    print("\n")

# function to print sudoku board
def print_sudoku_result(board: list, time_taken: float, peak_memory: float):
    """
        Print the final Sudoku board result along with time and memory usage stats.
        Shows formatted output for solved or unsolved boards.
    """
    print("")
    if board is None:
        print("Cannot Find the result!")
        print(f"Memory Usage: {peak_memory / (1024 * 1024):.2f} MB")
        print(f"Time Usage  : {time_taken:.6f} seconds\n")
        return
    for row in range(9):
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")
            val = board[row][col]
            print(f" {val if val != 0 else ' '} ", end="")
        print()
        if row % 3 == 2 and row != 8:
            print("- " * 17)
    print("\n          FINAL RESULT\n")
    print(f"Memory Usage: {peak_memory / (1024 * 1024):.2f} MB")
    print(f"Time Usage  : {time_taken:.6f} seconds\n")

def show_procedure(board_list: list, depth_list: list = None):
    """
        Visually show the step-by-step board transformation during the solving process.
        Optionally displays search depth per step if depth_list is provided.
    """
    depth_flag = None != depth_list
    skip_flag = False
    # get difference between two boards
    def get_diff(prev, curr):
        diff = set()
        for i in range(9):
            for j in range(9):
                if prev[i][j] != curr[i][j]:
                    diff.add((i, j))
        return diff

    total_step = len(board_list)
    step = 4
    current_step = 0

    for start in range(0, total_step, step):
        end = min(start + step, total_step)
        boards = board_list[start:end]
        depths = depth_list[start:end] if depth_flag else None
        diffs = []

        # get differences between previous and current boards
        for i in range(len(boards)):
            if start + i == 0:
                diffs.append(set())
            else:
                prev = board_list[start + i - 1]
                curr = boards[i]
                diffs.append(get_diff(prev, curr))

        # start to print
        print("\n" * 5)
        print(f"Max Depth: {max(depth_list)}" if depth_flag else "")
        for row in range(9):
            for b_idx, board in enumerate(boards):
                for col in range(9):
                    if col % 3 == 0 and col != 0:
                        print(" | ", end="")
                    val = board[row][col]
                    if (row, col) in diffs[b_idx]:
                        if val == 0:
                            print(f" < ", end="")
                        else:
                            print(f"*{val}*", end="")
                    else:
                        print(f" {val if val != 0 else ' '} ", end="")

                # arrow in the middle row only
                if row == 4 and b_idx < len(boards) - 1:
                    print(" -> ", end=" ")
                else:
                    print("  ", end="   ")  # spacing between boards

            print()

            # horizontal border (only once between row blocks)
            if row % 3 == 2 and row != 8:
                for _ in range(len(boards)):
                    print("- " * 17, end="    ")
                print()

        # print depths below each board
        if depth_flag:
            for b_idx, depth in enumerate(depths):
                print(f"          depth {depth:<2}                ", end="     ")
            print("\n")
        else:
            print("")
        print(f"Showing steps {start + 1}-{end} of {total_step}.")

        # input prompt to continue or skip
        if not skip_flag and end < total_step:
            choice = input(
                f"Press Enter to continue, or 'y' to skip to last step: ")
            if choice.strip().lower() == 'y':
                skip_flag = True

    print(f"\nFinished showing all {total_step} steps.\nReturning to menu...\n")

def animate_solving():
    """
        Display an animated 'Solving...' text in the terminal while the solver runs,
        using a separate thread.
    """
    symbols = ["Solving.  ", "Solving.. ", "Solving..."]
    idx = 0
    while solving:
        print("\r" + symbols[idx % len(symbols)], end="")
        time.sleep(0.5)
        idx += 1

def display_menu(title, options):
    """
    Display a CLI menu with a given title and list of options.
    """
    print(f"\n{title}")
    print("=" * len(title))
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    print("0. Exit")
    print("=" * len(title))

def trace_function(algorithm, test_data: list):
    """
        Measure time and memory usage of a given Sudoku solving algorithm.
        Also handles threading for animated solving feedback.
        Supports both function-based and class-based algorithm inputs.
        Returns the solution, solving process, optional depth log, time taken, and peak memory used.
    """
    global solving
    solving = True
    anim_thread = threading.Thread(target=animate_solving)
    anim_thread.start()

    tracemalloc.start()
    start_time = time.time()

    # Handle class-based algorithm like SimulatedAnnealingSudoku
    if isinstance(algorithm, type):
        # If a class is passed instead of a function
        instance = algorithm(test_data)
        solved = instance.solve()
        solution = instance.board.tolist() if instance.board is not None else None
        process = instance.process
        depth_log = None

    else:
        # Standard functional algorithm
        result = algorithm(test_data)
        if isinstance(result, tuple):
            # Safe unpacking for different lengths
            solution = result[0] if len(result) > 0 else None
            process = result[1] if len(result) > 1 else []
            depth_log = result[2] if len(result) > 2 else None
        else:
            # Single result fallback
            solution = result
            process = []
            depth_log = None

    solving = False
    anim_thread.join()
    print("\rDone !                            ")

    end_time = time.time()
    time_taken = end_time - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return solution, process, depth_log, time_taken, peak

if __name__ == "__main__":
    # test data 1, easiest
    sudoku_test_data = [
        # easy 1
        [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ],
        # easy 2
        [
            [1, 0, 0, 4, 8, 9, 0, 0, 6],
            [7, 3, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 1, 2, 9, 5],
            [0, 0, 7, 1, 2, 0, 6, 0, 0],
            [5, 0, 0, 7, 0, 3, 0, 0, 8],
            [0, 0, 6, 0, 9, 5, 7, 0, 0],
            [9, 1, 4, 6, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 3, 7],
            [8, 0, 0, 5, 1, 2, 0, 0, 4]
        ],
        # Intermediate 3
        [
            [0, 2, 0, 6, 0, 8, 0, 0, 0],
            [5, 8, 0, 0, 0, 9, 7, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
            [3, 7, 0, 0, 0, 0, 5, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 8, 0, 0, 0, 0, 1, 3],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 9, 8, 0, 0, 0, 3, 6],
            [0, 0, 0, 3, 0, 6, 0, 9, 0]
        ],
        # Difficult 4
        [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ],
        # Difficult 5
        [
            [2, 0, 0, 3, 0, 0, 0, 0, 0],
            [8, 0, 4, 0, 6, 2, 0, 0, 3],
            [0, 1, 3, 8, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 2, 0, 3, 9, 0],
            [5, 0, 7, 0, 0, 0, 6, 2, 1],
            [0, 3, 2, 0, 0, 6, 0, 0, 0],
            [0, 2, 0, 0, 0, 9, 1, 4, 0],
            [6, 0, 1, 2, 5, 0, 8, 0, 9],
            [0, 0, 0, 0, 0, 1, 0, 0, 2]
        ],
        # Not Fun 6
        [
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]
        ],
        # Extreme 7
        [
            [5, 0, 0, 4, 0, 0, 1, 0, 0],
            [3, 0, 0, 0, 0, 5, 0, 0, 7],
            [0, 9, 0, 0, 0, 3, 5, 0, 0],
            [2, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 8, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 9],
            [0, 0, 6, 0, 0, 0, 4, 0, 0],
            [0, 0, 1, 0, 0, 9, 2, 0, 0],
            [4, 0, 0, 0, 5, 0, 0, 8, 0]
        ],
        # Extreme 8
        [
            [0, 9, 3, 4, 7, 0, 0, 6, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 1],
            [8, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 3, 4, 0, 0, 9, 0, 0, 5],
            [1, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 2, 0, 0],
            [0, 6, 7, 0, 9, 0, 0, 1, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        # Extreme 9
        [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 0],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ],
        # cannot been solved 10
        [
            [5, 1, 6, 8, 4, 9, 7, 3, 2],
            [3, 0, 7, 6, 0, 5, 0, 0, 0],
            [8, 0, 9, 7, 0, 0, 0, 6, 5],
            [1, 3, 5, 0, 6, 0, 9, 0, 7],
            [4, 7, 2, 5, 9, 1, 0, 0, 6],
            [9, 6, 8, 3, 7, 0, 5, 0, 0],
            [2, 5, 3, 1, 8, 6, 0, 7, 4],
            [6, 8, 4, 2, 0, 7, 0, 5, 0],
            [7, 9, 1, 0, 5, 0, 6, 0, 8]
        ]
    ]

    algorithms_function = [solve_sudoku_a_star, solve_sudoku_with_logging, bfs_sudoku_solver,
                           iterative_deepening, SimulatedAnnealingSudoku]

    exit_flag = False
    sudoku_data = 0
    algorithm_function = iterative_deepening
    compare_all = False

    while not exit_flag:
        display_menu("Sudoku Solver", ["Select Data Set", "Choose Algorithm", "Solve Sudoku"])
        cmd = input("Enter your choice: ")

        if cmd == "1":
            datasets = [
                "Easy 1", "Easy 2", "Intermediate 1", "Difficult 1", "Difficult 2",
                "Difficult 3", "Extreme 1", "Extreme 2", "Extreme 3", "Impossible"
            ]
            display_menu("Choose Data Set", datasets)
            choice = input("Enter your choice: ")
            if choice.isdigit() and 0 <= int(choice) <= 10:
                if int(choice) == 0:
                    continue
                sudoku_data = int(choice) - 1
                print("\nSelected Sudoku Board:")
                print_board(sudoku_test_data[sudoku_data])
            else:
                print("Invalid choice.\n")

        elif cmd == "2":
            algorithms = [
                "A* Search", "Backtracking Search", "Breadth First Search", "Iterative Deepening Search",
                "Simulated Annealing", "Compare all algorithms"
            ]
            display_menu("Choose Algorithm", algorithms)
            algorithms_choice = input("Enter your choice: ")
            if algorithms_choice.isdigit() and 0 <= int(algorithms_choice) <= 6:
                if int(algorithms_choice) == 0:
                    continue
                if int(algorithms_choice) == 6:
                    compare_all = True
                else:
                    compare_all = False
                    algorithm_function = algorithms_function[int(algorithms_choice) - 1]
                    print(f"\nSelected Algorithms: {algorithms[int(algorithms_choice) - 1]}")
            else:
                print("Invalid choice.\n")

        elif cmd == "3":
            if compare_all:
                print("\nComparing all algorithms on the selected Sudoku puzzle...\n")
                algorithms = [
                    "A* Search", "Backtracking", "Breadth First Search",
                    "Iterative Deepening", "Simulated Annealing"
                ]

                results = []
                names = []
                for i, alg in enumerate(algorithms_function):
                    print(f"Running {algorithms[i]}...")
                    try:
                        solution, process, depth_log, time_taken, peak = trace_function(
                            alg, sudoku_test_data[sudoku_data]
                        )
                        results.append((solution, time_taken, peak))
                        names.append(algorithms[i])
                    except Exception as e:
                        print(f"{algorithms[i]} failed: {e}")
                        results.append((None, None, None))
                        names.append(algorithms[i])

                print("\nAll algorithms completed. Showing final boards\n")

                # Print algorithm names as headings
                for i, (board, time_taken, peak) in enumerate(results):
                    print(f"{names[i]:^30}")
                    print_sudoku_result(board, time_taken, peak)

                # Print time and memory usage per algorithm
                print("\nPerformance Summary:")
                for i, (s, t, m) in enumerate(results):
                    if t is not None:
                        solve = "  Solved  " if s is not None else "Not Solved"
                        print(f"{names[i]:<25} | {solve} | Time: {t:.4f}s | Memory: {m / (1024 * 1024):.2f} MB")
                    else:
                        print(f"{names[i]:<25} | Failed to run.")

            else:
                print("\nSolving the selected Sudoku puzzle...")
                solution, process, depth_log, time_taken, peak = trace_function(algorithm_function,
                                                                                           sudoku_test_data[sudoku_data])

                print(f"Memory Usage: {peak / (1024 * 1024):.2f} MB")
                print(f"Time Usage  : {time_taken:.6f} seconds\n")

                # Interactive loop
                # Interactive loop
                while True:
                    print(f"  1. View full solving process")
                    print("  2. View final solved board")
                    print("  0. Exit\n")

                    cmd = input("Enter your choice: ").strip()

                    if cmd == '0':
                        print("Exiting. Goodbye!")
                        break
                    elif cmd == '2':
                        print_sudoku_result(solution, time_taken, peak)
                    elif cmd == '1':
                        show_procedure(process)
                    else:
                        print("Invalid input. Please enter 0, 1, or 2.\n")
        elif cmd == "0":
            exit_flag = True
        else:
            print("Invalid input. Please try again.")