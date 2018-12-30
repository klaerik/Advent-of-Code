import networkx as nx
import matplotlib.pyplot as plt
from typing import NamedTuple
from collections import deque


class Point(NamedTuple):
    x: int
    y: int

def move(point, direction):
    dirs = {'N': (0, 1), 'W': (-1, 0), 'E': (1, 0), 'S': (0, -1)}
    dx, dy = dirs[direction]
    x, y = point
    return Point(x + dx, y + dy)

def import_file(file):
    with open('input/day20.txt') as f:
        raw = f.read().rstrip('\n')
    return raw

def create_graph(raw):
    stack = deque(raw)
    buffer = deque([Point(0,0),])
    cursor = buffer[-1]
    paths = nx.Graph()
    paths.add_node(cursor, **{'name':'start'})
    while stack:
        i = stack.popleft()
        if i in ('N','S','E','W'):
            next_point = move(cursor, i)
            paths.add_edge(cursor, next_point)
            cursor = next_point
        elif i == '(':
            buffer.append(cursor)
        elif i == '|':
            cursor = buffer[-1]
        elif i == ')':
            cursor = buffer.pop()
        elif i == '$':
            paths.node[cursor]['name'] = 'end'
    return paths

def find_longest_path(paths):
    shortest_lengths = nx.algorithms.shortest_path_length(paths, source=Point(0,0))
    max_length = max(shortest_lengths.values())
    return max_length

#paths[2]
#paths.edges
#paths.nodes
#nx.draw_networkx(paths)
#nx.draw(paths)

assert find_longest_path(create_graph('^WNE$')) == 3
assert find_longest_path(create_graph('^ENWWW(NEEE|SSE(EE|N))$')) == 10
assert find_longest_path(create_graph('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')) == 18


raw = import_file('input/day20.txt')
paths = create_graph(raw)
solution = find_longest_path(paths)
print(f"Solution 1: {solution}")

all_paths = nx.algorithms.shortest_path_length(paths, source=Point(0,0))
min1k = len([k for k,v in all_paths.items() if v >= 1000])
print(f"Solution 2: {min1k}")
