import time
import tracemalloc
from copy import deepcopy

solving = True
display_final = False

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

def print_sudoku(board: list, highlight=None):
    print("\n" * 2)
    for row in range(9):
        row_str = ""
        for col in range(9):
            val = board[row][col]
            if highlight and (row, col) in highlight:
                cell = f"\033[91m{val if val != 0 else ' '}\033[0m"
            else:
                cell = f"{val if val != 0 else ' '}"
            row_str += f" {cell} "
            if col % 3 == 2 and col != 8:
                row_str += "|"
        print(row_str)
        if row % 3 == 2 and row != 8:
            print("-" * 31)

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def user_continue():
    global display_final
    user_input = input("Press Enter or enter '1' skip to final result : ")
    if user_input.strip() == '1':
        display_final = True

def backtrack(board, process):
    global display_final
    empty = find_empty(board)
    if not empty:
        return True  # Solved
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            process.append((deepcopy(board), [(row, col)]))
            if not display_final:
                print_sudoku(board, [(row, col)])
                print(f"\nTrying number '{num}' at cell ({row}, {col}) \n")
                user_continue()
            if backtrack(board, process):
                return True
            board[row][col] = 0  # Backtrack
            process.append((deepcopy(board), [(row, col)]))
            if not display_final:
                print_sudoku(board, [(row, col)])
                print(f"\nBacktracking, removing number '{num}' from cell ({row}, {col}) \n")
                user_continue()
    return False

if __name__ == "__main__":
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
    process = []
    tracemalloc.start()
    start_time = time.time()
    backtrack(sudoku_data, process)
    end_time = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print("\n✅ Sudoku Solved!")
    print(f"📊 Memory Usage: {peak / (1024 * 1024):.2f} MB")
    print(f"📊 Time Usage  : {end_time - start_time:.6f} seconds\n")
    print_sudoku(sudoku_data)
