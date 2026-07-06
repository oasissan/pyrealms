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
            "quiz": [
                {
                    "prompt_md": "What does `[x * x for x in nums if x % 2 == 0]` produce for `nums = [1, 2, 3, 4]`?",
                    "options": ["`[1, 4, 9, 16]`", "`[4, 16]`", "`[2, 4]`", "`[1, 9]`"],
                    "correct": 1,
                    "explanation_md": "The `if` filters to even numbers (`2, 4`), then the output expression squares each — giving `[4, 16]`.",
                },
                {
                    "prompt_md": "In a comprehension, what is the correct reading order of the parts?",
                    "options": [
                        "condition, loop, output expression",
                        "output expression, loop, condition",
                        "loop, output expression, condition",
                        "output expression, condition, loop",
                    ],
                    "correct": 1,
                    "explanation_md": "Read it left to right as *output expression*, then *loop*, then optional *condition*: `[expr for x in xs if cond]`.",
                },
                {
                    "prompt_md": "Which comprehension builds a **dict** mapping each word to its length?",
                    "options": [
                        "`[len(w) for w in words]`",
                        "`{w: len(w) for w in words}`",
                        "`{len(w) for w in words}`",
                        "`(w: len(w) for w in words)`",
                    ],
                    "correct": 1,
                    "explanation_md": "A dict comprehension uses `{key: value for ...}`. `{len(w) for w in words}` (no colon) would be a *set* of lengths.",
                },
                {
                    "prompt_md": "What is the flatten idiom `[x for row in matrix for x in row]` equivalent to?",
                    "options": [
                        "Nested loops: outer `for row`, inner `for x`",
                        "Two independent loops",
                        "A single loop over `matrix`",
                        "A dict comprehension",
                    ],
                    "correct": 0,
                    "explanation_md": "Multiple `for` clauses read in the same order as nested `for` statements: the outer loop (`for row in matrix`) comes first, the inner (`for x in row`) second.",
                },
                {
                    "prompt_md": "What's the rule of thumb for when a comprehension is *too much*?",
                    "options": [
                        "More than 3 items",
                        "Beyond one loop and one `if` — use a real loop",
                        "Any use of a condition",
                        "Whenever it spans one line",
                    ],
                    "correct": 1,
                    "explanation_md": "Comprehensions shine for one loop and one filter. Past that (nested conditions, side effects), a plain `for` loop is clearer.",
                },
            ],
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
                    "example_tests": """\
from solution import squares_of_evens

def test_mixed():
    assert squares_of_evens([1, 2, 3, 4]) == [4, 16]

def test_no_evens():
    assert squares_of_evens([1, 3, 5]) == []
""",
                    "hidden_tests": """\
from solution import squares_of_evens

def test_mixed():
    assert squares_of_evens([1, 2, 3, 4]) == [4, 16]

def test_no_evens():
    assert squares_of_evens([1, 3, 5]) == []

def test_negative():
    assert squares_of_evens([-2, 0, 7]) == [4, 0]
""",
                    "solution_md": """\
```python
def squares_of_evens(nums):
    return [x * x for x in nums if x % 2 == 0]
```

**Why:** one comprehension carries both the filter (`if x % 2 == 0`) and the
transform (`x * x`), reading left to right. `0` is even, so it survives — a
neat reminder that `0 % 2 == 0`.
""",
                },
                {
                    "slug": "comprehensions-boss",
                    "title": "Boss: The Flattener",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `flatten(matrix)` that flattens a list of lists one level deep into a
single list. `flatten([[1, 2], [3], []])` returns `[1, 2, 3]`. A nested
comprehension — `[x for row in matrix for x in row]` — is the clean way here.
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
                    "solution_md": """\
```python
def flatten(matrix):
    return [x for row in matrix for x in row]
```

**Why:** in a nested comprehension the loops read in the *same order* you'd
write them as nested `for` statements — outer (`for row in matrix`) first,
inner (`for x in row`) second. Each inner item is collected in turn, preserving
order.
""",
                },
            ],
        },
        {
            "slug": "type-hints",
            "title": "Type Hints",
            "description": "Annotate signatures for tooling, editors, and readers.",
            "badge": {"id": "type-herald", "name": "Type Herald", "icon": "🏷️"},
            "quiz": [
                {
                    "prompt_md": "Does Python **enforce** type hints at runtime?",
                    "options": [
                        "Yes — a wrong type raises `TypeError`",
                        "No — they're for readers, editors, and type checkers only",
                        "Only inside classes",
                        "Only if you `import typing`",
                    ],
                    "correct": 1,
                    "explanation_md": "Hints are never enforced at runtime; pass the wrong type and Python won't complain. Tools like `mypy` are what flag the mismatch.",
                },
                {
                    "prompt_md": "How do you annotate \"a list of strings\" in modern Python?",
                    "options": ["`List(str)`", "`list[str]`", "`array<str>`", "`str[]`"],
                    "correct": 1,
                    "explanation_md": "Built-in generics like `list[str]`, `dict[str, int]`, and `tuple[int, int]` work directly since Python 3.9 — no `typing` import needed.",
                },
                {
                    "prompt_md": "What does the annotation `int | None` mean?",
                    "options": [
                        "An int that defaults to None",
                        "Either an int or None",
                        "An int or a boolean",
                        "A list of ints",
                    ],
                    "correct": 1,
                    "explanation_md": "`X | None` is the modern spelling of \"either an `X` or nothing\" — the honest return type for a function that might not find a value.",
                },
                {
                    "prompt_md": "Where do a function's type hints get stored?",
                    "options": [
                        "`function.__hints__`",
                        "`function.__annotations__`",
                        "`function.__types__`",
                        "Nowhere — they're discarded",
                    ],
                    "correct": 1,
                    "explanation_md": "Annotations live in the `__annotations__` dict on the function, mapping each parameter (and `return`) to its hint.",
                },
                {
                    "prompt_md": "What's the main practical benefit of adding type hints?",
                    "options": [
                        "The code runs faster",
                        "Documentation and tooling that catches bad calls before runtime",
                        "Reduced memory usage",
                        "Automatic input validation",
                    ],
                    "correct": 1,
                    "explanation_md": "Hints are cheap documentation that never goes stale and lets editors and type checkers catch mistakes early — but they don't affect runtime speed or validate inputs.",
                },
            ],
            "missions": [
                {
                    "slug": "type-hints-basics",
                    "title": "Annotating Signatures",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
**Type hints** annotate what a function expects and returns. Python doesn't
enforce them at runtime — they're for readers, editors, and type checkers like
`mypy`:

```python
def total_price(items: list[float], tax: float = 0.0) -> float:
    return sum(items) * (1 + tax)
```

Built-in generics read naturally: `list[str]`, `dict[str, int]`,
`tuple[int, int]`. The annotations live on the function in `__annotations__`.
Modern Python writes "either a str or None" as `str | None` (no import needed).
Hints are the cheapest documentation you'll ever write, and they never go stale
the way a comment can.
""",
                    "prompt_md": """\
Write `total_length(words)` that returns the summed length of the strings,
annotated as `(words: list[str]) -> int`. Include the type hints — they're
checked.
""",
                    "starter_code": "def total_length(words):\n    ...\n",
                    "example_tests": """\
from solution import total_length

def test_basic():
    assert total_length(["ab", "c"]) == 3

def test_empty():
    assert total_length([]) == 0
""",
                    "hidden_tests": """\
from solution import total_length

def test_basic():
    assert total_length(["ab", "c"]) == 3

def test_empty():
    assert total_length([]) == 0

def test_annotations():
    ann = total_length.__annotations__
    assert ann.get("words") == list[str]
    assert ann.get("return") == int
""",
                    "solution_md": """\
```python
def total_length(words: list[str]) -> int:
    return sum(len(word) for word in words)
```

**Why:** the annotations `list[str]` and `-> int` document intent and let tools
catch a bad call before you run it. They're stored on
`total_length.__annotations__` but never enforced at runtime — pass the wrong
type and Python won't complain; your type checker will.
""",
                },
                {
                    "slug": "type-hints-boss",
                    "title": "Boss: Maybe a Value",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `first_or_none(items)` that returns the first element, or `None` when the
list is empty. Annotate it as `(items: list[int]) -> int | None`.
""",
                    "starter_code": "def first_or_none(items):\n    ...\n",
                    "hidden_tests": """\
from solution import first_or_none

def test_first():
    assert first_or_none([5, 6]) == 5

def test_empty_is_none():
    assert first_or_none([]) is None

def test_annotations():
    ann = first_or_none.__annotations__
    assert ann.get("items") == list[int]
    assert ann.get("return") == (int | None)
""",
                    "solution_md": """\
```python
def first_or_none(items: list[int]) -> int | None:
    return items[0] if items else None
```

**Why:** `int | None` is the modern way to say "an int, or nothing" — the
honest return type for any function that might not find a value. Spelling it out
forces callers (and type checkers) to handle the `None` case instead of being
surprised by it.
""",
                },
            ],
        },
        {
            "slug": "args-kwargs-closures",
            "title": "*args, **kwargs & Closures",
            "description": "Flexible signatures and functions that remember.",
            "badge": {"id": "closure-craftsman", "name": "Closure Craftsman", "icon": "🔒"},
            "quiz": [
                {
                    "prompt_md": "Inside `def f(*args):`, what type is `args`?",
                    "options": ["A list", "A tuple", "A dict", "A set"],
                    "correct": 1,
                    "explanation_md": "`*args` collects extra **positional** arguments into a `tuple`.",
                },
                {
                    "prompt_md": "Inside `def f(**kwargs):`, what type is `kwargs`?",
                    "options": ["A tuple", "A dict", "A list", "A set"],
                    "correct": 1,
                    "explanation_md": "`**kwargs` collects extra **keyword** arguments into a `dict` mapping names to values.",
                },
                {
                    "prompt_md": "In the call `f(*my_list, **my_dict)`, what do the stars do?",
                    "options": [
                        "Collect arguments into args/kwargs",
                        "**Unpack** the list into positional args and the dict into keyword args",
                        "Multiply the arguments",
                        "Nothing — it's a syntax error",
                    ],
                    "correct": 1,
                    "explanation_md": "On the *calling* side the same stars unpack: list elements become positional arguments, dict items become keyword arguments. This is how decorators forward arbitrary arguments.",
                },
                {
                    "prompt_md": "A **closure** is best described as…",
                    "options": [
                        "A function that closes files",
                        "An inner function that remembers variables from its enclosing scope",
                        "A way to end a loop",
                        "A class with no methods",
                    ],
                    "correct": 1,
                    "explanation_md": "A closure is an inner function that captures (\"closes over\") variables from the scope it was defined in, keeping them alive after the outer function returns.",
                },
                {
                    "prompt_md": "Why does `make_counter`'s inner function need `nonlocal count`?",
                    "options": [
                        "To create a new local `count`",
                        "To rebind the *enclosing* `count` instead of shadowing it with a new local",
                        "To make `count` global",
                        "It's optional decoration",
                    ],
                    "correct": 1,
                    "explanation_md": "Assigning to `count` would otherwise create a new local variable. `nonlocal` tells Python to rebind the `count` in the enclosing scope, so the counter actually increments.",
                },
            ],
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
                    "example_tests": """\
from solution import sum_all

def test_three():
    assert sum_all(1, 2, 3) == 6

def test_none():
    assert sum_all() == 0
""",
                    "hidden_tests": """\
from solution import sum_all

def test_three():
    assert sum_all(1, 2, 3) == 6

def test_none():
    assert sum_all() == 0

def test_floats():
    assert sum_all(1.5, 2.5) == 4.0
""",
                    "solution_md": """\
```python
def sum_all(*args):
    return sum(args)
```

**Why:** `*args` gathers every positional argument into a tuple, and `sum`
already returns `0` for an empty one — so the zero-argument case needs no
special handling.
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
                    "solution_md": """\
```python
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter
```

**Why:** the inner `counter` *closes over* `count`, and `nonlocal` lets it
rebind that enclosing variable rather than shadowing it. Each call to
`make_counter` creates a fresh `count`, so the two counters never share state.
""",
                },
            ],
        },
        {
            "slug": "oop-basics",
            "title": "OOP Basics",
            "description": "Classes, inheritance, and dunder methods.",
            "badge": {"id": "object-whisperer", "name": "Object Whisperer", "icon": "🏛️"},
            "quiz": [
                {
                    "prompt_md": "What is `self` in a method definition?",
                    "options": [
                        "The class itself",
                        "The instance the method is called on",
                        "A reserved keyword",
                        "The parent class",
                    ],
                    "correct": 1,
                    "explanation_md": "`self` is the instance — the specific object the method was called on. Its attributes (`self.name`) hold that object's data.",
                },
                {
                    "prompt_md": "When does `__init__` run?",
                    "options": [
                        "Every time any method is called",
                        "When a new instance is constructed",
                        "When the class is defined",
                        "When the object is deleted",
                    ],
                    "correct": 1,
                    "explanation_md": "`__init__` is the initializer: it runs once when you construct an instance (e.g. `Dog(\"Rex\")`), setting up its attributes.",
                },
                {
                    "prompt_md": "Which dunder method controls what `==` does between two objects?",
                    "options": ["`__cmp__`", "`__eq__`", "`__equals__`", "`__is__`"],
                    "correct": 1,
                    "explanation_md": "`__eq__(self, other)` defines equality, letting two distinct objects with the same data compare `==`.",
                },
                {
                    "prompt_md": "Which dunder lets `len(obj)` work on your object?",
                    "options": ["`__size__`", "`__len__`", "`__count__`", "`__length__`"],
                    "correct": 1,
                    "explanation_md": "`__len__(self)` is what `len()` calls. Similarly `__add__` powers `+` and `__repr__` powers `repr()`.",
                },
                {
                    "prompt_md": "What does implementing `__repr__` give you?",
                    "options": [
                        "Faster attribute access",
                        "Control over the string shown by `repr(obj)`",
                        "Automatic equality",
                        "Immutability",
                    ],
                    "correct": 1,
                    "explanation_md": "`__repr__` controls the unambiguous string representation (ideally constructor-style, like `Vector(1, 2)`) shown by `repr()` and in the debugger.",
                },
            ],
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
                    "example_tests": """\
from solution import Rectangle

def test_area():
    assert Rectangle(3, 4).area() == 12

def test_perimeter():
    assert Rectangle(3, 4).perimeter() == 14
""",
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
                    "solution_md": """\
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)
```

**Why:** `__init__` stores the dimensions on `self`, and each method reads them
back. The methods compute on demand rather than caching, so the object stays
correct even if you later allow the width or height to change.
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
                    "solution_md": """\
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
```

