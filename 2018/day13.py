from collections import deque, defaultdict, Counter
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class Cart():
    def __init__(self, x, y, direction):
        self.loc = Point(x, y)
        self.directions = deque(['n', 'e', 's', 'w'])
        self.turn(direction)
        self.choices = deque([1, 0, -1]) #l, s, r
        self.crash = False

    def turn(self, direction):
        while self.direction != direction:
            self.directions.rotate()
    
    @property
    def direction(self):
        return self.directions[0]
        
    def take_intersection(self):
        choice = self.choices[0]
        self.directions.rotate(choice)
        self.choices.rotate(-1)
    
    def move(self, track):
        if not self.crash:
            x, y = self.loc
            options = track[Point(x, y)]
            if len(options) == 4: #Intersection
#                print("Turning!")
                self.take_intersection()
            d = self.direction
            next_step = options.get(d, None) 
#            print(f"Next step {next_step}")
            if next_step is None: #Turn
#                print(f"Found corner: {options}, {self.loc}")
                if d in ('w','e'):
                    d = [option for option in options if option in ('n','s')][0]
                else:
                    d = [option for option in options if option in ('w','e')][0]
                next_step = options[d]
                self.turn(d)
            self.loc = next_step
#            print(self.loc, self.direction)


def read_file(file):
    raw = []
    with open(file) as file:
        for line in file:
            raw.append(line.rstrip('\n'))
    return raw

def process_track(raw):
    track = defaultdict()
    carts = []
    for i,row in enumerate(raw):
        last = None
        for x,thing in enumerate(row):
            y = i
            loc = Point(x, y)
            neighbors = defaultdict()
            
            directions = {'<': 'w', '>': 'e', '^': 'n', 'v': 's'}
            if thing in directions:
                direction = directions[thing]
                cart = Cart(x, y, direction)
                carts.append(cart)
                if thing in ('<','>'):
                    thing = '-'
                else:
                    thing = '|'
                

            # Process directions
            if thing in ('-', '+'):
                neighbors['w'] = Point(x-1, y)
                neighbors['e'] = Point(x+1, y)
                
            if thing in ('|', '+'):
                neighbors['n'] = Point(x, y-1)
                neighbors['s'] = Point(x, y+1)
                
            if thing == '\\' and last in ('-','+'):
                neighbors['w'] = Point(x-1, y)
                neighbors['s'] = Point(x, y+1)
            elif thing == '/' and last in ('-','+'):
                neighbors['w'] = Point(x-1, y)
                neighbors['n'] = Point(x, y-1)
            elif thing == '\\':
                neighbors['n'] = Point(x, y-1)
                neighbors['e'] = Point(x+1, y)
            elif thing == '/':
                neighbors['s'] = Point(x, y+1)
                neighbors['e'] = Point(x+1, y)
            
            track[loc] = neighbors

            last = thing
                
    return track, carts

def check_collisions(carts):
    locations = Counter([cart.loc for cart in carts])
    for loc, cnt in locations.items():
        if cnt > 1:
            print(f"Collision! Location: {loc}")
#            return loc
            return loc
        else:
            return False

def solve_puzzle(file):
    raw = read_file(file)
    track, carts = process_track(raw)
    collisions = check_collisions(carts)
    while collisions is False:
        carts.sort(key=lambda cart: (cart.loc.y, cart.loc.x))
        print([(cart.loc, cart.direction) for cart in carts])
        for cart in carts:
            cart.move(track)
            collisions = check_collisions(carts)
            if collisions:
                break
    return collisions

assert solve_puzzle('input/day13-test.txt') == Point(7, 3)

solution = solve_puzzle('input/day13.txt')
