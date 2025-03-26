import sudoku_function as sudoku
import time
import tracemalloc
from copy import deepcopy

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def dfs(board, depth, max_depth, process):
    if depth > max_depth:
        return False

    empty = find_empty(board)
    if not empty:
        return True  # Solved

    row, col = empty

    for num in range(1, 10):
        if sudoku.is_valid(board, num, row, col):
            board[row][col] = num
            process.append(deepcopy(board))

            if dfs(board, depth + 1, max_depth, process):
                return True

            board[row][col] = 0  # Backtrack

    return False


def iterative_deepening(board):
    process = []
    for max_depth in range(1, 82):  # max 81 moves
        copied_board = deepcopy(board)
        if dfs(copied_board, 0, max_depth, process):
            return copied_board, process
    return None, process

if __name__ == "__main__":
    # example data of sudoku
    sudoku_data = [
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

    sudoku_answer_data = [
        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ],
        [
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
    ]

    # Start tracking
    tracemalloc.start()
    start_time = time.time()

    # solve function
    solution, process = iterative_deepening(sudoku_data)

    # record end time
    end_time = time.time()
    time_taken = end_time - start_time

    if solution:
        sudoku.show_procedure(process)
    else:
        print("No solution found.")

    # Get current and peak memory usage
    _, peak = tracemalloc.get_traced_memory()

    # result
    sudoku.print_sudoku(sudoku.process[-1])
    print(f"📊 Memory Usage: {peak / (1024 * 1024):.2f} MB")
    print(f"📊 Time Usage  : {time_taken:.6f} seconds")

    tracemalloc.stop()  # Stop tracking