**Why:** `__add__` returns a *new* `Vector` (never mutating the operands — see
`test_add_returns_new`), `__eq__` compares by value so two distinct objects with
the same components are equal, and `__repr__` gives the unambiguous
constructor-style string. Together they make `Vector` behave like a built-in.
""",
                },
            ],
        },
        {
            "slug": "dataclasses",
            "title": "Dataclasses",
            "description": "Let @dataclass write __init__, __repr__ and __eq__ for you.",
            "badge": {"id": "dataclass-drafter", "name": "Dataclass Drafter", "icon": "📐"},
            "quiz": [
                {
                    "prompt_md": "Which three methods does `@dataclass` generate for you?",
                    "options": [
                        "`__init__`, `__repr__`, `__eq__`",
                        "`__new__`, `__del__`, `__call__`",
                        "`__str__`, `__hash__`, `__len__`",
                        "`__enter__`, `__exit__`, `__iter__`",
                    ],
                    "correct": 0,
                    "explanation_md": "From the annotated fields, `@dataclass` synthesises a constructor, a readable `__repr__`, and a value-based `__eq__` — the boilerplate you wrote by hand for `Vector`.",
                },
                {
                    "prompt_md": "How does a dataclass know what fields to create?",
                    "options": [
                        "From methods you define",
                        "From the class-level **annotated** attributes (e.g. `x: int`)",
                        "From the `__init__` you write",
                        "From a `fields = [...]` list",
                    ],
                    "correct": 1,
                    "explanation_md": "Each annotated class variable (`x: int`) becomes a field. That single line is all `@dataclass` needs to build the constructor and dunders.",
                },
                {
                    "prompt_md": "How do you give a dataclass field a default value?",
                    "options": [
                        "`balance := 0.0`",
                        "`balance: float = 0.0`",
                        "`default balance = 0.0`",
                        "`balance = float(0.0)`",
                    ],
                    "correct": 1,
                    "explanation_md": "`balance: float = 0.0` makes that field optional, exactly like a normal parameter default.",
                },
                {
                    "prompt_md": "Can a dataclass have your own custom methods too?",
                    "options": [
                        "No — only fields are allowed",
                        "Yes — add methods alongside the fields",
                        "Only static methods",
                        "Only if you drop the decorator",
                    ],
                    "correct": 1,
                    "explanation_md": "Dataclasses aren't just dumb records — you can add real behavior (like a `deposit` method) right next to the generated dunders.",
                },
                {
                    "prompt_md": "What does `repr(Point(1, 2))` produce for a dataclass `Point` with fields `x` and `y`?",
                    "options": ["`\"Point(1, 2)\"`", "`\"Point(x=1, y=2)\"`", "`\"<Point>\"`", "`\"(1, 2)\"`"],
                    "correct": 1,
                    "explanation_md": "The generated `__repr__` names each field: `Point(x=1, y=2)`.",
                },
            ],
            "missions": [
                {
                    "slug": "dataclasses-basics",
                    "title": "@dataclass",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
The `@dataclass` decorator generates the boilerplate a plain data-holding class
needs — `__init__`, `__repr__`, and `__eq__` — from annotated fields:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

That's the whole class. `Point(1, 2)` constructs, `repr` gives
`Point(x=1, y=2)`, and two points with equal fields compare `==`. Fields can
have defaults (`z: int = 0`), and you can still add your own methods. It's the
idiomatic way to model records — far less noise than writing the dunders by
hand (compare the previous quest's `Vector`).
""",
                    "prompt_md": """\
Using `@dataclass`, define `Point` with two annotated `int` fields `x` and `y`.
Construction (`Point(1, 2)`), equality, and repr must all work automatically.
""",
                    "starter_code": (
                        "from dataclasses import dataclass\n\n\n"
                        "@dataclass\nclass Point:\n    ...\n"
                    ),
                    "example_tests": """\
from solution import Point

def test_construct():
    p = Point(1, 2)
    assert p.x == 1 and p.y == 2

def test_eq():
    assert Point(1, 2) == Point(1, 2)
""",
                    "hidden_tests": """\
from dataclasses import is_dataclass
from solution import Point

def test_construct():
    p = Point(1, 2)
    assert p.x == 1 and p.y == 2

def test_eq():
    assert Point(1, 2) == Point(1, 2)

def test_repr():
    assert repr(Point(1, 2)) == "Point(x=1, y=2)"

def test_is_dataclass():
    assert is_dataclass(Point)
""",
                    "solution_md": """\
```python
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
```

**Why:** the two annotated fields are all `@dataclass` needs to synthesise a
constructor, a value-based `__eq__`, and a readable `__repr__`. You wrote those
three dunders by hand for `Vector`; here they come free.
""",
                },
                {
                    "slug": "dataclasses-boss",
                    "title": "Boss: Fields with Behavior",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Using `@dataclass`, define `Account` with `owner: str` and a `balance: float`
that **defaults to `0.0`**. Add a method `deposit(amount)` that increases the
balance and returns the new balance.
""",
                    "starter_code": (
                        "from dataclasses import dataclass\n\n\n"
                        "@dataclass\nclass Account:\n    ...\n"
                    ),
                    "hidden_tests": """\
from solution import Account

def test_default_balance():
    a = Account("ada")
    assert a.balance == 0.0

def test_deposit():
    a = Account("grace", 10.0)
    assert a.deposit(5.0) == 15.0
    assert a.balance == 15.0

def test_eq():
    assert Account("x", 5.0) == Account("x", 5.0)
""",
                    "solution_md": """\
```python
from dataclasses import dataclass


@dataclass
class Account:
    owner: str
    balance: float = 0.0

    def deposit(self, amount):
        self.balance += amount
        return self.balance
```

**Why:** a field default (`balance: float = 0.0`) makes that argument optional,
exactly like a normal parameter default. Dataclasses aren't just dumb records —
you can hang real behavior like `deposit` right alongside the generated dunders.
""",
                },
            ],
        },
        {
            "slug": "file-io",
            "title": "File I/O & Context Managers",
            "description": "Reading, writing, and the `with` statement.",
            "badge": {"id": "file-wrangler", "name": "File Wrangler", "icon": "📁"},
            "quiz": [
                {
                    "prompt_md": "What is the main guarantee of the `with open(...) as f:` statement?",
                    "options": [
                        "The file loads faster",
                        "The file is closed automatically, even if an exception is raised",
                        "The file can't be modified",
                        "It reads the whole file into memory",
                    ],
                    "correct": 1,
                    "explanation_md": "`with` guarantees cleanup: the file handle is closed when the block exits, whether normally or via an exception. Never `open()` without it in real code.",
                },
                {
                    "prompt_md": "Which mode string opens a file for **writing** (truncating existing content)?",
                    "options": ["`\"r\"`", "`\"w\"`", "`\"a\"`", "`\"x\"`"],
                    "correct": 1,
                    "explanation_md": "`\"w\"` opens for writing and truncates. `\"r\"` reads, `\"a\"` appends to the end.",
                },
                {
                    "prompt_md": "What do you get when you iterate directly over a file object, as in `for line in f:`?",
                    "options": [
                        "One character at a time",
                        "One line at a time",
                        "The whole file as a string",
                        "A list of words",
                    ],
                    "correct": 1,
                    "explanation_md": "File objects are iterators of **lines**, so `for line in f:` streams the file line by line without loading it all into memory.",
                },
                {
                    "prompt_md": "Lines read from a file keep their trailing `\\n`. How do you strip just that newline?",
                    "options": [
                        "`line.strip()`",
                        "`line.rstrip(\"\\n\")`",
                        "`line.replace(line, \"\")`",
                        "`line[:-2]`",
                    ],
                    "correct": 1,
                    "explanation_md": "`rstrip(\"\\n\")` removes only the trailing newline. Plain `strip()` would also remove meaningful leading/trailing spaces.",
                },
                {
                    "prompt_md": "What does `f.read()` return versus iterating the file?",
                    "options": [
                        "The same thing",
                        "`read()` slurps the entire file into one string; iterating streams line by line",
                        "`read()` returns a list of lines",
                        "`read()` only reads one line",
                    ],
                    "correct": 1,
                    "explanation_md": "`f.read()` loads the whole file into a single string (handy for small files), while iterating processes it lazily, one line at a time.",
                },
            ],
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
                    "example_tests": """\
from solution import write_lines, read_lines

def test_round_trip(tmp_path):
    p = tmp_path / "notes.txt"
    write_lines(p, ["alpha", "beta"])
    assert read_lines(p) == ["alpha", "beta"]
""",
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
                    "solution_md": """\
```python
def write_lines(path, lines):
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\\n")


def read_lines(path):
    with open(path) as f:
        return [line.rstrip("\\n") for line in f]
```

**Why:** `with` closes the handle automatically, even if an error interrupts
the loop. Writing appends an explicit `"\\n"` per line; reading strips it back
off so the round-trip is clean.
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
                    "solution_md": """\
```python
def count_lines_words(path):
    with open(path) as f:
        text = f.read()
    if not text:
        return (0, 0)
    return (len(text.splitlines()), len(text.split()))
```

**Why:** reading once into `text` lets both counts come from the same content.
`splitlines()` counts lines without a spurious empty trailing entry, and
`split()` with no argument splits on any run of whitespace — so the empty file
short-circuits cleanly to `(0, 0)`.
""",
                },
            ],
        },
        {
            "slug": "modules-stdlib",
            "title": "Modules & the Standard Library",
            "description": "import, packages, venvs, and batteries included.",
            "badge": {"id": "module-navigator", "name": "Module Navigator", "icon": "🧭"},
            "quiz": [
                {
                    "prompt_md": "What distinguishes a **package** from a plain module?",
                    "options": [
                        "A package is compiled",
                        "A package is a directory of modules (traditionally with an `__init__.py`)",
                        "A package can't be imported",
                        "There's no difference",
                    ],
                    "correct": 1,
                    "explanation_md": "A module is a single `.py` file; a package is a directory grouping modules together, traditionally marked by an `__init__.py`.",
                },
                {
                    "prompt_md": "After `from math import hypot`, how do you call it?",
                    "options": ["`math.hypot(3, 4)`", "`hypot(3, 4)`", "`import.hypot(3, 4)`", "`math.import(hypot)`"],
                    "correct": 1,
                    "explanation_md": "`from math import hypot` binds `hypot` directly into your namespace, so you call it bare as `hypot(3, 4)` (no `math.` prefix).",
                },
                {
                    "prompt_md": "Why should each project run inside a **virtual environment**?",
                    "options": [
                        "It makes Python faster",
                        "So its dependencies stay isolated and don't pollute the system install",
                        "It's required to use `import`",
                        "It encrypts your code",
                    ],
                    "correct": 1,
                    "explanation_md": "A venv (`python -m venv .venv`) keeps each project's packages separate, so different projects can't break each other's dependency versions.",
                },
                {
                    "prompt_md": "Why prefer `math.pi` over typing `3.14159` yourself?",
                    "options": [
                        "It's shorter",
                        "`math.pi` is far more precise than any literal you'd type",
                        "Literals aren't allowed",
                        "It changes value over time",
                    ],
                    "correct": 1,
                    "explanation_md": "`math.pi` carries full floating-point precision — reach for the standard library rather than reinventing (or under-specifying) it.",
                },
                {
                    "prompt_md": "Which of these is part of Python's \"batteries included\" standard library?",
                    "options": ["`numpy`", "`itertools`", "`requests`", "`pandas`"],
                    "correct": 1,
                    "explanation_md": "`itertools` (like `math`, `datetime`, `functools`, `collections`, `pathlib`) ships with Python. The others are third-party packages you'd `pip install`.",
                },
            ],
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
                    "example_tests": """\
import math
from solution import circle_area, hypotenuse

def test_circle():
    assert abs(circle_area(1) - math.pi) < 1e-9

def test_hypotenuse():
    assert hypotenuse(3, 4) == 5.0
""",
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
                    "solution_md": """\
```python
import math


def circle_area(radius):
    return math.pi * radius ** 2


def hypotenuse(a, b):
    return math.hypot(a, b)
```

**Why:** reach for the standard library before reinventing it — `math.pi` is
more precise than any literal you'd type, and `math.hypot` computes
`sqrt(a² + b²)` correctly (and without intermediate overflow) so you don't have
to.
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
                    "solution_md": """\
```python
from datetime import date


def days_between(start, end):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    return (end_date - start_date).days
```

**Why:** `date.fromisoformat` parses the `"YYYY-MM-DD"` string directly, and
subtracting two `date` objects yields a `timedelta` whose `.days` is exactly
the signed day count — leap years and month lengths handled for you.
""",
                },
            ],
        },
        {
            "slug": "collections-module",
            "title": "The collections Module",
            "description": "Counter, defaultdict, and sorting with a key.",
            "badge": {"id": "collections-conjurer", "name": "Collections Conjurer", "icon": "🎒"},
            "quiz": [
                {
                    "prompt_md": "What does `Counter(\"mississippi\")` give you?",
                    "options": [
                        "A sorted string",
                        "A count of each character, e.g. `{'i': 4, 's': 4, 'p': 2, 'm': 1}`",
                        "The length, `11`",
                        "A set of unique letters",
                    ],
                    "correct": 1,
                    "explanation_md": "`Counter` tallies occurrences of each element — it's the hand-rolled counting loop from Tier 1, built in.",
                },
                {
                    "prompt_md": "What does `Counter(words).most_common(3)` return?",
                    "options": [
                        "The 3 rarest words",
                        "The top 3 `(word, count)` pairs by frequency",
                        "3 random words",
                        "The first 3 words",
                    ],
                    "correct": 1,
                    "explanation_md": "`most_common(n)` returns the `n` highest-frequency items as `(element, count)` pairs, ordered most-frequent first.",
                },
                {
                    "prompt_md": "What problem does `defaultdict(list)` solve?",
                    "options": [
                        "It sorts keys automatically",
                        "Missing keys auto-create an empty list, so you can `append` without a guard",
                        "It prevents duplicate keys",
                        "It makes the dict immutable",
                    ],
                    "correct": 1,
                    "explanation_md": "`defaultdict(list)` supplies an empty list the first time a key is touched, eliminating the `if key not in groups` boilerplate before appending.",
                },
                {
                    "prompt_md": "What does the `key` argument to `sorted` do?",
                    "options": [
                        "Picks which dict key to sort",
                        "Maps each item to the value it should be sorted *by*",
                        "Encrypts the sort",
                        "Reverses the order",
                    ],
                    "correct": 1,
                    "explanation_md": "`sorted(xs, key=f)` sorts by `f(item)` for each item — e.g. `key=len` sorts by length without changing the items themselves.",
                },
                {
                    "prompt_md": "What does `sorted(words, key=lambda w: (-len(w), w))` do?",
                    "options": [
                        "Sorts alphabetically only",
                        "Sorts by length **descending**, breaking ties alphabetically",
                        "Sorts by length ascending",
                        "Reverses the list",
                    ],
                    "correct": 1,
                    "explanation_md": "A tuple key sorts by its first element then the second. `-len(w)` flips length to descending; `w` breaks ties alphabetically — all in one stable pass.",
                },
            ],
            "missions": [
                {
                    "slug": "collections-counter",
                    "title": "Counter & friends",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
The `collections` module has purpose-built containers that replace fiddly
hand-rolled dict code:

```python
from collections import Counter, defaultdict

Counter("mississippi")          # {'i': 4, 's': 4, 'p': 2, 'm': 1}
Counter(words).most_common(3)   # top 3 (word, count) pairs

groups = defaultdict(list)      # missing keys auto-create an empty list
groups[key].append(value)       # no more `if key not in groups`
```

Related: **sorting with a key**. `sorted(xs, key=len)` sorts by length;
`key=lambda w: (-len(w), w)` sorts by length descending, then alphabetically.
The key function maps each item to what you want to sort *by*.
""",
                    "prompt_md": """\
Using `collections.Counter`, write `word_frequencies(text)` that lowercases
the text, splits on whitespace, and returns a plain `dict` mapping each word to
its count.
""",
                    "starter_code": (
                        "from collections import Counter\n\n\n"
                        "def word_frequencies(text):\n    ...\n"
                    ),
                    "example_tests": """\
from solution import word_frequencies

def test_basic():
    assert word_frequencies("a b a") == {"a": 2, "b": 1}

def test_case():
    assert word_frequencies("Hi hi") == {"hi": 2}
""",
                    "hidden_tests": """\
from solution import word_frequencies

def test_basic():
    assert word_frequencies("a b a") == {"a": 2, "b": 1}

def test_case():
    assert word_frequencies("Hi hi") == {"hi": 2}

def test_empty():
    assert word_frequencies("") == {}
""",
                    "solution_md": """\
```python
from collections import Counter


def word_frequencies(text):
    return dict(Counter(text.lower().split()))
```

**Why:** `Counter` *is* the tallying loop you wrote by hand back in Tier 1 —
feed it an iterable and it counts. Wrapping in `dict()` returns a plain mapping,
though a `Counter` already compares equal to the equivalent dict.
""",
                },
                {
                    "slug": "collections-sort-boss",
                    "title": "Boss: Rank and File",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `rank_words(words)` that returns the words sorted by length **longest
first**, breaking ties **alphabetically**. `rank_words(["bb", "a", "ccc", "dd"])`
returns `["ccc", "bb", "dd", "a"]`. Use `sorted` with a `key`.
""",
                    "starter_code": "def rank_words(words):\n    ...\n",
                    "hidden_tests": """\
from solution import rank_words

def test_basic():
    assert rank_words(["bb", "a", "ccc", "dd"]) == ["ccc", "bb", "dd", "a"]

def test_alpha_tiebreak():
    assert rank_words(["ab", "ba"]) == ["ab", "ba"]

def test_empty():
    assert rank_words([]) == []
""",
                    "solution_md": """\
```python
def rank_words(words):
    return sorted(words, key=lambda w: (-len(w), w))
```

**Why:** a **tuple key** sorts by its first element, then the second as a
tiebreak. `-len(w)` flips length into descending order (bigger length → smaller
number → sorts first), and `w` then orders equal-length words alphabetically —
all in one stable pass.
""",
                },
            ],
        },
        {
            "slug": "intro-pytest",
            "title": "Intro to pytest",
            "description": "Assertions, test functions, and pytest.raises.",
            "badge": {"id": "test-tactician", "name": "Test Tactician", "icon": "🧪"},
            "quiz": [
                {
                    "prompt_md": "How does pytest decide which functions are tests?",
                    "options": [
                        "Functions decorated with `@test`",
                        "Functions whose names start with `test_`",
                        "Every function in the file",
                        "Functions ending in `_test`",
                    ],
                    "correct": 1,
                    "explanation_md": "pytest auto-discovers functions named `test_*` and runs them — no registration or decorator required.",
                },
                {
                    "prompt_md": "How does pytest check conditions inside a test?",
                    "options": [
                        "`self.assertEqual(...)`",
                        "Plain `assert` statements",
                        "`expect(...)`",
                        "`check(...)`",
                    ],
                    "correct": 1,
                    "explanation_md": "pytest works with Python's built-in `assert` and rewrites it to show a helpful diff on failure — no special assertion methods needed.",
                },
                {
                    "prompt_md": "What is `with pytest.raises(ValueError):` used for?",
                    "options": [
                        "To ignore a ValueError",
                        "To assert that the enclosed block **raises** that exception",
                        "To raise a ValueError manually",
                        "To catch and silence all errors",
                    ],
                    "correct": 1,
                    "explanation_md": "`pytest.raises` asserts the block raises the given exception — the standard way to test error paths. The test *fails* if no such exception is raised.",
                },
                {
                    "prompt_md": "Why must `validate_age` check `isinstance(age, bool)` *before* the `int` check?",
                    "options": [
                        "Booleans are faster to check",
                        "Because `isinstance(True, int)` is `True`, so `True` would sneak through as a valid age",
                        "It's just a style preference",
                        "To catch `None`",
                    ],
                    "correct": 1,
                    "explanation_md": "`bool` is a subclass of `int`, so `True` passes an `isinstance(age, int)` test. You must rule out `bool` explicitly first.",
                },
                {
                    "prompt_md": "What makes code **designed to be tested**?",
                    "options": [
                        "It has no functions",
                        "It validates inputs and raises precise, specific exceptions",
                        "It never raises anything",
                        "It uses global variables",
                    ],
                    "correct": 1,
                    "explanation_md": "Testable code has clear, predictable behavior: it validates inputs and signals failure with precise exceptions you can assert on with `pytest.raises`.",
                },
            ],
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
                    "example_tests": """\
import pytest
from solution import validate_age

def test_valid():
    assert validate_age(30) == 30

def test_type_error():
    with pytest.raises(TypeError):
        validate_age("30")
""",
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
                    "solution_md": """\
```python
def validate_age(age):
    if isinstance(age, bool) or not isinstance(age, int):
        raise TypeError("age must be an int")
    if age < 0 or age > 130:
        raise ValueError("age out of range")
    return age
```

**Why:** the `bool` check comes *first* because `isinstance(True, int)` is
`True` — without ruling out `bool` explicitly, `True` would sneak through as a
valid age. Only after the type is settled do you range-check the value.
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
                    "solution_md": """\
```python
def transfer(balances, src, dst, amount):
    if src not in balances or dst not in balances:
        raise KeyError("unknown account")
    if amount <= 0 or amount > balances[src]:
        raise ValueError("invalid amount")
    balances[src] -= amount
    balances[dst] += amount
    return balances
```

**Why:** all validation happens *before* any mutation — that's what lets the
failure cases leave `balances` untouched (`test_insufficient` checks exactly
this). Checking existence first also means the `balances[src]` comparison can't
itself raise a `KeyError`.
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
                    "solution_md": """\
```python
class ShoppingCart:
    def __init__(self):
        self.lines = {}

    def add(self, name, price, qty=1):
        _, existing = self.lines.get(name, (price, 0))
        self.lines[name] = (price, existing + qty)

    def remove(self, name):
        del self.lines[name]

    def total(self):
        return sum(price * qty for price, qty in self.lines.values())

    def __len__(self):
        return sum(qty for _, qty in self.lines.values())
```

**Why:** each line stores `(price, qty)`; `add` accumulates quantity by reading
the current pair (defaulting to `qty 0`) and adding to it. `del` on a missing
key raises `KeyError` for free — no manual check needed — and `__len__` makes
`len(cart)` return total units by summing the quantities.
""",
                },
            ],
        },
    ],
}
