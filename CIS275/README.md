# Phase 05 — Core Algorithm Library
**Department:** Core Engineering | **Course:** CIS 275 — Data Structures | **Status:** Complete

---

## Purpose

Build FLLC's reusable algorithm and data structure library — production-quality implementations of fundamental data structures and algorithms with verified complexity analysis and benchmarking. These form the computational backbone of all FLLC applications.

## Deliverables

| File | Description | Key Concepts |
|------|------------|-------------|
| [`linked_list.py`](linked_list.py) | Singly + Doubly Linked List library | `SinglyLinkedList` (15 operations: prepend, append, insert_at, insert_sorted, delete_first/last/value/at, search, contains, get_at, reverse, find_middle, has_cycle, remove_duplicates), `DoublyLinkedList` with O(1) tail append, Floyd's cycle detection, iterator protocol |
| [`binary_search_tree.py`](binary_search_tree.py) | Full BST with all operations | Insert, search, delete (3 cases: leaf, one child, two children with in-order successor), 4 traversals (in-order, pre-order, post-order, level-order BFS), height, min/max, balance check, BST validation, duplicate handling, ASCII tree visualization |
| [`sorting_algorithms.py`](sorting_algorithms.py) | 7 sorting algorithms with benchmarks | Bubble sort, selection sort, insertion sort, merge sort, quick sort (median-of-three), counting sort, Python Timsort — all with operation counting, benchmarking framework, and complexity reference table |
| [`graph_traversal.py`](graph_traversal.py) | Full graph engine | Adjacency list `Graph` class (directed + undirected + weighted), BFS (standard, shortest path, level-order), DFS (recursive + iterative + all-paths), Dijkstra's shortest weighted path, topological sort (Kahn's), cycle detection (directed: 3-color, undirected: parent-tracking), connected components |

## Complexity Reference

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| BST Search | O(log n) | O(log n) | O(n) | O(1) |
| BFS/DFS | O(V+E) | O(V+E) | O(V+E) | O(V) |
| Dijkstra's | O((V+E) log V) | — | — | O(V) |

## Enterprise Application

- Graph engine used in **Phase 09** for dependency resolution and order routing
- Sorting benchmarks inform database index selection in **Phase 04**
- BST patterns apply to caching and search optimization across the platform
