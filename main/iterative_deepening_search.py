import time
import tracemalloc
from copy import deepcopy
import threading
import sudoku_function as sdk

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def dfs(board, depth, max_depth, process, depth_log):
    if depth > max_depth:
        return False

    empty = find_empty(board)
    if not empty:
        return True  # Solved

    row, col = empty

    for num in range(1, 10):
        if sdk.is_valid(board, num, row, col):
            board[row][col] = num
            process.append(deepcopy(board))
            depth_log.append(depth + 1)

            if dfs(board, depth + 1, max_depth, process, depth_log):
                return True

            board[row][col] = 0  # Backtrack

    return False



def iterative_deepening(board):
    process = []
    depth_log = []

    empty_cells = sum(row.count(0) for row in board)
    for max_depth in range(empty_cells, 81):  # max 81 moves
        copied_board = deepcopy(board)
        process.append(deepcopy(board))
        depth_log.append(0)
        if dfs(copied_board, 0, max_depth, process, depth_log):
            return copied_board, process, depth_log
    return None, process, depth_log


if __name__ == "__main__":
    # example data of sudoku
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

    # Start animation
    solving = True
    anim_thread = threading.Thread(target=sdk.animate_solving)
    anim_thread.start()

    # Start tracking
    tracemalloc.start()
    start_time = time.time()

    solution, process, depth_log = iterative_deepening(sudoku_test_data_10)

    # Stop animation
    sdk.solving = False
    anim_thread.join()
    print("\rDone !                            ")

    end_time = time.time()
    time_taken = end_time - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nSudoku Solved!")
    print(f"Memory Usage: {peak / (1024 * 1024):.2f} MB")
    print(f"Time Usage  : {time_taken:.6f} seconds\n")

    # Interactive loop
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
            sdk.print_sudoku_result(solution)
        elif cmd == "1" :
            sdk.show_procedure(process, depth_log)
        else:
            print("Invalid command. Try again.\n")
