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
    tail: "Knot" = None
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
        self.tail.move_tail(self)

    def move_tail(self, head: "Knot"):
        if self.touches(head):
            return
        dx = shared.sign(head.x - self.x)
        dy = shared.sign(head.y - self.y)
        self.x += dx
        self.y += dy
        if self.tail is not None:
            self.tail.move_tail(self)


@dataclass
class Rope:
    movements: list
    head: Knot = field(default_factory=Knot)
    tail: Knot = None
    knots: int = 2

    def __post_init__(self):
        knot = self.head
        for _ in range(self.knots - 1):
            knot.tail = Knot()
            knot = knot.tail
        self.tail = knot
        self.snapshot()

    def snapshot(self):
        self.tail.snapshot()

    def process_movement(self):
        direction, val = self.movements.pop().split()
        for _ in range(int(val)):
            self.head.move_head(direction)
            self.snapshot()

    def process_movements(self):
        while self.movements:
            self.process_movement()

    def tail_travel(self):
        return len(self.tail.history)


def solve(raw, knots=2):
    rope = Rope(movements=raw[::-1], knots=knots)
    rope.process_movements()
    return rope.tail_travel()


## Testing
assert solve(test) == 13
assert solve(test, knots=10) == 1
assert solve(test2, knots=10) == 36

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, knots=10)}")
