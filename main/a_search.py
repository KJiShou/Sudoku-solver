import heapq

def is_valid(grid, row, col, num):
    """Checks if placing 'num' at (row, col) is valid."""
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num or \
                grid[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

def find_empty(grid):
    """Finds the next empty cell (0) in the grid."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None

def heuristic(grid):
    """Heuristic: number of empty cells."""
    count = 0
    for row in grid:
        count += row.count(0)
    return count

def solve_sudoku_a_star(grid):
    """Solves Sudoku using A* search."""
    initial_state = (heuristic(grid), 0, grid)  # (f, g, grid)
    open_list = [initial_state]
    closed_set = set()

    while open_list:
        f, g, current_grid = heapq.heappop(open_list)
        grid_tuple = tuple(map(tuple, current_grid))

        if grid_tuple in closed_set:
            continue
        closed_set.add(grid_tuple)

        if find_empty(current_grid) is None:
            return current_grid  # Solution found

        row, col = find_empty(current_grid)
        for num in range(1, 10):
            if is_valid(current_grid, row, col, num):
                new_grid = [row[:] for row in current_grid]
                new_grid[row][col] = num
                h = heuristic(new_grid)
                new_state = (g + 1 + h, g + 1, new_grid)
                heapq.heappush(open_list, new_state)

    return None  # No solution found


sudoku_grid = [
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

solution = solve_sudoku_a_star(sudoku_grid)

if solution:
    for row in solution:
        print(row)
else:
    print("No solution found.")
