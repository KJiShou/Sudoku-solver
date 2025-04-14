import time
import tracemalloc
from copy import deepcopy

# TODO: record depth_log
# TODO: backtracking func -> solution, process, depth_log, None
# TODO: import sudoku_function and use show_process func

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

def solve_sudoku_with_logging(board):
    process = []
    depth_log = []

    def backtrack(board, depth):
        empty = find_empty(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if is_valid(board, num, row, col):
                board[row][col] = num
                process.append((deepcopy(board), [(row, col)]))
                depth_log.append(depth)
                if backtrack(board, depth + 1):
                    return True
                board[row][col] = 0
                process.append((deepcopy(board), [(row, col)]))
                depth_log.append(depth)
        return False

    board_copy = deepcopy(board)
    solved = backtrack(board_copy, 0)
    return (board_copy if solved else None), process, depth_log

def show_partial_process_by_depth_limit(process, depth_log, depth_limit):
    print(f"\nShowing steps up to depth {depth_limit}:\n")
    for step, ((board_state, highlight), depth) in enumerate(zip(process, depth_log)):
        if depth <= depth_limit:
            print(f"\n--- Step {step + 1} | Depth: {depth} ---")
            print_sudoku(board_state, highlight)
            input("Press Enter to continue...")
        else:
            break
    print("\nDone displaying selected steps.")

def menu_with_depth_options(process, depth_log):
    while True:
        print("\n=== Sudoku Solver Menu ===")
        print("1. Enter a depth limit (max: {}) to view step-by-step".format(max(depth_log) if depth_log else 0))
        print("2. Show final solved board only")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            try:
                limit = int(input("Enter depth limit: ").strip())
                show_partial_process_by_depth_limit(process, depth_log, limit)
            except ValueError:
                print("Invalid input. Please enter an integer.")
        elif choice == '2':
            break
        elif choice == '3':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    sudoku_data = [
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

    tracemalloc.start()
    start_time = time.time()
    solution, process, depth_log = solve_sudoku_with_logging(sudoku_data)
    end_time = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution:
        print("\nSudoku Solved!")
        print(f"🧠 Steps Taken : {len(process)}")
        print(f"📏 Max Depth   : {max(depth_log) if depth_log else 0}")
        print(f"📊 Memory Usage: {peak / (1024 * 1024):.2f} MB")
        print(f"⏱️ Time Usage  : {end_time - start_time:.6f} seconds")

        menu_with_depth_options(process, depth_log)
        print("\nFinal Solved Sudoku:")
        print_sudoku(solution)
    else:
        print("\nThis sudoku puzzle is unsolvable.\n")
