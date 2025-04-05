import copy
import time
import tracemalloc
from collections import deque

# Sudoku utility functions
def print_board(board):
    print("\n" + "-" * 25)
    for i in range(9):
        row = ""
        for j in range(9):
            if j % 3 == 0:
                row += "| "
            cell = board[i][j]
            row += (str(cell) if cell != 0 else " ") + " "
        row += "|"
        print(row)
        if (i + 1) % 3 == 0:
            print("-" * 25)

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

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

# Main BFS Solver
def bfs_sudoku_solver(board, mode):
    start_time = time.time()
    tracemalloc.start()

    queue = deque([board])
    step = 0
    enter_press_count = 0
    skip_to_end = False
    enter_limit_before_skip_prompt = 5

    while queue:
        current_board = queue.popleft()
        step += 1

        if mode == 1 and not skip_to_end:
            print(f"\nStep {step}")
            print_board(current_board)
            input("Press Enter to continue...")
            enter_press_count += 1

            if enter_press_count % enter_limit_before_skip_prompt == 0:
                choice = input("Do you want to skip to the final result now? (y/n): ").strip().lower()
                if choice == 'y':
                    skip_to_end = True

        elif mode == 2:
            print(f"\nStep {step}")
            print_board(current_board)
            time.sleep(0.1)

        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print("\nSudoku Solved! Final board:")
            print_board(current_board)
            print(f"\nTotal steps: {step}")
            print(f"Time taken: {end_time - start_time:.4f} seconds")
            print(f"Peak memory usage: {peak / (1024 * 1024):.2f} MB")
            return current_board

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = copy.deepcopy(current_board)
                new_board[row][col] = num
                queue.append(new_board)

    print("\nNo solution found.")
    return None

# Sample board
sudoku_board = [
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

bfs_sudoku_solver(sudoku_board, mode)
