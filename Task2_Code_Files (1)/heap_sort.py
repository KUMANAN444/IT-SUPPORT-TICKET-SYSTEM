"""
heap_sort.py
Implementation of the Heap Sort algorithm.

Heap Sort works in two phases:
  Phase 1 — Build Max-Heap  : O(n)
  Phase 2 — Extract & Sort  : O(n log n)
  Total                     : O(n log n) in ALL cases (best, average, worst)
  Space                     : O(1) — sorts in-place

This module provides:
  heap_sort(array)             — standard in-place sort (ascending)
  heap_sort_descending(array)  — sort in descending order
  heap_sort_verbose(array)     — sort with step-by-step printed trace
  HeapSorter class             — OOP wrapper with statistics

Time Complexity Analysis:
  - Building the max-heap via Floyd's algorithm : O(n)
  - Each of the n extractions calls heapify     : O(log n) each
  - Total                                       : O(n) + O(n log n) = O(n log n)
  - Unlike Quick Sort, there is NO worst-case O(n²) scenario

Space Complexity: O(1) — no additional array required (in-place)
"""

from heap import MaxHeap, MinHeap


# ─────────────────────────────────────────────────────────────────────────────
# Standalone functions
# ─────────────────────────────────────────────────────────────────────────────

def _heapify_down(array: list, n: int, i: int) -> None:
    """
    Restore the max-heap property for a subtree rooted at index i,
    where n is the size of the active heap portion of the array.
    This is the core sift-down operation used directly on an array.
    Time Complexity: O(log n)
    """
    largest = i          # Assume root is largest
    left    = 2 * i + 1
    right   = 2 * i + 2

    # Is left child larger than root?
    if left < n and array[left] > array[largest]:
        largest = left

    # Is right child larger than current largest?
    if right < n and array[right] > array[largest]:
        largest = right

    # If largest is not the root, swap and continue sifting down
    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        _heapify_down(array, n, largest)    # Recursive call


