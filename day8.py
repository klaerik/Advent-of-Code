
raw = ''
with open('input/day8.txt') as file:
    for line in file:
        raw = line

#raw = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'

data = [int(x) for x in raw.split()]

def parse_tree(data, tree={}, parent=None, sequence=0):
    
    # Read header
    child_nodes = data.pop(0)
    meta_nodes = data.pop(0)
    current_node = sequence
    sequence += 1

    # Output tree dictionary
    local = {'up': parent, 'down': [], 'metadata': []}
    tree[current_node] = local
    
    # Process nested children, manage results
    for child in range(child_nodes):
        tree[current_node]['down'].append(sequence)
        data, leaf, sequence = parse_tree(data, tree, parent=current_node, sequence=sequence)
        tree.update(leaf)
    
    # Process metadata nodes
    metadata = data[0:meta_nodes]
    del data[0:meta_nodes]
    tree[current_node]['metadata'] = metadata    
    
    # Return results
    #print(f"Current: {current_node}, Sequence: {sequence}")
    return data, tree, sequence


_, tree, _  = parse_tree(data)
meta_sum = sum([sum(node['metadata']) for node in tree.values()])

subgroups = sum([x for y in tree.values() for x in y['metadata']])

print(f"Solution 1 - Metadata sum: {meta_sum}")
