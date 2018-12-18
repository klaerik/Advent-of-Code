
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
    local = {'up': parent, 'down': [], 'metadata': [], 'sum': 0}
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
    
    # Calculate sums
    children = tree[current_node]['down']
    if len(children) == 0:
        tree[current_node]['sum'] = sum(metadata)
        #print(f"Found end leaf: {current_node}, {tree[current_node]['sum']}")
    else:
        for child_index in metadata:
            if child_index <= len(children):
                child_id = children[child_index - 1]
                child_sum = tree[child_id]['sum']
                tree[current_node]['sum'] += child_sum
                #print(f"Found child sum: {current_node}, {tree[current_node]['sum']}")
    
    # Return results
    #print(f"Current: {current_node}, Sequence: {sequence}")
    return data, tree, sequence


_, tree, _  = parse_tree(data)
meta_sum = sum([sum(node['metadata']) for node in tree.values()])

print(f"Solution 1 - Metadata sum: {meta_sum}")

print(f"Solution 2 - Child sum of root node: {tree[0]['sum']}")
        
