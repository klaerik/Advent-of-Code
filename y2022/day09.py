import y2022.shared as shared
from dataclasses import dataclass, field

## Data
raw = shared.read_file("day09.txt")
test = shared.read_file("day09-test.txt")
test2 = shared.read_file("day09-test2.txt")

## Functions
@dataclass
class Knot:
    x: int = 0
    y: int = 0
    history: set = field(default_factory=set)

    def snapshot(self):
        self.history.add((self.x, self.y))

    def touches(self, knot: "Knot"):
        touch_x = (knot.x - 1) <= self.x <= (knot.x + 1)
        touch_y = (knot.y - 1) <= self.y <= (knot.y + 1)
        return touch_x and touch_y

    def move_head(self, direction: str):
        dirs = {
            "U": (0, 1),
            "D": (0, -1),
            "L": (-1, 0),
            "R": (1, 0),
        }
        for d in direction:
            dx, dy = dirs[d]
            self.x += dx
            self.y += dy

    def move_tail(self, knot: "Knot"):
        if self.touches(knot):
            return
        dx = shared.sign(knot.x - self.x)
        dy = shared.sign(knot.y - self.y)
        self.x += dx
        self.y += dy


@dataclass
class Rope:
    movements: list
    head: Knot = field(default_factory=Knot)
    knots: int = 2
    tails: list = field(default_factory=list)

    def __post_init__(self):
        for _ in range(self.knots - 1):
            tail = Knot()
            self.tails.append(tail)
        self.snapshot()

    def snapshot(self):
        self.tails[-1].snapshot()

    def process_movement(self):
        direction, val = self.movements.pop().split()
        for _ in range(int(val)):
            self.head.move_head(direction)
            head = self.head
            for tail in self.tails:
                tail.move_tail(head)
                head = tail
            self.snapshot()

    def process_movements(self):
        while self.movements:
            self.process_movement()


def solve(raw, knots=2):
    rope = Rope(movements=raw[::-1], knots=knots)
    rope.process_movements()
    return len(rope.tails[-1].history)


## Testing
assert solve(test) == 13
assert solve(test, knots=10) == 1
assert solve(test2, knots=10) == 36

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, knots=10)}")
