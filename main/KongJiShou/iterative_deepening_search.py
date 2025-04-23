import time
import tracemalloc
from copy import deepcopy
import threading
from main.KongJiShou_TanZhongYen_NgZheWei_CheaHongJun_TeohYongMing import sudoku_function as sdk  # Contains helper methods like printing board and animation


def find_empty(board):
    """
    Find the first empty cell in the Sudoku board.
    Returns a tuple (row, col) if found, or None if the board is full.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def dfs(board, depth, max_depth, process, depth_log):
    """
    Perform Depth-First Search with a depth limit.
    If a solution is found within the current depth, return True.
    Logs each step and depth for visualization.
    """
    if depth > max_depth:
        return False

    empty = find_empty(board)
    if not empty:
        return True  # Puzzle is solved

    row, col = empty

    for num in range(1, 10):
        if sdk.is_valid(board, num, row, col):
            board[row][col] = num
            process.append(deepcopy(board))
            depth_log.append(depth + 1)

            if dfs(board, depth + 1, max_depth, process, depth_log):
                return True

            board[row][col] = 0  # Backtrack if not successful

    return False


def iterative_deepening(board):
    """
    Solve the Sudoku using Iterative Deepening Search.
    Starts with a shallow depth and increases it until a solution is found.
    Logs the solving process and depth levels.
    """
    process = []
    depth_log = []

    empty_cells = sum(row.count(0) for row in board)
    for max_depth in range(empty_cells, 81):  # 81 is the max number of empty moves
        copied_board = deepcopy(board)
        process.append(deepcopy(board))
        depth_log.append(0)
        if dfs(copied_board, 0, max_depth, process, depth_log):
            return copied_board, process, depth_log
    return None, process, depth_log


if __name__ == "__main__":
    # Sample Sudoku puzzle to test
    sudoku_test_data_10 = [
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

    # Start animation thread (shows "Solving..." animation)
    solving = True
    anim_thread = threading.Thread(target=sdk.animate_solving)
    anim_thread.start()

    # Start memory and time tracking
    tracemalloc.start()
    start_time = time.time()

    # Solve the puzzle using IDS
    solution, process, depth_log = iterative_deepening(sudoku_test_data_10)

    # Stop animation
    sdk.solving = False
    anim_thread.join()
    print("\rDone !                            ")

    # End tracking
    end_time = time.time()
    time_taken = end_time - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Output performance results
    print(f"\nSudoku Solved!")
    print(f"Memory Usage: {peak / (1024 * 1024):.2f} MB")
    print(f"Time Usage  : {time_taken:.6f} seconds\n")

    # CLI interaction to review solving process or result
    while True:
        print("Options:")
        print("  - press 1 show process")
        print("  - Type 'result' to see the final solved board")
        print("  - Type 'exit' to quit\n")

        cmd = input("What would you like to see? \n").strip().lower()

        if cmd == 'exit':
            print("Exiting. Goodbye!")
            break
        elif cmd == 'result':
            sdk.print_sudoku_result(solution, time_taken, peak)
        elif cmd == "1":
            sdk.show_procedure(process, depth_log)
        else:
            print("Invalid command. Try again.\n")
