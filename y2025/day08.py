import math
from dataclasses import dataclass

import y2025.shared as shared

## Data
raw = shared.read_file("day08.txt")
test = shared.read_file("day08-test.txt")


## Functions
@dataclass
class Junctions:
    raw: str

    def __post_init__(self):
        self.get_boxes()

    def get_boxes(self):
        boxes = {}
        circuits = {}
        distances = []
        i = 0
        for row in self.raw:
            x, y, z = [int(i) for i in row.split(",")]
            coord = (x, y, z)
            boxes[coord] = i
            circuits[i] = set([coord])
            i += 1
        boxlist = list(boxes.keys())
        while boxlist:
            box1 = boxlist.pop()
            for box2 in boxlist:
                dist = self.get_distance(box1, box2)
                distances.append((dist, box1, box2))
        self.boxes = boxes
        self.circuits = circuits
        distances.sort()
        self.distances = distances

    def get_distance(self, coord1, coord2) -> float:
        x1, y1, z1 = coord1
        x2, y2, z2 = coord2
        d = ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** (0.5)
        return d

    def combine_circuits(self, circuit1: int, circuit2: int):
        if circuit1 == circuit2:
            return
        for box in self.circuits[circuit2]:
            self.boxes[box] = circuit1
        self.circuits[circuit1].update(self.circuits.pop(circuit2))


def solve(test, n: int = 1000):
    junctions = Junctions(test)
    for _, box1, box2 in junctions.distances[:n]:
        circuit1, circuit2 = junctions.boxes[box1], junctions.boxes[box2]
        junctions.combine_circuits(circuit1, circuit2)
    lengths = [len(x) for x in junctions.circuits.values()]
    lengths.sort()
    return math.prod(lengths[-3:])


def solve2(test):
    junctions = Junctions(test)
    out = 0
    for _, box1, box2 in junctions.distances:
        circuit1, circuit2 = junctions.boxes[box1], junctions.boxes[box2]
        if circuit1 != circuit2:
            junctions.combine_circuits(circuit1, circuit2)
            out = box1[0] * box2[0]
    return out


## Testing
assert solve(test, 10) == 40
assert solve2(test) == 25272


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
