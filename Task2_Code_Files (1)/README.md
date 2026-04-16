# Task 2 — Self-Study: Heap Data Structure & Heap Sort Algorithm
## COMP2090SEF Course Project | Group 10 | HKMU 2026

---

## Files in This Folder

| File | Description |
|------|-------------|
| `heap.py` | MaxHeap and MinHeap class implementations (OOP) |
| `heap_sort.py` | Heap Sort functions and HeapSorter class |
| `demo.py` | Full demonstration and test runner |
| `generate_report.py` | Script that generates the PDF report |
| `Task2_Study_Report_Heap_HeapSort.pdf` | Final study report (submit this) |
| `README.md` | This file |

---

## How to Run

**Requirements:** Python 3.8 or higher. No external packages needed.

```bash
# Run the full demonstration
python demo.py

# Re-generate the PDF report (requires: pip install reportlab)
python generate_report.py
```

---

## What the Demo Shows

1. MaxHeap — insert, peek, extract_top (gives descending order)
2. MinHeap — same interface, reversed priority (gives ascending order)
3. heapify() — build heap from array in O(n) using Floyd's algorithm
4. heap_sort_verbose() — step-by-step trace of sorting [4, 10, 3, 5, 1]
5. Test cases — already sorted, reverse sorted, all equal, negatives, etc.
6. Heap Sort descending — using MinHeap
7. HeapSorter stats — comparison and swap counts tracked
8. Performance benchmark — n = 10, 100, 1000, 5000, 10000
9. Application — IT support priority queue simulation

---

## OOP Concepts Used

| Concept | Where |
|---------|-------|
| Class & Objects | MaxHeap, MinHeap, HeapSorter |
| Encapsulation | `_data` is private; access via methods only |
| Inheritance | MinHeap extends MaxHeap |
| Polymorphism | `_has_higher_priority()` overridden in MinHeap |
| Class Method | `MaxHeap.from_list()`, `HeapSorter.benchmark()` |
| Static Methods | `_left()`, `_right()`, `_parent()` |
| Magic Methods | `__len__`, `__str__`, `__repr__`, `__contains__` |

---

## Time Complexity Summary

| Operation | Complexity |
|-----------|------------|
| insert() | O(log n) |
| extract_top() | O(log n) |
| peek() | O(1) |
| heapify(array) | O(n) |
| Heap Sort total | O(n log n) — all cases |
| Space | O(1) auxiliary |

---

## GitHub Repository

https://github.com/KUMANAN444/IT-SUPPORT-TICKET-SYSTEM
