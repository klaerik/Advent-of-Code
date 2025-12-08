from pathlib import Path

# Determine current year
year = 2025
root = Path(f"y{year}")

# Get next day
last_day = max((int(f.stem[-2:]) for f in root.glob(r"day*.py")))
day = f"{(last_day+1):02d}"

# Create code file
template = root / "_template.py"
template_code = template.read_text().replace("XX", day)

# Target code file
target = root / f"day{day}.py"
target.write_text(template_code)

# Create input files
(root / "input" / f"day{day}.txt").touch()
(root / "input" / f"day{day}-test.txt").touch()
