import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import math
import time

# -------------------- Closest Pair of Points --------------------

def closest_pair(points):
    """Divide-and-conquer closest pair. Returns (distance, pair, trace)."""
    trace = []
    if len(points) < 2:
        raise ValueError("At least two points are required.")

    indexed = [(x, y, i) for i, (x, y) in enumerate(points)]
    px = sorted(indexed, key=lambda p: (p[0], p[1]))
    py = sorted(indexed, key=lambda p: (p[1], p[0]))

    def brute(items):
        best = (float("inf"), None)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                d = math.hypot(items[i][0] - items[j][0], items[i][1] - items[j][1])
                if d < best[0]:
                    best = (d, (items[i], items[j]))
        return best

    def solve(x_sorted, y_sorted, depth=0):
        n = len(x_sorted)
        indent = "  " * depth
        if n <= 3:
            best_d, best_pair = brute(x_sorted)
            trace.append(f"{indent}Base case: {n} point(s); checked pairs directly.")
            return best_d, best_pair

        mid = n // 2
        midpoint_x = x_sorted[mid][0]
        left_x = x_sorted[:mid]
        right_x = x_sorted[mid:]
        left_ids = {p[2] for p in left_x}
        left_y = [p for p in y_sorted if p[2] in left_ids]
        right_y = [p for p in y_sorted if p[2] not in left_ids]

        trace.append(f"{indent}Divide {n} points into {len(left_x)} left and {len(right_x)} right.")
        dl, pair_l = solve(left_x, left_y, depth + 1)
        dr, pair_r = solve(right_x, right_y, depth + 1)

        if dl <= dr:
            best_d, best_pair = dl, pair_l
        else:
            best_d, best_pair = dr, pair_r

        strip = [p for p in y_sorted if abs(p[0] - midpoint_x) < best_d]
        comparisons = 0
        for i in range(len(strip)):
            # At most the next 7 points need checking in the y-sorted strip.
            for j in range(i + 1, min(i + 8, len(strip))):
                if strip[j][1] - strip[i][1] >= best_d:
                    break
                comparisons += 1
                d = math.hypot(strip[i][0] - strip[j][0],
                               strip[i][1] - strip[j][1])
                if d < best_d:
                    best_d = d
                    best_pair = (strip[i], strip[j])

        trace.append(f"{indent}Combine: strip has {len(strip)} point(s); "
                     f"checked {comparisons} cross-strip pair(s).")
        return best_d, best_pair

    distance, pair = solve(px, py)
    p1, p2 = pair
    return distance, ((p1[0], p1[1]), (p2[0], p2[1])), trace


