import shared


def get_split_point(low, high):
    cut = (high - low) // 2
    cut += low
    return cut

def pick_side(side, low, high):
    if side in {'F','L'}:
        l,h = low, get_split_point(low, high)
    elif side in {'B','R'}:
        l,h = get_split_point(low, high) + 1, high
    return l,h

def calc_seat_id(row, col):
    return row * 8 + col

def get_seat(boarding_pass, row_size = (0, 127), col_size = (0, 7)):
    row = row_size
    col = col_size
    for i in boarding_pass:
        if i in ('F','B'):
            row = pick_side(i, *row)
        elif i in ('L','R'):
            col = pick_side(i, *col)
    row = row[0]
    col = col[0]
    seat_id = calc_seat_id(row, col)
    return row, col, seat_id



# Solve puzzle
raw = shared.read_file('input/day05.txt')
seats = [get_seat(bp) for bp in raw if bp]

seat_ids = [x[2] for x in seats]
print(f'Part 1: {max(seat_ids)} seat IDs in the boarding passes')

leftover = (set(range(min(seat_ids), max(seat_ids) + 1)) - set(seat_ids)).pop()
print(f'Part 2: {leftover} seat ID is my seat')
