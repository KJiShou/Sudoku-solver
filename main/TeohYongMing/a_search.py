import heapq
import time
import tracemalloc
from copy import deepcopy
from main.KongJiShou_TanZhongYen_NgZheWei_CheaHongJun_TeohYongMing import sudoku_function as func  # Contains helper methods like printing board and animation


# ======== Display Functions ========

def print_sudoku_board(board: list):
    """
    Format and return the Sudoku board as a string for pretty printing.
    """
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
    """
    Automatically display all board states in the solving path with a short delay.
    """
    total_step = len(board_list)
    for i in range(total_step):
        print(f"\nStep {i + 1}:")
        print(print_sudoku_board(board_list[i]))
        time.sleep(0.5)  # Adjust speed if needed


# ======== Sudoku Logic & Heuristic ========

def is_valid(board, row, col, num):
    """
    Check if placing `num` at (row, col) is valid under Sudoku rules.
    """
    if num in board[row]:  # Row check
        return False
    for i in range(9):  # Column check
        if board[i][col] == num:
            return False
    # Box check
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty(board):
    """
    Find the empty cell with the fewest valid candidate numbers (MRV heuristic).
    """
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
    """
    Heuristic function: returns number of violations in the board.
    Violations = repeated numbers in rows, columns, and boxes.
    """
    violations = 0

    # Row violations
    for row in board:
        seen = set()
        for num in row:
            if num != 0 and num in seen:
                violations += 1
            seen.add(num)

    # Column violations
    for col in range(9):
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != 0 and num in seen:
                violations += 1
            seen.add(num)

    # Box violations
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


# ======== A* Sudoku Solver ========

def solve_sudoku_a_star(initial_board, show_steps=False):
    """
    Solve Sudoku using A* search algorithm with heuristic guidance.
    Returns:
        - final board
        - list of visited boards (process path)
        - None (placeholder for compatibility)
    """

    open_list = [(heuristic(initial_board), 0, deepcopy(initial_board), [deepcopy(initial_board)])]
    closed_set = set()

    while open_list:
        f, g, current_board, path = heapq.heappop(open_list)
        board_tuple = tuple(map(tuple, current_board))

        if board_tuple in closed_set:
            continue
        closed_set.add(board_tuple)

        if heuristic(current_board) == 0 and find_empty(current_board) is None:
            return current_board, path, None

        empty_cell = find_empty(current_board)
        if empty_cell is None:
            return current_board, path, None

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = deepcopy(current_board)
                new_board[row][col] = num
                h = heuristic(new_board)
                new_path = deepcopy(path)
                new_path.append(deepcopy(new_board))
                heapq.heappush(open_list, (g + 1 + h, g + 1, new_board, new_path))

    return None, path, None


# ======== Main Program / Menu ========

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
                func.show_procedure(path)  # External function for side-by-side visual
                print("\nFinal Solved Board:")
                print(print_sudoku_board(solved_board))
            else:
                print("No solution found.")
            break

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
