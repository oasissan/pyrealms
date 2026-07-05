"""Tier 1 — Foundations (Novice). Curriculum seed data."""

TIER = {
    "slug": "foundations",
    "title": "Foundations",
    "subtitle": "The Novice Realm",
    "order": 1,
    "min_level": 1,
    "quests": [
        {
            "slug": "variables-types",
            "title": "Variables, Types & Operators",
            "description": "Name your data, know its type, bend it with operators.",
            "badge": {"id": "type-tamer", "name": "Type Tamer", "icon": "🐍"},
            "missions": [
                {
                    "slug": "variables-types-basics",
                    "title": "First Steps: Numbers & Names",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
A **variable** is a name bound to a value: `x = 5`. Python is dynamically
typed — the *value* has a type, the name doesn't. The core scalar types:

- `int` — whole numbers, arbitrary precision (`2 ** 100` just works)
- `float` — decimals (`3.14`), with the usual binary rounding caveats
- `str` — text (`"hello"`)
- `bool` — `True`/`False` (secretly a subclass of `int`!)

Arithmetic operators: `+ - * /` plus three interview regulars:

- `//` floor division: `7 // 2 == 3`
- `%` modulo: `7 % 2 == 1`
- `**` power: `2 ** 3 == 8`

Note `/` **always** returns a `float` in Python 3, even for `4 / 2`.
""",
                    "prompt_md": """\
Write `celsius_to_fahrenheit(celsius)` that converts a temperature using
`F = C × 9/5 + 32` and returns the result as a **float**.
""",
                    "starter_code": "def celsius_to_fahrenheit(celsius):\n    ...\n",
                    "example_tests": """\
from solution import celsius_to_fahrenheit

def test_freezing():
    assert celsius_to_fahrenheit(0) == 32.0

def test_boiling():
    assert celsius_to_fahrenheit(100) == 212.0
""",
                    "hidden_tests": """\
from solution import celsius_to_fahrenheit

def test_freezing():
    assert celsius_to_fahrenheit(0) == 32.0

def test_boiling():
    assert celsius_to_fahrenheit(100) == 212.0

def test_crossover_point():
    assert celsius_to_fahrenheit(-40) == -40.0

def test_returns_float():
    assert isinstance(celsius_to_fahrenheit(0), float)
""",
                    "solution_md": """\
```python
def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32
```

**Why:** straight from the formula. Because `/` always yields a `float` in
Python 3, the result is a float even when the maths comes out even — which is
exactly what `test_returns_float` checks.
""",
                },
                {
                    "slug": "variables-types-boss",
                    "title": "Boss: The Type Tamer",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `describe(value)` that returns the name of the value's type as a
string — e.g. `describe(3)` returns `"int"`. It must distinguish `bool`
from `int` correctly.
""",
                    "starter_code": "def describe(value):\n    ...\n",
                    "hidden_tests": """\
from solution import describe

def test_int():
    assert describe(3) == "int"

def test_float():
    assert describe(3.0) == "float"

def test_str():
    assert describe("hi") == "str"

def test_bool_is_not_int():
    assert describe(True) == "bool"

def test_none():
    assert describe(None) == "NoneType"
""",
                    "solution_md": """\
```python
def describe(value):
    return type(value).__name__
```

**Why:** `type(value)` is the exact class, and `.__name__` is its bare name —
`"NoneType"` for `None`, and crucially `"bool"` (not `"int"`) for `True`,
because `type()` returns the *real* class even though `bool` subclasses `int`.
An `isinstance` ladder would wrongly report `True` as an `int`.
""",
                },
            ],
        },
        {
            "slug": "control-flow",
            "title": "Control Flow",
            "description": "if/elif/else, while, for, break and continue.",
            "badge": {"id": "flow-master", "name": "Flow Master", "icon": "🌊"},
            "missions": [
                {
                    "slug": "control-flow-fizzbuzz",
                    "title": "Branching & Loops",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
Python branches with `if` / `elif` / `else` and loops with `for` and
`while`. A `for` loop iterates over anything iterable:

```python
for i in range(1, 4):   # 1, 2, 3 — stop is exclusive
    print(i)
```

`break` exits a loop early, `continue` skips to the next iteration.
Conditions chain naturally: `if n % 3 == 0 and n % 5 == 0`. Order matters —
check the most specific condition first.
""",
                    "prompt_md": """\
Write `fizzbuzz(n)` that returns a **list** of strings for the numbers
`1..n`: `"FizzBuzz"` for multiples of 15, `"Fizz"` for multiples of 3,
`"Buzz"` for multiples of 5, otherwise the number as a string.
""",
                    "starter_code": "def fizzbuzz(n):\n    ...\n",
                    "example_tests": """\
from solution import fizzbuzz

def test_first_five():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]

def test_fifteen():
    assert fizzbuzz(15)[-1] == "FizzBuzz"
""",
                    "hidden_tests": """\
from solution import fizzbuzz

def test_first_five():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]

def test_fifteen():
    assert fizzbuzz(15)[-1] == "FizzBuzz"

def test_length():
    assert len(fizzbuzz(30)) == 30

def test_all_strings():
    assert all(isinstance(x, str) for x in fizzbuzz(20))
""",
                    "solution_md": """\
```python
def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out
```

**Why:** the `% 15` case comes *first* — it's the most specific, and checking
it before `% 3` / `% 5` is what stops a multiple of fifteen from matching
`"Fizz"` early. `range(1, n + 1)` covers `1..n` inclusive.
""",
                },
                {
                    "slug": "control-flow-boss",
                    "title": "Boss: The Grade Gate",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `grade_letter(score)`:
`90–100 → "A"`, `80–89 → "B"`, `70–79 → "C"`, `60–69 → "D"`,
`0–59 → "F"`. Anything below 0 or above 100 returns `"invalid"`.
""",
                    "starter_code": "def grade_letter(score):\n    ...\n",
                    "hidden_tests": """\
from solution import grade_letter

def test_boundaries():
    assert grade_letter(90) == "A"
    assert grade_letter(89) == "B"
    assert grade_letter(80) == "B"
    assert grade_letter(60) == "D"

def test_extremes():
    assert grade_letter(100) == "A"
    assert grade_letter(0) == "F"

def test_invalid():
    assert grade_letter(101) == "invalid"
    assert grade_letter(-1) == "invalid"
""",
                    "solution_md": """\
```python
def grade_letter(score):
    if score < 0 or score > 100:
        return "invalid"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
```

**Why:** validate the out-of-range case first, then test the thresholds from
highest down. Descending order means each `>=` only has to name the floor of
its band — the higher bands have already been ruled out.
""",
                },
            ],
        },
        {
            "slug": "functions-scope",
            "title": "Functions & Scope",
            "description": "def, return, default arguments, and the LEGB rule.",
            "badge": {"id": "function-forger", "name": "Function Forger", "icon": "⚒️"},
            "missions": [
                {
                    "slug": "functions-basics",
                    "title": "Defining Functions",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
Functions are defined with `def` and return values with `return` (a bare
function returns `None`). Parameters can have **defaults**:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"
```

Scope follows **LEGB**: Local → Enclosing → Global → Built-in. A name
assigned inside a function is local unless declared `global` or
`nonlocal`. Interview trap: default values are evaluated **once**, at
definition time — never use a mutable default like `def f(x, acc=[])`.
""",
                    "prompt_md": """\
Write `make_greeting(name, greeting="Hello")` that returns
`"<greeting>, <name>!"` — e.g. `make_greeting("Ada")` returns
`"Hello, Ada!"`.
""",
                    "starter_code": "def make_greeting(name, greeting=\"Hello\"):\n    ...\n",
                    "example_tests": """\
from solution import make_greeting

def test_default():
    assert make_greeting("Ada") == "Hello, Ada!"

def test_custom():
    assert make_greeting("Grace", "Salute") == "Salute, Grace!"
""",
                    "hidden_tests": """\
from solution import make_greeting

def test_default():
    assert make_greeting("Ada") == "Hello, Ada!"

def test_custom():
    assert make_greeting("Grace", "Salute") == "Salute, Grace!"

def test_keyword():
    assert make_greeting(name="Guido", greeting="Yo") == "Yo, Guido!"
""",
                    "solution_md": """\
```python
def make_greeting(name, greeting="Hello"):
    return f"{greeting}, {name}!"
```

**Why:** the default `greeting="Hello"` fills in when the caller omits it, and
because callers can pass by keyword (`greeting="Yo"`), the parameter names are
part of your function's public interface — choose them deliberately.
""",
                },
                {
                    "slug": "functions-boss",
                    "title": "Boss: Higher Ground",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Functions are first-class values. Write `apply_twice(func, value)` that
applies `func` to `value` two times: `apply_twice(f, x)` returns
`f(f(x))`.
""",
                    "starter_code": "def apply_twice(func, value):\n    ...\n",
                    "hidden_tests": """\
from solution import apply_twice

def test_add():
    assert apply_twice(lambda x: x + 3, 10) == 16

def test_string():
    assert apply_twice(str.upper, "hi") == "HI"

def test_double():
    assert apply_twice(lambda x: x * 2, 1) == 4
""",
                    "solution_md": """\
```python
def apply_twice(func, value):
    return func(func(value))
```

**Why:** `func` is just a value you can call. Passing functions as arguments
is the foundation of `map`, `sorted(key=...)`, decorators, and callbacks —
everything "higher-order" starts here.
""",
                },
            ],
        },
        {
            "slug": "strings",
            "title": "Strings",
            "description": "Slicing, methods, f-strings, immutability.",
            "badge": {"id": "string-sorcerer", "name": "String Sorcerer", "icon": "🪄"},
            "missions": [
                {
                    "slug": "strings-clean",
                    "title": "String Surgery",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
Strings are **immutable** sequences — every method returns a *new* string.
The workhorses:

- `s.strip()` — trim whitespace from both ends
- `s.lower()` / `s.upper()` — case conversion
- `s.replace(old, new)` — substitution
- `s.split(sep)` / `sep.join(parts)` — the classic pair
- Slicing: `s[1:4]`, `s[::-1]` (reverse!)

f-strings interpolate expressions: `f"{name}: {score * 2}"`. Chaining
methods reads naturally: `raw.strip().lower()`.
""",
                    "prompt_md": """\
Write `clean_username(raw)` that strips surrounding whitespace,
lowercases, and replaces each space **between words** with an underscore.
`clean_username("  Ada Lovelace ")` returns `"ada_lovelace"`.
""",
                    "starter_code": "def clean_username(raw):\n    ...\n",
                    "example_tests": """\
from solution import clean_username

def test_basic():
    assert clean_username("  Ada Lovelace ") == "ada_lovelace"

def test_multiple_words():
    assert clean_username("Grace Brewster Hopper") == "grace_brewster_hopper"
""",
                    "hidden_tests": """\
from solution import clean_username

def test_basic():
    assert clean_username("  Ada Lovelace ") == "ada_lovelace"

def test_already_clean():
    assert clean_username("guido") == "guido"

def test_multiple_words():
    assert clean_username("Grace Brewster Hopper") == "grace_brewster_hopper"
""",
                    "solution_md": """\
```python
def clean_username(raw):
    return raw.strip().lower().replace(" ", "_")
```

**Why:** order matters — `strip()` first removes the *surrounding* spaces so
they never become underscores, then the inner `replace` only touches the
spaces *between* words. Chaining reads as a clean left-to-right pipeline.
""",
                },
                {
                    "slug": "strings-boss",
                    "title": "Boss: The Mirror Test",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `is_palindrome(text)` that returns `True` if the text reads the same
forwards and backwards, **ignoring case and any non-alphanumeric
characters**. `"A man, a plan, a canal: Panama"` is a palindrome.
""",
                    "starter_code": "def is_palindrome(text):\n    ...\n",
                    "hidden_tests": """\
from solution import is_palindrome

def test_classic():
    assert is_palindrome("A man, a plan, a canal: Panama") is True

def test_simple_false():
    assert is_palindrome("python") is False

def test_case_insensitive():
    assert is_palindrome("RaceCar") is True

def test_empty():
    assert is_palindrome("") is True
""",
                    "solution_md": """\
```python
def is_palindrome(text):
    cleaned = [c.lower() for c in text if c.isalnum()]
    return cleaned == cleaned[::-1]
```

**Why:** first reduce the text to just its lowercased alphanumeric characters,
then compare that against its own reverse (`[::-1]`). Filtering *before*
comparing is what lets punctuation and case fall away cleanly.
""",
                },
            ],
        },
        {
            "slug": "collections",
            "title": "Core Collections",
            "description": "list, tuple, dict, set — and when to reach for each.",
            "badge": {"id": "collection-keeper", "name": "Collection Keeper", "icon": "🧺"},
            "missions": [
                {
                    "slug": "collections-count",
                    "title": "Lists & Dicts in Anger",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
The big four:

- `list` — ordered, mutable: `[1, 2, 3]`
- `tuple` — ordered, **immutable** (hashable if contents are): `(1, 2)`
- `dict` — key → value mapping, insertion-ordered since 3.7: `{"a": 1}`
- `set` — unordered unique values, O(1) membership: `{1, 2, 3}`

Dict patterns you'll use daily:

```python
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
```

`d.get(key, default)` avoids `KeyError`; `key in d` tests membership.
""",
                    "prompt_md": """\
Write `count_words(text)` that lowercases the text, splits on whitespace,
and returns a dict mapping each word to how many times it appears.
""",
                    "starter_code": "def count_words(text):\n    ...\n",
                    "example_tests": """\
from solution import count_words

def test_basic():
    assert count_words("the cat and the hat") == {
        "the": 2, "cat": 1, "and": 1, "hat": 1
    }

def test_case_insensitive():
    assert count_words("Go go GO") == {"go": 3}
""",
                    "hidden_tests": """\
from solution import count_words

def test_basic():
    assert count_words("the cat and the hat") == {
        "the": 2, "cat": 1, "and": 1, "hat": 1
    }

def test_case_insensitive():
    assert count_words("Go go GO") == {"go": 3}

def test_empty():
    assert count_words("") == {}
""",
                    "solution_md": """\
```python
def count_words(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

**Why:** `.get(word, 0)` supplies a starting count so the first sighting of a
word doesn't `KeyError`. This is *the* tallying idiom — and later you'll meet
`collections.Counter`, which does exactly this in one line.
""",
                },
                {
                    "slug": "collections-boss",
                    "title": "Boss: Keeper of Order",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `unique_in_order(items)` that returns a **list** of the unique items
in their first-seen order. `unique_in_order([3, 1, 3, 2, 1])` returns
`[3, 1, 2]`. (A plain `set` won't cut it — order matters.)
""",
                    "starter_code": "def unique_in_order(items):\n    ...\n",
                    "hidden_tests": """\
from solution import unique_in_order

def test_numbers():
    assert unique_in_order([3, 1, 3, 2, 1]) == [3, 1, 2]

def test_strings():
    assert unique_in_order(["b", "a", "b", "c"]) == ["b", "a", "c"]

def test_empty():
    assert unique_in_order([]) == []

def test_returns_list():
    assert isinstance(unique_in_order((1, 1, 2)), list)
""",
                    "solution_md": """\
```python
def unique_in_order(items):
    return list(dict.fromkeys(items))
```

**Why:** `dict.fromkeys` builds a dict whose keys are the items — duplicates
collapse automatically, and since dicts keep insertion order, the keys come
back first-seen. Wrapping in `list()` drops the (unused) values. A `set` would
dedupe too, but scramble the order.
""",
                },
            ],
        },
        {
            "slug": "iteration-tools",
            "title": "enumerate & zip",
            "description": "Loop with an index, and walk two sequences together.",
            "badge": {"id": "iteration-initiate", "name": "Iteration Initiate", "icon": "🔁"},
            "missions": [
                {
                    "slug": "iteration-enumerate",
                    "title": "Counting While You Loop",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
Reaching for `range(len(xs))` to get an index is a code smell. **`enumerate`**
hands you the index *and* the item, and its `start` argument sets where the
count begins:

```python
for i, item in enumerate(items, start=1):
    print(f"{i}: {item}")     # 1-based numbering
```

Its sibling **`zip`** walks several sequences in lockstep, stopping at the
shortest:

```python
for name, score in zip(names, scores):
    ...
dict(zip(keys, values))       # build a dict from two lists
```

Between them, these two retire almost every manual index you'd ever write.
""",
                    "prompt_md": """\
Write `numbered(items)` that returns a list of strings numbering each item
from **1**, formatted as `"1. apple"`. `numbered(["a", "b"])` returns
`["1. a", "2. b"]`. Use `enumerate`.
""",
                    "starter_code": "def numbered(items):\n    ...\n",
                    "example_tests": """\
from solution import numbered

def test_basic():
    assert numbered(["a", "b"]) == ["1. a", "2. b"]

def test_empty():
    assert numbered([]) == []
""",
                    "hidden_tests": """\
from solution import numbered

def test_basic():
    assert numbered(["a", "b"]) == ["1. a", "2. b"]

def test_empty():
    assert numbered([]) == []

def test_starts_at_one():
    assert numbered(["apple"]) == ["1. apple"]

def test_longer():
    assert numbered(["x", "y", "z"])[2] == "3. z"
""",
                    "solution_md": """\
```python
def numbered(items):
    return [f"{i}. {item}" for i, item in enumerate(items, start=1)]
```

**Why:** `enumerate(items, start=1)` yields `(1, item)`, `(2, item)`, … so you
get human-friendly 1-based numbering without ever touching `range(len(...))`
or a manual counter.
""",
                },
                {
                    "slug": "iteration-zip-boss",
                    "title": "Boss: The Transposer",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `transpose(rows)` that transposes a matrix given as a list of equal-
length rows: columns become rows. `transpose([[1, 2, 3], [4, 5, 6]])` returns
`[(1, 4), (2, 5), (3, 6)]`.
""",
                    "starter_code": "def transpose(rows):\n    ...\n",
                    "hidden_tests": """\
from solution import transpose

def test_basic():
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [(1, 4), (2, 5), (3, 6)]

def test_square():
    assert transpose([[1, 2], [3, 4]]) == [(1, 3), (2, 4)]

def test_single_row():
    assert transpose([[1, 2, 3]]) == [(1,), (2,), (3,)]
""",
                    "solution_md": """\
```python
def transpose(rows):
    return list(zip(*rows))
```

**Why:** `zip(*rows)` unpacks each row as a separate argument to `zip`, which
then pulls one element from every row at a time — precisely a column. This
`zip(*matrix)` idiom is the canonical one-liner transpose.
""",
                },
            ],
        },
        {
            "slug": "error-handling",
            "title": "Basic Error Handling",
            "description": "try/except/else/finally and failing gracefully.",
            "badge": {"id": "exception-slayer", "name": "Exception Slayer", "icon": "🛡️"},
            "missions": [
                {
                    "slug": "errors-safe-divide",
                    "title": "try / except",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
Errors in Python are **exceptions** — objects that propagate up the call
stack until caught:

```python
try:
    risky()
except ValueError as e:      # catch a specific type — never bare `except:`
    handle(e)
else:
    runs_if_no_exception()
finally:
    always_runs()
```

Catch the *narrowest* exception you can. Common ones: `ValueError` (bad
value), `TypeError` (bad type), `KeyError`/`IndexError` (bad lookup),
`ZeroDivisionError`.
""",
                    "prompt_md": """\
Write `safe_divide(a, b)` that returns `a / b`, or `None` if `b` is zero.
Use `try`/`except`, not an `if` check.
""",
                    "starter_code": "def safe_divide(a, b):\n    ...\n",
                    "example_tests": """\
from solution import safe_divide

def test_normal():
    assert safe_divide(10, 4) == 2.5

def test_zero():
    assert safe_divide(1, 0) is None
""",
                    "hidden_tests": """\
from solution import safe_divide

def test_normal():
    assert safe_divide(10, 4) == 2.5

def test_zero():
    assert safe_divide(1, 0) is None

def test_negative():
    assert safe_divide(-9, 3) == -3.0
""",
                    "solution_md": """\
```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
```

**Why:** the "ask forgiveness, not permission" (EAFP) style Python favours —
attempt the division and catch the *specific* `ZeroDivisionError` rather than
pre-checking `if b == 0`. Catch the narrowest exception that fits.
""",
                },
                {
                    "slug": "errors-boss",
                    "title": "Boss: Graceful Under Fire",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `parse_int_or_default(text, default=0)` that converts `text` to an
`int` and returns it. If conversion fails **for any reason** (bad string,
`None`, a list...), return `default` instead. It must never raise.
""",
                    "starter_code": "def parse_int_or_default(text, default=0):\n    ...\n",
                    "hidden_tests": """\
from solution import parse_int_or_default

def test_valid():
    assert parse_int_or_default("42") == 42

def test_invalid_string():
    assert parse_int_or_default("forty-two") == 0

def test_custom_default():
    assert parse_int_or_default("nope", default=-1) == -1

def test_none_input():
    assert parse_int_or_default(None, default=7) == 7

def test_list_input():
    assert parse_int_or_default([1, 2], default=5) == 5
""",
                    "solution_md": """\
```python
def parse_int_or_default(text, default=0):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default
```

**Why:** a bad string raises `ValueError` while `None`/a list raise
`TypeError`, so catching *both* (as a tuple) covers every failure the prompt
names. It's still narrow and deliberate — not a blanket `except:` that would
also swallow bugs like `KeyboardInterrupt`.
""",
                },
            ],
        },
        {
            "slug": "tier1-boss-battle",
            "title": "Boss Battle: The Gatekeeper",
            "description": "Timed, hint-free, hidden tests. Pass to unlock the next realm.",
            "is_boss_battle": True,
            "badge": {"id": "novice-no-more", "name": "Novice No More", "icon": "⚔️"},
            "missions": [
                {
                    "slug": "tier1-gatekeeper",
                    "title": "The Gatekeeper",
                    "kind": "tier_boss",
                    "xp": 200,
                    "time_limit_seconds": 900,
                    "prompt_md": """\
**⏱ Timed Boss Battle — 15 minutes, no hints, hidden test suite.**

You run a potion shop. Implement **both** functions:

1. `summarize_inventory(pairs)` — takes a list of `(name, quantity)`
   tuples (names may repeat) and returns a dict mapping each name to its
   **total** quantity.
2. `low_stock(inventory, threshold)` — takes such a dict and returns an
   **alphabetically sorted list** of names whose quantity is strictly
   below `threshold`.
""",
                    "starter_code": (
                        "def summarize_inventory(pairs):\n    ...\n\n\n"
                        "def low_stock(inventory, threshold):\n    ...\n"
                    ),
                    "hidden_tests": """\
from solution import summarize_inventory, low_stock

def test_summarize():
    pairs = [("mana", 3), ("health", 5), ("mana", 2)]
    assert summarize_inventory(pairs) == {"mana": 5, "health": 5}

def test_summarize_empty():
    assert summarize_inventory([]) == {}

def test_low_stock_sorted():
    inv = {"mana": 5, "health": 1, "elixir": 2}
    assert low_stock(inv, 3) == ["elixir", "health"]

def test_low_stock_strict():
    assert low_stock({"mana": 3}, 3) == []

def test_combined():
    inv = summarize_inventory([("a", 1), ("b", 9), ("a", 1)])
    assert low_stock(inv, 3) == ["a"]
""",
                    "solution_md": """\
```python
def summarize_inventory(pairs):
    totals = {}
    for name, qty in pairs:
        totals[name] = totals.get(name, 0) + qty
    return totals


def low_stock(inventory, threshold):
    return sorted(
        name for name, qty in inventory.items() if qty < threshold
    )
```

**Why:** `summarize_inventory` is the tally idiom again — accumulate quantities
into a dict with `.get(name, 0)`. `low_stock` filters `.items()` on the strict
`<` (so a quantity *equal* to the threshold is safe) and `sorted` gives the
alphabetical order the tests demand.
""",
                },
            ],
        },
    ],
}
