# Introduction to Algorithms
## CIS 120 — Intro to Computing | Preston Furulie

---

## 1. What Is an Algorithm?

An **algorithm** is a finite, well-defined sequence of steps that solves a specific problem. Every algorithm must have:

- **Input** — zero or more values provided to the algorithm
- **Output** — at least one result produced
- **Definiteness** — each step is precisely defined and unambiguous
- **Finiteness** — the algorithm terminates after a finite number of steps
- **Effectiveness** — each step is basic enough to be carried out in finite time

---

## 2. Pseudocode Conventions

Pseudocode is a human-readable notation for describing algorithms without committing to a specific programming language:

```
ALGORITHM Name(parameters):
    INPUT: description of inputs
    OUTPUT: description of outputs

    step 1
    step 2
    IF condition THEN
        action
    ELSE
        alternative action
    END IF
    RETURN result
```

---

## 3. Searching Algorithms

### 3.1 Linear Search

Scans every element sequentially until a match is found.

```
ALGORITHM LinearSearch(list, target):
    INPUT: list of n elements, target value
    OUTPUT: index of target, or -1 if not found

    FOR i = 0 TO n - 1:
        IF list[i] == target:
            RETURN i
    RETURN -1
```

- **Best case:** O(1) — target is the first element
- **Worst case:** O(n) — target is last or not present
- **Average case:** O(n/2) ≈ O(n)
- **Use when:** data is unsorted or the list is small

### 3.2 Binary Search

Divides a **sorted** list in half repeatedly to find the target.

```
ALGORITHM BinarySearch(sorted_list, target):
    INPUT: sorted list of n elements, target value
    OUTPUT: index of target, or -1 if not found

    low = 0
    high = n - 1
    WHILE low <= high:
        mid = (low + high) / 2  (integer division)
        IF sorted_list[mid] == target:
            RETURN mid
        ELSE IF sorted_list[mid] < target:
            low = mid + 1
        ELSE:
            high = mid - 1
    RETURN -1
```

- **Best case:** O(1) — target is at the midpoint
- **Worst case:** O(log n) — halving reduces search space exponentially
- **Prerequisite:** data must be sorted first
- **Use when:** data is sorted and the list is large

---

## 4. Sorting Algorithms

### 4.1 Bubble Sort

Repeatedly swaps adjacent elements if they are in the wrong order.

```
ALGORITHM BubbleSort(list):
    n = length(list)
    FOR i = 0 TO n - 1:
        swapped = FALSE
        FOR j = 0 TO n - i - 2:
            IF list[j] > list[j + 1]:
                SWAP list[j], list[j + 1]
                swapped = TRUE
        IF NOT swapped:
            BREAK   (optimization: list is already sorted)
    RETURN list
```

- **Time:** O(n²) worst/average, O(n) best (already sorted with optimization)
- **Space:** O(1) — sorts in place
- **Stable:** Yes (equal elements maintain relative order)

### 4.2 Selection Sort

Finds the minimum element and places it at the beginning, then repeats for the remaining sublist.

```
ALGORITHM SelectionSort(list):
    n = length(list)
    FOR i = 0 TO n - 2:
        min_index = i
        FOR j = i + 1 TO n - 1:
            IF list[j] < list[min_index]:
                min_index = j
        SWAP list[i], list[min_index]
    RETURN list
```

- **Time:** O(n²) in all cases (always scans full remaining sublist)
- **Space:** O(1)
- **Stable:** No

### 4.3 Insertion Sort

Builds a sorted portion one element at a time by inserting each new element into its correct position.

```
ALGORITHM InsertionSort(list):
    FOR i = 1 TO length(list) - 1:
        key = list[i]
        j = i - 1
        WHILE j >= 0 AND list[j] > key:
            list[j + 1] = list[j]
            j = j - 1
        list[j + 1] = key
    RETURN list
```

- **Time:** O(n²) worst/average, O(n) best (nearly sorted data)
- **Space:** O(1)
- **Stable:** Yes
- **Use when:** data is small or nearly sorted

### 4.4 Merge Sort

Divides the list in half recursively, sorts each half, then merges the sorted halves.

```
ALGORITHM MergeSort(list):
    IF length(list) <= 1:
        RETURN list
    mid = length(list) / 2
    left = MergeSort(list[0..mid-1])
    right = MergeSort(list[mid..end])
    RETURN Merge(left, right)

ALGORITHM Merge(left, right):
    result = empty list
    WHILE left is not empty AND right is not empty:
        IF left[0] <= right[0]:
            append left[0] to result, remove from left
        ELSE:
            append right[0] to result, remove from right
    append remaining elements of left and right to result
    RETURN result
```

- **Time:** O(n log n) in all cases
- **Space:** O(n) — requires additional space for merging
- **Stable:** Yes
- **Use when:** guaranteed O(n log n) is required

---

## 5. Complexity Analysis (Big-O Notation)

Big-O describes the **upper bound** of an algorithm's growth rate as input size increases:

| Notation     | Name          | Example                    | 10 items | 1,000 items   |
|-------------|---------------|----------------------------|----------|---------------|
| O(1)        | Constant      | Array index access         | 1        | 1             |
| O(log n)    | Logarithmic   | Binary search              | 3        | 10            |
| O(n)        | Linear        | Linear search              | 10       | 1,000         |
| O(n log n)  | Linearithmic  | Merge sort                 | 33       | 10,000        |
| O(n²)       | Quadratic     | Bubble sort                | 100      | 1,000,000     |
| O(2ⁿ)       | Exponential   | Recursive Fibonacci        | 1,024    | 10^301        |
| O(n!)       | Factorial     | Traveling salesman (brute) | 3.6M     | Impossible    |

### Rules for Determining Big-O:
1. **Drop constants:** O(3n) → O(n)
2. **Drop lower-order terms:** O(n² + n) → O(n²)
3. **Worst case by default** unless specified otherwise
4. **Nested loops multiply:** two nested loops over n → O(n²)
5. **Sequential operations add:** O(n) + O(m) → O(n + m)

---

## 6. Flowchart Symbols

| Symbol       | Shape         | Purpose                          |
|-------------|---------------|----------------------------------|
| Terminal    | Rounded rect  | Start / End of algorithm         |
| Process     | Rectangle     | Action or computation            |
| Decision    | Diamond       | Yes/No or True/False branch      |
| I/O         | Parallelogram | Input or output operation        |
| Connector   | Circle        | Jump to another part of flowchart|
| Arrow       | Line          | Flow direction                   |

---

## 7. Recursion vs. Iteration

| Aspect       | Recursion                        | Iteration                     |
|-------------|----------------------------------|-------------------------------|
| Mechanism   | Function calls itself            | Loop repeats a block          |
| Memory      | Uses call stack (risk of overflow)| Uses loop variable            |
| Readability | Often more elegant for tree/divide problems | More straightforward for linear tasks |
| Performance | Overhead from function calls     | Generally faster              |
| Example     | Merge sort, tree traversal       | Linear search, bubble sort    |

**Key principle:** Every recursive algorithm can be rewritten iteratively (and vice versa), but some problems are naturally recursive (trees, fractals, divide-and-conquer).
