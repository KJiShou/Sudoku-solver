import time
import tracemalloc
from copy import deepcopy
import threading
import iterative_deepening_search as ids
import backtracking_search as bs
import a_search as ass
import simulated_annealing as sa
import breadth_first_search as bfs

# Animation thread flag
solving = True


def is_valid(board: list, num: int, row: int, col: int) -> bool:
    """
        Check if placing 'num' at position (row, col) is valid
        according to Sudoku rules (row, column, and 3x3 grid).
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


def animate_solving():
    """
        Display an animated 'Solving...' text in the terminal while the solver runs,
        using a separate thread.
    """
    symbols = ["Solving.  ", "Solving.. ", "Solving..."]
    idx = 0
    while solving:
        print("\r" + symbols[idx % len(symbols)], end="")
        time.sleep(0.5)
        idx += 1


# function to print sudoku board
def print_sudoku_result(board: list, time_taken: float, peak_memory: float):
    """
        Print the final Sudoku board result along with time and memory usage stats.
        Shows formatted output for solved or unsolved boards.
    """
    print("")
    if board is None:
        print("Cannot Find the result!")
        print(f"Memory Usage: {peak_memory / (1024 * 1024):.2f} MB")
        print(f"Time Usage  : {time_taken:.6f} seconds\n")
        return
    for row in range(9):
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")
            val = board[row][col]
            print(f" {val if val != 0 else ' '} ", end="")
        print()
        if row % 3 == 2 and row != 8:
            print("- " * 17)
    print("\n          FINAL RESULT\n")
    print(f"Memory Usage: {peak_memory / (1024 * 1024):.2f} MB")
    print(f"Time Usage  : {time_taken:.6f} seconds\n")


def print_board(board):
    """
        Print a Sudoku board in formatted 9x9 layout.
    """
    if board is None:
        print("Cannot Find the result!")
        return
    for row in range(9):
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")
            val = board[row][col]
            print(f" {val if val != 0 else ' '} ", end="")
        print()
        if row % 3 == 2 and row != 8:
            print("- " * 17)
    print("\n")

def show_procedure(board_list: list, depth_list: list = None):
    """
        Visually show the step-by-step board transformation during the solving process.
        Optionally displays search depth per step if depth_list is provided.
    """
    depth_flag = None != depth_list
    skip_flag = False
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
        depths = depth_list[start:end] if depth_flag else None
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
        print(f"Max Depth: {max(depth_list)}" if depth_flag else "")
        for row in range(9):
            for b_idx, board in enumerate(boards):
                for col in range(9):
                    if col % 3 == 0 and col != 0:
                        print(" | ", end="")
                    val = board[row][col]
                    if (row, col) in diffs[b_idx]:
                        if val == 0:
                            print(f" < ", end="")
                        else:
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
        if depth_flag:
            for b_idx, depth in enumerate(depths):
                print(f"          depth {depth:<2}                ", end="     ")
            print("\n")
        else:
            print("")
        print(f"Showing steps {start + 1}-{end} of {total_step}.")

        # input prompt to continue or skip
        if not skip_flag and end < total_step:
            choice = input(
                f"Press Enter to continue, or 'y' to skip to last step: ")
            if choice.strip().lower() == 'y':
                skip_flag = True

    print(f"\nFinished showing all {total_step} steps.\nReturning to menu...\n")


# tract memory and time function
def trace_function(algorithm, test_data: list):
    """
        Measure time and memory usage of a given Sudoku solving algorithm.
        Also handles threading for animated solving feedback.
        Supports both function-based and class-based algorithm inputs.
        Returns the solution, solving process, optional depth log, time taken, and peak memory used.
    """
    global solving
    solving = True
    anim_thread = threading.Thread(target=animate_solving)
    anim_thread.start()

    tracemalloc.start()
    start_time = time.time()

    # Handle class-based algorithm like SimulatedAnnealingSudoku
    if isinstance(algorithm, type):
        # If a class is passed instead of a function
        instance = algorithm(test_data)
        solved = instance.solve()
        solution = instance.board.tolist() if instance.board is not None else None
        process = instance.process
        depth_log = None

    else:
        # Standard functional algorithm
        result = algorithm(test_data)
        if isinstance(result, tuple):
            # Safe unpacking for different lengths
            solution = result[0] if len(result) > 0 else None
            process = result[1] if len(result) > 1 else []
            depth_log = result[2] if len(result) > 2 else None
        else:
            # Single result fallback
            solution = result
            process = []
            depth_log = None

    solving = False
    anim_thread.join()
    print("\rDone !                            ")

    end_time = time.time()
    time_taken = end_time - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return solution, process, depth_log, time_taken, peak


def display_menu(title, options):
    """
        Display a CLI menu with a given title and list of options.
    """
    print(f"\n{title}")
    print("=" * len(title))
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    print("0. Exit")
    print("=" * len(title))

if __name__ == "__main__":
    # test data 1, easiest
    sudoku_test_data = [
        # easy 1
        [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ],
        # easy 2
        [
            [1, 0, 0, 4, 8, 9, 0, 0, 6],
            [7, 3, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 1, 2, 9, 5],
            [0, 0, 7, 1, 2, 0, 6, 0, 0],
            [5, 0, 0, 7, 0, 3, 0, 0, 8],
            [0, 0, 6, 0, 9, 5, 7, 0, 0],
            [9, 1, 4, 6, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 3, 7],
            [8, 0, 0, 5, 1, 2, 0, 0, 4]
        ],
        # Intermediate 3
        [
            [0, 2, 0, 6, 0, 8, 0, 0, 0],
            [5, 8, 0, 0, 0, 9, 7, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
            [3, 7, 0, 0, 0, 0, 5, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 8, 0, 0, 0, 0, 1, 3],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 9, 8, 0, 0, 0, 3, 6],
            [0, 0, 0, 3, 0, 6, 0, 9, 0]
        ],
        # Difficult 4
        [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ],
        # Difficult 5
        [
            [2, 0, 0, 3, 0, 0, 0, 0, 0],
            [8, 0, 4, 0, 6, 2, 0, 0, 3],
            [0, 1, 3, 8, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 2, 0, 3, 9, 0],
            [5, 0, 7, 0, 0, 0, 6, 2, 1],
            [0, 3, 2, 0, 0, 6, 0, 0, 0],
            [0, 2, 0, 0, 0, 9, 1, 4, 0],
            [6, 0, 1, 2, 5, 0, 8, 0, 9],
            [0, 0, 0, 0, 0, 1, 0, 0, 2]
        ],
        # Not Fun 6
        [
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]
        ],
        # Extreme 7
        [
            [5, 0, 0, 4, 0, 0, 1, 0, 0],
            [3, 0, 0, 0, 0, 5, 0, 0, 7],
            [0, 9, 0, 0, 0, 3, 5, 0, 0],
            [2, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 8, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 9],
            [0, 0, 6, 0, 0, 0, 4, 0, 0],
            [0, 0, 1, 0, 0, 9, 2, 0, 0],
            [4, 0, 0, 0, 5, 0, 0, 8, 0]
        ],
        # Extreme 8
        [
            [0, 9, 3, 4, 7, 0, 0, 6, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 1],
            [8, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 3, 4, 0, 0, 9, 0, 0, 5],
            [1, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 5, 2, 0, 0],
            [0, 6, 7, 0, 9, 0, 0, 1, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        # Extreme 9
        [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 0],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ],
        # cannot been solved 10
        [
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
    ]

    algorithms_function = [ass.solve_sudoku_a_star, bs.solve_sudoku_with_logging, bfs.bfs_sudoku_solver,
                           ids.iterative_deepening, sa.SimulatedAnnealingSudoku]

    exit_flag = False
    sudoku_data = 0
    algorithm_function = ids.iterative_deepening
    compare_all = False

    while not exit_flag:
        display_menu("Sudoku Solver", ["Select Data Set", "Choose Algorithm", "Solve Sudoku"])
        cmd = input("Enter your choice: ")

        if cmd == "1":
            datasets = [
                "Easy 1", "Easy 2", "Intermediate 1", "Difficult 1", "Difficult 2",
                "Difficult 3", "Extreme 1", "Extreme 2", "Extreme 3", "Impossible"
            ]
            display_menu("Choose Data Set", datasets)
            choice = input("Enter your choice: ")
            if choice.isdigit() and 0 <= int(choice) <= 10:
                if int(choice) == 0:
                    continue
                sudoku_data = int(choice) - 1
                print("\nSelected Sudoku Board:")
                print_board(sudoku_test_data[sudoku_data])
            else:
                print("Invalid choice.\n")

        elif cmd == "2":
            algorithms = [
                "A* Search", "Backtracking Search", "Breadth First Search", "Iterative Deepening Search",
                "Simulated Annealing", "Compare all algorithms"
            ]
            display_menu("Choose Algorithm", algorithms)
            algorithms_choice = input("Enter your choice: ")
            if algorithms_choice.isdigit() and 0 <= int(algorithms_choice) <= 6:
                if int(algorithms_choice) == 0:
                    continue
                if int(algorithms_choice) == 6:
                    compare_all = True
                else:
                    compare_all = False
                    algorithm_function = algorithms_function[int(algorithms_choice) - 1]
                    print(f"\nSelected Algorithms: {algorithms[int(algorithms_choice) - 1]}")
            else:
                print("Invalid choice.\n")

        elif cmd == "3":
            if compare_all:
                print("\nComparing all algorithms on the selected Sudoku puzzle...\n")
                algorithms = [
                    "A* Search", "Backtracking", "Breadth First Search",
                    "Iterative Deepening", "Simulated Annealing"
                ]

                results = []
                names = []
                for i, alg in enumerate(algorithms_function):
                    print(f"Running {algorithms[i]}...")
                    try:
                        solution, process, depth_log, time_taken, peak = trace_function(
                            alg, sudoku_test_data[sudoku_data]
                        )
                        results.append((solution, time_taken, peak))
                        names.append(algorithms[i])
                    except Exception as e:
                        print(f"{algorithms[i]} failed: {e}")
                        results.append((None, None, None))
                        names.append(algorithms[i])

                print("\nAll algorithms completed. Showing final boards\n")

                # Print algorithm names as headings
                for i, (board, time_taken, peak) in enumerate(results):
                    print(f"{names[i]:^30}")
                    print_sudoku_result(board, time_taken, peak)

                # Print time and memory usage per algorithm
                print("\nPerformance Summary:")
                for i, (s, t, m) in enumerate(results):
                    if t is not None:
                        solve = "  Solved  " if s is not None else "Not Solved"
                        print(f"{names[i]:<25} | {solve} | Time: {t:.4f}s | Memory: {m / (1024 * 1024):.2f} MB")
                    else:
                        print(f"{names[i]:<25} | Failed to run.")

            else:
                print("\nSolving the selected Sudoku puzzle...")
                solution, process, depth_log, time_taken, peak = trace_function(algorithm_function,
                                                                                           sudoku_test_data[sudoku_data])

                print(f"Memory Usage: {peak / (1024 * 1024):.2f} MB")
                print(f"Time Usage  : {time_taken:.6f} seconds\n")

                # Interactive loop
                # Interactive loop
                while True:
                    print(f"  1. View full solving process")
                    print("  2. View final solved board")
                    print("  0. Exit\n")

                    cmd = input("Enter your choice: ").strip()

                    if cmd == '0':
                        print("Exiting. Goodbye!")
                        break
                    elif cmd == '2':
                        print_sudoku_result(solution, time_taken, peak)
                    elif cmd == '1':
                        show_procedure(process)
                    else:
                        print("Invalid input. Please enter 0, 1, or 2.\n")
        elif cmd == "0":
            exit_flag = True
        else:
            print("Invalid input. Please try again.")