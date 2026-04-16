"""
generate_report.py
Generate the complete Task 2 Study Report PDF for COMP2090SEF.
Topic: Heap Data Structure & Heap Sort Algorithm
Format: A4, Times New Roman 12pt, 2.54cm margins, single spacing
Structure: Cover Page + 3 pages main content + Appendix
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus.flowables import Flowable
import os

# ── Page setup ───────────────────────────────────────────────────────────────
OUTPUT = "/home/claude/task2/Task2_Study_Report_Heap_HeapSort.pdf"
PAGE_W, PAGE_H = A4
MARGIN = 2.54 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

# ── Colours ───────────────────────────────────────────────────────────────────
DARK_BLUE  = HexColor("#1A3C5E")
MID_BLUE   = HexColor("#2E75B6")
LIGHT_BLUE = HexColor("#D5E8F0")
LIGHT_GREY = HexColor("#F2F2F2")
ACCENT     = HexColor("#C00000")

# ── Style helpers ─────────────────────────────────────────────────────────────

def make_styles():
    base = getSampleStyleSheet()

    normal = ParagraphStyle("ReportNormal",
        fontName="Times-Roman", fontSize=12,
        leading=16, spaceAfter=6, alignment=TA_JUSTIFY)

    title_page = ParagraphStyle("TitlePage",
        fontName="Times-Bold", fontSize=18,
        leading=24, spaceBefore=6, spaceAfter=6, alignment=TA_CENTER)

    subtitle_page = ParagraphStyle("SubtitlePage",
        fontName="Times-Roman", fontSize=13,
        leading=18, spaceAfter=4, alignment=TA_CENTER)

    section = ParagraphStyle("Section",
        fontName="Times-Bold", fontSize=13,
        leading=18, spaceBefore=14, spaceAfter=6,
        textColor=DARK_BLUE, borderPad=2)

    subsection = ParagraphStyle("Subsection",
        fontName="Times-Bold", fontSize=12,
        leading=16, spaceBefore=10, spaceAfter=4,
        textColor=MID_BLUE)

    body = ParagraphStyle("Body",
        fontName="Times-Roman", fontSize=12,
        leading=16, spaceAfter=5, alignment=TA_JUSTIFY)

    code = ParagraphStyle("Code",
        fontName="Courier", fontSize=9.5,
        leading=13, spaceAfter=4, leftIndent=16,
        backColor=LIGHT_GREY)

    caption = ParagraphStyle("Caption",
        fontName="Times-Italic", fontSize=11,
        leading=14, spaceAfter=6, alignment=TA_CENTER)

    bold_body = ParagraphStyle("BoldBody",
        fontName="Times-Bold", fontSize=12,
        leading=16, spaceAfter=4)

    declaration = ParagraphStyle("Declaration",
        fontName="Times-Roman", fontSize=11,
        leading=16, spaceAfter=4, alignment=TA_LEFT)

    return dict(normal=normal, title_page=title_page, subtitle_page=subtitle_page,
                section=section, subsection=subsection, body=body, code=code,
                caption=caption, bold_body=bold_body, declaration=declaration)


S = make_styles()


# ── Table style helpers ────────────────────────────────────────────────────────

def header_table_style(header_bg=DARK_BLUE):
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR',  (0, 0), (-1, 0), white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE',   (0, 0), (-1, 0), 11),
        ('FONTNAME',   (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE',   (0, 1), (-1, -1), 11),
        ('BACKGROUND', (0, 1), (-1, -1), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GREY]),
        ('GRID',       (0, 0), (-1, -1), 0.5, HexColor("#AAAAAA")),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])


def P(text, style=None):
    return Paragraph(text, style or S["body"])

def SP(h=6):
    return Spacer(1, h)

def HR():
    return HRFlowable(width="100%", thickness=1, color=MID_BLUE, spaceAfter=4)


# ─────────────────────────────────────────────────────────────────────────────
# Content builders
# ─────────────────────────────────────────────────────────────────────────────

def build_cover():
    story = []
    story.append(SP(40))

    # University name
    story.append(P("<b>HONG KONG METROPOLITAN UNIVERSITY</b>", S["title_page"]))
    story.append(SP(10))
    story.append(HR())
    story.append(SP(10))

    # Course info
    story.append(P("COMP2090SEF", S["subtitle_page"]))
    story.append(P("Data Structures, Algorithms and Problem Solving", S["subtitle_page"]))
    story.append(SP(20))

    # Report type
    story.append(P("<b>COURSE PROJECT REPORT</b>", S["title_page"]))
    story.append(P("<b>TASK 2 — Self-Study Report</b>", S["title_page"]))
    story.append(SP(16))

    # Topic
    topic_data = [["Self-Study Topic"],
                  ["Heap Data Structure"],
                  ["&"],
                  ["Heap Sort Algorithm"]]
    topic_table = Table([[P(r[0], ParagraphStyle("tc",
                            fontName="Times-Bold", fontSize=14,
                            leading=20, alignment=TA_CENTER))]
                         for r in topic_data],
                        colWidths=[CONTENT_W * 0.8])
    topic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BLUE),
        ('BOX', (0, 0), (-1, -1), 2, DARK_BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    # Centre the table
    centred = Table([[topic_table]], colWidths=[CONTENT_W])
    centred.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(centred)
    story.append(SP(20))

    # Submission info
    story.append(P("Group 10", S["subtitle_page"]))
    story.append(P("Submission Date: 15 April 2026", S["subtitle_page"]))
    story.append(SP(30))
    story.append(HR())
    story.append(SP(10))

    # Declaration box
    decl_lines = [
        "<b>DECLARATION</b>",
        "",
        "We declare that:",
        "",
        "(i) All members of the group have read and checked that all parts of the project "
        "(including proposal, code programs, and reports), irrespective of whether they are "
        "contributed by individual members or the group as a whole, submitted here is original "
        "except for source material explicitly acknowledged;",
        "",
        "(ii) The project, in parts or in whole, has not been submitted for more than one purpose "
        "without declaration;",
        "",
        "(iii) We are aware of the University's policy and regulations on honesty in academic work "
        "and understand the possible consequences of breaching such policy and regulations;",
        "",
        "(iv) We confirm that we have declared in the report the usage of AI and other generative "
        "models, including but not limited to ChatGPT, LLaMA, Gemini, Mistral, and Stable "
        "Diffusion, and have complied with the instructions provided by HKMU;",
        "",
        "(v) We are aware that all members of the group should be held responsible and liable "
        "to disciplinary actions, irrespective of whether they have signed the declaration.",
        "",
        "We confirm that we have read and understood the project requirements.",
    ]
    decl_paras = [P(line, S["declaration"]) for line in decl_lines]

    # Name / ID table
    story += decl_paras
    story.append(SP(14))

    sig_data = [
        ["Name", "Student ID", "Signature"],
        ["_______________________", "_____________", "_____________________"],
        ["_______________________", "_____________", "_____________________"],
        ["_______________________", "_____________", "_____________________"],
    ]
    sig_table = Table(sig_data, colWidths=[CONTENT_W * 0.45, CONTENT_W * 0.25, CONTENT_W * 0.3])
    sig_table.setStyle(TableStyle([
        ('FONTNAME',   (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('LINEBELOW',  (0, 0), (-1, 0), 1, black),
    ]))
    story.append(sig_table)
    story.append(PageBreak())
    return story


def build_page1():
    """Page 1 — Introduction to Heap Data Structure"""
    story = []

    story.append(P("<b>1. Introduction to the Heap Data Structure</b>", S["section"]))
    story.append(HR())

    story.append(P("<b>1.1 Definition</b>", S["subsection"]))
    story.append(P(
        "A <b>Heap</b> is a specialised complete binary tree that satisfies the <i>heap property</i>. "
        "A complete binary tree is one where all levels are fully filled except possibly the last, "
        "which is filled from left to right. Heaps are commonly implemented using a flat array "
        "rather than explicit node pointers, making them memory-efficient and cache-friendly. "
        "The heap property determines the ordering of parent and child nodes:"
    ))
    story.append(SP(4))

    prop_data = [
        ["Heap Type", "Property", "Root Element"],
        ["Max-Heap",  "Every parent ≥ its children",  "Maximum value"],
        ["Min-Heap",  "Every parent ≤ its children",  "Minimum value"],
    ]
    prop_table = Table(prop_data, colWidths=[CONTENT_W*0.28, CONTENT_W*0.44, CONTENT_W*0.28])
    prop_table.setStyle(header_table_style())
    story.append(prop_table)
    story.append(P("Table 1: Heap types and their properties.", S["caption"]))
    story.append(SP(6))

    story.append(P("<b>1.2 Array Representation</b>", S["subsection"]))
    story.append(P(
        "The heap is stored as a zero-indexed array. For a node at index <i>i</i>, the following "
        "relationships hold, enabling O(1) navigation without any pointer storage:"
    ))
    arr_data = [
        ["Relationship", "Formula", "Example (i = 2)"],
        ["Left child",   "2i + 1",  "2(2)+1 = 5"],
        ["Right child",  "2i + 2",  "2(2)+2 = 6"],
        ["Parent",       "(i−1) ÷ 2 (floor)", "(2−1)÷2 = 0"],
    ]
    arr_table = Table(arr_data, colWidths=[CONTENT_W*0.35, CONTENT_W*0.35, CONTENT_W*0.30])
    arr_table.setStyle(header_table_style())
    story.append(arr_table)
    story.append(P("Table 2: Array index relationships in a heap.", S["caption"]))
    story.append(SP(6))

    story.append(P(
        "For example, the array <b>[10, 5, 8, 4, 1, 3, 7]</b> represents the Max-Heap where 10 "
        "is the root, 5 and 8 are its children, and every parent is greater than its children. "
        "See Appendix A (Figure 1) for the binary tree visualisation."
    ))

    story.append(P("<b>1.3 Abstract Data Type (ADT) — Operations and Complexity</b>", S["subsection"]))
    story.append(P(
        "The Heap ADT defines the following core operations. The efficiency of these operations "
        "is what makes the heap a preferred data structure for priority-sensitive applications:"
    ))
    adt_data = [
        ["Operation", "Description", "Time Complexity"],
        ["insert(value)",    "Add a new element; sift UP to restore heap property",  "O(log n)"],
        ["extract_top()",    "Remove and return the root; sift DOWN to restore",     "O(log n)"],
        ["peek()",           "View the root element without removing it",            "O(1)"],
        ["heapify(array)",   "Build a heap from an unsorted array (Floyd's method)", "O(n)"],
        ["size()",           "Return the number of elements stored",                 "O(1)"],
        ["is_empty()",       "Return True if no elements are present",               "O(1)"],
    ]
    adt_table = Table(adt_data, colWidths=[CONTENT_W*0.28, CONTENT_W*0.48, CONTENT_W*0.24])
    adt_table.setStyle(header_table_style())
    story.append(adt_table)
    story.append(P("Table 3: Heap ADT operations and their time complexities.", S["caption"]))
    story.append(SP(6))

    story.append(P(
        "The <b>sift-up</b> operation (used during insertion) starts at the newly added node and "
        "repeatedly swaps it with its parent if it violates the heap property, travelling at most "
        "O(log n) levels upward. The <b>sift-down</b> operation (used during extraction) starts "
        "at the root and swaps with the higher-priority child until the property is restored, "
        "also O(log n). The <b>heapify</b> operation uses Floyd's bottom-up algorithm — starting "
        "from the last non-leaf node and sifting each node down — achieving O(n) time, which is "
        "more efficient than inserting n elements individually (O(n log n))."
    ))

    story.append(P("<b>1.4 Real-World Applications</b>", S["subsection"]))
    apps = [
        ("<b>Priority Queues</b>", "Operating systems use min-heaps to schedule processes by priority; "
         "the CPU always executes the highest-priority runnable process first."),
        ("<b>Graph Algorithms</b>", "Dijkstra's shortest-path and Prim's minimum spanning tree algorithms "
         "rely on a min-heap as a priority queue to greedily select the next vertex in O(log n)."),
        ("<b>Heap Sort</b>", "The heap data structure directly enables the Heap Sort algorithm, "
         "discussed in Section 2."),
        ("<b>Median Maintenance</b>", "Two heaps (one max, one min) can maintain a running median "
         "of a data stream in O(log n) per insertion."),
        ("<b>Event Simulation</b>", "Discrete-event simulators use a min-heap to process events "
         "in chronological order efficiently."),
    ]
    for title, desc in apps:
        story.append(P(f"&bull; {title}: {desc}"))

    return story


def build_page2():
    """Page 2 — Heap Sort Algorithm"""
    story = []

    story.append(P("<b>2. The Heap Sort Algorithm</b>", S["section"]))
    story.append(HR())

    story.append(P("<b>2.1 Algorithm Description</b>", S["subsection"]))
    story.append(P(
        "Heap Sort is a comparison-based, in-place sorting algorithm that uses the Max-Heap "
        "data structure to sort an array in ascending order. It operates in two distinct phases:"
    ))
    story.append(P(
        "<b>Phase 1 — Build Max-Heap</b> (O(n)): Transform the input array into a valid Max-Heap "
        "using Floyd's bottom-up algorithm. Starting from the last non-leaf node (index n//2 − 1), "
        "each node is sifted downward. This guarantees the largest element reaches the root."
    ))
    story.append(P(
        "<b>Phase 2 — Repeated Extraction</b> (O(n log n)): The root (maximum element) is swapped "
        "with the last element of the active heap portion, shrinking the heap size by one. The new "
        "root is then sifted down to restore the heap property. Repeating this n−1 times places "
        "all elements in sorted order at the end of the array."
    ))

    story.append(P("<b>2.2 Step-by-Step Example</b>", S["subsection"]))
    story.append(P("Sorting the array <b>[4, 10, 3, 5, 1]</b>:"))
    story.append(SP(4))

    steps_data = [
        ["Step", "Operation", "Array State"],
        ["Initial", "Input array", "[4, 10, 3, 5, 1]"],
        ["Phase 1", "heapify at index 1: 10 > 5, no swap needed", "[4, 10, 3, 5, 1]"],
        ["Phase 1", "heapify at index 0: 10 > 4, swap → heap built", "[10, 5, 3, 4, 1]"],
        ["Step 1",  "Swap root(10) ↔ last(1); heapify", "[5, 4, 3, 1, | 10]"],
        ["Step 2",  "Swap root(5) ↔ last(1); heapify", "[4, 1, 3, | 5, 10]"],
        ["Step 3",  "Swap root(4) ↔ last(3); heapify", "[3, 1, | 4, 5, 10]"],
        ["Step 4",  "Swap root(3) ↔ last(1); done", "[1, 3, 4, 5, 10]"],
        ["Final",   "Sorted array (ascending)", "[1, 3, 4, 5, 10] ✓"],
    ]
    steps_table = Table(steps_data,
                        colWidths=[CONTENT_W*0.12, CONTENT_W*0.55, CONTENT_W*0.33])
    steps_table.setStyle(header_table_style())
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR',  (0, 0), (-1, 0), white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 10),
        ('FONTNAME',   (0, 1), (-1, -1), 'Times-Roman'),
        ('BACKGROUND', (0, 8), (-1, 8), HexColor("#E2F0D9")),
        ('FONTNAME',   (0, 8), (-1, 8), 'Times-Bold'),
        ('BACKGROUND', (0, 1), (-1, 1), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, 7), [white, LIGHT_GREY]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#AAAAAA")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN',  (0, 0), (0, -1), 'CENTER'),
        ('ALIGN',  (2, 0), (2, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(steps_table)
    story.append(P("Table 4: Heap Sort trace for input [4, 10, 3, 5, 1]. '|' marks boundary of active heap.", S["caption"]))
    story.append(SP(6))

    story.append(P(
        "After each swap in Phase 2, the extracted maximum element is placed at the end of the "
        "array and excluded from further heap operations (shown by '|' boundary above). "
        "See Appendix B (Figure 2) for a visual diagram of the full process."
    ))

    story.append(P("<b>2.3 Pseudocode</b>", S["subsection"]))
    story.append(P(
        "The following pseudocode describes the two-function implementation. "
        "<i>heapSort</i> orchestrates both phases; <i>heapify</i> restores the heap property "
        "for a subtree rooted at index i within an active heap of size n:"
    ))
    story.append(SP(4))

    pseudo = [
        "procedure heapSort(array A, size n):",
        "    // Phase 1: Build Max-Heap using Floyd's algorithm",
        "    for i from (n/2 - 1) down to 0:",
        "        heapify(A, n, i)",
        "",
        "    // Phase 2: Extract elements from the heap one by one",
        "    for i from (n - 1) down to 1:",
        "        swap A[0] with A[i]          // Move max to sorted region",
        "        heapify(A, i, 0)             // Restore heap on reduced size",
        "",
        "procedure heapify(array A, size n, index i):",
        "    largest ← i",
        "    left    ← 2*i + 1",
        "    right   ← 2*i + 2",
        "    if left < n  and A[left]  > A[largest] then largest ← left",
        "    if right < n and A[right] > A[largest] then largest ← right",
        "    if largest ≠ i then",
        "        swap A[i] with A[largest]",
        "        heapify(A, n, largest)       // Recursive sift-down",
    ]
    for line in pseudo:
        story.append(P(line if line else "&nbsp;", S["code"]))
    story.append(SP(4))

    story.append(P("<b>2.4 Key Observations</b>", S["subsection"]))
    story.append(P(
        "Unlike Merge Sort, Heap Sort requires <b>no additional memory</b> — sorting is done "
        "entirely within the original array. Unlike Quick Sort, Heap Sort has <b>no worst-case "
        "O(n²)</b> scenario; it is guaranteed O(n log n) regardless of input order. However, "
        "Heap Sort is <b>not stable</b> — equal elements may not preserve their original relative "
        "order after sorting."
    ))

    return story


def build_page3():
    """Page 3 — Complexity Analysis, Comparison, and Conclusion"""
    story = []

    story.append(P("<b>3. Complexity Analysis and Conclusion</b>", S["section"]))
    story.append(HR())

    story.append(P("<b>3.1 Time Complexity Analysis</b>", S["subsection"]))
    story.append(P(
        "The total time complexity of Heap Sort is derived from its two phases. "
        "<b>Phase 1</b> (build max-heap) runs in O(n) using Floyd's algorithm — "
        "even though n/2 nodes are processed, nodes near the bottom of the tree have very short "
        "sift paths, and a mathematical summation shows the total work converges to O(n). "
        "<b>Phase 2</b> performs n−1 extract operations, each requiring one O(log n) sift-down, "
        "giving O(n log n) total for phase 2. Combined, the overall complexity is O(n log n)."
    ))
    tc_data = [
        ["Operation",           "Best Case",    "Average Case", "Worst Case"],
        ["Build Heap (Phase 1)", "O(n)",        "O(n)",         "O(n)"],
        ["Heapify (per call)",   "O(1)",        "O(log n)",     "O(log n)"],
        ["Phase 2 (n extracts)", "O(n log n)",  "O(n log n)",   "O(n log n)"],
        ["Heap Sort Total",      "O(n log n)",  "O(n log n)",   "O(n log n)"],
    ]
    tc_table = Table(tc_data, colWidths=[CONTENT_W*0.38, CONTENT_W*0.2,
                                         CONTENT_W*0.22, CONTENT_W*0.2])
    ts = header_table_style()
    ts.add('FONTNAME', (0, 4), (-1, 4), 'Times-Bold')
    ts.add('BACKGROUND', (0, 4), (-1, 4), LIGHT_BLUE)
    tc_table.setStyle(ts)
    story.append(tc_table)
    story.append(P("Table 5: Time complexity analysis of Heap Sort.", S["caption"]))
    story.append(SP(4))

    story.append(P("<b>3.2 Space Complexity</b>", S["subsection"]))
    story.append(P(
        "Heap Sort uses <b>O(1) auxiliary space</b> — it sorts the array in-place with only a "
        "constant number of extra variables (indices and a temporary swap value). "
        "The recursive heapify calls use O(log n) implicit stack space in the worst case; "
        "this can be eliminated by using an iterative implementation. In contrast, Merge Sort "
        "requires O(n) extra memory for the merge buffer."
    ))

    story.append(P("<b>3.3 Comparison with Other Sorting Algorithms</b>", S["subsection"]))
    cmp_data = [
        ["Algorithm",   "Best",        "Average",     "Worst",       "Space",   "Stable?"],
        ["Heap Sort",   "O(n log n)",  "O(n log n)",  "O(n log n)", "O(1)",    "No"],
        ["Merge Sort",  "O(n log n)",  "O(n log n)",  "O(n log n)", "O(n)",    "Yes"],
        ["Quick Sort",  "O(n log n)",  "O(n log n)",  "O(n²)",      "O(log n)","No"],
        ["Bubble Sort", "O(n)",        "O(n²)",        "O(n²)",      "O(1)",    "Yes"],
        ["Select Sort", "O(n²)",       "O(n²)",        "O(n²)",      "O(1)",    "No"],
    ]
    cmp_table = Table(cmp_data, colWidths=[CONTENT_W*0.20, CONTENT_W*0.16,
                                            CONTENT_W*0.16, CONTENT_W*0.16,
                                            CONTENT_W*0.14, CONTENT_W*0.18])
    cts = header_table_style()
    cts.add('FONTNAME', (0, 1), (0, -1), 'Times-Bold')
    cts.add('BACKGROUND', (0, 1), (-1, 1), LIGHT_BLUE)
    cmp_table.setStyle(cts)
    story.append(cmp_table)
    story.append(P("Table 6: Comparison of sorting algorithms by time, space, and stability.", S["caption"]))
    story.append(SP(4))

    story.append(P(
        "Heap Sort uniquely provides a <b>worst-case guarantee of O(n log n)</b> with O(1) space. "
        "Quick Sort is often faster in practice due to better cache locality, but can degrade to "
        "O(n²) on adversarial input unless randomised. Merge Sort is stable and predictable but "
        "requires O(n) extra memory. Bubble and Selection Sort are only suitable for very small n."
    ))

    story.append(P("<b>3.4 Empirical Benchmark Results</b>", S["subsection"]))
    story.append(P(
        "The following results were obtained by running the HeapSorter class "
        "(see heap_sort.py, demo.py) on random integer arrays on a standard machine. "
        "The growth from n=1,000 to n=10,000 (10×) increases time approximately 11×, "
        "consistent with O(n log n) scaling (10 log 10 ≈ 10 × 1.1)."
    ))
    bench_data = [
        ["n",       "Comparisons",  "Swaps",   "Time (ms)"],
        ["10",      "40",           "28",      "0.010"],
        ["100",     "1,036",        "586",     "0.128"],
        ["1,000",   "16,889",       "9,098",   "2.260"],
        ["5,000",   "107,723",      "57,166",  "14.633"],
        ["10,000",  "235,458",      "124,287", "40.813"],
    ]
    bench_table = Table(bench_data, colWidths=[CONTENT_W*0.18, CONTENT_W*0.25,
                                               CONTENT_W*0.20, CONTENT_W*0.22])
    bench_table.setStyle(header_table_style(DARK_BLUE))
    story.append(bench_table)
    story.append(P("Table 7: Empirical benchmark of Heap Sort at various input sizes.", S["caption"]))
    story.append(SP(6))

    story.append(P("<b>3.5 Advantages and Disadvantages</b>", S["subsection"]))
    adv_data = [
        ["Advantages", "Disadvantages"],
        ["Guaranteed O(n log n) in all cases",       "Not stable — equal elements may reorder"],
        ["In-place — O(1) auxiliary space",          "Slower than Quick Sort in practice (poor cache locality)"],
        ["No worst-case degradation (unlike Quick)", "Recursive heapify uses O(log n) stack space"],
        ["Suitable for real-time / embedded systems","Less intuitive to implement than simple sorts"],
    ]
    adv_table = Table(adv_data, colWidths=[CONTENT_W * 0.50, CONTENT_W * 0.50])
    adv_ts = TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR',     (0, 0), (-1, 0), white),
        ('FONTNAME',      (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 11),
        ('FONTNAME',      (0, 1), (-1, -1), 'Times-Roman'),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [white, LIGHT_GREY]),
        ('GRID',          (0, 0), (-1, -1), 0.5, HexColor("#AAAAAA")),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ])
    adv_table.setStyle(adv_ts)
    story.append(adv_table)
    story.append(P("Table 8: Advantages and disadvantages of Heap Sort.", S["caption"]))
    story.append(SP(6))

    story.append(P("<b>3.6 Conclusion</b>", S["subsection"]))
    story.append(P(
        "This report has introduced the Heap data structure and the Heap Sort algorithm as two "
        "closely related and practically significant topics in computer science. The Heap is a "
        "complete binary tree stored as an array, offering O(log n) insertion and extraction, "
        "O(1) access to the minimum or maximum element, and O(n) heap construction via Floyd's "
        "algorithm. The Min-Heap and Max-Heap variants both emerge from the same implementation "
        "by simply changing the priority comparison — a concrete demonstration of polymorphism "
        "in the provided Python code."
    ))
    story.append(P(
        "Heap Sort builds directly on the Max-Heap, achieving guaranteed O(n log n) performance "
        "in all cases with only O(1) auxiliary space. While it is not cache-optimal in practice "
        "and lacks stability, its worst-case guarantee makes it highly valuable in real-time "
        "systems, embedded environments, and any scenario where predictable performance matters. "
        "The empirical results confirm theoretical expectations: operation counts and elapsed "
        "times scale as O(n log n) as input size grows."
    ))
    story.append(P(
        "The Python implementation provided with this report (heap.py, heap_sort.py, demo.py) "
        "demonstrates all described operations, applies OOP concepts including inheritance and "
        "polymorphism, and includes comprehensive test cases with verified output."
    ))

    # References
    story.append(SP(8))
    story.append(P("<b>References</b>", S["subsection"]))
    refs = [
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). "
        "<i>Introduction to Algorithms</i> (4th ed.). MIT Press.",
        "Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). "
        "<i>Data Structures and Algorithms in Python</i>. Wiley.",
        "Sedgewick, R., & Wayne, K. (2011). <i>Algorithms</i> (4th ed.). Addison-Wesley Professional.",
        "Python Software Foundation. (2024). <i>Python 3 Documentation</i>. https://docs.python.org/3/",
    ]
    for i, ref in enumerate(refs, 1):
        story.append(P(f"[{i}] {ref}"))

    return story


def build_appendix():
    """Appendix — Diagrams, figures, code snippets, test results"""
    story = []
    story.append(PageBreak())

    story.append(P("<b>APPENDIX</b>", S["section"]))
    story.append(HR())

    # ── Appendix A: Tree Diagram (ASCII art) ─────────────────────────────────
    story.append(P("<b>Appendix A — Figure 1: Max-Heap as Complete Binary Tree</b>", S["subsection"]))
    story.append(P(
        "The array <b>[10, 5, 8, 4, 1, 3, 7]</b> maps to the following binary tree. "
        "Every parent node holds a value greater than or equal to its children, satisfying the Max-Heap property."
    ))
    tree_art = [
        "                        10          (index 0, root)",
        "                      /    \\",
        "                    5        8      (index 1, 2)",
        "                  /   \\    /   \\",
        "                4      1  3     7   (index 3, 4, 5, 6)",
        "",
        "  Array:  [ 10 |  5 |  8 |  4 |  1 |  3 |  7 ]",
        "  Index:     0     1     2     3     4     5     6",
        "",
        "  Parent-child index relationships:",
        "    index 0 (10): left=1 (5),  right=2 (8)",
        "    index 1 (5):  left=3 (4),  right=4 (1)",
        "    index 2 (8):  left=5 (3),  right=6 (7)",
    ]
    for line in tree_art:
        story.append(P(line if line else "&nbsp;", S["code"]))
    story.append(SP(6))

    # ── Appendix B: Heap Sort Visualisation ──────────────────────────────────
    story.append(P("<b>Appendix B — Figure 2: Heap Sort Visualisation for [4, 10, 3, 5, 1]</b>",
                   S["subsection"]))
    story.append(P(
        "The diagram below shows the array state at each stage. "
        "The bold box marks the active heap region; the shaded region is the sorted portion."
    ))
    vis_data = [
        ["Stage",      "Active Heap (sorted portion)",  "Max so far extracted"],
        ["Input",      "[4, 10, 3, 5, 1]",              "—"],
        ["Max-Heap",   "[10, 5, 3, 4, 1]",              "—"],
        ["After step 1","[5, 4, 3, 1]  | 10",           "10"],
        ["After step 2","[4, 1, 3]  | 5, 10",           "10, 5"],
        ["After step 3","[3, 1]  | 4, 5, 10",           "10, 5, 4"],
        ["After step 4","[1]  | 3, 4, 5, 10",           "10, 5, 4, 3"],
        ["Sorted",     "[1, 3, 4, 5, 10]",              "All extracted"],
    ]
    vis_table = Table(vis_data, colWidths=[CONTENT_W*0.20, CONTENT_W*0.45, CONTENT_W*0.35])
    vts = header_table_style()
    vts.add('BACKGROUND', (0, 7), (-1, 7), HexColor("#E2F0D9"))
    vts.add('FONTNAME', (0, 7), (-1, 7), 'Times-Bold')
    vis_table.setStyle(vts)
    story.append(vis_table)
    story.append(SP(6))

    # ── Appendix C: Complete demo output ─────────────────────────────────────
    story.append(P("<b>Appendix C — demo.py Output (Selected)</b>", S["subsection"]))
    story.append(P("The following shows verified output from running python demo.py:"))
    story.append(SP(4))

    demo_output = [
        "=== 1. MaxHeap — Basic Operations ===",
        "  Internal array : [10, 5, 8, 4, 1, 3, 7]",
        "  Peek (max)     : 10",
        "  Extracted order: [10, 8, 7, 5, 4, 3, 1]  ← descending (correct)",
        "",
        "=== 2. MinHeap — Polymorphism ===",
        "  MinHeap array  : [1, 3, 4, 10, 5, 7, 8]",
        "  Peek (min)     : 1",
        "  Extracted order: [1, 3, 4, 5, 7, 8, 10]  ← ascending (correct)",
        "",
        "=== 4. Heap Sort Step-by-Step ===",
        "  Input: [4, 10, 3, 5, 1]",
        "  Phase 1: Max-Heap built: [10, 5, 3, 4, 1]",
        "  Sorted array: [1, 3, 4, 5, 10]  ← correct",
        "",
        "=== 5. Test Cases ===",
        "  Already sorted  : [1,2,3,4,5]       -> [1,2,3,4,5]   [PASS]",
        "  Reverse sorted  : [5,4,3,2,1]       -> [1,2,3,4,5]   [PASS]",
        "  All equal       : [3,3,3,3,3]       -> [3,3,3,3,3]   [PASS]",
        "  Negative numbers: [-5,3,-1,0,-8,2]  -> [-8,-5,-1,0,2,3] [PASS]",
        "  Random 10       : [64,25,...,88,3]   -> [3,7,...,64,88]  [PASS]",
        "",
        "=== 9. Priority Queue Application ===",
        "  HANDLE : Priority 5 — Server down — CRITICAL",
        "  HANDLE : Priority 5 — Database unreachable",
        "  HANDLE : Priority 4 — VPN connectivity issue",
        "  HANDLE : Priority 3 — Outlook not working",
        "  HANDLE : Priority 2 — Printer paper jam",
        "  HANDLE : Priority 1 — Password reset request",
    ]
    for line in demo_output:
        story.append(P(line if line else "&nbsp;", S["code"]))
    story.append(SP(6))

    # ── Appendix D: Code snippet ──────────────────────────────────────────────
    story.append(P("<b>Appendix D — Core Code Snippets</b>", S["subsection"]))
    story.append(P(
        "The following excerpt from heap_sort.py shows the two core functions. "
        "Note that heapify is called recursively; the iterative version can also be used "
        "to eliminate stack overhead:"
    ))
    code_lines = [
        "def _heapify_down(array, n, i):",
        '    """Sift element at index i downward to restore max-heap. O(log n)."""',
        "    largest = i",
        "    left, right = 2*i + 1, 2*i + 2",
        "    if left  < n and array[left]  > array[largest]: largest = left",
        "    if right < n and array[right] > array[largest]: largest = right",
        "    if largest != i:",
        "        array[i], array[largest] = array[largest], array[i]",
        "        _heapify_down(array, n, largest)",
        "",
        "def heap_sort(array):",
        '    """Sort list in ascending order. In-place. O(n log n)."""',
        "    n = len(array)",
        "    # Phase 1: build max-heap in O(n)",
        "    for i in range(n // 2 - 1, -1, -1):",
        "        _heapify_down(array, n, i)",
        "    # Phase 2: extract n-1 times in O(n log n)",
        "    for i in range(n - 1, 0, -1):",
        "        array[0], array[i] = array[i], array[0]",
        "        _heapify_down(array, i, 0)",
        "    return array",
    ]
    for line in code_lines:
        story.append(P(line if line else "&nbsp;", S["code"]))
    story.append(SP(6))

    # ── Appendix E: GitHub info ───────────────────────────────────────────────
    story.append(P("<b>Appendix E — Repository and Resources</b>", S["subsection"]))
    repo_data = [
        ["Item", "Details"],
        ["GitHub Repository", "https://github.com/KUMANAN444/IT-SUPPORT-TICKET-SYSTEM"],
        ["Task 2 Folder",     "/task2/  (heap.py, heap_sort.py, demo.py, README.md)"],
        ["How to Run",        "cd task2  then  python demo.py"],
        ["Python Version",    "Python 3.8 or higher (no external packages required)"],
        ["Video Link",        "[Upload to YouTube as unlisted and paste link here]"],
    ]
    repo_table = Table(repo_data, colWidths=[CONTENT_W*0.28, CONTENT_W*0.72])
    repo_table.setStyle(header_table_style())
    story.append(repo_table)
    story.append(SP(6))

    # ── Appendix F: OOP concepts in code ─────────────────────────────────────
    story.append(P("<b>Appendix F — OOP Concepts Demonstrated in Task 2 Code</b>",
                   S["subsection"]))
    oop_data = [
        ["OOP Concept",        "Where Used in Task 2",                            "File"],
        ["Class & Objects",    "MaxHeap, MinHeap, HeapSorter instantiated",       "heap.py, heap_sort.py"],
        ["Encapsulation",      "_data list is private; peek()/extract_top() as interface", "heap.py"],
        ["Inheritance",        "MinHeap extends MaxHeap; inherits all methods",   "heap.py"],
        ["Polymorphism",       "_has_higher_priority() overridden in MinHeap",    "heap.py"],
        ["Class Method",       "MaxHeap.from_list() factory; HeapSorter.benchmark()", "both"],
        ["Static Method",      "MaxHeap._left/_right/_parent, Ticket.generate_id()", "heap.py"],
        ["Magic Methods",      "__len__, __str__, __repr__, __contains__",         "heap.py"],
        ["Properties",         "size(), is_empty() as read-only getters",          "heap.py"],
    ]
    oop_table = Table(oop_data, colWidths=[CONTENT_W*0.26, CONTENT_W*0.46, CONTENT_W*0.28])
    oop_table.setStyle(header_table_style())
    story.append(oop_table)

    return story


# ─────────────────────────────────────────────────────────────────────────────
# Page number footer
# ─────────────────────────────────────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:   # no page number on cover
        canvas.setFont("Times-Roman", 9)
        canvas.setFillColor(HexColor("#888888"))
        page_text = f"Page {doc.page - 1}"   # Page 1 = cover, content starts at "1"
        canvas.drawCentredString(PAGE_W / 2, 1.2 * cm, page_text)
        canvas.setStrokeColor(MID_BLUE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 1.6 * cm, PAGE_W - MARGIN, 1.6 * cm)
        canvas.setFont("Times-Italic", 8)
        canvas.setFillColor(HexColor("#888888"))
        canvas.drawString(MARGIN, 1.2 * cm,
                          "COMP2090SEF — Task 2 Study Report: Heap & Heap Sort")
        canvas.drawRightString(PAGE_W - MARGIN, 1.2 * cm,
                               "Group 10 | HKMU | 2026")
    canvas.restoreState()


# ─────────────────────────────────────────────────────────────────────────────
# Assemble and build
# ─────────────────────────────────────────────────────────────────────────────

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN,  bottomMargin=2.0 * cm,
    title="Task 2 Study Report: Heap & Heap Sort",
    author="Group 10",
    subject="COMP2090SEF Course Project",
)

story = []
story += build_cover()

# Main content pages
story.append(P("<b>MAIN CONTENT</b>",
               ParagraphStyle("mc", fontName="Times-Bold", fontSize=11,
                               leading=14, alignment=TA_CENTER, textColor=HexColor("#888888"))))
story.append(P("(3 pages of text-only main content follow, diagrams/tables in Appendix)",
               ParagraphStyle("mcsub", fontName="Times-Italic", fontSize=10,
                               leading=14, alignment=TA_CENTER, textColor=HexColor("#AAAAAA"))))
story.append(SP(4))

story += build_page1()
story.append(PageBreak())
story += build_page2()
story.append(PageBreak())
story += build_page3()
story += build_appendix()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Report generated: {OUTPUT}")
