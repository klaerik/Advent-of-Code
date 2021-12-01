
def read_file(file, include_blank_lines=False, convert=None):
    out = []
    with open(file) as f:
        for line in f:
            clean = line.strip() if convert is None else convert(line.strip())
            if clean or include_blank_lines:
                out.append(clean)
    return out


def product(nums):
    out = 1
    for num in nums:
        out *= num
    return out
