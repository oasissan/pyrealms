"""Tier 6 — Hero's Trial (Capstone / Endgame). Curriculum seed data.

The final realm: classic design patterns (factory/registry, observer,
strategy/command) and from-scratch "build" challenges (an LRU cache, a tiny
in-memory ORM, a bounded async pipeline), culminating in a capstone that
combines a pattern with a build.

Everything is graded in the same 5s, no-network pytest subprocess, so the
async work uses in-memory fake sources and yields with `asyncio.sleep(0)` —
never real I/O or wall-clock timing.
"""

TIER = {
    "slug": "heros-trial",
    "title": "Hero's Trial",
    "subtitle": "The Endgame",
    "order": 6,
    "min_level": 12,
    "quests": [
        {
            "slug": "factory-registry",
            "title": "Factory & Registry",
            "description": "Construct objects by key instead of hard-coding classes.",
            "badge": {"id": "pattern-smith", "name": "Pattern Smith", "icon": "🏭"},
            "quiz": [
                {
                    "prompt_md": "What problem does the **Factory** pattern address?",
                    "options": [
                        "Making classes faster",
                        "Decoupling *what* to create from the code that requests it — construct by key/config, not hard-coded class names",
                        "Preventing inheritance",
                        "Compressing objects",
                    ],
                    "correct": 1,
                    "explanation_md": "A factory centralises object creation so callers ask for a thing by name/key and stay ignorant of concrete classes.",
                },
                {
                    "prompt_md": "What is a **registry** in this pattern?",
                    "options": [
                        "A log file",
                        "A mapping from a key (often a string) to the class or factory that builds it",
                        "A database table",
                        "A Windows feature",
                    ],
                    "correct": 1,
                    "explanation_md": "The registry is the `{key: class}` map the factory consults to decide what to instantiate.",
                },
                {
                    "prompt_md": "Why is a *decorator* a natural way to register classes?",
                    "options": [
                        "It runs faster",
                        "`@registry.register(\"name\")` above a class self-registers it at definition time and can return the class unchanged",
                        "Decorators delete the class",
                        "It's the only way",
                    ],
                    "correct": 1,
                    "explanation_md": "A registration decorator records the class in the registry as it's defined, then returns it untouched — clean, declarative wiring.",
                },
                {
                    "prompt_md": "What should a factory do when asked for an unknown key?",
                    "options": [
                        "Return `None` silently",
                        "Raise a clear error (e.g. `KeyError`/`ValueError`) so the mistake surfaces",
                        "Create a random object",
                        "Crash the interpreter",
                    ],
                    "correct": 1,
                    "explanation_md": "Failing loudly on an unknown key beats a silent `None` that explodes far away from the real bug.",
                },
                {
                    "prompt_md": "A key benefit of the registry approach is…",
                    "options": [
                        "Objects use less memory",
                        "New types can be plugged in without editing the factory's own code (open/closed principle)",
                        "It removes the need for classes",
                        "It disables the GIL",
                    ],
                    "correct": 1,
                    "explanation_md": "Adding a type is just another registration — the factory code never changes, which is the open/closed principle in action.",
                },
            ],
            "missions": [
                {
                    "slug": "factory-shapes",
                    "title": "Build by Name",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
A **factory** turns a key into an object, so callers don't hard-code concrete
classes. Back it with a **registry** — a `{name: class}` dict:

```python
class Factory:
    def __init__(self):
        self._registry = {}
    def register(self, name, cls):
        self._registry[name] = cls
    def create(self, name, *args):
        return self._registry[name](*args)
```

Adding a new product is a `register` call — the factory code itself never
changes.
""",
                    "prompt_md": """\
Write a class `ShapeFactory` with `register(name, cls)` and
`create(name, *args, **kwargs)` that instantiates the registered class with
the given arguments. Requesting an unregistered name must raise `KeyError`.
""",
                    "starter_code": "class ShapeFactory:\n    ...\n",
                    "example_tests": """\
from solution import ShapeFactory

class Circle:
    def __init__(self, r):
        self.r = r

def test_creates_registered():
    f = ShapeFactory()
    f.register("circle", Circle)
    c = f.create("circle", 5)
    assert isinstance(c, Circle) and c.r == 5
""",
                    "hidden_tests": """\
import pytest
from solution import ShapeFactory

class Circle:
    def __init__(self, r):
        self.r = r

class Rect:
    def __init__(self, w, h):
        self.w, self.h = w, h

def test_creates_registered():
    f = ShapeFactory()
    f.register("circle", Circle)
    c = f.create("circle", 5)
    assert isinstance(c, Circle) and c.r == 5

def test_passes_kwargs():
    f = ShapeFactory()
    f.register("rect", Rect)
    r = f.create("rect", w=2, h=3)
    assert (r.w, r.h) == (2, 3)

def test_unknown_raises():
    with pytest.raises(KeyError):
        ShapeFactory().create("triangle")
""",
                    "solution_md": """\
```python
class ShapeFactory:
    def __init__(self):
        self._registry = {}

    def register(self, name, cls):
        self._registry[name] = cls

    def create(self, name, *args, **kwargs):
        if name not in self._registry:
            raise KeyError(name)
        return self._registry[name](*args, **kwargs)
```

**Why:** the registry dict decouples the key from the concrete class, and
`create` just forwards `*args`/`**kwargs` to whatever was registered.
Unknown keys raise `KeyError` so a typo fails loudly instead of returning a
confusing `None`.
""",
                },
                {
                    "slug": "factory-plugin",
                    "title": "Boss: The Plugin Registry",
                    "kind": "boss",
                    "xp": 130,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write a class `Registry` whose `register(name)` returns a **decorator** that
registers the decorated class under `name` and returns it unchanged. Also
provide:

- `create(name, *args, **kwargs)` — instantiate the registered class (raise
  `KeyError` for unknown names),
- `names()` — the registered names, sorted.
""",
                    "starter_code": "class Registry:\n    ...\n",
                    "hidden_tests": """\
import pytest
from solution import Registry

def test_decorator_registration_and_create():
    reg = Registry()

    @reg.register("dog")
    class Dog:
        def speak(self):
            return "woof"

    @reg.register("cat")
    class Cat:
        def speak(self):
            return "meow"

    assert reg.create("dog").speak() == "woof"
    assert reg.create("cat").speak() == "meow"

def test_names_sorted():
    reg = Registry()

    @reg.register("zebra")
    class Z: pass

    @reg.register("ant")
    class A: pass

    assert reg.names() == ["ant", "zebra"]

def test_decorator_returns_class_unchanged():
    reg = Registry()

    @reg.register("x")
    class X:
        pass

    assert X.__name__ == "X"

def test_unknown_raises():
    with pytest.raises(KeyError):
        Registry().create("ghost")
""",
                    "solution_md": """\
```python
class Registry:
    def __init__(self):
        self._items = {}

    def register(self, name):
        def decorator(cls):
            self._items[name] = cls
            return cls
        return decorator

    def create(self, name, *args, **kwargs):
        if name not in self._items:
            raise KeyError(name)
        return self._items[name](*args, **kwargs)

    def names(self):
        return sorted(self._items)
```

**Why:** `register(name)` is a decorator *factory* — it returns the real
decorator, which stashes the class and returns it unchanged so the name still
binds normally. New plugins register themselves declaratively at definition
time; `create` never needs editing when a type is added.
""",
                },
            ],
        },
        {
            "slug": "observer-pubsub",
            "title": "Observer & Pub/Sub",
            "description": "Broadcast events to subscribers that come and go.",
            "badge": {"id": "signal-keeper", "name": "Signal Keeper", "icon": "📡"},
            "quiz": [
                {
                    "prompt_md": "What does the **Observer** pattern decouple?",
                    "options": [
                        "Classes from their methods",
                        "The source of an event from the (zero or more) things that react to it",
                        "Threads from the GIL",
                        "Functions from arguments",
                    ],
                    "correct": 1,
                    "explanation_md": "An observable emits events without knowing who's listening; subscribers react without the source depending on them.",
                },
                {
                    "prompt_md": "In pub/sub, what does `emit` (publish) do?",
                    "options": [
                        "Registers a listener",
                        "Notifies every current subscriber, typically in subscription order",
                        "Removes all subscribers",
                        "Creates a new channel",
                    ],
                    "correct": 1,
                    "explanation_md": "Publishing fans the event out to all currently-registered subscribers.",
                },
                {
                    "prompt_md": "Why iterate over a **copy** of the subscriber list when emitting?",
                    "options": [
                        "It's faster",
                        "A subscriber might unsubscribe (mutate the list) during the callback, which would break a live iteration",
                        "Copies use less memory",
                        "It's required by the GIL",
                    ],
                    "correct": 1,
                    "explanation_md": "Emitting over `list(self._subs)` protects against a callback that subscribes/unsubscribes mid-broadcast.",
                },
                {
                    "prompt_md": "A convenient thing `subscribe` can return is…",
                    "options": [
                        "The event",
                        "An `unsubscribe` handle (a callable) so the caller can detach later",
                        "The subscriber count",
                        "Nothing useful",
                    ],
                    "correct": 1,
                    "explanation_md": "Returning a disposer callable is a common ergonomic touch — call it to unsubscribe without re-passing the callback.",
                },
                {
                    "prompt_md": "Compared to direct method calls, pub/sub gives you…",
                    "options": [
                        "Guaranteed ordering across processes",
                        "Loose coupling — the publisher needs no reference to, or knowledge of, its subscribers",
                        "Faster execution",
                        "Type safety",
                    ],
                    "correct": 1,
                    "explanation_md": "The whole point is decoupling: publishers and subscribers evolve independently.",
                },
            ],
            "missions": [
                {
                    "slug": "observer-emitter",
                    "title": "A Simple Emitter",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
An event emitter keeps a list of callbacks and calls them all when something
happens:

```python
class Emitter:
    def __init__(self):
        self._subs = []
    def subscribe(self, cb):
        self._subs.append(cb)
    def emit(self, *args):
        for cb in self._subs:
            cb(*args)
```

Subscribers are notified in the order they registered, and the emitter never
needs to know what they actually do.
""",
                    "prompt_md": """\
Write a class `EventEmitter` with `subscribe(cb)` and `emit(*args)` that calls
every subscribed callback with the emitted arguments, in subscription order.
""",
                    "starter_code": "class EventEmitter:\n    ...\n",
                    "example_tests": """\
from solution import EventEmitter

def test_notifies_subscriber():
    e = EventEmitter()
    got = []
    e.subscribe(got.append)
    e.emit(1)
    e.emit(2)
    assert got == [1, 2]
""",
                    "hidden_tests": """\
from solution import EventEmitter

def test_notifies_subscriber():
    e = EventEmitter()
    got = []
    e.subscribe(got.append)
    e.emit(1)
    e.emit(2)
    assert got == [1, 2]

def test_multiple_in_order():
    e = EventEmitter()
    order = []
    e.subscribe(lambda x: order.append(("a", x)))
    e.subscribe(lambda x: order.append(("b", x)))
    e.emit(9)
    assert order == [("a", 9), ("b", 9)]

def test_emit_multiple_args():
    e = EventEmitter()
    got = []
    e.subscribe(lambda a, b: got.append(a + b))
    e.emit(2, 3)
    assert got == [5]
""",
                    "solution_md": """\
```python
class EventEmitter:
    def __init__(self):
        self._subs = []

    def subscribe(self, cb):
        self._subs.append(cb)

    def emit(self, *args):
        for cb in self._subs:
            cb(*args)
```

**Why:** the emitter just holds a list of callables and forwards the emitted
arguments to each in registration order. It has no idea what the subscribers
do — that decoupling is the whole pattern.
""",
                },
                {
                    "slug": "observer-signal",
                    "title": "Boss: The Detachable Signal",
                    "kind": "boss",
                    "xp": 140,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write a class `Signal` supporting:

- `subscribe(cb)` — register `cb` and **return a callable** that unsubscribes it,
- `unsubscribe(cb)` — remove `cb` if present (safe if it isn't),
- `emit(*args, **kwargs)` — call every current subscriber with those arguments
  (safe even if a callback unsubscribes during emission),
- `subscriber_count()` — how many are currently subscribed.
""",
                    "starter_code": "class Signal:\n    ...\n",
                    "hidden_tests": """\
from solution import Signal

def test_emit_with_args():
    s = Signal()
    got = []
    s.subscribe(lambda a, b: got.append(a + b))
    s.emit(2, 3)
    assert got == [5]

def test_unsubscribe_method():
    s = Signal()
    got = []
    def cb(x):
        got.append(x)
    s.subscribe(cb)
    s.emit(1)
    s.unsubscribe(cb)
    s.emit(2)
    assert got == [1]

def test_subscribe_returns_disposer():
    s = Signal()
    got = []
    unsub = s.subscribe(lambda x: got.append(x))
    s.emit(1)
    unsub()
    s.emit(2)
    assert got == [1]
    assert s.subscriber_count() == 0

def test_unsubscribe_missing_is_safe():
    s = Signal()
    s.unsubscribe(lambda: None)
    assert s.subscriber_count() == 0

def test_count():
    s = Signal()
    s.subscribe(lambda: None)
    s.subscribe(lambda: None)
    assert s.subscriber_count() == 2
""",
                    "solution_md": """\
```python
class Signal:
    def __init__(self):
        self._subs = []

    def subscribe(self, cb):
        self._subs.append(cb)
        return lambda: self.unsubscribe(cb)

    def unsubscribe(self, cb):
        if cb in self._subs:
            self._subs.remove(cb)

    def emit(self, *args, **kwargs):
        for cb in list(self._subs):
            cb(*args, **kwargs)

    def subscriber_count(self):
        return len(self._subs)
```

**Why:** `subscribe` returns a closure over `cb` so callers get a one-shot
disposer. `emit` iterates a *copy* (`list(self._subs)`) so a callback that
unsubscribes mid-broadcast can't corrupt the loop, and `unsubscribe` is a
no-op for absent callbacks.
""",
                },
            ],
        },
        {
            "slug": "strategy-command",
            "title": "Strategy & Command",
            "description": "Swappable behavior, and actions you can undo.",
            "badge": {"id": "tactician", "name": "Tactician", "icon": "♟️"},
            "quiz": [
                {
                    "prompt_md": "What does the **Strategy** pattern let you swap?",
                    "options": [
                        "The class of an object at runtime",
                        "An interchangeable algorithm/behavior, chosen at runtime, behind a common interface",
                        "The memory layout",
                        "The event loop",
                    ],
                    "correct": 1,
                    "explanation_md": "Strategy encapsulates a family of algorithms so you can pick one at runtime without branching all over the caller.",
                },
                {
                    "prompt_md": "In Python, a strategy is often just…",
                    "options": [
                        "A metaclass",
                        "A plain function or callable passed in or looked up in a dict",
                        "A thread",
                        "A subclass of `object`",
                    ],
                    "correct": 1,
                    "explanation_md": "Because functions are first-class, a callable (or a `{name: func}` dispatch dict) is the idiomatic Python strategy.",
                },
                {
                    "prompt_md": "What does the **Command** pattern encapsulate?",
                    "options": [
                        "A database row",
                        "A request/action as an object (or record), often with enough info to undo it",
                        "A network packet",
                        "A type hint",
                    ],
                    "correct": 1,
                    "explanation_md": "Command turns 'do this' into a first-class thing you can queue, log, and reverse.",
                },
                {
                    "prompt_md": "How is **undo** typically implemented with commands?",
                    "options": [
                        "By re-running the program",
                        "Keep a stack of applied commands (or the info to reverse them); pop and invert on undo",
                        "By catching exceptions",
                        "Undo is impossible",
                    ],
                    "correct": 1,
                    "explanation_md": "An undo stack records each applied command's inverse (or the delta), so undo pops the last and reverses it.",
                },
                {
                    "prompt_md": "What should `undo` do when the history is empty?",
                    "options": [
                        "Raise `IndexError`",
                        "Nothing — be a safe no-op",
                        "Reset the whole object",
                        "Crash",
                    ],
                    "correct": 1,
                    "explanation_md": "Undo with nothing to undo should quietly do nothing rather than blow up.",
                },
            ],
            "missions": [
                {
                    "slug": "strategy-dispatch",
                    "title": "Choosing an Algorithm",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
Because functions are first-class, the Strategy pattern in Python is usually a
lookup table of callables:

```python
STRATEGIES = {"sum": sum, "max": max, "min": min}

def reduce_with(name, data):
    return STRATEGIES[name](data)
```

No subclass hierarchy needed — you pick behavior by key at runtime.
""",
                    "prompt_md": """\
Write `make_reducer(strategy)` that returns a function reducing a list:
`"sum"` → total, `"max"` → largest, `"min"` → smallest. An unknown strategy
name must raise `ValueError`.
""",
                    "starter_code": "def make_reducer(strategy):\n    ...\n",
                    "example_tests": """\
from solution import make_reducer

def test_sum():
    assert make_reducer("sum")([1, 2, 3]) == 6
""",
                    "hidden_tests": """\
import pytest
from solution import make_reducer

def test_sum():
    assert make_reducer("sum")([1, 2, 3]) == 6

def test_max():
    assert make_reducer("max")([1, 5, 3]) == 5

def test_min():
    assert make_reducer("min")([4, 2, 8]) == 2

def test_unknown_strategy():
    with pytest.raises(ValueError):
        make_reducer("median")
""",
                    "solution_md": """\
```python
def make_reducer(strategy):
    strategies = {"sum": sum, "max": max, "min": min}
    if strategy not in strategies:
        raise ValueError(strategy)
    return strategies[strategy]
```

**Why:** the `{name: callable}` map *is* the strategy set — selecting behavior
is a dict lookup, and an unknown key raises `ValueError` instead of silently
returning something useless. First-class functions make the whole pattern a
few lines.
""",
                },
                {
                    "slug": "command-undo",
                    "title": "Boss: The Undo Stack",
                    "kind": "boss",
                    "xp": 140,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write a class `Counter` implementing a command/undo stack over an integer
`value` (starting at 0):

- `value` — the current total (attribute or property),
- `do(delta)` — add `delta` and record the command,
- `undo()` — reverse the most recent `do` (safe no-op when there's nothing to
  undo).
""",
                    "starter_code": "class Counter:\n    ...\n",
                    "hidden_tests": """\
from solution import Counter

def test_do_accumulates():
    c = Counter()
    c.do(5)
    c.do(3)
    assert c.value == 8

def test_undo_reverses_last():
    c = Counter()
    c.do(5)
    c.do(3)
    c.undo()
    assert c.value == 5

def test_undo_to_zero():
    c = Counter()
    c.do(5)
    c.undo()
    assert c.value == 0

def test_undo_empty_is_safe():
    c = Counter()
    c.undo()
    assert c.value == 0

def test_interleaved():
    c = Counter()
    c.do(10)
    c.do(-4)
    assert c.value == 6
    c.undo()
    assert c.value == 10
""",
                    "solution_md": """\
```python
class Counter:
    def __init__(self):
        self.value = 0
        self._history = []

    def do(self, delta):
        self.value += delta
        self._history.append(delta)

    def undo(self):
        if self._history:
            self.value -= self._history.pop()
```

**Why:** each `do` records its delta on a history stack, so `undo` just pops
the last delta and subtracts it — the command carries exactly the information
needed to reverse itself. An empty stack makes `undo` a no-op rather than an
error.
""",
                },
            ],
        },
        {
            "slug": "lru-cache",
            "title": "Build: An LRU Cache",
            "description": "Memoization, then eviction when capacity runs out.",
            "badge": {"id": "cache-architect", "name": "Cache Architect", "icon": "🗃️"},
            "quiz": [
                {
                    "prompt_md": "What does memoization trade?",
                    "options": [
                        "Correctness for speed",
                        "Memory for speed — cache results so repeated calls skip recomputation",
                        "Speed for memory",
                        "Nothing",
                    ],
                    "correct": 1,
                    "explanation_md": "Memoization stores computed results, spending memory to avoid redoing work.",
                },
                {
                    "prompt_md": "What does **LRU** eviction discard when the cache is full?",
                    "options": [
                        "A random entry",
                        "The **least recently used** entry",
                        "The largest entry",
                        "The newest entry",
                    ],
                    "correct": 1,
                    "explanation_md": "LRU evicts whatever hasn't been touched for the longest time, betting recent use predicts near-future use.",
                },
                {
                    "prompt_md": "Why is `collections.OrderedDict` handy for an LRU cache?",
                    "options": [
                        "It sorts keys",
                        "It remembers insertion order and offers O(1) `move_to_end` and `popitem(last=False)`",
                        "It's thread-safe",
                        "It uses less memory",
                    ],
                    "correct": 1,
                    "explanation_md": "`move_to_end` marks an entry most-recent and `popitem(last=False)` pops the oldest — exactly the two LRU operations, both O(1).",
                },
                {
                    "prompt_md": "On a cache **hit** (`get`), what keeps recency correct?",
                    "options": [
                        "Nothing needs to change",
                        "Mark that key most-recently-used (e.g. `move_to_end`)",
                        "Delete the key",
                        "Evict something",
                    ],
                    "correct": 1,
                    "explanation_md": "A read counts as a use, so the key must be bumped to most-recent, or it may be wrongly evicted next.",
                },
                {
                    "prompt_md": "What does the standard library offer for function memoization with LRU semantics?",
                    "options": [
                        "`itertools.cache`",
                        "`functools.lru_cache`",
                        "`collections.cache`",
                        "`sys.lru`",
                    ],
                    "correct": 1,
                    "explanation_md": "`functools.lru_cache` (and `functools.cache`) memoize a function's results with optional LRU eviction — production code rarely rolls its own.",
                },
            ],
            "missions": [
                {
                    "slug": "lru-memoize",
                    "title": "Memoize a Function",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
Memoization caches results so repeated calls with the same arguments skip the
work:

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

The arguments tuple is the cache key, so it must be hashable.
""",
                    "prompt_md": """\
Write a decorator `memoize` that caches a function's return value per
positional-arguments tuple, so the wrapped function only actually runs once
per distinct argument set.
""",
                    "starter_code": "import functools\n\n\ndef memoize(func):\n    ...\n",
                    "example_tests": """\
from solution import memoize

def test_caches_result():
    calls = []
    @memoize
    def slow(x):
        calls.append(x)
        return x * 2
    assert slow(3) == 6
    assert slow(3) == 6
    assert calls == [3]
""",
                    "hidden_tests": """\
from solution import memoize

def test_caches_result():
    calls = []
    @memoize
    def slow(x):
        calls.append(x)
        return x * 2
    assert slow(3) == 6
    assert slow(3) == 6
    assert calls == [3]

def test_distinct_args_recompute():
    calls = []
    @memoize
    def f(x):
        calls.append(x)
        return x + 1
    assert f(1) == 2
    assert f(2) == 3
    assert calls == [1, 2]

def test_preserves_name():
    @memoize
    def named(x):
        return x
    assert named.__name__ == "named"
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

**Why:** the `args` tuple keys the cache, so a repeat call is a dict hit and
`func` never re-runs. `functools.wraps` keeps the wrapper's `__name__`/docs
pointing at the original — the detail interviewers love to check.
""",
                },
                {
                    "slug": "lru-eviction",
                    "title": "Boss: Least Recently Used",
                    "kind": "boss",
                    "xp": 150,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Build a class `LRUCache(capacity)` with:

- `get(key)` — return the value and mark it most-recently-used, or `None` if
  absent,
- `put(key, value)` — insert/update, mark most-recent, and if over capacity
  evict the least-recently-used entry.

Both operations should be O(1) (use `collections.OrderedDict`).
""",
                    "starter_code": "from collections import OrderedDict\n\n\nclass LRUCache:\n    ...\n",
                    "hidden_tests": """\
from solution import LRUCache

def test_get_put():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    assert c.get("b") == 2

def test_missing_returns_none():
    assert LRUCache(1).get("x") is None

def test_evicts_least_recently_used():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)          # capacity 2 -> evicts "a"
    assert c.get("a") is None
    assert c.get("b") == 2
    assert c.get("c") == 3

def test_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")             # "a" is now most-recent
    c.put("c", 3)          # evicts "b", not "a"
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3

def test_update_existing_keeps_one_slot():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("a", 10)
    c.put("b", 2)
    assert c.get("a") == 10
    assert c.get("b") == 2
""",
                    "solution_md": """\
```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)
```

**Why:** the `OrderedDict` keeps keys in recency order. `move_to_end` marks a
key most-recently-used on both read and update, and once size exceeds
capacity, `popitem(last=False)` drops the oldest — the least-recently-used
entry — all in O(1).
""",
                },
            ],
        },
        {
            "slug": "tiny-orm",
            "title": "Build: A Tiny ORM",
            "description": "An in-memory table you can insert into and query.",
            "badge": {"id": "data-smith", "name": "Data Smith", "icon": "🛢️"},
            "quiz": [
                {
                    "prompt_md": "What does an ORM (object-relational mapper) fundamentally provide?",
                    "options": [
                        "A faster database",
                        "An object-oriented interface over stored records, so you query with methods instead of raw text",
                        "A GUI",
                        "A type checker",
                    ],
                    "correct": 1,
                    "explanation_md": "An ORM maps rows/records to objects and exposes query methods, hiding the raw storage/query language.",
                },
                {
                    "prompt_md": "In our tiny in-memory ORM, a record is naturally represented as…",
                    "options": [
                        "A string",
                        "A dict of `{field: value}` (or a small object)",
                        "A tuple with no names",
                        "A file",
                    ],
                    "correct": 1,
                    "explanation_md": "A `{field: value}` dict is the simplest faithful record — named fields, easy to compare and filter.",
                },
                {
                    "prompt_md": "A `filter(**conditions)` that matches *all* given fields is doing what logically?",
                    "options": [
                        "An OR across conditions",
                        "An AND across conditions — every field must match",
                        "A sort",
                        "A join",
                    ],
                    "correct": 1,
                    "explanation_md": "Requiring every `field == value` to hold is a logical AND across the conditions.",
                },
                {
                    "prompt_md": "Why return a **new list** from a query rather than the internal storage?",
                    "options": [
                        "Lists are faster",
                        "To avoid callers mutating the table's internal state by accident",
                        "It uses less memory",
                        "It's required by Python",
                    ],
                    "correct": 1,
                    "explanation_md": "Handing out the internal list lets callers corrupt your storage; returning a fresh list keeps the table encapsulated.",
                },
                {
                    "prompt_md": "A `first(**conditions)` helper should return what when nothing matches?",
                    "options": [
                        "Raise `StopIteration`",
                        "`None`",
                        "An empty dict",
                        "The whole table",
                    ],
                    "correct": 1,
                    "explanation_md": "`None` is the idiomatic 'no such record' sentinel for a single-result lookup.",
                },
            ],
            "missions": [
                {
                    "slug": "orm-table",
                    "title": "Insert & List",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
The heart of a tiny ORM is a list of record dicts:

```python
class Table:
    def __init__(self):
        self._rows = []
    def insert(self, **fields):
        self._rows.append(dict(fields))
    def all(self):
        return list(self._rows)     # a copy, so callers can't mutate storage
```

`**fields` lets callers insert with named columns; returning a *copy* from
`all()` keeps the internal list private.
""",
                    "prompt_md": """\
Write a class `Table` with `insert(**fields)` (stores the row as a dict) and
`all()` (returns a list of the stored rows, as a copy — mutating it must not
affect the table).
""",
                    "starter_code": "class Table:\n    ...\n",
                    "example_tests": """\
from solution import Table

def test_insert_and_all():
    t = Table()
    t.insert(name="Ada", age=36)
    assert t.all() == [{"name": "Ada", "age": 36}]
""",
                    "hidden_tests": """\
from solution import Table

def test_insert_and_all():
    t = Table()
    t.insert(name="Ada", age=36)
    t.insert(name="Alan", age=41)
    assert t.all() == [
        {"name": "Ada", "age": 36},
        {"name": "Alan", "age": 41},
    ]

def test_empty():
    assert Table().all() == []

def test_all_returns_copy():
    t = Table()
    t.insert(name="Ada")
    rows = t.all()
    rows.append({"name": "Intruder"})
    assert t.all() == [{"name": "Ada"}]
""",
                    "solution_md": """\
```python
class Table:
    def __init__(self):
        self._rows = []

    def insert(self, **fields):
        self._rows.append(dict(fields))

    def all(self):
        return list(self._rows)
```

**Why:** each row is a `{field: value}` dict built from `**fields`, and
`all()` returns `list(self._rows)` — a fresh list, so a caller appending to
the result can't corrupt the table's private storage.
""",
                },
                {
                    "slug": "orm-query",
                    "title": "Boss: The Query Engine",
                    "kind": "boss",
                    "xp": 150,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Build a class `Table` (in-memory) with:

- `insert(**fields)` — append a record dict,
- `filter(**conditions)` — return a list of records where **every** given
  field equals the condition (AND semantics); no conditions returns all rows,
- `first(**conditions)` — the first matching record, or `None`.
""",
                    "starter_code": "class Table:\n    ...\n",
                    "hidden_tests": """\
from solution import Table

def make():
    t = Table()
    t.insert(name="Ada", role="dev", active=True)
    t.insert(name="Alan", role="dev", active=False)
    t.insert(name="Grace", role="admiral", active=True)
    return t

def test_filter_single_field():
    devs = make().filter(role="dev")
    assert [r["name"] for r in devs] == ["Ada", "Alan"]

def test_filter_multiple_fields_and():
    r = make().filter(role="dev", active=True)
    assert [x["name"] for x in r] == ["Ada"]

def test_filter_no_conditions_returns_all():
    assert len(make().filter()) == 3

def test_filter_no_match():
    assert make().filter(role="ghost") == []

def test_first():
    t = make()
    assert t.first(role="admiral")["name"] == "Grace"
    assert t.first(role="ghost") is None
""",
                    "solution_md": """\
```python
class Table:
    def __init__(self):
        self._rows = []

    def insert(self, **fields):
        self._rows.append(dict(fields))

    def filter(self, **conditions):
        return [
            row
            for row in self._rows
            if all(row.get(field) == value for field, value in conditions.items())
        ]

    def first(self, **conditions):
        matches = self.filter(**conditions)
        return matches[0] if matches else None
```

**Why:** `filter` keeps every row where *all* conditions hold — `all(...)`
over an empty conditions dict is `True`, so no-args returns everything, which
is exactly the ORM convention. `first` reuses `filter` and returns `None` when
there's no match, the idiomatic 'not found' sentinel.
""",
                },
            ],
        },
        {
            "slug": "async-pipeline",
            "title": "Build: An Async Pipeline",
            "description": "Async generators and bounded-concurrency processing.",
            "badge": {"id": "flow-master", "name": "Flow Master", "icon": "🌊"},
            "quiz": [
                {
                    "prompt_md": "What is an **async generator**?",
                    "options": [
                        "A generator that runs on threads",
                        "A function using both `async def` and `yield`, iterated with `async for`",
                        "A faster generator",
                        "A coroutine that returns a list",
                    ],
                    "correct": 1,
                    "explanation_md": "`async def` + `yield` makes an async generator; you consume it with `async for` (or an `async` comprehension).",
                },
                {
                    "prompt_md": "How do you collect an async generator into a list?",
                    "options": [
                        "`list(agen)`",
                        "`[x async for x in agen]` inside a coroutine",
                        "`agen.to_list()`",
                        "`await agen`",
                    ],
                    "correct": 1,
                    "explanation_md": "An async comprehension `[x async for x in agen]` (run within a coroutine) drives the async generator to completion.",
                },
                {
                    "prompt_md": "In a bounded pipeline, what caps how many items are processed at once?",
                    "options": [
                        "A `for` loop",
                        "An `asyncio.Semaphore(limit)` guarding the worker section",
                        "The number of CPU cores",
                        "The GIL",
                    ],
                    "correct": 1,
                    "explanation_md": "A semaphore limits concurrent entries into the protected `async with` block to `limit`.",
                },
                {
                    "prompt_md": "Why use `asyncio.gather` to run the workers?",
                    "options": [
                        "It sorts results",
                        "It runs them concurrently and returns results in the original input order",
                        "It creates threads",
                        "It blocks the loop",
                    ],
                    "correct": 1,
                    "explanation_md": "`gather` schedules all workers concurrently yet preserves input order in the returned list.",
                },
                {
                    "prompt_md": "Why can these pipelines be tested deterministically?",
                    "options": [
                        "They use real network calls",
                        "The fake source and workers yield with `asyncio.sleep(0)` and results are order-preserving — no wall-clock timing",
                        "They run single-threaded only",
                        "Randomness is seeded",
                    ],
                    "correct": 1,
                    "explanation_md": "With an in-memory source, `sleep(0)` yields, and order-preserving `gather`, the outcome is fully deterministic — perfect for auto-grading.",
                },
            ],
            "missions": [
                {
                    "slug": "async-stream",
                    "title": "An Async Stream",
                    "kind": "standard",
                    "xp": 80,
                    "lesson_md": """\
An **async generator** combines `async def` with `yield`, and you consume it
with `async for`:

```python
import asyncio

async def count_up(n):
    for i in range(n):
        await asyncio.sleep(0)     # cooperative yield point
        yield i

async def main():
    return [x async for x in count_up(3)]   # [0, 1, 2]
```

This is the shape of a streaming data source that produces values lazily over
time.
""",
                    "prompt_md": """\
Write an **async generator** `count_up(n)` that yields `0, 1, ..., n-1`, doing
`await asyncio.sleep(0)` before each yield. It must be consumable with
`async for` / an async comprehension.
""",
                    "starter_code": "import asyncio\n\n\nasync def count_up(n):\n    ...\n",
                    "example_tests": """\
import asyncio
from solution import count_up

def test_yields_range():
    async def main():
        return [x async for x in count_up(4)]
    assert asyncio.run(main()) == [0, 1, 2, 3]
""",
                    "hidden_tests": """\
import asyncio
from solution import count_up

def test_yields_range():
    async def main():
        return [x async for x in count_up(4)]
    assert asyncio.run(main()) == [0, 1, 2, 3]

def test_zero():
    async def main():
        return [x async for x in count_up(0)]
    assert asyncio.run(main()) == []

def test_one():
    async def main():
        return [x async for x in count_up(1)]
    assert asyncio.run(main()) == [0]
""",
                    "solution_md": """\
```python
import asyncio


async def count_up(n):
    for i in range(n):
        await asyncio.sleep(0)
        yield i
```

**Why:** `async def` plus `yield` makes this an async generator — each
`await asyncio.sleep(0)` is a cooperative yield point, and `async for`
(or the `async` comprehension in the tests) drives it to completion, one value
at a time.
""",
                },
                {
                    "slug": "async-pipeline-workers",
                    "title": "Boss: The Bounded Pipeline",
                    "kind": "boss",
                    "xp": 160,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write an `async def run_pipeline(source, worker, limit)` where `source` is an
**async generator** of items and `worker` is an async function. It must:

- drain every item from `source`,
- apply `worker` to them with at most `limit` running concurrently
  (`asyncio.Semaphore`),
- return the results as a list in the original item order.
""",
                    "starter_code": "import asyncio\n\n\nasync def run_pipeline(source, worker, limit):\n    ...\n",
                    "hidden_tests": """\
import asyncio
from solution import run_pipeline

async def fake_source(values):
    for v in values:
        await asyncio.sleep(0)
        yield v

async def double(x):
    await asyncio.sleep(0)
    return x * 2

def test_processes_all_in_order():
    async def main():
        return await run_pipeline(fake_source([1, 2, 3, 4]), double, 2)
    assert asyncio.run(main()) == [2, 4, 6, 8]

def test_empty_source():
    async def main():
        return await run_pipeline(fake_source([]), double, 2)
    assert asyncio.run(main()) == []

def test_never_exceeds_limit():
    active = 0
    peak = 0

    async def worker(x):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0)
        active -= 1
        return x

    async def main():
        await run_pipeline(fake_source(list(range(12))), worker, 3)
        return peak

    assert asyncio.run(main()) <= 3
""",
                    "solution_md": """\
```python
import asyncio


async def run_pipeline(source, worker, limit):
    items = [item async for item in source]
    sem = asyncio.Semaphore(limit)

    async def run(item):
        async with sem:
            return await worker(item)

    return await asyncio.gather(*(run(item) for item in items))
```

**Why:** the async comprehension drains the streaming `source` into a list,
then each item gets a worker coroutine that must hold the shared `Semaphore` —
so no more than `limit` run at once. `gather` keeps the results in input order
regardless of which worker finishes first.
""",
                },
            ],
        },
        {
            "slug": "heros-capstone",
            "title": "Boss Battle: The Hero's Capstone",
            "description": "Timed, hint-free — an event bus and an LRU cache, together.",
            "is_boss_battle": True,
            "badge": {"id": "python-hero", "name": "Python Hero", "icon": "🦸"},
            "missions": [
                {
                    "slug": "heros-capstone-boss",
                    "title": "The Hero's Capstone",
                    "kind": "tier_boss",
                    "xp": 300,
                    "time_limit_seconds": 1800,
                    "prompt_md": """\
**⏱ Timed Capstone — 30 minutes, no hints, hidden test suite.**

The final trial: one pattern, one build, one submission.

1. An `EventBus` implementing observer/pub-sub — `subscribe(cb)` returns a
   callable that unsubscribes it, and `emit(event)` notifies every current
   subscriber (safe if a callback unsubscribes mid-emit).
2. An `LRUCache(capacity)` — `get(key)` returns the value (and refreshes
   recency) or `None`; `put(key, value)` inserts/updates and evicts the
   least-recently-used entry when over capacity.
""",
                    "starter_code": (
                        "from collections import OrderedDict\n\n\n"
                        "class EventBus:\n    ...\n\n\n"
                        "class LRUCache:\n    ...\n"
                    ),
                    "hidden_tests": """\
from solution import EventBus, LRUCache

def test_bus_emits_in_order():
    bus = EventBus()
    got = []
    bus.subscribe(got.append)
    bus.emit("a")
    bus.emit("b")
    assert got == ["a", "b"]

def test_bus_unsubscribe_handle():
    bus = EventBus()
    got = []
    unsub = bus.subscribe(got.append)
    bus.emit(1)
    unsub()
    bus.emit(2)
    assert got == [1]

def test_bus_safe_when_unsubscribing_during_emit():
    bus = EventBus()
    got = []
    def once(event):
        got.append(event)
        unsub()
    unsub = bus.subscribe(once)
    bus.emit("x")
    bus.emit("y")
    assert got == ["x"]

def test_lru_evicts_least_recently_used():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") is None
    assert c.get("b") == 2
    assert c.get("c") == 3

def test_lru_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")
    c.put("c", 3)
    assert c.get("b") is None
    assert c.get("a") == 1

def test_lru_missing_is_none():
    assert LRUCache(1).get("nope") is None
""",
                    "solution_md": """\
```python
from collections import OrderedDict


class EventBus:
    def __init__(self):
        self._subs = []

    def subscribe(self, cb):
        self._subs.append(cb)
        return lambda: self._subs.remove(cb) if cb in self._subs else None

    def emit(self, event):
        for cb in list(self._subs):
            cb(event)


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)
```

**Why:** `EventBus.subscribe` returns a disposer closure and `emit` iterates a
copy so a callback can unsubscribe itself mid-broadcast. `LRUCache` leans on
`OrderedDict`: `move_to_end` refreshes recency on read and update, and
`popitem(last=False)` evicts the oldest when capacity is exceeded — the
observer pattern and the eviction build standing side by side.
""",
                },
            ],
        },
    ],
}
