"""Tier 2 — Core Craftsmanship (Apprentice). Curriculum seed data."""

TIER = {
    "slug": "core-craftsmanship",
    "title": "Core Craftsmanship",
    "subtitle": "The Apprentice Realm",
    "order": 2,
    "min_level": 3,
    "quests": [
        {
            "slug": "comprehensions",
            "title": "Comprehensions",
            "description": "Build lists, dicts and sets in a single expressive line.",
            "badge": {"id": "comprehension-connoisseur", "name": "Comprehension Connoisseur", "icon": "🧠"},
            "missions": [
                {
                    "slug": "comprehensions-basics",
                    "title": "List & Dict Comprehensions",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
A comprehension is a loop-and-collect in one expression:

```python
squares = [x * x for x in nums]              # list
evens   = [x for x in nums if x % 2 == 0]    # with filter
lengths = {w: len(w) for w in words}         # dict
seen    = {c.lower() for c in text}          # set
```

Read them left to right: *output expression*, *loop*, *condition*. They're
usually faster than the equivalent `for`+`append` loop and signal intent.
Rule of thumb: one loop and one `if` — beyond that, use a real loop.
""",
                    "prompt_md": """\
Write `squares_of_evens(nums)` returning a list of the squares of only the
**even** numbers, in order. `squares_of_evens([1, 2, 3, 4])` returns
`[4, 16]`.
""",
                    "starter_code": "def squares_of_evens(nums):\n    ...\n",
                    "hidden_tests": """\
from solution import squares_of_evens

def test_mixed():
    assert squares_of_evens([1, 2, 3, 4]) == [4, 16]

def test_no_evens():
    assert squares_of_evens([1, 3, 5]) == []

def test_negative():
    assert squares_of_evens([-2, 0, 7]) == [4, 0]
""",
                },
                {
                    "slug": "comprehensions-boss",
                    "title": "Boss: The Flattener",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `flatten(matrix)` that flattens a list of lists one level deep into
a single list, using a **nested comprehension**.
`flatten([[1, 2], [3], []])` returns `[1, 2, 3]`.
""",
                    "starter_code": "def flatten(matrix):\n    ...\n",
                    "hidden_tests": """\
from solution import flatten

def test_basic():
    assert flatten([[1, 2], [3], []]) == [1, 2, 3]

def test_empty():
    assert flatten([]) == []

def test_strings():
    assert flatten([["a"], ["b", "c"]]) == ["a", "b", "c"]

def test_preserves_order():
    assert flatten([[3, 1], [2]]) == [3, 1, 2]
""",
                },
            ],
        },
        {
            "slug": "args-kwargs-closures",
            "title": "*args, **kwargs & Closures",
            "description": "Flexible signatures and functions that remember.",
            "badge": {"id": "closure-craftsman", "name": "Closure Craftsman", "icon": "🔒"},
            "missions": [
                {
                    "slug": "args-kwargs-basics",
                    "title": "Variadic Functions",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
`*args` collects extra positional arguments into a **tuple**; `**kwargs`
collects extra keyword arguments into a **dict**:

```python
def report(*args, **kwargs):
    print(args)     # (1, 2)
    print(kwargs)   # {"mode": "fast"}

report(1, 2, mode="fast")
```

The same stars *unpack* on the calling side: `f(*a_list, **a_dict)`.
This is how decorators forward arbitrary arguments — you'll need it soon.
""",
                    "prompt_md": """\
Write `sum_all(*args)` that accepts any number of numeric arguments and
returns their sum. Zero arguments returns `0`.
""",
                    "starter_code": "def sum_all(*args):\n    ...\n",
                    "hidden_tests": """\
from solution import sum_all

def test_three():
    assert sum_all(1, 2, 3) == 6

def test_none():
    assert sum_all() == 0

def test_floats():
    assert sum_all(1.5, 2.5) == 4.0
""",
                },
                {
                    "slug": "closures-boss",
                    "title": "Boss: The Counter That Remembers",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `make_counter()` that returns a function. Each call to that returned
function returns the next integer, starting at `1`. Two separate counters
must count independently. (Hint you won't get: `nonlocal`.)
""",
                    "starter_code": "def make_counter():\n    ...\n",
                    "hidden_tests": """\
from solution import make_counter

def test_counts():
    c = make_counter()
    assert c() == 1
    assert c() == 2
    assert c() == 3

def test_independent():
    a = make_counter()
    b = make_counter()
    a()
    a()
    assert b() == 1
""",
                },
            ],
        },
        {
            "slug": "oop-basics",
            "title": "OOP Basics",
            "description": "Classes, inheritance, and dunder methods.",
            "badge": {"id": "object-whisperer", "name": "Object Whisperer", "icon": "🏛️"},
            "missions": [
                {
                    "slug": "oop-rectangle",
                    "title": "Your First Class",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
A class bundles data (attributes) and behavior (methods). `__init__` runs
on construction; `self` is the instance:

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} says woof"
```

**Dunder** ("double underscore") methods hook into Python's syntax:
`__repr__` controls `repr(obj)`, `__eq__` controls `==`, `__add__`
controls `+`, `__len__` controls `len()`. Implementing them makes your
objects feel native.
""",
                    "prompt_md": """\
Write a class `Rectangle` constructed as `Rectangle(width, height)` with
two methods: `area()` and `perimeter()`.
""",
                    "starter_code": "class Rectangle:\n    def __init__(self, width, height):\n        ...\n",
                    "hidden_tests": """\
from solution import Rectangle

def test_area():
    assert Rectangle(3, 4).area() == 12

def test_perimeter():
    assert Rectangle(3, 4).perimeter() == 14

def test_square():
    r = Rectangle(5, 5)
    assert r.area() == 25 and r.perimeter() == 20
""",
                },
                {
                    "slug": "oop-boss",
                    "title": "Boss: Vector Arithmetic",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write a class `Vector` constructed as `Vector(x, y)` supporting:

- `v1 + v2` → a new `Vector` (component-wise)
- `v1 == v2` → equality by components
- `repr(v)` → exactly `"Vector(1, 2)"` style
""",
                    "starter_code": "class Vector:\n    def __init__(self, x, y):\n        ...\n",
                    "hidden_tests": """\
from solution import Vector

def test_add():
    assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)

def test_eq():
    assert Vector(1, 2) == Vector(1, 2)
    assert Vector(1, 2) != Vector(2, 1)

def test_repr():
    assert repr(Vector(1, 2)) == "Vector(1, 2)"

def test_add_returns_new():
    v = Vector(0, 0)
    w = v + Vector(1, 1)
    assert v == Vector(0, 0) and w == Vector(1, 1)
""",
                },
            ],
        },
        {
            "slug": "file-io",
            "title": "File I/O & Context Managers",
            "description": "Reading, writing, and the `with` statement.",
            "badge": {"id": "file-wrangler", "name": "File Wrangler", "icon": "📁"},
            "missions": [
                {
                    "slug": "file-io-basics",
                    "title": "with open(...)",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
`with` guarantees cleanup even when exceptions fly — for files, that means
the handle is closed:

```python
with open(path, "w") as f:      # "r" read, "w" write, "a" append
    f.write("hello\\n")

with open(path) as f:
    for line in f:              # file objects are iterators of lines
        process(line.rstrip("\\n"))
```

Never call `open()` without `with` in real code. `f.readlines()` slurps
everything; iterating streams line by line.
""",
                    "prompt_md": """\
Write two functions:

1. `write_lines(path, lines)` — writes each string in `lines` to the file
   at `path`, one per line (newline-terminated).
2. `read_lines(path)` — returns the file's lines as a list of strings
   **without** trailing newlines.

Both must use `with`.
""",
                    "starter_code": (
                        "def write_lines(path, lines):\n    ...\n\n\n"
                        "def read_lines(path):\n    ...\n"
                    ),
                    "hidden_tests": """\
from solution import write_lines, read_lines

def test_round_trip(tmp_path):
    p = tmp_path / "notes.txt"
    write_lines(p, ["alpha", "beta"])
    assert read_lines(p) == ["alpha", "beta"]

def test_empty(tmp_path):
    p = tmp_path / "empty.txt"
    write_lines(p, [])
    assert read_lines(p) == []

def test_no_trailing_newlines(tmp_path):
    p = tmp_path / "x.txt"
    write_lines(p, ["one"])
    assert read_lines(p)[0] == "one"
""",
                },
                {
                    "slug": "file-io-boss",
                    "title": "Boss: The Word Counter",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `count_lines_words(path)` that reads a text file and returns a tuple
`(line_count, word_count)`, where words are whitespace-separated. An empty
file is `(0, 0)`.
""",
                    "starter_code": "def count_lines_words(path):\n    ...\n",
                    "hidden_tests": """\
from solution import count_lines_words

def test_basic(tmp_path):
    p = tmp_path / "t.txt"
    p.write_text("the quick fox\\njumps over\\n")
    assert count_lines_words(p) == (2, 5)

def test_empty(tmp_path):
    p = tmp_path / "e.txt"
    p.write_text("")
    assert count_lines_words(p) == (0, 0)

def test_single_line(tmp_path):
    p = tmp_path / "s.txt"
    p.write_text("hello world")
    assert count_lines_words(p) == (1, 2)
""",
                },
            ],
        },
        {
            "slug": "modules-stdlib",
            "title": "Modules & the Standard Library",
            "description": "import, packages, venvs, and batteries included.",
            "badge": {"id": "module-navigator", "name": "Module Navigator", "icon": "🧭"},
            "missions": [
                {
                    "slug": "modules-math",
                    "title": "Importing Power",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
A **module** is a `.py` file; a **package** is a directory of modules with
an `__init__.py`. Import styles:

```python
import math                    # math.pi
from math import hypot         # hypot(3, 4)
from datetime import date      # namespaced, explicit
```

Every project should run inside a **virtual environment**
(`python -m venv .venv && source .venv/bin/activate`) so its dependencies
don't pollute the system. The standard library is huge — `math`,
`datetime`, `itertools`, `functools`, `collections`, `pathlib` cover most
daily needs before you ever `pip install`.
""",
                    "prompt_md": """\
Using the `math` module, write:

1. `circle_area(radius)` — area of a circle (use `math.pi`).
2. `hypotenuse(a, b)` — length of the hypotenuse (use `math.hypot`).
""",
                    "starter_code": (
                        "import math\n\n\n"
                        "def circle_area(radius):\n    ...\n\n\n"
                        "def hypotenuse(a, b):\n    ...\n"
                    ),
                    "hidden_tests": """\
import math
from solution import circle_area, hypotenuse

def test_circle():
    assert abs(circle_area(1) - math.pi) < 1e-9

def test_circle_scaled():
    assert abs(circle_area(2) - 4 * math.pi) < 1e-9

def test_hypotenuse():
    assert hypotenuse(3, 4) == 5.0
""",
                },
                {
                    "slug": "modules-boss",
                    "title": "Boss: Time Traveler",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `days_between(start, end)` where both arguments are date strings in
`"YYYY-MM-DD"` format. Return the number of days from `start` to `end` as
an `int` (negative if `end` is earlier). Use the `datetime` module.
""",
                    "starter_code": "def days_between(start, end):\n    ...\n",
                    "hidden_tests": """\
from solution import days_between

def test_forward():
    assert days_between("2026-01-01", "2026-01-31") == 30

def test_same_day():
    assert days_between("2026-07-05", "2026-07-05") == 0

def test_backward():
    assert days_between("2026-02-01", "2026-01-01") == -31

def test_across_year():
    assert days_between("2025-12-31", "2026-01-01") == 1
""",
                },
            ],
        },
        {
            "slug": "intro-pytest",
            "title": "Intro to pytest",
            "description": "Assertions, test functions, and pytest.raises.",
            "badge": {"id": "test-tactician", "name": "Test Tactician", "icon": "🧪"},
            "missions": [
                {
                    "slug": "pytest-basics",
                    "title": "Thinking in Tests",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
`pytest` discovers functions named `test_*` and runs their plain `assert`
statements:

```python
def test_add():
    assert add(2, 2) == 4

def test_rejects_negatives():
    with pytest.raises(ValueError):
        add(-1, 1)
```

`pytest.raises` asserts that a block raises a specific exception — the
standard way to test error paths. Every challenge you've beaten so far was
graded by a hidden pytest suite exactly like this. Now write code that's
*designed* to be tested: validate inputs and raise precise exceptions.
""",
                    "prompt_md": """\
Write `validate_age(age)`:

- returns `age` unchanged if it's an `int` between 0 and 130 inclusive
- raises `TypeError` if `age` is not an `int` (`bool` doesn't count!)
- raises `ValueError` if it's out of range
""",
                    "starter_code": "def validate_age(age):\n    ...\n",
                    "hidden_tests": """\
import pytest
from solution import validate_age

def test_valid():
    assert validate_age(30) == 30

def test_bounds():
    assert validate_age(0) == 0
    assert validate_age(130) == 130

def test_type_error():
    with pytest.raises(TypeError):
        validate_age("30")

def test_bool_rejected():
    with pytest.raises(TypeError):
        validate_age(True)

def test_value_error():
    with pytest.raises(ValueError):
        validate_age(131)
""",
                },
                {
                    "slug": "pytest-boss",
                    "title": "Boss: The Bank Vault",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `transfer(balances, src, dst, amount)` operating on a dict of
account → balance:

- moves `amount` from `src` to `dst`, mutating and returning `balances`
- raises `KeyError` if either account doesn't exist
- raises `ValueError` if `amount` is not positive or exceeds the source
  balance (and in that case balances must be left untouched)
""",
                    "starter_code": "def transfer(balances, src, dst, amount):\n    ...\n",
                    "hidden_tests": """\
import pytest
from solution import transfer

def test_moves_money():
    b = {"a": 100, "b": 0}
    assert transfer(b, "a", "b", 40) == {"a": 60, "b": 40}

def test_missing_account():
    with pytest.raises(KeyError):
        transfer({"a": 10}, "a", "ghost", 5)

def test_insufficient():
    b = {"a": 10, "b": 0}
    with pytest.raises(ValueError):
        transfer(b, "a", "b", 11)
    assert b == {"a": 10, "b": 0}

def test_non_positive():
    with pytest.raises(ValueError):
        transfer({"a": 10, "b": 0}, "a", "b", 0)
""",
                },
            ],
        },
        {
            "slug": "tier2-boss-battle",
            "title": "Boss Battle: The Foundry Trial",
            "description": "Timed, hint-free, hidden tests. Pass to unlock the next realm.",
            "is_boss_battle": True,
            "badge": {"id": "craftsman-forged", "name": "Craftsman Forged", "icon": "🔨"},
            "missions": [
                {
                    "slug": "tier2-foundry",
                    "title": "The Foundry Trial",
                    "kind": "tier_boss",
                    "xp": 200,
                    "time_limit_seconds": 900,
                    "prompt_md": """\
**⏱ Timed Boss Battle — 15 minutes, no hints, hidden test suite.**

Build a `ShoppingCart` class:

- `add(name, price, qty=1)` — add items (adding an existing name
  accumulates its quantity; price is per unit)
- `remove(name)` — remove a line entirely; raises `KeyError` if absent
- `total()` — sum of `price × qty` over all lines
- `len(cart)` — total number of **units** in the cart
""",
                    "starter_code": "class ShoppingCart:\n    def __init__(self):\n        ...\n",
                    "hidden_tests": """\
import pytest
from solution import ShoppingCart

def test_total():
    c = ShoppingCart()
    c.add("sword", 100.0, 1)
    c.add("potion", 10.0, 3)
    assert c.total() == 130.0

def test_accumulates():
    c = ShoppingCart()
    c.add("potion", 10.0, 1)
    c.add("potion", 10.0, 2)
    assert len(c) == 3
    assert c.total() == 30.0

def test_remove():
    c = ShoppingCart()
    c.add("sword", 100.0)
    c.remove("sword")
    assert c.total() == 0
    assert len(c) == 0

def test_remove_missing():
    with pytest.raises(KeyError):
        ShoppingCart().remove("ghost")

def test_default_qty():
    c = ShoppingCart()
    c.add("shield", 50.0)
    assert len(c) == 1
""",
                },
            ],
        },
    ],
}
