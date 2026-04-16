"""
heap.py
Implementation of the Heap data structure (Max-Heap and Min-Heap).

A Heap is a complete binary tree stored as an array where:
  - Max-Heap: every parent node >= its children
  - Min-Heap: every parent node <= its children

Array index relationships for node at index i:
  - Left child  : 2*i + 1
  - Right child : 2*i + 2
  - Parent      : (i - 1) // 2

OOP Concepts Demonstrated:
  - Class and Object          : MaxHeap, MinHeap classes
  - Encapsulation             : _data list is private; methods control access
  - Inheritance               : MinHeap inherits from MaxHeap and overrides comparison
  - Polymorphism              : _has_higher_priority() overridden in MinHeap
  - Magic/Dunder Methods      : __len__, __str__, __repr__, __contains__
  - Class Method / Static     : Heap.from_list() factory method

Time Complexities:
  insert()       : O(log n)
  extract_top()  : O(log n)
  peek()         : O(1)
  heapify_array(): O(n)
  size()         : O(1)

Space Complexity: O(n)
"""


class MaxHeap:
    """
    Max-Heap implementation using an array (list).

    The root always contains the MAXIMUM element.
    Useful for: priority queues, scheduling, graph algorithms.
    """

    def __init__(self):
        """Initialise an empty Max-Heap."""
        self._data = []          # Encapsulated internal storage

    # ── Properties and size ───────────────────────────────────────────────────

    def size(self) -> int:
        """Return the number of elements. O(1)."""
        return len(self._data)

    def is_empty(self) -> bool:
        """Return True if the heap contains no elements."""
        return len(self._data) == 0

    def peek(self):
        """
        Return the top element (maximum for Max-Heap) without removing it.
        Time Complexity: O(1)
        Raises IndexError if the heap is empty.
        """
        if self.is_empty():
            raise IndexError("peek() called on an empty heap")
        return self._data[0]

    # ── Index helpers (array representation) ─────────────────────────────────

    @staticmethod
    def _left(i: int) -> int:
        """Return index of left child of node i."""
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        """Return index of right child of node i."""
        return 2 * i + 2

    @staticmethod
    def _parent(i: int) -> int:
        """Return index of parent of node i."""
        return (i - 1) // 2

    # ── Priority comparison (Polymorphism hook) ───────────────────────────────

    def _has_higher_priority(self, a, b) -> bool:
        """
        Return True if value 'a' should be closer to the root than 'b'.
        Max-Heap: larger value = higher priority.
        Overridden in MinHeap to reverse this logic (Polymorphism).
        """
        return a > b

    # ── Core operations ───────────────────────────────────────────────────────

    def insert(self, value) -> None:
        """
        Insert a new value into the heap.
        Steps: append to end, then sift UP to restore heap property.
        Time Complexity: O(log n)
        """
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def extract_top(self):
        """
        Remove and return the top element (max for Max-Heap, min for Min-Heap).
        Steps: swap root with last element, pop last, then sift DOWN.
        Time Complexity: O(log n)
        Raises IndexError if the heap is empty.
        """
        if self.is_empty():
            raise IndexError("extract_top() called on an empty heap")
        # Swap root with last element
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        # Remove and save the old root (now at the end)
        top = self._data.pop()
        # Restore heap property from the root downwards
        if not self.is_empty():
            self._sift_down(0)
        return top

    def _sift_up(self, i: int) -> None:
        """
        Move element at index i upward until the heap property is satisfied.
        Called after insertion. O(log n) in the worst case.
        """
        while i > 0:
            parent = self._parent(i)
            if self._has_higher_priority(self._data[i], self._data[parent]):
                # Child has higher priority — swap with parent
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break   # Heap property satisfied

    def _sift_down(self, i: int) -> None:
        """
        Move element at index i downward until the heap property is satisfied.
        Called after extraction. O(log n) in the worst case.
        """
        n = len(self._data)
        while True:
            top_idx = i                  # Assume current node is highest-priority
            left  = self._left(i)
            right = self._right(i)

            # Check left child
            if (left < n and
                    self._has_higher_priority(self._data[left], self._data[top_idx])):
                top_idx = left

            # Check right child
            if (right < n and
                    self._has_higher_priority(self._data[right], self._data[top_idx])):
                top_idx = right

            if top_idx == i:
                break   # Node is already in correct position

            # Swap with the higher-priority child
            self._data[i], self._data[top_idx] = self._data[top_idx], self._data[i]
            i = top_idx

    # ── Build heap from existing array ────────────────────────────────────────

    def heapify(self, array: list) -> None:
        """
        Build a heap from an unsorted array IN-PLACE.
        Uses Floyd's algorithm: start from last non-leaf and sift down.
        Time Complexity: O(n)  — more efficient than inserting one-by-one O(n log n)
        """
        self._data = list(array)    # Copy to internal storage
        n = len(self._data)
        # Last non-leaf node is at index n//2 - 1
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    @classmethod
    def from_list(cls, array: list) -> "MaxHeap":
        """
        Class factory method: create a MaxHeap from a list.
        Example: heap = MaxHeap.from_list([3, 1, 4, 1, 5])
        """
        h = cls()
        h.heapify(array)
        return h

    def to_sorted_list(self) -> list:
        """
        Return a sorted list WITHOUT destroying the heap.
        (Uses a copy.) Returns ascending order for Max-Heap.
        """
        import copy
        backup = copy.deepcopy(self)
        result = []
        while not backup.is_empty():
            result.append(backup.extract_top())
        result.reverse()    # Max-Heap gives descending; reverse for ascending
        return result

    # ── Dunder (magic) methods ────────────────────────────────────────────────

    def __len__(self) -> int:
        """Support len(heap)."""
        return len(self._data)

    def __contains__(self, value) -> bool:
        """Support 'x in heap' membership test. O(n)."""
        return value in self._data

    def __str__(self) -> str:
        """Human-readable array representation."""
        return f"{self.__class__.__name__}({self._data})"

    def __repr__(self) -> str:
        """Developer representation."""
        return f"<{self.__class__.__name__} size={len(self._data)} top={self._data[0] if self._data else None}>"

    def get_array(self) -> list:
        """Return a copy of the internal array (read-only access)."""
        return list(self._data)


# ─────────────────────────────────────────────────────────────────────────────
# MinHeap — Inheritance + Polymorphism
# ─────────────────────────────────────────────────────────────────────────────

class MinHeap(MaxHeap):
    """
    Min-Heap: the root always holds the MINIMUM element.
    Inherits all methods from MaxHeap.
    Only overrides _has_higher_priority() to reverse comparison.

    Demonstrates:
      - Inheritance  : MinHeap IS-A MaxHeap (inherits all methods)
      - Polymorphism : _has_higher_priority() behaves differently at runtime
    """

    def _has_higher_priority(self, a, b) -> bool:
        """
        Min-Heap: SMALLER value = higher priority (closer to root).
        Overrides MaxHeap's version. This single change flips all behaviour.
        """
        return a < b        # Reversed comparison
