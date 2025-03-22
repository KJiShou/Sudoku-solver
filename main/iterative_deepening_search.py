import sudoku_function as sudoku
import time
import tracemalloc
from copy import deepcopy


def solve(board: list) -> list:
    process = list()
    # calculate the max depth for the sudoku
    max_depth = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != 0:
                max_depth += 1

    coordinate_x = 0
    coordinate_y = 0
    depth = 0
    while depth < max_depth:
        for i in range(1, 10):
            if sudoku.is_valid(board, i, coordinate_x, coordinate_y):
                board[coordinate_x][coordinate_y] = i
                process.append(deepcopy(board))
            else:
                pass


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
    # sudoku.solve(sudoku_data)

    # record end time
    end_time = time.time()
    time_taken = end_time - start_time
    sudoku.show_procedure(sudoku.process)

    # Get current and peak memory usage
    _, peak = tracemalloc.get_traced_memory()

    # result
    sudoku.print_sudoku(sudoku.process[-1])
    print(f"📊 Memory Usage: {peak / (1024 * 1024):.2f} MB")
    print(f"📊 Time Usage  : {time_taken:.6f} seconds")

    tracemalloc.stop()  # Stop tracking
