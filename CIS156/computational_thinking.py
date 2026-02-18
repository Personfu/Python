# ============================================================
# Assignment — Computational Thinking
# CIS 156 — Computer Science Concepts | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# CompTIA ITF+ Alignment: Software Development domain —
# understanding how problems are analyzed and solved using
# computational methods before any code is written.
# ============================================================

"""
Computational Thinking — The Four Pillars
==========================================
Computational thinking is a structured approach to problem-solving
that applies concepts from computer science to everyday challenges.

The four pillars are:
  1. Decomposition        — Break a complex problem into smaller parts
  2. Pattern Recognition  — Identify similarities or trends
  3. Abstraction          — Focus on what matters, ignore the rest
  4. Algorithm Design     — Create step-by-step instructions
"""


# ────────────────────────────────────────────────────────────
# 1. PROBLEM DECOMPOSITION
# ────────────────────────────────────────────────────────────
# Decomposition means taking a large, overwhelming problem and
# splitting it into manageable sub-problems that can each be
# solved independently.

def decompose_problem(problem, sub_problems):
    """Demonstrate breaking a complex problem into parts."""
    print(f"\n{'='*60}")
    print("PILLAR 1: PROBLEM DECOMPOSITION")
    print(f"{'='*60}")
    print(f"\nMain Problem : {problem}")
    print(f"Sub-problems : {len(sub_problems)} identified\n")
    for i, sub in enumerate(sub_problems, 1):
        print(f"  Step {i}: {sub}")
    print(f"\nBy solving each sub-problem, we solve the whole.")


def decomposition_example():
    """Real-world decomposition: planning a website."""
    problem = "Build an e-commerce website for FLLC Enterprise"
    sub_problems = [
        "Design the database schema (products, users, orders)",
        "Create the front-end layout and navigation",
        "Implement user authentication and authorization",
        "Build the product catalog with search and filtering",
        "Develop the shopping cart and checkout flow",
        "Set up payment processing integration",
        "Configure hosting, domain, and SSL certificate",
        "Write automated tests and deploy",
    ]
    decompose_problem(problem, sub_problems)


# ────────────────────────────────────────────────────────────
# 2. PATTERN RECOGNITION
# ────────────────────────────────────────────────────────────
# Pattern recognition is the ability to notice similarities,
# trends, or regularities in data or problems. Recognizing
# patterns lets us reuse proven solutions.

