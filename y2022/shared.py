from pathlib import Path
import inspect
import typing

def read_file(path: str|Path = None, strip=True, include_blank_lines: bool = False, convert: typing.Callable = None):

    if type(path) is str:
        print("Building path for input file")
        path = Path() / 'y2022' / 'input' / path

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
