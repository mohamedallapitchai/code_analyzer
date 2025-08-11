Title
Bounding Box Analyzer – Requirements and Examples

Purpose
- Analyze a rectangular character grid containing only '*' and '-'.
- Identify 4-connected components of '*'.
- Discard any component whose axis-aligned bounding rectangle overlaps with any other component’s bounding rectangle.
- For each remaining component, compute the maximum rectangle area formed by the component’s top-left anchor and any other point in that component.
- Report results according to the global maximum area and the revised zero-area rule.

Scope and conventions
- Indexing is 1-based:
  - Rows are numbered from 1 at the top.
  - Columns are numbered from 1 at the left.
- Connectivity is 4-directional only (up, down, left, right); diagonals do not connect.
- Input is read from resources/groups.txt (one grid line per file line).

Input format and validation
- The input is a grid of N lines, each of length M, N ≥ 1, M ≥ 1.
- Allowed characters are only:
  - '*' for a filled cell
  - '-' for an empty cell
- Validation rules:
  - If no lines are provided, reject input.
  - If not all lines have the same length, reject input.
  - If any character is not '*' or '-', reject input.
- Error handling: a clear error message should be produced when validation fails.

Definitions
- Component: a maximal set of '*' cells connected by 4-neighbor adjacency.
- Bounding rectangle of a component:
  - left = minimum column among its points
  - right = maximum column among its points
  - top = minimum row among its points
  - bottom = maximum row among its points
- Anchor (top-left point) of a component:
  - the point with the smallest row; among those, the smallest column.
- Area between two points (r1, c1) and (r2, c2) used in this problem:
  - b = r2 − r1
  - l = c2 − c1
  - area = b × l
- Manhattan distance between two points:
  - |r2 − r1| + |c2 − c1|

Processing steps
1) Read input
- Read all lines from resources/groups.txt into memory.

2) Validate input
- Ensure all lines are non-empty, same length, and contain only '*' and '-'.

3) Detect components
- Traverse the grid; group '*' cells into components using 4-neighbor connectivity (up, down, left, right).
- Represent each component as a set or list of Point(row, column).

4) Filter by non-overlapping bounding rectangles
- For every pair of components, compute their bounding rectangles.
- Two rectangles are considered non-overlapping if any of the following holds:
  - R.right <= S.left
  - S.right <= R.left
  - R.bottom <= S.top
  - R.top >= S.bottom
- Touching at edges or corners (equality cases) counts as non-overlapping.
- Discard any component that overlaps with at least one other component; keep only components that do not overlap any others.

5) For each remaining component, compute the component’s best area
- Determine the anchor (top-left point).
- For each point p in the component, compute area(anchor, p).
- The component’s best area is the maximum area over its points.
- If multiple points yield the same best area, use row-then-column order to select the representative opposite corner (smallest row, then smallest column).

6) Global selection and revised zero-area rule
- Let A be the maximum best area among all remaining components (if none remain, see Output rules).
- If A > 0:
  - Report every remaining component whose best area equals A.
  - For each, output the anchor and one opposite corner that achieves the max (tie-broken by row then column).
- If A = 0 (revised rule):
  - For each remaining component, output the anchor paired with a non-anchor point from that component.
  - Choose the non-anchor farthest from the anchor by Manhattan distance; if there is a tie, choose by row then column.
  - If a component has only one point, pair the anchor with itself.

Output rules and formatting
- If there are no '*' in the entire grid: output "()".
- Otherwise, for each selected component, output a pair of coordinates with no separator between them:
  - "(r1, c1)(r2, c2)"
  - The first coordinate is the anchor; the second is the chosen point as per the rules above.
- Multiple component pairs are joined by commas, with no extra spaces:
  - Example: "(1, 1)(3, 3),(4, 10)(6, 12)"
- Coordinate formatting: "(row, column)" with a single space after the comma.