def heap_sort(array: list) -> list:
    """
    Sort a list in ASCENDING order using Heap Sort.
    The input list is sorted IN-PLACE and also returned.

    Algorithm:
      1. Build a Max-Heap from the array               O(n)
      2. For each element from end to start:
         a. Swap root (max) with last unsorted element  O(1)
         b. Reduce heap size by 1
         c. Restore max-heap property (heapify down)    O(log n)
      Total: O(n log n)

    Args:
        array: List of comparable elements
    Returns:
        The same list, sorted in ascending order
    """
    n = len(array)

    # ── Phase 1: Build Max-Heap ───────────────────────────────────────────────
    # Start from the last non-leaf node (index n//2 - 1) and sift down each
    for i in range(n // 2 - 1, -1, -1):
        _heapify_down(array, n, i)

    # ── Phase 2: Extract elements from heap one by one ───────────────────────
    for i in range(n - 1, 0, -1):
        # Move current root (maximum element) to the end
        array[0], array[i] = array[i], array[0]
        # Restore heap property on the reduced heap (size = i)
        _heapify_down(array, i, 0)

    return array


def heap_sort_descending(array: list) -> list:
    """
    Sort a list in DESCENDING order using a Min-Heap.
    Time Complexity: O(n log n), Space: O(n)

    Args:
        array: List of comparable elements
    Returns:
        New list sorted in descending order
    """
    heap = MinHeap()
    heap.heapify(array)

    result = []
    while not heap.is_empty():
        result.append(heap.extract_top())
    return result


def heap_sort_verbose(array: list) -> list:
    """
    Sort with step-by-step printed trace for educational purposes.
    Shows the array state after each major operation.

    Returns the sorted list.
    """
    arr = list(array)   # Work on a copy
    n = len(arr)
    print(f"Input array : {arr}")
    print(f"Array size  : {n}")
    print()

    # ── Phase 1: Build Max-Heap ───────────────────────────────────────────────
    print("=== Phase 1: Building Max-Heap ===")
    for i in range(n // 2 - 1, -1, -1):
        _heapify_down(arr, n, i)
        print(f"  After heapify at index {i}: {arr}")
    print(f"  Max-Heap built: {arr}")
    print()

    # ── Phase 2: Extract and sort ─────────────────────────────────────────────
    print("=== Phase 2: Extracting Elements ===")
    for i in range(n - 1, 0, -1):
        print(f"  Step {n - i}: Swap arr[0]={arr[0]} with arr[{i}]={arr[i]}")
        arr[0], arr[i] = arr[i], arr[0]
        print(f"           After swap     : {arr}")
        _heapify_down(arr, i, 0)
        print(f"           After heapify  : {arr}")

    print()
    print(f"Sorted array: {arr}")
    return arr


# ─────────────────────────────────────────────────────────────────────────────
# OOP Wrapper: HeapSorter Class
# ─────────────────────────────────────────────────────────────────────────────

class HeapSorter:
    """
    OOP wrapper around the Heap Sort algorithm.
    Tracks statistics: comparison count, swap count, elapsed time.

    Demonstrates:
      - Encapsulation : internal state (counts) hidden behind methods
      - Class method  : HeapSorter.benchmark() for testing
    """

    def __init__(self):
        """Initialise a HeapSorter with zeroed statistics."""
        self._comparisons = 0
        self._swaps       = 0
        self._last_input  = []
        self._last_output = []

    # ── Instrumented sort ─────────────────────────────────────────────────────

    def sort(self, array: list) -> list:
        """
        Sort the array and record statistics.
        Returns the sorted list (input is NOT modified).
        """
        import time
        self._comparisons = 0
        self._swaps       = 0
        arr = list(array)
        self._last_input = list(array)

        start = time.perf_counter()
        self._heap_sort_instrumented(arr)
        elapsed = time.perf_counter() - start

        self._last_output = arr
        self._elapsed = elapsed
        return arr

    def _heapify_down_instrumented(self, arr: list, n: int, i: int) -> None:
        """Heapify with comparison and swap counting."""
        largest = i
        left  = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            self._comparisons += 1
            if arr[left] > arr[largest]:
                largest = left

        if right < n:
            self._comparisons += 1
            if arr[right] > arr[largest]:
                largest = right

        if largest != i:
            self._swaps += 1
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify_down_instrumented(arr, n, largest)

    def _heap_sort_instrumented(self, arr: list) -> None:
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down_instrumented(arr, n, i)
        for i in range(n - 1, 0, -1):
            self._swaps += 1
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify_down_instrumented(arr, i, 0)

    # ── Statistics ────────────────────────────────────────────────────────────

    def get_stats(self) -> dict:
        """Return a dict of statistics from the last sort call."""
        return {
            "comparisons": self._comparisons,
            "swaps":        self._swaps,
            "input_size":  len(self._last_input),
            "elapsed_ms":  round(getattr(self, "_elapsed", 0) * 1000, 4),
        }

    def print_stats(self) -> None:
        """Print statistics for the last sort."""
        s = self.get_stats()
        print(f"HeapSorter Statistics")
        print(f"  Input size   : {s['input_size']}")
        print(f"  Comparisons  : {s['comparisons']}")
        print(f"  Swaps        : {s['swaps']}")
        print(f"  Time elapsed : {s['elapsed_ms']} ms")

    # ── Class method for benchmarking ─────────────────────────────────────────

    @classmethod
    def benchmark(cls, sizes: list) -> None:
        """
        Class method: run and print benchmark across multiple input sizes.
        Example: HeapSorter.benchmark([100, 1000, 10000])
        """
        import random
        sorter = cls()
        print(f"{'Size':>8}  {'Comparisons':>12}  {'Swaps':>8}  {'Time (ms)':>10}")
        print("-" * 46)
        for size in sizes:
            data = [random.randint(0, size * 10) for _ in range(size)]
            sorter.sort(data)
            s = sorter.get_stats()
            print(f"{s['input_size']:>8}  {s['comparisons']:>12}  "
                  f"{s['swaps']:>8}  {s['elapsed_ms']:>10}")

    # ── Dunder methods ────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"<HeapSorter last_sort_size={len(self._last_input)}>"

    def __str__(self) -> str:
        s = self.get_stats()
        return (f"HeapSorter(size={s['input_size']}, "
                f"comparisons={s['comparisons']}, swaps={s['swaps']})")
