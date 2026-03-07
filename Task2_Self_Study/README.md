# Task 2: Self-Study on New Data Structure & Algorithm

## Chosen Topics
- **Data Structure:** Heap
- **Algorithm:** Heap Sort

## Why These Topics?
Our IT Support Ticket System handles tickets with different priorities (P1, P2, P3, P4). A Heap allows us to always access the highest priority ticket first. Heap Sort helps generate sorted reports.

## Key Points
- **Heap:** A tree-based structure where parent has higher priority than children
- **Heap Sort:** Uses heap to sort items in O(n log n) time

## Time Complexity
| Operation | Complexity |
| :--- | :--- |
| Insert | O(log n) |
| Get highest priority | O(1) |
| Delete highest | O(log n) |
| Heap Sort | O(n log n) |

## How We Use It
1. Store incoming tickets in a Max-Heap (P1 at top)
2. Engineers always get highest priority ticket
3. Heap Sort generates priority-sorted reports for Admin

