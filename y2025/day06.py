from dataclasses import dataclass
import math

import y2025.shared as shared

## Data
raw = shared.read_file("day06.txt", strip=False)
test = shared.read_file("day06-test.txt", strip=False)


## Functions
@dataclass
class Calculator:
    raw: list[str]

    def __post_init__(self):
        self.parse()
        self.esrap()

    def parse(self):
        ops = self.raw[-1].split()
        nums = [x.split() for x in self.raw[:-1] if x]
        self.problems = []
        for i, op in enumerate(ops):
            problem = {"op": op}
            problem["nums"] = [int(x[i]) for x in nums]
            self.problems.append(problem)

    def esrap(self):
        nums = [x.strip(r"\n") for x in self.raw[:-1]]
        problem_idx = 0
        for i in range(len(nums[0])):
            num = "".join([x[i] for x in nums])
            num = num.strip()
            if num:
                self.problems[problem_idx].setdefault("ceph_nums", []).append(int(num))
            else:
                problem_idx += 1

    def solve_problem(self, problem: dict, ceph_nums: bool = False) -> int:
        op = problem["op"]
        nums = problem["ceph_nums"] if ceph_nums else problem["nums"]
        if op == "+":
            return sum(nums)
        elif op == "*":
            return math.prod(nums)

    def solve_problems(self, ceph_nums: bool = False) -> list[int]:
        return [self.solve_problem(x, ceph_nums) for x in self.problems]


def solve(test):
    calc = Calculator(test)
    return sum(calc.solve_problems())


def solve2(test):
    calc = Calculator(test)
    return sum(calc.solve_problems(ceph_nums=True))


## Testing
assert solve(test) == 4277556
assert solve2(test) == 3263827


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
