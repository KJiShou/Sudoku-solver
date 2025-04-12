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
def bfs_sudoku_solver(board, mode):
    start_time = time.time()
    tracemalloc.start()

    queue = deque([(board, 0)])  # (board, breadth level)
    step = 0
    enter_press_count = 0
    skip_to_end = False
    enter_limit_before_skip_prompt = 5
    visited = set()

    path_list = []         # Store board states
    breadth_levels = []    # Store corresponding breadth levels

    while queue:
        current_board, breadth = queue.popleft()
        step += 1

        path_list.append(copy.deepcopy(current_board))
        breadth_levels.append(breadth)

        if mode == 1 and not skip_to_end:
            print(f"\nStep {step} | Breadth Level {breadth}")
            print_board_tidy(current_board, prev_board=None if step == 1 else prev_board)
            input("Press Enter to continue...")
            enter_press_count += 1

            if enter_press_count % enter_limit_before_skip_prompt == 0:
                choice = input("Do you want to skip to the final result now? (y/n): ").strip().lower()
                if choice == 'y':
                    skip_to_end = True

        elif mode == 2:
            print(f"\nStep {step} | Breadth Level {breadth}")
            print_board_tidy(current_board, prev_board=None if step == 1 else prev_board)
            time.sleep(0.05)

        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print("\nSudoku Solved! Final board:")
            print_board_tidy(current_board)
            print(f"\nTotal steps: {step}")
            print(f"Final breadth level: {breadth}")
            print(f"Time taken: {end_time - start_time:.4f} seconds")
            print(f"Peak memory usage: {peak / (1024 * 1024):.2f} MB")

            # Return final board, full path, and levels
            return current_board, path_list, breadth_levels

        row, col = empty_cell
        prev_board = current_board
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = copy.deepcopy(current_board)
                new_board[row][col] = num
                queue.append((new_board, breadth + 1))

    print("\nNo solution found.")
    return None, path_list, breadth_levels

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

# Mode selection
print("Sudoku Solver - Breadth-First Search")
print("Select mode:")
print("1. Manual (press Enter for each step)")
print("2. Auto step-by-step")
print("3. Direct to final result")
while True:
    try:
        mode = int(input("Enter mode (1/2/3): "))
        if mode in [1, 2, 3]:
            break
        else:
            print("Please choose 1, 2, or 3.")
    except ValueError:
        print("Invalid input. Try again.")

if mode == 3:
    mode = 0  # For skipping to final

# Run solver and store the full path
solved_board, path_list, breadth_levels = bfs_sudoku_solver(sudoku_board, mode)
sf.show_procedure(path_list, breadth_levels)

# Optional: print path afterwards
# for idx, (b, lvl) in enumerate(zip(path_list, breadth_levels), 1):
#     print(f"\nStep {idx} | Breadth Level {lvl}")
#     print_board_tidy(b)
