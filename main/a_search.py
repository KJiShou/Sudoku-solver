import heapq
import time
import tracemalloc
from copy import deepcopy
import sudoku_function as func

def print_sudoku_board(board: list):
    output = ""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            output += "- - - - - - - - - - -\n"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                output += "| "
            num = board[i][j]
            output += f"{num if num != 0 else ' '} "
        output += "\n"
    return output

def show_procedure_auto(board_list: list):
    total_step = len(board_list)
    for i in range(total_step):
        print(f"\nStep {i + 1}:")
        print(print_sudoku_board(board_list[i]))
        time.sleep(0.5) # Adjust speed if needed

def is_valid(board, row, col, num):
    """Checks if placing 'num' at (row, col) is valid for that specific cell."""
    # Check row
    if num in board[row]:
        return False
    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False
    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty(board):
    """Finds the empty cell with the fewest possible valid values."""
    min_options = float('inf')
    best_empty = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                options = 0
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        options += 1
                if options < min_options:
                    min_options = options
                    best_empty = (row, col)
    return best_empty

def heuristic(board):
    """Heuristic: total number of rule violations in the current grid."""
    violations = 0
    # Check rows
    for row in board:
        seen = set()
        for num in row:
            if num != 0 and num in seen:
                violations += 1
            seen.add(num)
    # Check columns
    for col in range(9):
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != 0 and num in seen:
                violations += 1
            seen.add(num)
    # Check 3x3 blocks
    for block_row in range(3):
        for block_col in range(3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    num = board[3 * block_row + i][3 * block_col + j]
                    if num != 0 and num in seen:
                        violations += 1
                    seen.add(num)
    return violations

def solve_sudoku_a_star(initial_board, show_steps=False):
    """Solves Sudoku using A* search for selecting the next empty cell."""
    tracemalloc.start()
    start_time = time.time()

    open_list = [(heuristic(initial_board), 0, deepcopy(initial_board), [deepcopy(initial_board)])]  # (f, g, board, path)
    closed_set = set()
    path = []
    while open_list:
        f, g, current_board, path = heapq.heappop(open_list)
        board_tuple = tuple(map(tuple, current_board))

        if board_tuple in closed_set:
            continue
        closed_set.add(board_tuple)

        if heuristic(current_board) == 0 and find_empty(current_board) is None:
            return current_board, path, None

        empty_cell = find_empty(current_board)
        if empty_cell is None: # Should be caught by the heuristic check above, but for robustness
            return current_board, path, None

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = deepcopy(current_board)
                new_board[row][col] = num
                h = heuristic(new_board)
                new_path = deepcopy(path)
                new_path.append(deepcopy(new_board))
                new_state = (g + 1 + h, g + 1, new_board, new_path)
                heapq.heappush(open_list, new_state)

    return None, path, None

if __name__ == "__main__":
    sudoku_board = [
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

    while True:
        choice = input("Select an option:\n"
                       " 1.  Show final result\n"
                       " 2.  Step by step\n"
                       " 3.  Show all steps automatically\n"
                       " 00. Exit\n\n"
                       " Enter your choice: ")
        if choice == '1':
            solved_board, _, _ = solve_sudoku_a_star(sudoku_board)
            if solved_board:
                print("\nFinal Solved Board:")
                print(print_sudoku_board(solved_board))
            else:
                print("No solution found.")
            break
        elif choice == '2':
            solved_board, path, _ = solve_sudoku_a_star(sudoku_board)
            if solved_board:
                print("\nSolving Steps:")
                func.show_procedure(path)
                print("\nFinal Solved Board:")
                print(print_sudoku_board(solved_board))
            else:
                print("No solution found.")
            break
        # Printing all steps automatically, remove if necessary
        elif choice == '3':
            solved_board, path, _ = solve_sudoku_a_star(sudoku_board)
            if solved_board:
                print("\nSolving Steps:")
                show_procedure_auto(path)
                print("\nFinal Solved Board:")
                print(print_sudoku_board(solved_board))
            else:
                print("No solution found.")
            break
        elif choice == '00':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 00.")