# Introduction to Algorithms
## CIS 120 — Intro to Computing | Preston Furulie

## Linear Search Algorithm

Given a list of `n` elements and a target value, find the index of the target.

```
ALGORITHM LinearSearch(list, target):
    FOR i = 0 TO length(list) - 1:
        IF list[i] == target:
            RETURN i
    RETURN -1
```

## Bubble Sort Algorithm

```
ALGORITHM BubbleSort(list):
    n = length(list)
    FOR i = 0 TO n - 1:
        FOR j = 0 TO n - i - 2:
            IF list[j] > list[j + 1]:
                SWAP list[j], list[j + 1]
    RETURN list
```

## Complexity Analysis

| Algorithm       | Time     | Space |
|-----------------|----------|-------|
| Linear Search   | O(n)     | O(1)  |
| Bubble Sort     | O(n²)   | O(1)  |
| Binary Search   | O(log n) | O(1)  |
