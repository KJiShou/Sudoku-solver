
import time
import tracemalloc
from copy import deepcopy
import threading

# Animation thread flag
solving = True


def is_valid(board: list, num: int, row: int, col: int) -> bool:
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True



def animate_solving():
    symbols = ["Solving.  ", "Solving.. ", "Solving..."]
    idx = 0
    while solving:
        print("\r" + symbols[idx % len(symbols)], end="")
        time.sleep(0.5)
        idx += 1


# function to print sudoku board
def print_sudoku(board: list):
    print("\n" * 5)
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


def show_procedure(board_list: list, depth_list: list):
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
        depths = depth_list[start:end]
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
        print(f"Max Depth: {max(depth_list)}")
        for row in range(9):
            for b_idx, board in enumerate(boards):
                for col in range(9):
                    if col % 3 == 0 and col != 0:
                        print(" | ", end="")
                    val = board[row][col]
                    if (row, col) in diffs[b_idx] and val != 0:
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
        for b_idx, depth in enumerate(depths):
            print(f"          depth {depth:<2}                ", end="     ")
        print("\n")

        # input prompt to continue or skip
        if end < total_step:
            choice = input(
                f"Showing steps {start + 1}-{end} of {total_step}. Press Enter to continue, or 'y' to skip to last step: ")
            if choice.strip().lower() == 'y':
                break

    print(f"\nFinished showing all {total_step} steps for this depth.\nReturning to menu...\n")


if __name__ == "__main__":
    # test data 1, easiest
    sudoku_test_data_1 = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]

    sudoku_test_data_2 = [
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 6, 0, 0],
        [5, 0, 0, 7, 0, 3, 0, 0, 8],
        [0, 0, 6, 0, 9, 5, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 7],
        [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ]

    # Intermediate
    sudoku_test_data_3 = [
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0]
    ]

    # Difficult
    sudoku_test_data_4 = [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ]

    sudoku_test_data_5 = [
        [2, 0, 0, 3, 0, 0, 0, 0, 0],
        [8, 0, 4, 0, 6, 2, 0, 0, 3],
        [0, 1, 3, 8, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 2, 0, 3, 9, 0],
        [5, 0, 7, 0, 0, 0, 6, 2, 1],
        [0, 3, 2, 0, 0, 6, 0, 0, 0],
        [0, 2, 0, 0, 0, 9, 1, 4, 0],
        [6, 0, 1, 2, 5, 0, 8, 0, 9],
        [0, 0, 0, 0, 0, 1, 0, 0, 2]
    ]

    # Not Fun
    sudoku_test_data_6 = [
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 3],
        [0, 7, 4, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 2],
        [0, 8, 0, 0, 4, 0, 0, 1, 0],
        [6, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 7, 8, 0],
        [5, 0, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 4, 0]
    ]

    # Extreme
    sudoku_test_data_7 = [
        [5, 0, 0, 4, 0, 0, 1, 0, 0],
        [3, 0, 0, 0, 0, 5, 0, 0, 7],
        [0, 9, 0, 0, 0, 3, 5, 0, 0],
        [2, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 8, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 6, 0, 0, 0, 4, 0, 0],
        [0, 0, 1, 0, 0, 9, 2, 0, 0],
        [4, 0, 0, 0, 5, 0, 0, 8, 0]
    ]

    sudoku_test_data_8 = [
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

    # world hardest sudoku
    sudoku_test_data_9 = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 0],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]

    # cannot been solved
    sudoku_test_data_10 = [
        [4, 7, 9, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [3, 4, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 6, 0, 5, 0, 0, 0, 9],
        [8, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 4, 2, 7],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 9, 5, 0, 0, 0]
    ]
