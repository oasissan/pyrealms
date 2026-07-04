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
                    "hidden_tests": """\
from solution import make_greeting

def test_default():
    assert make_greeting("Ada") == "Hello, Ada!"

def test_custom():
    assert make_greeting("Grace", "Salute") == "Salute, Grace!"

def test_keyword():
    assert make_greeting(name="Guido", greeting="Yo") == "Yo, Guido!"
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
                    "hidden_tests": """\
from solution import clean_username

def test_basic():
    assert clean_username("  Ada Lovelace ") == "ada_lovelace"

def test_already_clean():
    assert clean_username("guido") == "guido"

def test_multiple_words():
    assert clean_username("Grace Brewster Hopper") == "grace_brewster_hopper"
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
                    "hidden_tests": """\
from solution import safe_divide

def test_normal():
    assert safe_divide(10, 4) == 2.5

def test_zero():
    assert safe_divide(1, 0) is None

def test_negative():
    assert safe_divide(-9, 3) == -3.0
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
                },
            ],
        },
    ],
}
