from pathlib import Path
import random

ROOT = Path(__file__).parent
random.seed(2026)

for folder in ("closest_pair", "integer_multiplication"):
    (ROOT / "datasets" / folder).mkdir(parents=True, exist_ok=True)

# Ten closest-pair datasets. Every dataset has more than 100 points.
sizes = [120, 150, 180, 220, 260, 320, 400, 500, 650, 800]
for index, n in enumerate(sizes, start=1):
    points = set()
    while len(points) < n:
        points.add((random.randint(-100000, 100000),
                    random.randint(-100000, 100000)))
    lines = [str(n)] + [f"{x} {y}" for x, y in sorted(points)]
    path = ROOT / "datasets" / "closest_pair" / f"closest_pair_{index:02d}.txt"
    path.write_text("\n".join(lines) + "\n")

# Ten multiplication datasets. Both operands contain more than 100 digits.
digit_sizes = [120, 150, 180, 220, 260, 320, 400, 500, 650, 800]
for index, digits in enumerate(digit_sizes, start=1):
    first = random.randint(10 ** (digits - 1), 10 ** digits - 1)
    second = random.randint(10 ** (digits - 1), 10 ** digits - 1)
    path = ROOT / "datasets" / "integer_multiplication" / f"multiplication_{index:02d}.txt"
    path.write_text(f"{first}\n{second}\n")

print("Generated 10 closest-pair and 10 integer-multiplication input files.")
