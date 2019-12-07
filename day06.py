
raw = []
with open('input/day06.txt') as f:
    for l in f:
        raw.append(l.strip())

def raw_to_tree(raw):
    tree = {}
    for i in raw:
        inner,outer = i.split(')')
        tree.setdefault(inner,[]).append(outer)
    return tree

def count_orbits(tree, node='COM', indirect_orbits=0):
    orbits = indirect_orbits
    satellites = tree.get(node, [])
    for satellite in satellites:
        orbits += count_orbits(tree, satellite, indirect_orbits+1)
    return orbits


test = ['COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L']
    
assert count_orbits(raw_to_tree(test)) == 42

print(f'Part 1: Orbits = {count_orbits(raw_to_tree(raw))}')


def get_path(tree, finish_node, start_node='COM'):
    path = [start_node]
    if start_node == finish_node:
        return path
    else:
        satellites = tree.get(start_node, [])
        for satellite in satellites:
            child_path = get_path(tree, finish_node, satellite)
            path.extend(child_path)
    return path if len(path) > 1 else []

assert get_path(raw_to_tree(test), finish_node='I') == ['COM', 'B', 'C', 'D', 'I']


def count_orbital_transfers(tree, santa='SAN', me='YOU'):
    path1 = get_path(tree, santa)[:-1]
    path2 = get_path(tree, me)[:-1]
    diff = set(path1) ^ set(path2)
    return len(diff)


test.append('K)YOU')
test.append('I)SAN')

assert count_orbital_transfers(raw_to_tree(test)) == 4

print(f'Part 2: Orbital transfers = {count_orbital_transfers(raw_to_tree(raw))}')