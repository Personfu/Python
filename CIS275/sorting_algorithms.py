# Sorting Algorithm Comparison
# CIS 275 — Data Structures | Preston Furulie

import time
import random

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


# Benchmark with 5000 elements
data = [random.randint(1, 10000) for _ in range(5000)]

start = time.time()
bubble_sort(data.copy())
bubble_time = time.time() - start

start = time.time()
quick_sort(data.copy())
quick_time = time.time() - start

print(f"Bubble Sort: {bubble_time:.4f}s")
print(f"Quick Sort:  {quick_time:.4f}s")
print(f"Quick Sort is {bubble_time/quick_time:.1f}x faster")
