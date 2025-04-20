import time
import tracemalloc
from copy import deepcopy

# ======= Utility Functions =======

def is_valid(board: list, num: int, row: int, col: int) -> bool:
    """
    Check if placing a number in the given cell is valid.
    It must not exist in the same row, column, or 3x3 subgrid.
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


def print_sudoku(board: list):
    """
    Print the Sudoku board in a structured 9x9 grid format.
    """
    print("\n" * 1)
    for row in range(9):
        row_str = ""
        for col in range(9):
            val = board[row][col]
            cell = f"{val if val != 0 else ' '}"
            row_str += f" {cell} "
            if col % 3 == 2 and col != 8:
                row_str += "|"
        print(row_str)
        if row % 3 == 2 and row != 8:
            print("-" * 31)


def find_empty(board):
    """
    Find the first empty cell in the board (represented by 0).
    Returns a tuple (row, col), or None if no empty cells are found.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


# ======= Backtracking Solver =======

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


# ======= Menu & Display =======

def menu_after_solving(process, depth_log, solution):
    """
    Display a menu to the user to view the solving process:
    - step-by-step
    - auto playback
    - final result only
    """
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
        # Manual step-through with Enter
        for board, depth in zip(process, depth_log):
            step += 1
            print(f"\nStep {step} | Depth: {depth}")
            print_sudoku(board)
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
        # Auto-play mode with delay
        for step, (board, depth) in enumerate(zip(process, depth_log), 1):
            print(f"\nStep {step} | Depth: {depth}")
            print_sudoku(board)
            time.sleep(0.05)

        print(f"\nFinal Solved Board (Depth: {depth_log[-1]}):")
        print_sudoku(solution)

    else:
        # Final result only
        print(f"\nFinal Solved Board (Depth: {depth_log[-1]}):")
        print_sudoku(solution)
        print(f"Max Depth Level: {max(depth_log)}")
        print(f"Steps Taken: {len(process)}")


# ======= Main Program =======

if __name__ == "__main__":
    # Sudoku puzzle input
    sudoku_data = [
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

    print("\nSolving Sudoku with Backtracking...\n")
    tracemalloc.start()
    start = time.time()

    # Solve Sudoku and trace
    solution, process, depth_log = solve_sudoku_with_logging(sudoku_data)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Display performance metrics and solution viewer
    if solution:
        print(f"\nSudoku Solved!\n")
        print(f"Max Depth Level: {max(depth_log)}")
        print(f"Steps Taken: {len(process)}")
        print(f"Memory Usage: {peak / (1024 * 1024):.2f} MB")
        print(f"Time Usage: {end - start:.4f} s")
        menu_after_solving(process, depth_log, solution)
    else:
        print("Puzzle could not be solved.")