def recognize_patterns(dataset):
    """Analyze a dataset for simple statistical patterns."""
    print(f"\n{'='*60}")
    print("PILLAR 2: PATTERN RECOGNITION")
    print(f"{'='*60}")
    print(f"\nDataset: {dataset}\n")

    n = len(dataset)
    total = sum(dataset)
    mean = total / n
    sorted_data = sorted(dataset)
    median = (
        sorted_data[n // 2]
        if n % 2 != 0
        else (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    )

    diffs = [dataset[i + 1] - dataset[i] for i in range(n - 1)]
    is_increasing = all(d > 0 for d in diffs)
    is_decreasing = all(d < 0 for d in diffs)

    print(f"  Count   : {n}")
    print(f"  Sum     : {total}")
    print(f"  Mean    : {mean:.2f}")
    print(f"  Median  : {median}")
    print(f"  Min     : {min(dataset)}")
    print(f"  Max     : {max(dataset)}")
    print(f"  Range   : {max(dataset) - min(dataset)}")

    if is_increasing:
        print("  Trend   : Strictly increasing")
    elif is_decreasing:
        print("  Trend   : Strictly decreasing")
    else:
        print("  Trend   : No strict monotonic trend")

    constant_diff = len(set(diffs)) == 1
    if constant_diff and diffs:
        print(f"  Pattern : Arithmetic sequence (common difference = {diffs[0]})")


def pattern_example():
    """Demonstrate pattern recognition with server load data."""
    print("\n  --- FLLC Server Load (requests/min over 8 hours) ---")
    server_load = [120, 135, 150, 165, 180, 195, 210, 225]
    recognize_patterns(server_load)

    print("\n  --- Monthly Support Tickets ---")
    tickets = [45, 38, 52, 41, 55, 39, 48, 42, 50, 44, 47, 43]
    recognize_patterns(tickets)


# ────────────────────────────────────────────────────────────
# 3. ABSTRACTION
# ────────────────────────────────────────────────────────────
# Abstraction means filtering out unnecessary details so we
# can focus on what is relevant. In programming, classes and
# functions are tools of abstraction.

class Vehicle:
    """
    Abstraction example: a Vehicle hides internal complexity.
    The driver doesn't need to know how fuel injection or
    transmission internals work — just the interface.
    """

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self._fuel_level = 100  # internal detail hidden from user
        self._engine_temp = 190  # internal detail hidden from user

    def start(self):
        return f"{self.year} {self.make} {self.model} started."

    def drive(self, miles):
        fuel_used = miles * 0.03
        self._fuel_level = max(0, self._fuel_level - fuel_used)
        return f"Drove {miles} mi. Fuel remaining: {self._fuel_level:.1f}%"

    def status(self):
        return f"  Make: {self.make} | Model: {self.model} | Year: {self.year}"


def abstraction_example():
    """Show how abstraction hides complexity behind a clean interface."""
    print(f"\n{'='*60}")
    print("PILLAR 3: ABSTRACTION")
    print(f"{'='*60}")
    print("\nA Vehicle object hides engine temp, fuel chemistry, etc.")
    print("The user interacts only with start(), drive(), status().\n")

    car = Vehicle("Toyota", "Camry", 2024)
    print(f"  {car.start()}")
    print(f"  {car.drive(50)}")
    print(f"  {car.drive(120)}")
    print(car.status())
    print("\nAbstraction lets us manage complexity at every scale —")
    print("from a single function up to an entire enterprise system.")


# ────────────────────────────────────────────────────────────
# 4. ALGORITHM DESIGN
# ────────────────────────────────────────────────────────────
# An algorithm is a finite, ordered set of unambiguous steps
# that produces a result. Good algorithms are correct,
# efficient, and clearly expressed.

def recipe_algorithm():
    """Everyday algorithm: making a peanut butter & jelly sandwich."""
    print(f"\n{'='*60}")
    print("PILLAR 4: ALGORITHM DESIGN — Recipe Example")
    print(f"{'='*60}")
    steps = [
        "Gather ingredients: bread, peanut butter, jelly, knife",
        "Place two slices of bread on a clean surface",
        "Open the peanut butter jar",
        "Use the knife to spread peanut butter on slice 1",
        "Wipe the knife clean",
        "Open the jelly jar",
        "Use the knife to spread jelly on slice 2",
        "Place slice 1 on top of slice 2 (spreads facing inward)",
        "Cut diagonally if desired",
        "Serve and enjoy",
    ]
    print("\nAlgorithm: Make a PB&J Sandwich\n")
    for i, step in enumerate(steps, 1):
        print(f"  {i:>2}. {step}")
    print(f"\nSteps: {len(steps)} | Deterministic: Yes | Terminates: Yes")


# ────────────────────────────────────────────────────────────
# PRACTICAL EXAMPLE: ATM STATE MACHINE
# ────────────────────────────────────────────────────────────
# A finite state machine (FSM) models a system with a limited
# number of states and well-defined transitions between them.

def atm_state_machine():
    """Simulate an ATM using a finite state machine."""
    print(f"\n{'='*60}")
    print("PRACTICAL EXAMPLE: ATM State Machine")
    print(f"{'='*60}")

    states = {
        "IDLE":         "Waiting for card insertion",
        "CARD_READ":    "Card detected — prompt for PIN",
        "PIN_ENTRY":    "Validating PIN against bank records",
        "MENU":         "Display transaction options",
        "WITHDRAW":     "Dispensing cash",
        "BALANCE":      "Displaying account balance",
        "EJECT_CARD":   "Returning card to customer",
    }

    transitions = [
        ("IDLE",       "Insert card",      "CARD_READ"),
        ("CARD_READ",  "Card validated",   "PIN_ENTRY"),
        ("PIN_ENTRY",  "PIN correct",      "MENU"),
        ("PIN_ENTRY",  "PIN incorrect x3", "EJECT_CARD"),
        ("MENU",       "Select withdraw",  "WITHDRAW"),
        ("MENU",       "Select balance",   "BALANCE"),
        ("WITHDRAW",   "Cash dispensed",   "EJECT_CARD"),
        ("BALANCE",    "Done viewing",     "EJECT_CARD"),
        ("EJECT_CARD", "Card removed",     "IDLE"),
    ]

    print("\nStates:")
    for state, desc in states.items():
        print(f"  {state:<14} — {desc}")

    print("\nTransitions:")
    for src, event, dst in transitions:
        print(f"  {src:<14} --[ {event:<18} ]--> {dst}")

    # Simulate a successful withdrawal
    print("\n--- Simulation: successful $200 withdrawal ---")
    path = ["IDLE", "CARD_READ", "PIN_ENTRY", "MENU", "WITHDRAW", "EJECT_CARD", "IDLE"]
    for i, state in enumerate(path):
        prefix = "  >>>" if i == len(path) - 1 else "  -->"
        print(f"{prefix} {state}: {states[state]}")


# ────────────────────────────────────────────────────────────
# PRACTICAL EXAMPLE: SEARCH OPTIMIZATION
# ────────────────────────────────────────────────────────────
# Comparing linear search O(n) vs binary search O(log n)
# demonstrates how algorithm choice impacts performance.

import time


def linear_search(data, target):
    """Search every element until the target is found."""
    for i, value in enumerate(data):
        if value == target:
            return i
    return -1


def binary_search(data, target):
    """Requires sorted data. Halves the search space each step."""
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def search_optimization_demo():
    """Compare linear vs binary search performance."""
    print(f"\n{'='*60}")
    print("PRACTICAL EXAMPLE: Search Optimization")
    print(f"{'='*60}")

    dataset = list(range(1, 1_000_001))  # 1 to 1,000,000
    target = 999_999
    print(f"\nDataset size : 1,000,000 sorted integers")
    print(f"Target value : {target}\n")

    start = time.perf_counter()
    idx_lin = linear_search(dataset, target)
    time_lin = time.perf_counter() - start

    start = time.perf_counter()
    idx_bin = binary_search(dataset, target)
    time_bin = time.perf_counter() - start

    print(f"  Linear Search — index: {idx_lin:>10,} | time: {time_lin:.6f}s")
    print(f"  Binary Search — index: {idx_bin:>10,} | time: {time_bin:.6f}s")

    if time_bin > 0:
        speedup = time_lin / time_bin
        print(f"\n  Binary search was ~{speedup:.0f}x faster on this dataset.")
    print("\n  Key insight: algorithm choice matters more than hardware speed.")


# ────────────────────────────────────────────────────────────
# MAIN — Run all demonstrations
# ────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  CIS 156 — Computational Thinking")
    print("  FLLC Enterprise | Preston Furulie | Spring 2026")
    print("=" * 60)

    decomposition_example()
    pattern_example()
    abstraction_example()
    recipe_algorithm()
    atm_state_machine()
    search_optimization_demo()

    print(f"\n{'='*60}")
    print("  End of Computational Thinking Module")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
