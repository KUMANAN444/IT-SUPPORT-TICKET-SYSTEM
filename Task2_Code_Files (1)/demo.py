"""
demo.py
Demonstration and test script for Heap Data Structure and Heap Sort.

Run with: python demo.py

This script shows:
  1. MaxHeap operations (insert, peek, extract_top)
  2. MinHeap operations (inherits from MaxHeap, polymorphism)
  3. Heap Sort step-by-step trace
  4. Performance benchmark across sizes
  5. Applications: Priority Queue simulation
"""

from heap import MaxHeap, MinHeap
from heap_sort import heap_sort, heap_sort_descending, heap_sort_verbose, HeapSorter


def separator(title: str):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# 1. MaxHeap demonstration
# ─────────────────────────────────────────────────────────────────────────────

separator("1. MaxHeap — Basic Operations")

max_heap = MaxHeap()
print(f"Empty heap: {max_heap}")
print(f"Is empty  : {max_heap.is_empty()}")

# Insert values
for v in [4, 10, 3, 5, 1, 7, 8]:
    max_heap.insert(v)
    print(f"  insert({v:2d})  -> heap: {max_heap.get_array()}")

print(f"\nAfter inserting [4, 10, 3, 5, 1, 7, 8]:")
print(f"  Internal array : {max_heap.get_array()}")
print(f"  Size           : {len(max_heap)}")
print(f"  Peek (max)     : {max_heap.peek()}")
print(f"  10 in heap     : {10 in max_heap}")
print(f"  99 in heap     : {99 in max_heap}")

print("\nExtracting all elements (descending order):")
extracted = []
while not max_heap.is_empty():
    val = max_heap.extract_top()
    extracted.append(val)
    print(f"  extract_top() = {val}  | remaining: {max_heap.get_array()}")
print(f"Extracted order: {extracted}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. MinHeap demonstration
# ─────────────────────────────────────────────────────────────────────────────

separator("2. MinHeap — Polymorphism (same code, reversed priority)")

min_heap = MinHeap()
for v in [4, 10, 3, 5, 1, 7, 8]:
    min_heap.insert(v)

print(f"MinHeap array  : {min_heap.get_array()}")
print(f"Peek (min)     : {min_heap.peek()}")
print("Extracting all (ascending order):")
extracted_min = []
while not min_heap.is_empty():
    extracted_min.append(min_heap.extract_top())
print(f"Extracted order: {extracted_min}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. heapify() — Build from array O(n)
# ─────────────────────────────────────────────────────────────────────────────

separator("3. heapify() — Build heap from array in O(n)")

data = [4, 10, 3, 5, 1]
print(f"Input array : {data}")
h = MaxHeap.from_list(data)
print(f"Max-Heap    : {h.get_array()}")
print(f"(Note: the array is rearranged to satisfy the heap property,")
print(f" it is NOT fully sorted — sorting happens during extraction)")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Heap Sort — Step-by-step trace
# ─────────────────────────────────────────────────────────────────────────────

separator("4. Heap Sort — Step-by-Step Trace")
result = heap_sort_verbose([4, 10, 3, 5, 1])


# ─────────────────────────────────────────────────────────────────────────────
# 5. Heap Sort — Various test cases
# ─────────────────────────────────────────────────────────────────────────────

separator("5. Heap Sort — Test Cases")

test_cases = [
    ("Already sorted",   [1, 2, 3, 4, 5]),
    ("Reverse sorted",   [5, 4, 3, 2, 1]),
    ("All equal",        [3, 3, 3, 3, 3]),
    ("Single element",   [42]),
    ("Two elements",     [9, 1]),
    ("Random 10",        [64, 25, 12, 22, 11, 45, 33, 7, 88, 3]),
    ("Negative numbers", [-5, 3, -1, 0, -8, 2]),
]

for name, arr in test_cases:
    original = list(arr)
    sorted_arr = heap_sort(arr)
    check = sorted_arr == sorted(original)
    print(f"  {name:<20}: {str(original):<35} -> {sorted_arr}  [{'PASS' if check else 'FAIL'}]")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Descending sort
# ─────────────────────────────────────────────────────────────────────────────

separator("6. Heap Sort Descending")
arr = [4, 10, 3, 5, 1, 7]
desc = heap_sort_descending(list(arr))
print(f"Input      : {arr}")
print(f"Descending : {desc}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. HeapSorter statistics
# ─────────────────────────────────────────────────────────────────────────────

separator("7. HeapSorter — Statistics Tracking")

sorter = HeapSorter()
data = [64, 25, 12, 22, 11, 45, 33, 7, 88, 3]
result = sorter.sort(data)
print(f"Input  : {data}")
print(f"Output : {result}")
sorter.print_stats()


# ─────────────────────────────────────────────────────────────────────────────
# 8. Performance benchmark
# ─────────────────────────────────────────────────────────────────────────────

separator("8. Performance Benchmark")
HeapSorter.benchmark([10, 100, 1000, 5000, 10000])


# ─────────────────────────────────────────────────────────────────────────────
# 9. Application: Priority Queue Simulation
# ─────────────────────────────────────────────────────────────────────────────

separator("9. Application: IT Support Priority Queue")

print("Simulating IT ticket priority queue (higher number = higher urgency)")
print()
ticket_heap = MaxHeap()
tickets = [
    (3, "Outlook not working"),
    (5, "Server down — CRITICAL"),
    (1, "Password reset request"),
    (4, "VPN connectivity issue"),
    (2, "Printer paper jam"),
    (5, "Database unreachable"),
]

for priority, description in tickets:
    ticket_heap.insert((priority, description))
    print(f"  Added  : Priority {priority} — {description}")

print(f"\nProcessing tickets in priority order:")
while not ticket_heap.is_empty():
    priority, desc = ticket_heap.extract_top()
    print(f"  HANDLE : Priority {priority} — {desc}")


print()
print("=" * 60)
print("  All demonstrations complete.")
print("=" * 60)
