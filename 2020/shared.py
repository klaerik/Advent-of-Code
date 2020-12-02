
def read_file(file):
    out = []
    with open(file) as f:
        for line in f:
            clean = line.strip()
            if clean:
                out.append(clean)
    return out


