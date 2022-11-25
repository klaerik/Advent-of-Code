import shared

## Data
raw = shared.read_file('2021/input/day02.txt')

test = [
    'forward 5',
    'down 5',
    'forward 8',
    'up 3',
    'down 8',
    'forward 2',
    ]

## Functions
def convert_to_commands(raw):
    out = []
    for line in raw:
        dir, dist = line.strip().split(' ')
        dist = int(dist)
        out.append((dir,dist))
    return out

class Sub():
    def __init__(self, x=0, z=0, aim=0, movement_type='simple'):
        self.x = x
        self.z = z
        self.aim = aim
        self.movement_type = movement_type
    
    def move(self, direction, distance):
        if self.movement_type == 'simple':
            if direction == 'forward':
                self.x += distance
            elif direction == 'down':
                self.z += distance
            elif direction == 'up':
                self.z -= distance
        elif self.movement_type == 'aim':
            if direction == 'forward':
                self.x += distance
                self.z += self.aim * distance
            elif direction == 'down':
                self.aim += distance
            elif direction == 'up':
                self.aim -= distance
    
    def dive(self, commands):
        for command in commands:
            self.move(*command)

    def __str__(self):
        return f'Sub location: {self.x}, {self.z}, {self.aim}'


def solve_puzzle(raw, movement_type='simple'):
    sub = Sub(movement_type = movement_type)
    sub.dive(convert_to_commands(raw))
    return sub.x * sub.z


## Func testing
assert convert_to_commands(test)[0] == ('forward', 5)
assert solve_puzzle(test) == 150
assert solve_puzzle(test, 'aim') == 900


## Solve part 1
print(f'Part 1: final depth times horizontal position is {solve_puzzle(raw)}')

## Solve part 2
print(f'Part 2: final position with aim-based movement is {solve_puzzle(raw, "aim")}')

