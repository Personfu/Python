# ============================================================
# Sorting Algorithms — Complete Implementation & Comparison
# CIS 275 — Data Structures | Preston Furulie
# ============================================================
# Covers: bubble sort, selection sort, insertion sort,
# merge sort, quick sort, counting sort, Python's Timsort,
# stability analysis, benchmarking, and visualization.
# ============================================================

import time
import random


# ── 1. Bubble Sort — O(n²) ──────────────────────────────────

def bubble_sort(arr):
    """Compare adjacent elements, swap if out of order.
    Optimized: early exit if no swaps occur (already sorted).

    Time:  O(n²) worst/average, O(n) best (sorted input)
    Space: O(1) — in-place
    Stable: Yes
    """
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break  # optimization: list is sorted

    return arr, comparisons, swaps


# ── 2. Selection Sort — O(n²) ───────────────────────────────

def selection_sort(arr):
    """Find the minimum element in unsorted portion, swap to front.

    Time:  O(n²) in all cases (always scans remaining)
    Space: O(1) — in-place
    Stable: No (swapping can change relative order of equal elements)
    """
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

    return arr, comparisons, swaps


# ── 3. Insertion Sort — O(n²) ───────────────────────────────

def insertion_sort(arr):
    """Build sorted portion by inserting each element into its
    correct position, shifting larger elements right.

    Time:  O(n²) worst/average, O(n) best (nearly sorted)
    Space: O(1) — in-place
    Stable: Yes
    Best for: small arrays or nearly-sorted data
    """
    arr = arr.copy()
    comparisons = 0
    shifts = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            shifts += 1
            j -= 1
        comparisons += 1  # the failing comparison
        arr[j + 1] = key

    return arr, comparisons, shifts


# ── 4. Merge Sort — O(n log n) ──────────────────────────────

def merge_sort(arr):
    """Divide list in half recursively, sort each half, merge.
    
    Time:  O(n log n) in all cases (guaranteed)
    Space: O(n) — requires temporary arrays for merging
    Stable: Yes
    Best for: large datasets where guaranteed performance is needed
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:   # <= preserves stability
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ── 5. Quick Sort — O(n log n) average ──────────────────────

def quick_sort(arr):
    """Choose a pivot, partition into less-than/equal/greater-than,
    recursively sort partitions.

    Time:  O(n log n) average, O(n²) worst (bad pivot selection)
    Space: O(log n) for recursion stack
    Stable: No (partitioning can change relative order)
    Best for: general-purpose sorting; fastest in practice
    """
    if len(arr) <= 1:
        return arr

    # Median-of-three pivot selection (reduces worst-case likelihood)
    first, mid_val, last = arr[0], arr[len(arr) // 2], arr[-1]
    pivot = sorted([first, mid_val, last])[1]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# ── 6. Counting Sort — O(n + k) ────────────────────────────

def counting_sort(arr):
    """Non-comparison sort for integers. Counts occurrences of each
    value and reconstructs the sorted array.

    Time:  O(n + k) where k = range of input values
    Space: O(k) for the count array
    Stable: Yes
    Limitation: only works for non-negative integers
    """
    if not arr:
        return arr

    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    result = []
    for val, cnt in enumerate(count):
        result.extend([val] * cnt)

    return result


# ── Benchmarking Framework ──────────────────────────────────

def benchmark(sort_func, data, name):
    """Time a sorting function and return results."""
    start = time.perf_counter()
    if name in ("Bubble", "Selection", "Insertion"):
        result, comps, ops = sort_func(data.copy())
        elapsed = time.perf_counter() - start
        return {"name": name, "time": elapsed, "comparisons": comps, "ops": ops}
    else:
        result = sort_func(data.copy())
        elapsed = time.perf_counter() - start
        return {"name": name, "time": elapsed, "comparisons": "-", "ops": "-"}


# ── Main Demonstration ──────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("  SORTING ALGORITHMS — CIS 275 | Preston Furulie")
    print("=" * 70)

    # Verify correctness on small data
    test_data = [64, 34, 25, 12, 22, 11, 90, 1, 55, 38]
    print(f"\n  Original: {test_data}")
    print(f"  Bubble:    {bubble_sort(test_data)[0]}")
    print(f"  Selection: {selection_sort(test_data)[0]}")
    print(f"  Insertion: {insertion_sort(test_data)[0]}")
    print(f"  Merge:     {merge_sort(test_data)}")
    print(f"  Quick:     {quick_sort(test_data)}")
    print(f"  Counting:  {counting_sort(test_data)}")
    print(f"  Timsort:   {sorted(test_data)}")

    # Benchmark with larger dataset
    sizes = [1000, 5000]
    for size in sizes:
        data = [random.randint(1, 10000) for _ in range(size)]
        print(f"\n  {'─' * 60}")
        print(f"  Benchmark: {size} random integers")
        print(f"  {'Algorithm':<14} {'Time (s)':>10} {'Comparisons':>14} {'Ops':>10}")
        print(f"  {'─' * 50}")

        results = [
            benchmark(bubble_sort, data, "Bubble"),
            benchmark(selection_sort, data, "Selection"),
            benchmark(insertion_sort, data, "Insertion"),
            benchmark(merge_sort, data, "Merge"),
            benchmark(quick_sort, data, "Quick"),
            benchmark(counting_sort, data, "Counting"),
            benchmark(sorted, data, "Timsort"),
        ]

        for r in results:
            comps = f"{r['comparisons']:>14,}" if isinstance(r['comparisons'], int) else f"{r['comparisons']:>14}"
            ops = f"{r['ops']:>10,}" if isinstance(r['ops'], int) else f"{r['ops']:>10}"
            print(f"  {r['name']:<14} {r['time']:>10.6f} {comps} {ops}")

    # Complexity reference table
    print(f"\n  {'─' * 60}")
    print(f"  COMPLEXITY REFERENCE")
    print(f"  {'Algorithm':<14} {'Best':>10} {'Average':>10} {'Worst':>10} {'Space':>8} {'Stable':>8}")
    print(f"  {'─' * 60}")
    table = [
        ("Bubble",    "O(n)",      "O(n²)",     "O(n²)",     "O(1)",  "Yes"),
        ("Selection", "O(n²)",     "O(n²)",     "O(n²)",     "O(1)",  "No"),
        ("Insertion", "O(n)",      "O(n²)",     "O(n²)",     "O(1)",  "Yes"),
        ("Merge",     "O(n lg n)", "O(n lg n)", "O(n lg n)", "O(n)",  "Yes"),
        ("Quick",     "O(n lg n)", "O(n lg n)", "O(n²)",     "O(lg n)","No"),
        ("Counting",  "O(n+k)",   "O(n+k)",    "O(n+k)",    "O(k)",  "Yes"),
        ("Timsort",   "O(n)",      "O(n lg n)", "O(n lg n)", "O(n)",  "Yes"),
    ]
    for row in table:
        print(f"  {row[0]:<14} {row[1]:>10} {row[2]:>10} {row[3]:>10} {row[4]:>8} {row[5]:>8}")
