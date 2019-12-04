
def read_file():
    input_file = 'input/day03.txt'
    raw = []
    with open(input_file) as f:
        for line in f:
            raw.append(line.strip())
    route1 = raw[0].split(',')
    route2 = raw[1].split(',')
    return route1, route2


dirs = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

def track_route(route):
    out = {}
    x,y = (0,0)
    steps = 0
    for i in route:
        dx,dy = dirs[i[0]]
        l = int(i[1:])
        for _ in range(l):
            x += dx
            y += dy
            steps += 1
            if (x,y) not in out:
                out[(x,y)] = steps
    return out

def get_dists(path1, path2):
    shared = path1.keys() & path2.keys()
    dists = []
    #print(shared)
    for x,y in shared:
        dist = abs(x) + abs(y)
        dists.append((dist, path1[(x,y)] + path2[(x,y)]))
    #min_dist = min(dists)
    return dists

def get_solution(route1, route2, min_dist=True):
    path1 = track_route(route1)
    path2 = track_route(route2)
    if min_dist:
        return min(get_dists(path1, path2))[0]
    else:
        return min([steps for dist,steps in get_dists(path1, path2)])

route1 = ['U7','R6','D4','L4']
route2 = ['R8','U5','L5','D3']
assert get_solution(route1, route2) == 6

route1, route2 = read_file()
print(f'Found solution 1: {get_solution(route1, route2)}')
print(f'Solution 2: {get_solution(route1, route2, min_dist=False)}')