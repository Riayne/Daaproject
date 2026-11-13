# Divide & Conquer Algorithm Lab

## Included
- `main.py`: Tkinter GUI, Closest Pair of Points, and Karatsuba multiplication.
- `generate_datasets.py`: reproducibly generates 10 input files for each algorithm.
- `datasets/closest_pair/`: 10 point datasets (120 to 800 points).
- `datasets/integer_multiplication/`: 10 pairs of integers (120 to 800 digits each).
- `results/`: precomputed output files for all 20 datasets.

## Run
1. Install Python 3 (Tkinter is included with most standard Windows Python installations).
2. Open a terminal in this folder.
3. Run `python main.py`.
4. Click **Choose Input File**, select any `.txt` file from `datasets`, then click **Run Algorithm**.
5. The Result tab shows the answer and complexity. Algorithm Working shows the recursive divide/combine trace.
6. Each GUI run also saves a result and trace in `user_results/`.

## Input formats
Closest pair:
- First line: number of points `n`
- Next `n` lines: `x y`

Integer multiplication:
- Exactly two integers, one per line (or separated by whitespace).

## Algorithms
- Closest pair: O(n log n) divide-and-conquer. Points are sorted once; recursive calls split by x-coordinate and merge using a y-sorted strip.
- Integer multiplication: Karatsuba divide-and-conquer, O(n^log2(3)) ≈ O(n^1.585).

All generated input values are valid. The closest-pair datasets contain unique integer-coordinate points.
