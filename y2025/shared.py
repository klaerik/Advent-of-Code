import re
import typing
from dataclasses import dataclass
from pathlib import Path

YEAR = 2025


def init_day(num: int):
    """Set up a new day."""
    folder = Path(f"y{YEAR}")
    day = str(num).zfill(2)
    template = folder / "_template.py"
    script = folder / f"day{day}.py"
    if not script.exists():
        text = template.read_text()
        text = re.sub(r"dayXX", f"day{day}", text)
        script.write_text(text)
    data = folder / "input" / f"day{day}.txt"
    if not data.exists():
        data.touch()
    data = folder / "input" / f"day{day}-test.txt"
    if not data.exists():
        data.touch()


@dataclass
class Counter(typing.Dict):
    iterable: typing.Iterable

    def __post_init__(self):
        self.counts: dict = {}
        self.count()

    def count(self):
        for i in self.iterable:
            if i in self.counts:
                self.counts[i] += 1
            else:
                self.counts[i] = 1


def read_file(
    path: typing.Union[str, Path] = None,
    strip=True,
    include_blank_lines: bool = False,
    convert: typing.Callable = None,
):
    if type(path) is str:
        print("Building path for input file")
        path = Path() / f"y{YEAR}" / "input" / path

    print(f"Loading file from {path}")
    out = []
    with open(path) as f:
        for line in f:
            clean = line.strip() if strip else line
            if clean and convert is not None:
                clean = convert(clean)
            if clean or include_blank_lines:
                out.append(clean)
    return out


def product(nums):
    out = 1
    for num in nums:
        out *= num
    return out


def sign(num):
    if num == 0:
        return 0
    elif num > 0:
        return 1
    else:
        return -1
