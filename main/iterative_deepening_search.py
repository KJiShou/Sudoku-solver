import time
import tracemalloc
from copy import deepcopy
import threading
import sys

# Animation thread flag
solving = True


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


def animate_solving():
    symbols = ["Solving.  ", "Solving.. ", "Solving..."]
    idx = 0
    while solving:
        print("\r🔄 " + symbols[idx % len(symbols)], end="")
        time.sleep(0.5)
        idx += 1


# function to print sudoku board
def print_sudoku(board: list):
    print("\n" * 5)
    for row in range(9):
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")
            val = board[row][col]
            print(f" {val if val != 0 else ' '} ", end="")
        print()
        if row % 3 == 2 and row != 8:
            print("- " * 17)
    print("\n          ✅ FINAL RESULT\n")


def show_procedure(board_list: list, depth_list: list):
    # get difference between two boards
    def get_diff(prev, curr):
        diff = set()
        for i in range(9):
            for j in range(9):
                if prev[i][j] != curr[i][j]:
                    diff.add((i, j))
        return diff

    total_step = len(board_list)
    step = 4
    current_step = 0

    for start in range(0, total_step, step):
        end = min(start + step, total_step)
        boards = board_list[start:end]
        depths = depth_list[start:end]
        diffs = []

        # get differences between previous and current boards
        for i in range(len(boards)):
            if start + i == 0:
                diffs.append(set())
            else:
                prev = board_list[start + i - 1]
                curr = boards[i]
                diffs.append(get_diff(prev, curr))

        # start to print
        print("\n" * 5)

        for row in range(9):
            for b_idx, board in enumerate(boards):
                for col in range(9):
                    if col % 3 == 0 and col != 0:
                        print(" | ", end="")
                    val = board[row][col]
                    if (row, col) in diffs[b_idx] and val != 0:
                        print(f"*{val}*", end="")
                    else:
                        print(f" {val if val != 0 else ' '} ", end="")

                # arrow in the middle row only
                if row == 4 and b_idx < len(boards) - 1:
                    print(" -> ", end=" ")
                else:
                    print("  ", end="   ")  # spacing between boards

            print()

            # horizontal border (only once between row blocks)
            if row % 3 == 2 and row != 8:
                for _ in range(len(boards)):
                    print("- " * 17, end="    ")
                print()

        # print depths below each board
        for b_idx, depth in enumerate(depths):
            print(f"          depth {depth:<2}                ", end="     ")
        print("\n")

        # input prompt to continue or skip
        if end < total_step:
            choice = input(
                f"Showing steps {start + 1}-{end} of {total_step}. Press Enter to continue, or 'y' to skip to last step: ")
            if choice.strip().lower() == 'y':
                break

    print(f"\n✅ Finished showing all {total_step} steps for this depth.\nReturning to menu...\n")


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
        if is_valid(board, num, row, col):
            board[row][col] = num
            process.append(deepcopy(board))
            depth_log.append(max_depth)

            if dfs(board, depth + 1, max_depth, process, depth_log):
                return True

            board[row][col] = 0  # Backtrack

    return False



def iterative_deepening(board):
    process = []
    depth_log = []
    for max_depth in range(1, 82):  # max 81 moves
        copied_board = deepcopy(board)
        if dfs(copied_board, 0, max_depth, process, depth_log):
            return copied_board, process, depth_log
    return None, process, depth_log


if __name__ == "__main__":
    # example data of sudoku
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

    # Start animation
    solving = True
    anim_thread = threading.Thread(target=animate_solving)
    anim_thread.start()

    # Start tracking
    tracemalloc.start()
    start_time = time.time()

    solution, process, depth_log = iterative_deepening(sudoku_data)

    # Stop animation
    solving = False
    anim_thread.join()
    print("\r✅ Solved!                            ")

    end_time = time.time()
    time_taken = end_time - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\n✅ Sudoku Solved!")
    print(f"📊 Memory Usage: {peak / (1024 * 1024):.2f} MB")
    print(f"📊 Time Usage  : {time_taken:.6f} seconds\n")

    # 🎮 Interactive loop
    while True:
        print("📌 Options:")
        print(f"  - Enter a depth number (max: {depth_log[-1]}) to view that step process")
        print("  - Type 'result' to see the final solved board")
        print("  - Type 'exit' to quit\n")

        cmd = input("🔎 What would you like to see? \n").strip().lower()

        if cmd == 'exit':
            print("👋 Exiting. Goodbye!")
            break
        elif cmd == 'result':
            print_sudoku(solution)
        elif cmd.isdigit():
            depth_choice = int(cmd)
            filtered_boards = []
            filtered_depths = []
            for b, d in zip(process, depth_log):
                if d == depth_choice:
                    filtered_boards.append(b)
                    filtered_depths.append(d)

            if not filtered_boards:
                print(f"⚠️  No steps found for depth {depth_choice}. Try another.\n")
            else:
                print(f"\n📈 Showing {len(filtered_boards)} step(s) for depth {depth_choice}")
                show_procedure(filtered_boards, filtered_depths)
        else:
            print("❓ Invalid command. Try again.\n")