def read_points(path):
    lines = [line.strip() for line in Path(path).read_text().splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    n = int(lines[0])
    points = []
    for line in lines[1:]:
        parts = line.replace(",", " ").split()
        if len(parts) != 2:
            raise ValueError("Each point line must contain exactly x and y.")
        points.append((float(parts[0]), float(parts[1])))
    if len(points) != n:
        raise ValueError(f"File says {n} points, but contains {len(points)}.")
    return points


# -------------------- Integer Multiplication (Karatsuba) --------------------

def karatsuba(x, y, trace=None, depth=0):
    """Recursive Karatsuba multiplication for non-negative integers."""
    if trace is None:
        trace = []
    indent = "  " * depth
    sign = -1 if (x < 0) ^ (y < 0) else 1
    x, y = abs(x), abs(y)

    if x < 10 or y < 10:
        result = x * y
        trace.append(f"{indent}Base case: multiply {x} * {y} = {result}")
        return sign * result, trace

    n = max(len(str(x)), len(str(y)))
    half = n // 2
    power = 10 ** half
    a, b = divmod(x, power)
    c, d = divmod(y, power)
    trace.append(f"{indent}Split: x = {a}*10^{half} + {b}; "
                 f"y = {c}*10^{half} + {d}")

    z0, _ = karatsuba(b, d, trace, depth + 1)
    z2, _ = karatsuba(a, c, trace, depth + 1)
    z1, _ = karatsuba(a + b, c + d, trace, depth + 1)
    middle = z1 - z2 - z0
    result = z2 * (10 ** (2 * half)) + middle * power + z0
    trace.append(f"{indent}Combine: z2={z2}, middle={middle}, z0={z0}")
    return sign * result, trace


def read_integers(path):
    tokens = Path(path).read_text().split()
    if len(tokens) != 2:
        raise ValueError("Integer multiplication file must contain exactly two integers.")
    return int(tokens[0]), int(tokens[1])


# -------------------- Result formatting and UI --------------------

def run_file(path):
    path = Path(path)
    # Closest-pair files begin with a point count and have multiple coordinate rows.
    lines = [line.strip() for line in path.read_text().splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    if len(lines) > 2:
        points = read_points(path)
        start = time.perf_counter()
        distance, pair, trace = closest_pair(points)
        elapsed = time.perf_counter() - start
        result = (
            "ALGORITHM: CLOSEST PAIR OF POINTS (DIVIDE AND CONQUER)\n"
            f"Number of points: {len(points)}\n"
            f"Closest pair: {pair[0]} and {pair[1]}\n"
            f"Minimum distance: {distance:.12f}\n"
            f"Execution time: {elapsed:.6f} seconds\n"
            "Expected time complexity: O(n log n)\n"
        )
        return "Closest Pair of Points", result, trace

    x, y = read_integers(path)
    start = time.perf_counter()
    product, trace = karatsuba(x, y)
    elapsed = time.perf_counter() - start
    result = (
        "ALGORITHM: INTEGER MULTIPLICATION (KARATSUBA DIVIDE AND CONQUER)\n"
        f"First integer digits: {len(str(abs(x)))}\n"
        f"Second integer digits: {len(str(abs(y)))}\n"
        f"Product: {product}\n"
        f"Execution time: {elapsed:.6f} seconds\n"
        "Expected time complexity: O(n^log2(3)) ~ O(n^1.585)\n"
    )
    return "Integer Multiplication", result, trace


class AlgorithmViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Divide & Conquer Algorithm Lab")
        self.root.geometry("1120x760")
        self.root.minsize(900, 620)
        self.root.configure(bg="#101827")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#101827")
        style.configure("TLabel", background="#101827", foreground="#e5edf7",
                        font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 23, "bold"),
                        foreground="#ffffff")
        style.configure("Sub.TLabel", foreground="#9fb2c8", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=9)
        style.configure("Accent.TButton", background="#2563eb", foreground="white")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("TNotebook", background="#101827", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 9), font=("Segoe UI", 10, "bold"))

        outer = ttk.Frame(root, padding=22)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="Divide & Conquer Algorithm Lab",
                  style="Header.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Explore Closest Pair of Points and Karatsuba Integer Multiplication",
                  style="Sub.TLabel").pack(anchor="w", pady=(3, 18))

        top = ttk.Frame(outer)
        top.pack(fill="x", pady=(0, 14))
        self.path_var = tk.StringVar(value="No input file selected")
        ttk.Label(top, textvariable=self.path_var).pack(side="left", fill="x", expand=True)
        ttk.Button(top, text="Choose Input File", style="Accent.TButton",
                   command=self.choose_file).pack(side="right", padx=(10, 0))
        ttk.Button(top, text="Run Algorithm", command=self.run).pack(side="right")

        self.status = tk.StringVar(value="Select a valid .txt input file to begin.")
        ttk.Label(outer, textvariable=self.status, style="Sub.TLabel").pack(anchor="w", pady=(0, 10))

        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill="both", expand=True)

        result_tab = ttk.Frame(self.tabs, padding=12)
        trace_tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(result_tab, text="  Result  ")
        self.tabs.add(trace_tab, text="  Algorithm Working  ")

        self.result_text = self.make_text(result_tab)
        self.trace_text = self.make_text(trace_tab)

        footer = ttk.Frame(outer)
        footer.pack(fill="x", pady=(12, 0))
        ttk.Label(footer, text="Input format: closest pair = first line n, then x y per line | "
                               "multiplication = two integers",
                  style="Sub.TLabel").pack(side="left")

        self.selected_file = None

    def make_text(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        text = tk.Text(frame, wrap="word", bg="#0b1220", fg="#dbeafe",
                       insertbackground="white", relief="flat",
                       font=("Consolas", 10), padx=14, pady=14)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return text

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="Select an algorithm input file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            self.selected_file = Path(path)
            self.path_var.set(str(self.selected_file))
            self.status.set("File selected. Click Run Algorithm.")

    def run(self):
        if not self.selected_file:
            messagebox.showwarning("No file", "Please choose an input .txt file first.")
            return
        try:
            name, result, trace = run_file(self.selected_file)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", result)
            self.trace_text.delete("1.0", "end")
            self.trace_text.insert("end", f"WORKING TRACE — {name}\n\n")
            self.trace_text.insert("end", "\n".join(trace))
            output_dir = Path(__file__).parent / "user_results"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{self.selected_file.stem}_result.txt"
            output_path.write_text(result + "\nWORKING TRACE\n\n" + "\n".join(trace), encoding="utf-8")
            self.status.set(f"Completed successfully. Result saved to: {output_path}")
            self.tabs.select(0)
        except Exception as exc:
            messagebox.showerror("Input / execution error", str(exc))
            self.status.set("Could not run the selected file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmViewer(root)
    root.mainloop()
