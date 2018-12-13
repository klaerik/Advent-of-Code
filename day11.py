
def build_grid(serial):
    grid = []
    for y in range(301):
        row = []
        for x in range(301):
            if x == 0 or y == 0:
                row.append(None)
            else:
                rack_id = x + 10
                power = rack_id * y
                power += serial
                power *= rack_id
                power = int(str(power).zfill(3)[-3])
                power -= 5
                row.append(power)
        grid.append(row)
    return(grid)

def get_max_cell(grid, fixed):
    max_cell = 0, 0, 0, 0
    for y in range(1, 298):
        for x in range(1, 298):
            cell = [val for row in grid[y: y+3] for val in row[x: x+3]]
            ttl = sum(cell)
            if ttl > max_cell[3]:
                max_cell = x, y, len(cell), ttl
    return max_cell

def solve_puzzle(serial, fixed=True):
    grid = build_grid(serial)
    max_cell = get_max_cell(grid, fixed)
    print(f"Max cell for serial {serial} was {max_cell}")
    return max_cell

serial = 73
solve_puzzle(serial)

assert solve_puzzle(18) == (33, 45, 9, 29)
assert solve_puzzle(42) == (21, 61, 9, 30)

solution = solve_puzzle(9995)
print(f'Solution 1: {solution}')