import copy
import time
import tracemalloc
from main.KongJiShou_TanZhongYen_NgZheWei_CheaHongJun_TeohYongMing import sudoku_function as sf  # Contains helper methods like printing board and animation
from collections import deque

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
# Check if a number is valid in a given cell
# --------------------------------------------
def is_valid(board, row, col, num):
    """
    Return True if placing `num` at (row, col) is valid in current board.
    Checks row, column, and 3x3 subgrid.
    """
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

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

        path_list.append(copy.deepcopy(current_board))
        breadth_levels.append(breadth)

        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board, path_list, breadth_levels  # Solved

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = copy.deepcopy(current_board)
                new_board[row][col] = num
                queue.append((new_board, breadth + 1))

    return None, path_list, breadth_levels  # No solution found

# --------------------------------------------
# Main Test Script
# --------------------------------------------
if __name__ == "__main__":
    # Sample Sudoku puzzle (moderate difficulty)
    sudoku_board = [
        [0, 9, 3, 4, 7, 0, 0, 6, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 1],
        [8, 0, 0, 0, 0, 0, 0, 3, 0],
        [0, 3, 4, 0, 0, 9, 0, 0, 5],
        [1, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 2, 0, 0],
        [0, 6, 7, 0, 9, 0, 0, 1, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    print("Solving...\n")

    # Start memory and time tracking
    tracemalloc.start()
    start_time = time.time()

    # Run the BFS solver
    solved_board, path_list, breadth_levels = bfs_sudoku_solver(sudoku_board)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Show the solving animation
    sf.show_procedure(path_list, breadth_levels)

    # Output performance statistics
    print(f"\nSolved in {end_time - start_time:.2f} seconds")
    print(f"Peak memory usage: {peak / (1024 ** 2):.2f} MB")
