
def read_file(file):
    out = []
    with open(file) as f:
        for line in f:
            clean = line.strip()
            if clean:
                out.append(clean)
    return out


def product(nums):
    out = 1
    for num in nums:
        out *= num
    return out
