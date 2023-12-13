import y2023.shared as shared
from dataclasses import dataclass

## Data
raw = shared.read_file("day09.txt")
test = shared.read_file("day09-test.txt")


## Functions
@dataclass
class OasisReport:
    raw: list[str]
    rows: list[int] | None = None
    reverse: bool = False

    def __post_init__(self):
        self.rows = []
        for row in self.raw:
            self.rows.append([int(x) for x in row.split(" ")])
        if self.reverse:
            self.rows = [row[::-1] for row in self.rows]

    def generate_next_row(self, row: list[int]) -> list[int]:
        out = []
        for i, j in zip(row, row[1:]):
            out.append(j - i)
        return out

    def is_all_zeros(self, row: list[int]) -> bool:
        return not any(row)

    def calculate_next_value(self, row: list[int]) -> int:
        rows = [row]
        while not self.is_all_zeros(rows[-1]):
            rows.append(self.generate_next_row(rows[-1]))
        return sum([row[-1] for row in rows])

    def get_extrapolated_sum(self) -> int:
        return sum([self.calculate_next_value(row) for row in self.rows])


def solve(test, reverse=False):
    report = OasisReport(test, reverse=reverse)
    return report.get_extrapolated_sum()


## Testing
report = OasisReport(test)
row = report.rows[2]
report.generate_next_row(row[::-1])
row1 = report.generate_next_row(row)
row2 = report.generate_next_row(row1)
report.is_all_zeros(row2)
report.calculate_next_value(row[::-1])


assert solve(test) == 114
assert solve(test, reverse=True) == 2


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, reverse=True)}")
