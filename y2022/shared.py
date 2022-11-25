from pathlib import Path
import inspect
import typing

def read_file(path: Path|str = None, include_blank_lines: bool = False, convert: typing.Callable = None):

    if path is None:
        calling_path = Path(inspect.stack()[1].filename)
        path = calling_path.parent / 'input' / calling_path.stem

    print(f"Loading file from {path}")
    out = []
    with open(path) as f:
        for line in f:
            clean = line.strip() 
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
