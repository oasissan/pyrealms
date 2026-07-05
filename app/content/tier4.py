"""Tier 4 — The Proving Grounds (optional DSA / interview realm).

Optional: unlocks on level alone and never gates another realm. This is the
algorithm-and-data-structure practice the core realms deliberately skip —
recursion, two pointers, sliding windows, hash-map patterns, and
sort/search — framed the way technical interviews ask them.
"""

TIER = {
    "slug": "proving-grounds",
    "title": "The Proving Grounds",
    "subtitle": "Optional — Interview Algorithms",
    "order": 4,
    "min_level": 3,
    "optional": True,
    "quests": [
        {
            "slug": "recursion-bigo",
            "title": "Recursion & Big-O",
            "description": "Base cases, recursive cases, and reasoning about cost.",
            "badge": {"id": "recursion-runner", "name": "Recursion Runner", "icon": "🌀"},
            "missions": [
                {
                    "slug": "recursion-sum",
                    "title": "Thinking Recursively",
                    "kind": "standard",
                    "xp": 60,
                    "lesson_md": """\
A recursive function calls itself on a **smaller** input until it hits a
**base case** that returns without recursing:

```python
def factorial(n):
    if n <= 1:          # base case — stops the recursion
        return 1
    return n * factorial(n - 1)   # recursive case — shrinks n
```

Every recursion needs a base case (or it blows the stack) and each step must
move *toward* it. **Big-O** describes how work grows with input size: this
`factorial` is O(n) — n calls, each O(1). When you analyse a recursive
solution, count the calls and the work per call. Interviewers care less about
the answer than whether you can name its time and space cost.
""",
                    "prompt_md": """\
Write `recursive_sum(nums)` that returns the sum of a list **using
recursion** — no loops, no built-in `sum`. An empty list sums to `0`.
""",
                    "starter_code": "def recursive_sum(nums):\n    ...\n",
                    "example_tests": """\
from solution import recursive_sum

def test_basic():
    assert recursive_sum([1, 2, 3, 4]) == 10

def test_empty():
    assert recursive_sum([]) == 0
""",
                    "hidden_tests": """\
from solution import recursive_sum

def test_basic():
    assert recursive_sum([1, 2, 3, 4]) == 10

def test_empty():
    assert recursive_sum([]) == 0

def test_single():
    assert recursive_sum([7]) == 7

def test_negatives():
    assert recursive_sum([-1, -2, 3]) == 0
""",
                    "solution_md": """\
```python
def recursive_sum(nums):
    if not nums:            # base case: empty list
        return 0
    return nums[0] + recursive_sum(nums[1:])
```

**Why:** the base case handles the empty list; every recursive step peels off
one element and sums the rest. It's O(n) calls — though slicing `nums[1:]`
copies, so this particular form is O(n²) space/time. A pointer-based helper
(`recursive_sum(nums, i)`) avoids the copies; naming that trade-off is exactly
the Big-O reasoning interviewers want.
""",
                },
                {
                    "slug": "recursion-boss",
                    "title": "Boss: The Infinite Nesting",
                    "kind": "boss",
                    "xp": 120,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `flatten_deep(nested)` that flattens an **arbitrarily** nested list of
integers into a single flat list, preserving order.
`flatten_deep([1, [2, [3, 4], 5]])` returns `[1, 2, 3, 4, 5]`.
""",
                    "starter_code": "def flatten_deep(nested):\n    ...\n",
                    "hidden_tests": """\
from solution import flatten_deep

def test_nested():
    assert flatten_deep([1, [2, [3, 4], 5]]) == [1, 2, 3, 4, 5]

def test_flat():
    assert flatten_deep([1, 2, 3]) == [1, 2, 3]

def test_empty():
    assert flatten_deep([]) == []

def test_very_deep():
    assert flatten_deep([[[[1]]], 2]) == [1, 2]
""",
                    "solution_md": """\
```python
def flatten_deep(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_deep(item))
        else:
            result.append(item)
    return result
```

**Why:** the recursion mirrors the data's shape — a list recurses, anything
else is a leaf you append. Recursion shines exactly when the structure is
itself recursive (arbitrary depth), where a fixed number of loops can't reach.
""",
                },
            ],
        },
        {
            "slug": "two-pointers",
            "title": "Two Pointers",
            "description": "Walk a sequence from both ends — or at two speeds.",
            "badge": {"id": "two-pointer-tactician", "name": "Two-Pointer Tactician", "icon": "👉"},
            "missions": [
                {
                    "slug": "two-pointers-reverse",
                    "title": "Converging Pointers",
                    "kind": "standard",
                    "xp": 60,
                    "lesson_md": """\
The **two-pointer** pattern keeps two indices moving through a sequence,
often from opposite ends toward the middle:

```python
left, right = 0, len(xs) - 1
while left < right:
    ...            # compare / swap xs[left] and xs[right]
    left += 1
    right -= 1
```

It turns many O(n²) brute-force scans into a single O(n) pass with O(1) extra
space. Reversing in place, testing palindromes, and finding pairs in a sorted
array are the canonical uses.
""",
                    "prompt_md": """\
Write `reverse_in_place(nums)` that reverses the list **in place** using two
converging pointers — no slicing (`[::-1]`) and no `reversed`. Return the same
list object.
""",
                    "starter_code": "def reverse_in_place(nums):\n    ...\n",
                    "example_tests": """\
from solution import reverse_in_place

def test_odd():
    assert reverse_in_place([1, 2, 3]) == [3, 2, 1]

def test_even():
    assert reverse_in_place([1, 2, 3, 4]) == [4, 3, 2, 1]
""",
                    "hidden_tests": """\
from solution import reverse_in_place

def test_odd():
    assert reverse_in_place([1, 2, 3]) == [3, 2, 1]

def test_even():
    assert reverse_in_place([1, 2, 3, 4]) == [4, 3, 2, 1]

def test_in_place():
    x = [1, 2, 3]
    assert reverse_in_place(x) is x

def test_empty():
    assert reverse_in_place([]) == []
""",
                    "solution_md": """\
```python
def reverse_in_place(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    return nums
```

**Why:** the pointers swap the outermost pair, then step inward until they
meet. It mutates the original (note the `is x` test) and uses O(1) extra space
— unlike `nums[::-1]`, which allocates a whole new list.
""",
                },
                {
                    "slug": "two-pointers-boss",
                    "title": "Boss: Push the Zeroes",
                    "kind": "boss",
                    "xp": 120,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `move_zeroes(nums)` that moves every `0` to the end **in place** while
keeping the order of the non-zero elements, and returns the same list.
`move_zeroes([0, 1, 0, 3, 12])` returns `[1, 3, 12, 0, 0]`.
""",
                    "starter_code": "def move_zeroes(nums):\n    ...\n",
                    "hidden_tests": """\
from solution import move_zeroes

def test_basic():
    assert move_zeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]

def test_no_zeros():
    assert move_zeroes([1, 2, 3]) == [1, 2, 3]

def test_all_zeros():
    assert move_zeroes([0, 0]) == [0, 0]

def test_in_place():
    x = [0, 1]
    assert move_zeroes(x) is x
""",
                    "solution_md": """\
```python
def move_zeroes(nums):
    insert = 0                       # next slot for a non-zero
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[insert], nums[i] = nums[i], nums[insert]
            insert += 1
    return nums
```

**Why:** a slow pointer (`insert`) marks where the next non-zero belongs while
a fast pointer (`i`) scans ahead — the two-speed variant of two pointers. One
O(n) pass, O(1) space, order preserved.
""",
                },
            ],
        },
        {
            "slug": "sliding-window",
            "title": "Sliding Window",
            "description": "Reuse work across overlapping ranges instead of recomputing.",
            "badge": {"id": "window-watcher", "name": "Window Watcher", "icon": "🪟"},
            "missions": [
                {
                    "slug": "sliding-window-sum",
                    "title": "The Rolling Sum",
                    "kind": "standard",
                    "xp": 60,
                    "lesson_md": """\
A **sliding window** keeps a running summary of a contiguous range and updates
it incrementally as the range slides, instead of recomputing from scratch:

```python
window = sum(xs[:k])
for i in range(k, len(xs)):
    window += xs[i] - xs[i - k]   # add the entering, drop the leaving
```

Recomputing each window is O(n·k); sliding is O(n). Fixed-size windows use
this rolling update; variable-size windows grow and shrink two pointers to
maintain a condition.
""",
                    "prompt_md": """\
Write `max_window_sum(nums, k)` returning the largest sum of any **contiguous
window of exactly `k`** elements. Assume `1 <= k <= len(nums)`.
`max_window_sum([2, 1, 5, 1, 3, 2], 3)` returns `9`.
""",
                    "starter_code": "def max_window_sum(nums, k):\n    ...\n",
                    "example_tests": """\
from solution import max_window_sum

def test_basic():
    assert max_window_sum([2, 1, 5, 1, 3, 2], 3) == 9

def test_k_one():
    assert max_window_sum([1, 4, 2], 1) == 4
""",
                    "hidden_tests": """\
from solution import max_window_sum

def test_basic():
    assert max_window_sum([2, 1, 5, 1, 3, 2], 3) == 9

def test_k_one():
    assert max_window_sum([1, 4, 2], 1) == 4

def test_whole_list():
    assert max_window_sum([1, 2, 3], 3) == 6

def test_negatives():
    assert max_window_sum([-1, -2, -3, -1], 2) == -3
""",
                    "solution_md": """\
```python
def max_window_sum(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]   # slide: add new, drop old
        best = max(best, window)
    return best
```

**Why:** the first window is summed once; every slide is O(1) — add the
entering element, subtract the leaving one. That's O(n) total instead of the
O(n·k) you'd get resumming each window.
""",
                },
                {
                    "slug": "sliding-window-boss",
                    "title": "Boss: The Longest Streak",
                    "kind": "boss",
                    "xp": 120,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `longest_unique(s)` returning the length of the longest substring of `s`
with **no repeating characters**. `"abcabcbb"` → `3` (`"abc"`), `"bbbb"` → `1`,
`""` → `0`.
""",
                    "starter_code": "def longest_unique(s):\n    ...\n",
                    "hidden_tests": """\
from solution import longest_unique

def test_classic():
    assert longest_unique("abcabcbb") == 3

def test_all_same():
    assert longest_unique("bbbb") == 1

def test_empty():
    assert longest_unique("") == 0

def test_mixed():
    assert longest_unique("pwwkew") == 3
""",
                    "solution_md": """\
```python
def longest_unique(s):
    last_seen = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1   # jump past the earlier duplicate
        last_seen[ch] = i
        best = max(best, i - start + 1)
    return best
```

**Why:** a variable-size window `[start, i]` grows as you scan; on a repeat you
slide `start` just past the previous occurrence. A dict of last-seen indices
keeps every step O(1), so the whole scan is O(n).
""",
                },
            ],
        },
        {
            "slug": "hashmap-patterns",
            "title": "Hash-Map Patterns",
            "description": "Trade memory for O(1) lookups — the interview workhorse.",
            "badge": {"id": "hash-hunter", "name": "Hash Hunter", "icon": "#️⃣"},
            "missions": [
                {
                    "slug": "hashmap-two-sum",
                    "title": "Seen-Before Lookups",
                    "kind": "standard",
                    "xp": 60,
                    "lesson_md": """\
A dict gives **O(1)** average lookup, which collapses many nested-loop
problems to a single pass. The core trick: as you scan, remember what you've
seen so the *complement* you need is one lookup away.

```python
seen = {}
for i, n in enumerate(nums):
    if want - n in seen:        # have we already seen the partner?
        return (seen[want - n], i)
    seen[n] = i                 # remember this value's index
```

This turns the O(n²) "check every pair" into O(n) time / O(n) space — the
classic time-for-memory trade every interviewer probes.
""",
                    "prompt_md": """\
Write `two_sum(nums, target)` returning the pair of indices `(i, j)` with
`i < j` whose values sum to `target`. Exactly one solution exists; return it
as a tuple. `two_sum([2, 7, 11, 15], 9)` returns `(0, 1)`.
""",
                    "starter_code": "def two_sum(nums, target):\n    ...\n",
                    "example_tests": """\
from solution import two_sum

def test_basic():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)

def test_middle():
    assert two_sum([3, 2, 4], 6) == (1, 2)
""",
                    "hidden_tests": """\
from solution import two_sum

def test_basic():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)

def test_middle():
    assert two_sum([3, 2, 4], 6) == (1, 2)

def test_negatives():
    assert two_sum([-3, 4, 3, 90], 0) == (0, 2)

def test_duplicates():
    assert two_sum([3, 3], 6) == (0, 1)
""",
                    "solution_md": """\
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return (seen[target - n], i)
        seen[n] = i
```

**Why:** one pass, one dict. For each number you ask "have I already seen its
partner?" — an O(1) lookup — so the whole thing is O(n) instead of the O(n²)
double loop. Storing the index *after* checking guarantees `i < j`.
""",
                },
                {
                    "slug": "hashmap-boss",
                    "title": "Boss: The Anagram Vault",
                    "kind": "boss",
                    "xp": 120,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `group_anagrams(words)` returning a dict that maps each word's canonical
key — its letters **sorted** and joined — to the list of words sharing it, in
first-seen order.
`group_anagrams(["eat", "tea", "tan", "ate"])` returns
`{"aet": ["eat", "tea", "ate"], "ant": ["tan"]}`.
""",
                    "starter_code": "def group_anagrams(words):\n    ...\n",
                    "hidden_tests": """\
from solution import group_anagrams

def test_basic():
    assert group_anagrams(["eat", "tea", "tan", "ate"]) == {
        "aet": ["eat", "tea", "ate"],
        "ant": ["tan"],
    }

def test_empty():
    assert group_anagrams([]) == {}

def test_single():
    assert group_anagrams(["abc"]) == {"abc": ["abc"]}

def test_all_same_group():
    assert group_anagrams(["ab", "ba"]) == {"ab": ["ab", "ba"]}
""",
                    "solution_md": """\
```python
def group_anagrams(words):
    groups = {}
    for word in words:
        key = "".join(sorted(word))   # anagrams share sorted letters
        groups.setdefault(key, []).append(word)
    return groups
```

**Why:** anagrams collapse to the same key once you sort their letters, so a
single dict groups them in one O(n·k log k) pass. `setdefault` creates the
list on first sight and appends on every hit — the idiomatic accumulate-into-a-
dict move.
""",
                },
            ],
        },
        {
            "slug": "sort-search",
            "title": "Sorting & Searching",
            "description": "Binary search and interval merging on sorted data.",
            "badge": {"id": "binary-boss", "name": "Binary Boss", "icon": "🔍"},
            "missions": [
                {
                    "slug": "binary-search",
                    "title": "Halving the Haystack",
                    "kind": "standard",
                    "xp": 60,
                    "lesson_md": """\
On **sorted** data you never scan linearly — you halve. **Binary search**
checks the middle and discards half the range each step:

```python
lo, hi = 0, len(xs) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if xs[mid] == target: return mid
    if xs[mid] < target:  lo = mid + 1   # target is in the right half
    else:                 hi = mid - 1   # ... the left half
```

That's O(log n) — a million elements in ~20 steps. The pitfalls interviewers
watch for: the `<=` (not `<`) loop condition, and `mid + 1` / `mid - 1` to
avoid an infinite loop.
""",
                    "prompt_md": """\
Write `binary_search(nums, target)` on an **ascending-sorted** list, returning
the index of `target` or `-1` if absent. Use binary search — no linear scan,
no `.index()`.
""",
                    "starter_code": "def binary_search(nums, target):\n    ...\n",
                    "example_tests": """\
from solution import binary_search

def test_found():
    assert binary_search([1, 3, 5, 7, 9], 7) == 3

def test_absent():
    assert binary_search([1, 3, 5], 4) == -1
""",
                    "hidden_tests": """\
from solution import binary_search

def test_found():
    assert binary_search([1, 3, 5, 7, 9], 7) == 3

def test_absent():
    assert binary_search([1, 3, 5], 4) == -1

def test_first_and_last():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0
    assert binary_search([1, 3, 5, 7, 9], 9) == 4

def test_empty():
    assert binary_search([], 5) == -1
""",
                    "solution_md": """\
```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**Why:** each comparison throws away half the remaining range, so lookup is
O(log n). The `lo <= hi` bound checks the final single-element range, and the
`± 1` updates guarantee the window always shrinks (no infinite loop).
""",
                },
                {
                    "slug": "sort-search-boss",
                    "title": "Boss: Merge the Overlaps",
                    "kind": "boss",
                    "xp": 120,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `merge_intervals(intervals)` that takes a list of `[start, end]` pairs
and returns a new list of merged, non-overlapping intervals sorted by start.
Touching intervals merge (`[1, 4]` and `[4, 5]` → `[1, 5]`).
`merge_intervals([[1, 3], [2, 6], [8, 10]])` returns `[[1, 6], [8, 10]]`.
""",
                    "starter_code": "def merge_intervals(intervals):\n    ...\n",
                    "hidden_tests": """\
from solution import merge_intervals

def test_basic():
    assert merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]

def test_touching():
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]

def test_unsorted_input():
    assert merge_intervals([[8, 10], [1, 3]]) == [[1, 3], [8, 10]]

def test_empty():
    assert merge_intervals([]) == []
""",
                    "solution_md": """\
```python
def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # extend the last one
        else:
            merged.append([start, end])
    return merged
```

**Why:** sorting by start means any overlap must be with the *most recent*
merged interval, so a single pass suffices. Overall O(n log n), dominated by
the sort — the merge itself is O(n).
""",
                },
            ],
        },
        {
            "slug": "proving-grounds-boss-battle",
            "title": "Boss Battle: The Grandmaster's Gauntlet",
            "description": "Timed, hint-free, hidden tests. Prove your algorithm chops.",
            "is_boss_battle": True,
            "badge": {"id": "algorithm-ace", "name": "Algorithm Ace", "icon": "🏆"},
            "missions": [
                {
                    "slug": "proving-grounds-gauntlet",
                    "title": "The Grandmaster's Gauntlet",
                    "kind": "tier_boss",
                    "xp": 250,
                    "time_limit_seconds": 1200,
                    "prompt_md": """\
**⏱ Timed Boss Battle — 20 minutes, no hints, hidden test suite.**

Two classics, one submission:

1. `merge_sort(nums)` — return a **new** sorted list using the merge-sort
   algorithm (divide, recurse, merge). Don't call `sorted` or `.sort()`.
2. `max_subarray(nums)` — return the largest sum of any **non-empty
   contiguous** subarray (Kadane's algorithm).
   `max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])` returns `6`.
""",
                    "starter_code": (
                        "def merge_sort(nums):\n    ...\n\n\n"
                        "def max_subarray(nums):\n    ...\n"
                    ),
                    "hidden_tests": """\
from solution import merge_sort, max_subarray

def test_merge_sort_basic():
    assert merge_sort([3, 1, 2]) == [1, 2, 3]

def test_merge_sort_empty():
    assert merge_sort([]) == []

def test_merge_sort_duplicates():
    assert merge_sort([5, 3, 5, 1, 3]) == [1, 3, 3, 5, 5]

def test_merge_sort_negatives():
    assert merge_sort([9, -1, 0, 4, -1]) == [-1, -1, 0, 4, 9]

def test_max_subarray():
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

def test_max_subarray_all_negative():
    assert max_subarray([-3, -1, -2]) == -1

def test_max_subarray_single():
    assert max_subarray([5]) == 5
""",
                    "solution_md": """\
```python
def merge_sort(nums):
    if len(nums) <= 1:
        return list(nums)
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def max_subarray(nums):
    best = current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)   # extend the run, or start fresh at n
        best = max(best, current)
    return best
```

**Why:** merge sort splits to single elements (the sorted base case) then
merges sorted halves with a two-pointer walk — O(n log n) guaranteed. Kadane's
insight is that the best subarray ending at each position is either just that
element or the previous best extended by it, giving an O(n) single pass.
""",
                },
            ],
        },
    ],
}
