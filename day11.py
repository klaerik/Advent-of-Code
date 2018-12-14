
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
    if fixed:
        cell_size = [fixed,]
    else:
        cell_size = range(2,101)
    for size in cell_size:
        for y in range(1, 301 - size):
            for x in range(1, 301 - size):
                cell = [val for row in grid[y: y+size] for val in row[x: x+size]]
                ttl = sum(cell)
                if ttl > max_cell[3]:
                    max_cell = x, y, size, ttl
    return max_cell

def solve_puzzle(serial, fixed=3):
    grid = build_grid(serial)
    max_cell = get_max_cell(grid, fixed)
    print(f"Max cell for serial {serial} was {max_cell}")
    return max_cell

serial = 73
solve_puzzle(serial)

assert solve_puzzle(18) == (33, 45, 9, 29)
assert solve_puzzle(42) == (21, 61, 9, 30)

solution = solve_puzzle(9995)
print(f'Solution 1: {",".join([str(i) for i in solution[:2]])}')


assert solve_puzzle(18, fixed=16) == (90, 269, 16, 113)
assert solve_puzzle(42, fixed=False) == (232, 251, 12, 119)


solution2 = solve_puzzle(9995, fixed=False)
print(f'Solution 2: {",".join([str(i) for i in solution2[:3]])}')
