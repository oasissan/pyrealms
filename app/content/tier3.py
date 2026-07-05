"""Tier 3 — Pythonic Mastery (Journeyman). Curriculum seed data."""

TIER = {
    "slug": "pythonic-mastery",
    "title": "Pythonic Mastery",
    "subtitle": "The Journeyman Realm",
    "order": 3,
    "min_level": 5,
    "quests": [
        {
            "slug": "iterators-generators",
            "title": "Iterators & Generators",
            "description": "yield, lazy evaluation, and the iterator protocol.",
            "badge": {"id": "generator-guru", "name": "Generator Guru", "icon": "♻️"},
            "missions": [
                {
                    "slug": "generators-countdown",
                    "title": "yield: Lazy by Design",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
A function containing `yield` returns a **generator** — it runs lazily,
pausing at each `yield` and resuming on the next `next()`:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

list(countdown(3))   # [3, 2, 1]
```

Generators implement the **iterator protocol** (`__iter__`/`__next__`)
for free, hold O(1) memory regardless of sequence length, and can even be
infinite. Interview staple: explain why `sum(x*x for x in range(10**9))`
doesn't blow up memory but the list version does.
""",
                    "prompt_md": """\
Write a **generator function** `countdown(n)` that yields
`n, n-1, ..., 1`. It must yield lazily — no building a list.
""",
                    "starter_code": "def countdown(n):\n    ...\n",
                    "example_tests": """\
import types
from solution import countdown

def test_values():
    assert list(countdown(3)) == [3, 2, 1]

def test_is_generator():
    assert isinstance(countdown(1), types.GeneratorType)
""",
                    "hidden_tests": """\
import types
from solution import countdown

def test_values():
    assert list(countdown(3)) == [3, 2, 1]

def test_is_generator():
    assert isinstance(countdown(1), types.GeneratorType)

def test_lazy():
    gen = countdown(10**12)  # would OOM if it built a list
    assert next(gen) == 10**12

def test_zero():
    assert list(countdown(0)) == []
""",
                    "solution_md": """\
```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

**Why:** the presence of `yield` makes this a generator function — calling it
runs *none* of the body until you iterate. Each `next()` resumes right after the
last `yield`, so it produces one value at a time and never materialises the full
sequence (that's what `test_lazy` proves with a trillion-length countdown).
""",
                },
                {
                    "slug": "generators-boss",
                    "title": "Boss: The Endless Spiral",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write an **infinite** generator `fibonacci()` yielding
`0, 1, 1, 2, 3, 5, ...` forever. Callers will slice it with
`itertools.islice`.
""",
                    "starter_code": "def fibonacci():\n    ...\n",
                    "hidden_tests": """\
from itertools import islice
from solution import fibonacci

def test_first_eight():
    assert list(islice(fibonacci(), 8)) == [0, 1, 1, 2, 3, 5, 8, 13]

def test_independent_iterators():
    a, b = fibonacci(), fibonacci()
    next(a)
    assert next(b) == 0

def test_goes_far():
    assert next(islice(fibonacci(), 30, 31)) == 832040
""",
                    "solution_md": """\
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

**Why:** an infinite `while True` loop is safe *because* the generator is lazy —
it only computes as far as the caller pulls. The tuple assignment
`a, b = b, a + b` advances both numbers in one atomic step, and each call to
`fibonacci()` gets its own independent `a`/`b`.
""",
                },
            ],
        },
        {
            "slug": "decorators",
            "title": "Decorators",
            "description": "Functions wrapping functions, done properly with functools.wraps.",
            "badge": {"id": "decorator-wizard", "name": "Decorator Wizard", "icon": "🎩"},
            "missions": [
                {
                    "slug": "decorators-basics",
                    "title": "Wrapping Functions",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
A decorator takes a function and returns a replacement:

```python
import functools

def logged(func):
    @functools.wraps(func)          # preserves __name__, __doc__...
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a, b):
    return a + b
```

`@logged` is just sugar for `add = logged(add)`. **Always** use
`functools.wraps` — without it, the wrapped function's identity
(`__name__`, docstring, signature for introspection) is lost, which is a
classic interview question.
""",
                    "prompt_md": """\
Write a decorator `shout(func)` that uppercases whatever string the
decorated function returns. It must forward any arguments and preserve the
function's `__name__` via `functools.wraps`.
""",
                    "starter_code": "import functools\n\n\ndef shout(func):\n    ...\n",
                    "example_tests": """\
from solution import shout

@shout
def greet(name):
    return f"hello {name}"

def test_uppercases():
    assert greet("ada") == "HELLO ADA"

def test_wraps_preserves_name():
    assert greet.__name__ == "greet"
""",
                    "hidden_tests": """\
from solution import shout

@shout
def greet(name):
    return f"hello {name}"

def test_uppercases():
    assert greet("ada") == "HELLO ADA"

def test_forwards_kwargs():
    @shout
    def echo(text="hi"):
        return text
    assert echo(text="ok") == "OK"

def test_wraps_preserves_name():
    assert greet.__name__ == "greet"
""",
                    "solution_md": """\
```python
import functools


def shout(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper
```

**Why:** `wrapper` forwards every argument with `*args, **kwargs`, calls the
original, and uppercases its result. `@functools.wraps(func)` copies the
original's `__name__`/docstring onto `wrapper`, so the decorated function still
introspects as `greet` rather than `wrapper`.
""",
                },
                {
                    "slug": "decorators-boss",
                    "title": "Boss: The Memory Palace",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write a decorator `memoize(func)` that caches results by positional
arguments, so repeat calls with the same arguments never re-execute the
function. Preserve `__name__` with `functools.wraps`.
""",
                    "starter_code": "import functools\n\n\ndef memoize(func):\n    ...\n",
                    "hidden_tests": """\
from solution import memoize

def test_caches():
    calls = []

    @memoize
    def square(x):
        calls.append(x)
        return x * x

    assert square(4) == 16
    assert square(4) == 16
    assert calls == [4]

def test_distinct_args():
    @memoize
    def add(a, b):
        return a + b
    assert add(1, 2) == 3
    assert add(2, 1) == 3

def test_name_preserved():
    @memoize
    def thing():
        return 1
    assert thing.__name__ == "thing"
""",
                    "solution_md": """\
```python
import functools


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper
```

**Why:** the `cache` dict lives in the closure, keyed by the `args` tuple —
which is hashable, so it works as a dict key directly. A cache miss computes and
stores; a hit returns instantly (`test_caches` verifies the function body ran
only once). This is `functools.lru_cache` in miniature.
""",
                },
            ],
        },
        {
            "slug": "context-managers",
            "title": "Custom Context Managers",
            "description": "__enter__/__exit__ and @contextmanager.",
            "badge": {"id": "context-commander", "name": "Context Commander", "icon": "🚪"},
            "missions": [
                {
                    "slug": "context-suppress",
                    "title": "The Protocol Behind `with`",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
`with expr as x:` calls `expr.__enter__()` (its return value becomes `x`)
and guarantees `expr.__exit__(exc_type, exc, tb)` runs afterwards. If
`__exit__` returns a truthy value, the exception is **swallowed**:

```python
class Suppress:
    def __init__(self, exc_type):
        self.exc_type = exc_type
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return exc_type is not None and issubclass(exc_type, self.exc_type)
```

The `contextlib.contextmanager` decorator offers a generator shortcut:
code before `yield` is setup, after is teardown (wrap the `yield` in
`try/finally` for guaranteed cleanup).
""",
                    "prompt_md": """\
Re-implement `contextlib.suppress` as a **class** `Suppress(exc_type)`
usable as `with Suppress(ValueError): ...`. It swallows exceptions of the
given type (including subclasses) and lets everything else propagate.
Don't import contextlib.
""",
                    "starter_code": "class Suppress:\n    def __init__(self, exc_type):\n        ...\n",
                    "example_tests": """\
from solution import Suppress

def test_swallows():
    with Suppress(ValueError):
        raise ValueError("gone")

def test_subclass_swallowed():
    with Suppress(ArithmeticError):
        raise ZeroDivisionError
""",
                    "hidden_tests": """\
import pytest
from solution import Suppress

def test_swallows():
    with Suppress(ValueError):
        raise ValueError("gone")

def test_subclass_swallowed():
    with Suppress(ArithmeticError):
        raise ZeroDivisionError

def test_others_propagate():
    with pytest.raises(KeyError):
        with Suppress(ValueError):
            raise KeyError("boom")

def test_no_exception_ok():
    with Suppress(ValueError):
        pass
""",
                    "solution_md": """\
```python
class Suppress:
    def __init__(self, exc_type):
        self.exc_type = exc_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return exc_type is not None and issubclass(exc_type, self.exc_type)
```

**Why:** the magic is `__exit__`'s return value — returning **truthy** tells
Python to swallow the exception. `issubclass(exc_type, self.exc_type)` matches
the target type *and its subclasses* (so `ZeroDivisionError` is caught by
`Suppress(ArithmeticError)`), while any other exception yields `False` and
propagates.
""",
                },
                {
                    "slug": "context-boss",
                    "title": "Boss: The Rollback Ritual",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Using `contextlib.contextmanager`, write `transaction(data)` for a dict:
inside the `with` block the caller mutates `data` freely; if the block
raises, `data` is restored to its state from before the block (and the
exception propagates). If it completes, changes stick.
""",
                    "starter_code": (
                        "from contextlib import contextmanager\n\n\n"
                        "@contextmanager\ndef transaction(data):\n    ...\n"
                    ),
                    "hidden_tests": """\
import pytest
from solution import transaction

def test_commit():
    d = {"gold": 10}
    with transaction(d):
        d["gold"] = 99
    assert d == {"gold": 99}

def test_rollback():
    d = {"gold": 10}
    with pytest.raises(RuntimeError):
        with transaction(d):
            d["gold"] = 0
            d["cursed"] = True
            raise RuntimeError
    assert d == {"gold": 10}

def test_rollback_removes_new_keys():
    d = {}
    with pytest.raises(ValueError):
        with transaction(d):
            d["x"] = 1
            raise ValueError
    assert d == {}
""",
                    "solution_md": """\
```python
from contextlib import contextmanager


@contextmanager
def transaction(data):
    backup = dict(data)
    try:
        yield data
    except Exception:
        data.clear()
        data.update(backup)
        raise
```

**Why:** snapshot the dict *before* yielding control. On success the changes
simply persist. On any exception, `clear()` + `update(backup)` restores the
exact prior contents — removing keys added inside the block too — and the bare
`raise` re-raises so the caller still sees the error.
""",
                },
            ],
        },
        {
            "slug": "advanced-oop",
            "title": "Advanced OOP",
            "description": "ABCs, mixins, and the Method Resolution Order.",
            "badge": {"id": "mro-sage", "name": "MRO Sage", "icon": "🧬"},
            "missions": [
                {
                    "slug": "oop-abc",
                    "title": "Abstract Base Classes",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
An **ABC** defines an interface: subclasses *must* implement its abstract
methods, and the ABC itself cannot be instantiated:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...
```

With multiple inheritance, Python resolves attribute lookup via the
**MRO** (Method Resolution Order, C3 linearization) — inspect it with
`Cls.__mro__`. **Mixins** are small classes that add one behavior and are
designed to sit early in the MRO. Interview favorites: "what's the MRO of
a diamond hierarchy?" and "why does `super()` work in a mixin?"
""",
                    "prompt_md": """\
Using `abc`, define an ABC `Shape` with an abstract method `area()`, and
two concrete subclasses: `Circle(radius)` and `Square(side)` (use
`math.pi`). Instantiating `Shape()` directly must fail.
""",
                    "starter_code": (
                        "import math\nfrom abc import ABC, abstractmethod\n\n\n"
                        "class Shape(ABC):\n    ...\n"
                    ),
                    "example_tests": """\
import math
from solution import Circle, Square

def test_circle():
    assert abs(Circle(2).area() - 4 * math.pi) < 1e-9

def test_square():
    assert Square(3).area() == 9
""",
                    "hidden_tests": """\
import math
import pytest
from solution import Shape, Circle, Square

def test_abstract():
    with pytest.raises(TypeError):
        Shape()

def test_circle():
    assert abs(Circle(2).area() - 4 * math.pi) < 1e-9

def test_square():
    assert Square(3).area() == 9

def test_subclasses():
    assert issubclass(Circle, Shape) and issubclass(Square, Shape)
""",
                    "solution_md": """\
```python
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        ...


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2
```

**Why:** inheriting from `ABC` plus an `@abstractmethod` makes `Shape` a
contract — Python refuses to instantiate it directly (`test_abstract`), forcing
every subclass to supply a real `area`. That's how you express "this is an
interface, not a usable object" in Python.
""",
                },
                {
                    "slug": "advanced-oop-boss",
                    "title": "Boss: The Mixin Forge",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write a mixin class `JsonMixin` providing `to_json(self)` that serializes
the instance's `__dict__` to a JSON string with **sorted keys**. Then
define `Point(JsonMixin)` constructed as `Point(x, y)` storing `x` and
`y` attributes.
""",
                    "starter_code": (
                        "import json\n\n\n"
                        "class JsonMixin:\n    ...\n\n\n"
                        "class Point(JsonMixin):\n    def __init__(self, x, y):\n        ...\n"
                    ),
                    "hidden_tests": """\
import json
from solution import JsonMixin, Point

def test_to_json():
    assert Point(1, 2).to_json() == '{"x": 1, "y": 2}'

def test_sorted_keys():
    class Zebra(JsonMixin):
        def __init__(self):
            self.b = 2
            self.a = 1
    assert Zebra().to_json() == '{"a": 1, "b": 2}'

def test_round_trip():
    assert json.loads(Point(3, 4).to_json()) == {"x": 3, "y": 4}

def test_mixin_in_mro():
    assert JsonMixin in Point.__mro__
""",
                    "solution_md": """\
```python
import json


class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=True)


class Point(JsonMixin):
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

**Why:** a mixin adds one capability without caring about the concrete class —
`JsonMixin.to_json` just serialises whatever is in `self.__dict__`, so *any*
class that mixes it in becomes JSON-dumpable. `sort_keys=True` makes the output
deterministic, and `JsonMixin` sits in `Point.__mro__` so the method resolves.
""",
                },
            ],
        },
        {
            "slug": "functional-tools",
            "title": "Functional Tools",
            "description": "map/filter/reduce, itertools, functools.",
            "badge": {"id": "lambda-lord", "name": "Lambda Lord", "icon": "λ"},
            "missions": [
                {
                    "slug": "functional-reduce",
                    "title": "map, filter, reduce",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
The functional trio:

```python
map(f, xs)               # lazy: apply f to each item
filter(pred, xs)         # lazy: keep items where pred is true
functools.reduce(f, xs, init)   # fold xs into one value
```

`map`/`filter` return lazy iterators (wrap in `list()` to realize).
`reduce` lives in `functools` and folds left:
`reduce(lambda a, b: a + b, [1, 2, 3], 0)` → `6`. In modern Python,
comprehensions often read better than `map`/`filter`, but `reduce`,
`itertools` (chains, product, groupby) and `functools` (`partial`,
`lru_cache`) remain interview territory.
""",
                    "prompt_md": """\
Using `functools.reduce`, write `product_of_odds(nums)` that returns the
product of the **odd** numbers in `nums`. An input with no odd numbers
returns `1`.
""",
                    "starter_code": "from functools import reduce\n\n\ndef product_of_odds(nums):\n    ...\n",
                    "example_tests": """\
from solution import product_of_odds

def test_mixed():
    assert product_of_odds([1, 2, 3, 4, 5]) == 15

def test_no_odds():
    assert product_of_odds([2, 4]) == 1
""",
                    "hidden_tests": """\
from solution import product_of_odds

def test_mixed():
    assert product_of_odds([1, 2, 3, 4, 5]) == 15

def test_no_odds():
    assert product_of_odds([2, 4]) == 1

def test_empty():
    assert product_of_odds([]) == 1

def test_single():
    assert product_of_odds([7]) == 7
""",
                    "solution_md": """\
```python
from functools import reduce


def product_of_odds(nums):
    odds = [n for n in nums if n % 2 != 0]
    return reduce(lambda a, b: a * b, odds, 1)
```

**Why:** filter to the odds first, then `reduce` folds them into a single
product. The explicit `init=1` is what makes the empty case return `1` instead
of raising — it's both the identity for multiplication and the safe seed.
""",
                },
                {
                    "slug": "functional-boss",
                    "title": "Boss: The Grouping Grounds",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Write `group_by(items, keyfunc)` returning a dict mapping each key (the
result of `keyfunc(item)`) to the **list** of items that produced it, in
their original order.
""",
                    "starter_code": "def group_by(items, keyfunc):\n    ...\n",
                    "hidden_tests": """\
from solution import group_by

def test_by_length():
    out = group_by(["a", "bb", "cc", "d"], len)
    assert out == {1: ["a", "d"], 2: ["bb", "cc"]}

def test_by_parity():
    out = group_by([1, 2, 3, 4], lambda x: x % 2)
    assert out == {1: [1, 3], 0: [2, 4]}

def test_empty():
    assert group_by([], len) == {}

def test_preserves_order():
    out = group_by(["zz", "aa"], len)
    assert out[2] == ["zz", "aa"]
""",
                    "solution_md": """\
```python
def group_by(items, keyfunc):
    groups = {}
    for item in items:
        groups.setdefault(keyfunc(item), []).append(item)
    return groups
```

**Why:** `setdefault(key, [])` returns the existing list or installs a fresh one
in a single step, so each item appends to its group's list. Because you iterate
`items` in order and only ever append, first-seen order is preserved within each
group.
""",
                },
            ],
        },
        {
            "slug": "custom-exceptions",
            "title": "Exception Chaining & Custom Exceptions",
            "description": "raise ... from ..., exception hierarchies, __cause__.",
            "badge": {"id": "exception-alchemist", "name": "Exception Alchemist", "icon": "⚗️"},
            "missions": [
                {
                    "slug": "exceptions-custom",
                    "title": "Your Own Exception Types",
                    "kind": "standard",
                    "xp": 50,
                    "lesson_md": """\
Define domain-specific errors by subclassing `Exception`:

```python
class InvalidConfigError(Exception):
    pass

raise InvalidConfigError("missing key: host")
```

Callers can then catch *your* error precisely instead of a generic
`ValueError`. Libraries typically define one base exception and grow a
hierarchy under it, so users can catch broadly (`except LibError`) or
narrowly. Keep exception classes empty or nearly so — the type *is* the
information.
""",
                    "prompt_md": """\
Define `InvalidConfigError(Exception)`, then write `load_config(data)`
that requires the keys `"host"` and `"port"` in the dict `data`. Missing
either raises `InvalidConfigError` with the missing key's name in the
message; otherwise return the dict unchanged.
""",
                    "starter_code": (
                        "class InvalidConfigError(Exception):\n    pass\n\n\n"
                        "def load_config(data):\n    ...\n"
                    ),
                    "example_tests": """\
import pytest
from solution import InvalidConfigError, load_config

def test_valid():
    cfg = {"host": "localhost", "port": 8000}
    assert load_config(cfg) == cfg

def test_missing_host():
    with pytest.raises(InvalidConfigError) as exc:
        load_config({"port": 8000})
    assert "host" in str(exc.value)
""",
                    "hidden_tests": """\
import pytest
from solution import InvalidConfigError, load_config

def test_valid():
    cfg = {"host": "localhost", "port": 8000}
    assert load_config(cfg) == cfg

def test_missing_host():
    with pytest.raises(InvalidConfigError) as exc:
        load_config({"port": 8000})
    assert "host" in str(exc.value)

def test_missing_port():
    with pytest.raises(InvalidConfigError) as exc:
        load_config({"host": "x"})
    assert "port" in str(exc.value)

def test_is_exception_subclass():
    assert issubclass(InvalidConfigError, Exception)
""",
                    "solution_md": """\
```python
class InvalidConfigError(Exception):
    pass


def load_config(data):
    for key in ("host", "port"):
        if key not in data:
            raise InvalidConfigError(f"missing key: {key}")
    return data
```

**Why:** an empty `Exception` subclass is a *type* callers can catch precisely
(`except InvalidConfigError`) instead of a vague `ValueError`. Putting the
missing key in the message aids debugging without changing that the type itself
is the primary signal.
""",
                },
                {
                    "slug": "exceptions-boss",
                    "title": "Boss: The Chain of Blame",
                    "kind": "boss",
                    "xp": 100,
                    "prompt_md": """\
**Boss challenge — hidden tests, no hints.**

Define `LookupFailedError(Exception)`, then write `fetch_value(data, key)`
that returns `data[key]` but, when the key is missing, raises
`LookupFailedError` **chained from** the original `KeyError` (so
`__cause__` is the `KeyError` — use `raise ... from ...`).
""",
                    "starter_code": (
                        "class LookupFailedError(Exception):\n    pass\n\n\n"
                        "def fetch_value(data, key):\n    ...\n"
                    ),
                    "hidden_tests": """\
import pytest
from solution import LookupFailedError, fetch_value

def test_found():
    assert fetch_value({"a": 1}, "a") == 1

def test_raises_custom():
    with pytest.raises(LookupFailedError):
        fetch_value({}, "ghost")

def test_chained_cause():
    with pytest.raises(LookupFailedError) as exc:
        fetch_value({}, "ghost")
    assert isinstance(exc.value.__cause__, KeyError)
""",
                    "solution_md": """\
```python
class LookupFailedError(Exception):
    pass


def fetch_value(data, key):
    try:
        return data[key]
    except KeyError as exc:
        raise LookupFailedError(key) from exc
```

**Why:** `raise ... from exc` sets `__cause__` to the original `KeyError`, so the
traceback reads "LookupFailedError … *directly caused by* KeyError." You get a
clean domain-level error at the surface without discarding the low-level reason
underneath.
""",
                },
            ],
        },
        {
            "slug": "tier3-boss-battle",
            "title": "Boss Battle: The Master's Gauntlet",
            "description": "Timed, hint-free, hidden tests. The final trial of the MVP realms.",
            "is_boss_battle": True,
            "badge": {"id": "pythonic-master", "name": "Pythonic Master", "icon": "🐉"},
            "missions": [
                {
                    "slug": "tier3-gauntlet",
                    "title": "The Master's Gauntlet",
                    "kind": "tier_boss",
                    "xp": 200,
                    "time_limit_seconds": 1200,
                    "prompt_md": """\
**⏱ Timed Boss Battle — 20 minutes, no hints, hidden test suite.**

Two trials, one submission:

1. A decorator `retry(times)` — the decorated function is retried on
   **any** exception, up to `times` total attempts; if the last attempt
   still raises, that exception propagates. Preserve `__name__` with
   `functools.wraps`.
2. A generator `chunked(iterable, size)` — lazily yields **lists** of up
   to `size` items from any iterable (the last chunk may be smaller).
""",
                    "starter_code": (
                        "import functools\n\n\n"
                        "def retry(times):\n    ...\n\n\n"
                        "def chunked(iterable, size):\n    ...\n"
                    ),
                    "hidden_tests": """\
import types
import pytest
from solution import retry, chunked

def test_retry_succeeds_eventually():
    attempts = []

    @retry(3)
    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise RuntimeError("not yet")
        return "ok"

    assert flaky() == "ok"
    assert len(attempts) == 3

def test_retry_exhausted():
    @retry(2)
    def broken():
        raise ValueError("always")

    with pytest.raises(ValueError):
        broken()

def test_retry_preserves_name():
    @retry(1)
    def named():
        return 1
    assert named.__name__ == "named"

def test_chunked_basic():
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

def test_chunked_is_lazy():
    gen = chunked(iter(range(10**12)), 3)
    assert isinstance(gen, types.GeneratorType) or hasattr(gen, "__next__")
    assert next(iter(gen)) == [0, 1, 2]

def test_chunked_exact():
    assert list(chunked("abcd", 2)) == [["a", "b"], ["c", "d"]]
""",
                    "solution_md": """\
```python
import functools


def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
            raise last_exc
        return wrapper
    return decorator


def chunked(iterable, size):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
```

**Why:** `retry` is a *parameterised* decorator — three nested layers: it takes
`times`, returns a decorator, which returns the wrapper. The wrapper returns on
first success or re-raises the last exception once attempts run out. `chunked`
buffers items and `yield`s a full list every `size` elements, flushing any
partial final chunk — and because it uses `yield`, it stays lazy over even an
infinite iterable.
""",
                },
            ],
        },
    ],
}
