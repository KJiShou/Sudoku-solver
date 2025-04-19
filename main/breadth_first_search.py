import copy
import time
import tracemalloc
import sudoku_function as sf
from collections import deque

# Tidy board printing with highlighted changes
def print_board_tidy(board, prev_board=None):
    print("-" * 49)
    for i in range(9):
        row = ""
        for j in range(9):
            if j % 3 == 0:
                row += "| "
            num = board[i][j]
            if prev_board and prev_board[i][j] != num:
                if num == 0:
                    cell = "     "
                else:
                    cell = f"*{num}*".center(5)
            else:
                if num == 0:
                    cell = "     "
                else:
                    cell = f"{num}".center(5)
            row += cell
        row += "|"
        print(row)
        if (i + 1) % 3 == 0:
            print("-" * 49)

# Find next empty cell
def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# Check validity
def is_valid(board, row, col, num):
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

# BFS Sudoku Solver
def bfs_sudoku_solver(board):
    queue = deque([(board, 0)])  # (board, breadth level)
    path_list = []               # Store board states
    breadth_levels = []          # Store corresponding breadth levels

    while queue:
        current_board, breadth = queue.popleft()

        path_list.append(copy.deepcopy(current_board))
        breadth_levels.append(breadth)

        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board, path_list, breadth_levels

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = copy.deepcopy(current_board)
                new_board[row][col] = num
                queue.append((new_board, breadth + 1))

    return None, path_list, breadth_levels

if __name__ == "__main__":
    # Sample Sudoku board
    sudoku_board = [
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

    # Run solver and store the full path
    solved_board, path_list, breadth_levels = bfs_sudoku_solver(sudoku_board)
    sf.show_procedure(path_list, breadth_levels)
