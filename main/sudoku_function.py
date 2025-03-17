import time
import tracemalloc
from copy import deepcopy

# TODO: show one by one the 2D array && process bar

process = list()

# function to print sudoku board
def print_sudoku(board: list):
    print("\n" * 10)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else " ", end=" ")
        print()
    print()

def show_procedure(board: list):
    total_step = len(board)
    for i in range(total_step):
        print_sudoku(board[i])
        # TODO: a more reactive UI for next step && showing the remaining step
        print(f"Process({i+1}/{total_step})")
        if i + 1 == total_step:
            input("Press Enter to continue...")
            return
        if input("next? (y/n): ").lower() == "y":
            pass
        else:
            return


def is_valid(board, num, row, col):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, num, row, col):
                        board[row][col] = num
                        process.append(deepcopy(board))
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def sudoku_solver():
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
    solve(sudoku_data)

    # record end time
    end_time = time.time()
    time_taken = end_time - start_time
    show_procedure(process)

    # Get current and peak memory usage
    _, peak = tracemalloc.get_traced_memory()

    # result
    print_sudoku(process[-1])
    print(f"📊 Memory Usage: {peak / (1024 * 1024):.2f} MB")
    print(f"📊 Time Usage  : {time_taken:.6f} seconds")

    tracemalloc.stop()  # Stop tracking