Edge cases and clarifications
- Rectangles that touch at edges or corners are considered non-overlapping and do not cause components to be discarded.
- If all remaining components have best area zero, the revised rule outputs one pair per remaining component using a non-anchor point (or itself if single-point).
- If overlap occurs between any two components, both are excluded from the final consideration (and any other overlapping ones as well).
- Anchor is always top-left (minimum row, then minimum column) within the component.

Complexity notes
- Component detection is O(N×M).
- Per-component best area computation is O(K) where K is the number of points in the component.
- Naive pairwise overlap checking is O(B^2) for B components.

Worked examples

Example 1: Two disjoint blocks; tie on global max
- Grid (6 rows × 10 cols):
  --**------
  --**--***-
  --**--***-
  ----------
  -----**---
  -----**---
- Components (all 4-connected):
  - A: rows 1..3, cols 3..4; anchor (1, 3); best area = 2 at (3, 4)
  - B: rows 2..3, cols 7..9; anchor (2, 7); best area = 2 at (3, 9)
  - C: rows 5..6, cols 6..7; anchor (5, 6); best area = 1 at (6, 7)
- No overlaps among bounding rectangles → all remain.
- Global max area = 2 → A and B are reported.
- Output: (1, 3)(3, 4),(2, 7)(3, 9)

Example 2: Overlapping rectangles are discarded
- Grid (4 rows × 12 cols):
  Row 1: **-------***
  Row 2: -*--**--***-
  Row 3: -----***--**
  Row 4: -------***--
- Components:
  - C1: {(1,1),(1,2),(2,2)}; bounds rows 1..2, cols 1..2
  - C2: {(2,5),(2,6),(3,6),(3,7),(3,8),(4,8),(4,9),(4,10)}; bounds rows 2..4, cols 5..10
  - C3: {(1,10),(1,11),(1,12),(2,9),(2,10),(2,11),(3,11),(3,12)}; bounds rows 1..3, cols 9..12
- Overlap: C2 and C3 overlap (rows 2..3 intersect and cols 9..10 intersect) → both discarded.
- Remaining: C1 only. Best area = 1 at (2, 2).
- Output: (1, 1)(2, 2)

Example 3: Zero-area case (revised rule)
- Grid (4 rows × 8 cols):
  Row 1: *-------
  Row 2: *-------
  Row 3: ------**
  Row 4: --------
- Components:
  - F: {(1,1),(2,1)}; bounds rows 1..2, cols 1..1
  - G: {(3,7),(3,8)}; bounds rows 3..3, cols 7..8
- No overlaps → both remain.
- All best areas are zero.
- Revised rule → pair anchor with farthest non-anchor by Manhattan:
  - F → (1, 1)(2, 1)
  - G → (3, 7)(3, 8)
- Output: (1, 1)(2, 1),(3, 7)(3, 8)

Example 4: Single-point component
- Grid (3 rows × 3 cols):
  ---
  -*-
  ---
- One component: {(2,2)}; anchor (2, 2); best area = 0.
- Revised rule for zero-area with single-point → anchor with itself.
- Output: (2, 2)(2, 2)

Example 5: Touching rectangles are allowed (non-overlapping)
- Grid (4 rows × 7 cols):
  **-***-
  **-***-
  ---*---
  ---*---
- Components:
  - H: rows 1..2, cols 1..2
  - I: rows 1..2, cols 4..6
  - J: rows 3..4, cols 4..4
- H and I rectangles are separated by one column (touching would also be allowed); no overlaps among any.
- Best areas:
  - H: anchor (1,1) → best area = 1 at (2,2)
  - I: anchor (1,4) → best area = 2 at (2,6)
  - J: anchor (3,4) → best area = 0
- Global max area = 2 → only I is reported.
- Output: (1, 4)(2, 6)

I/O details for your implementation
- Input source: read all lines from resources/groups.txt.
- Output: print to stdout using the formatting rules above.
