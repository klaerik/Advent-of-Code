import shared



def split_tiles(raw):
    out = {}
    tile = None
    for row in raw:
        if row.startswith('Tile'):
            tile = int(row.split()[1][:-2])
            out[tile] = []
        else:
            out[tile].append(row)
    return {k:Tile(v) for k,v in out.items()}

class Tile():
    def __init__(self, rows):
        self.rows = rows
        self.states = self.get_all_edges()
        self.all_edges = {edge for edges in self.states for edge in edges}

    def get_all_edges(self):
        edges = [self.get_edges(),]
        self.flip()
        edges.append(self.get_edges())
        self.flip()
        self.flipup()
        edges.append(self.get_edges())
        self.flipup()
        return edges

    def rotate(self):
        new = []
        for x in range(len(self.rows)):
            temp = ''.join([self.rows[y][x] for y in range(len(self.rows)-1, -1, -1)])
            new.append(temp)
        self.rows = new
    
    def flip(self):
        new = [row[::-1] for row in self.rows]
        self.rows = new
    
    def flipup(self):
        self.rows = self.rows[::-1]
    
    def convert_to_num(self, row):
        row = row.replace('#','1').replace('.','0')
        return int(row, base=2)

    def get_edges(self):
        l = len(self.rows)
        edges = []
        edges.append(self.rows[0])
        edges.append([self.rows[y][l-1] for y in range(l)])
        edges.append(self.rows[l-1])
        edges.append([self.rows[y][0] for y in range(l)])
        return tuple([self.convert_to_num(''.join(i)) for i in edges])

    def __str__(self):
        return '\n'.join(self.rows)




raw = shared.read_file('2020/input/day20_demo.txt')
tiles = split_tiles(raw)


tile = tiles[231]
tile.all_edges

tile.get_edges()

print(tile)
tile.flip()
print(tile)
tile.flip()
print(tile)
tile.rotate()
print(tile)
tile.rotate()
print(tile)
tile.rotate()
