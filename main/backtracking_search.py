import time
import tracemalloc
from copy import deepcopy

# ======= Utility Functions =======

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
    print("\n" * 1)
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

# ======= Backtracking Solver =======

def solve_sudoku_with_logging(board):
    process = []
    depth_log = []

    board_copy = deepcopy(board)
    process.append((deepcopy(board_copy), []))  # Initial state, depth 0
    depth_log.append(0)

    def backtrack(board, depth):
        empty = find_empty(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if is_valid(board, num, row, col):
                board[row][col] = num
                process.append((deepcopy(board)))
                depth_log.append(depth + 1)

                if backtrack(board, depth + 1):
                    return True

                board[row][col] = 0
                process.append((deepcopy(board)))
                depth_log.append(depth + 1)
        return False

# ======= need checking ========
    solved = backtrack(board_copy, 0)
    return (board_copy if solved else None), process, depth_log, None

# ======= Menu & Display =======

def menu_after_solving(process, depth_log, solution):
    step = 0
    enter_limit = 5
    enter_count = 0
    skip = False

    print("\n=== View Options ===")
    print("1. Manual step-by-step (press Enter)")
    print("2. Auto show all steps")
    print("3. Final result only")
    print("4. Exit")
    
    while True:
        choice = input("Choose mode (1/2/3/4): ").strip()
        if choice in ('1', '2', '3', '4'):
            break
        print("Invalid choice.")

    if choice == '4':
        print("Exiting viewer. Goodbye!")
        return

    elif choice == '1':
        for (board, highlight), depth in zip(process, depth_log):
            step += 1
            print(f"\nStep {step} | Depth: {depth}")
            print_sudoku(board, highlight)
            input("Press Enter to continue...")
            enter_count += 1
            if enter_count % enter_limit == 0:
                ans = input("Skip to final result? (y/n): ").lower()
                if ans == 'y':
                    skip = True
            if skip:
                break

        print(f"\nFinal Solved Board (Depth: {depth_log[-1]}):")
        print_sudoku(solution)

    elif choice == '2':
        for step, ((board, highlight), depth) in enumerate(zip(process, depth_log), 1):
            print(f"\nStep {step} | Depth: {depth}")
            print_sudoku(board, highlight)
            time.sleep(0.05)

        print(f"\nFinal Solved Board (Depth: {depth_log[-1]}):")
        print_sudoku(solution)

    else:
        print(f"\nFinal Solved Board (Depth: {depth_log[-1]}):")
        print_sudoku(solution)
        print(f"Max Depth Level: {max(depth_log)}")
        print(f"Steps Taken: {len(process)}")

# ======= Main Program =======

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

    print("\nSolving Sudoku with Backtracking...\n")
    tracemalloc.start()
    start = time.time()

    solution, process, depth_log, _ = solve_sudoku_with_logging(sudoku_data)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution:
        print(f"\nSudoku Solved!\n")
        print(f"Max Depth Level: {max(depth_log)}")
        print(f"Steps Taken: {len(process)}")
        print(f"Memory Usage: {peak / (1024 * 1024):.2f} MB")
        print(f"Time Usage: {end - start:.4f} s")
        menu_after_solving(process, depth_log, solution)
    else:
        print("Puzzle could not be solved.")
