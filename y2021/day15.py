import shared
import heapq

## Data
raw = shared.read_file('2021/input/day15.txt')

test = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''.split('\n')

## Functions
def find_neighbors(x, y, x_max, y_max, diagonal=False):
    neighbors = ((x+1, y), (x-1, y), (x, y+1), (x, y-1),)
    if diagonal:
        neighbors = neighbors + ((x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1))
    out = set()
    for x1,y1 in neighbors:
        if x1 < 0 or x1 >= x_max or y1 < 0 or y1 >= y_max:
            continue
        else:
            out.add((x1,y1))
    return out

def traverse_cavern(map):
    best = float('inf')
    paths = [(0, (0,0)),]
    heapq.heapify(paths)
    x_max, y_max = len(map[0]), len(map)
    seen = {(0,0): 0}
    while paths:
        score, position = heapq.heappop(paths)
        neighbors = find_neighbors(*position, x_max, y_max)
        for x,y in neighbors:
            new_score = score + int(map[y][x])
            if (x,y) in seen and seen[(x,y)] <= new_score:
                continue  # skip if score is worse 
            else:
                seen[(x,y)] = new_score
            if x == x_max-1 and y == y_max-1: # hit the final node
                best = min(best, new_score)
            else:
                heapq.heappush(paths, (new_score, (x,y)))
    return best

def expand_map(map):
    out = []
    for yx in range(5):
        for row in map:
            out.append([])
            for xx in range(5):
                out[-1].extend([1+((int(x)+xx+yx) % 10) if (int(x)+xx+yx) > 9 else (int(x)+xx+yx) for x in row])
    return out    

## Testing
assert traverse_cavern(test) == 40
assert traverse_cavern(expand_map(test)) == 315

## Solutions
print(f'Part 1: Lowest risk path is {traverse_cavern(raw)}')
print(f'Part 2: Lowest risk path in expanded map is {traverse_cavern(expand_map(raw))}')


