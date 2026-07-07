"""Tier 5 — Systems & Performance (Expert). Curriculum seed data.

The interview-crusher realm: object memory layout (`__slots__`), the
descriptor protocol behind every attribute, garbage collection & `weakref`,
concurrency with threads/locks/queues, `asyncio` coroutines, and the runtime
side of the typing system.

Grading constraint: every hidden suite must be deterministic inside the 5s,
no-network pytest subprocess — threads are always `join()`ed and coroutines
yield with `asyncio.sleep(0)`; nothing asserts on wall-clock timing.
"""

TIER = {
    "slug": "systems-performance",
    "title": "Systems & Performance",
    "subtitle": "The Expert Realm",
    "order": 5,
    "min_level": 8,
    "quests": [
        {
            "slug": "slots-memory",
            "title": "__slots__ & Memory Layout",
            "description": "Trade the per-instance dict for fixed, cheaper slots.",
            "badge": {"id": "slot-smith", "name": "Slot Smith", "icon": "🧩"},
            "quiz": [
                {
                    "prompt_md": "What does defining `__slots__` remove from each instance?",
                    "options": [
                        "The ability to subclass",
                        "The per-instance `__dict__` (so it can't grow arbitrary attributes)",
                        "All methods",
                        "The `__init__` method",
                    ],
                    "correct": 1,
                    "explanation_md": "`__slots__` replaces the per-instance `__dict__` with a fixed set of C-level descriptors, cutting memory and forbidding stray attributes.",
                },
                {
                    "prompt_md": "What happens when you assign an attribute **not** listed in `__slots__`?",
                    "options": [
                        "It's silently ignored",
                        "`AttributeError` is raised",
                        "It's added to a hidden dict",
                        "`TypeError` is raised",
                    ],
                    "correct": 1,
                    "explanation_md": "With no `__dict__` to hold it, assigning an unlisted attribute raises `AttributeError`.",
                },
                {
                    "prompt_md": "Why does `__slots__` reduce memory for many small instances?",
                    "options": [
                        "It compresses the values",
                        "It avoids allocating a dict per instance, storing fields in a compact fixed layout",
                        "It shares one dict across all instances",
                        "It stores everything on disk",
                    ],
                    "correct": 1,
                    "explanation_md": "A dict per instance has real overhead; slots store attributes in a fixed array-like layout, which adds up across thousands of objects.",
                },
                {
                    "prompt_md": "Which is a real trade-off of using `__slots__`?",
                    "options": [
                        "Instances become immutable",
                        "You lose dynamic attribute assignment and `__dict__`-based tricks",
                        "The class can't have methods",
                        "Attribute access becomes slower",
                    ],
                    "correct": 1,
                    "explanation_md": "Slots forbid ad-hoc attributes and a `__dict__`; attribute *access* is actually as fast or faster.",
                },
                {
                    "prompt_md": "Does a slotted instance have a `__dict__`?",
                    "options": [
                        "Yes, always",
                        "No — unless a base class without `__slots__` reintroduces one",
                        "Only after the first attribute set",
                        "Only in Python 2",
                    ],
                    "correct": 1,
                    "explanation_md": "A fully-slotted class has no `__dict__`; but if any base class lacks `__slots__`, a `__dict__` sneaks back in.",
                },
            ],
            "missions": [
                {
                    "slug": "slots-point",
                    "title": "A Slotted Point",
                    "kind": "standard",
                    "xp": 60,
                    "lesson_md": """\
By default every instance carries a `__dict__` so you can attach any
attribute at runtime. That flexibility costs memory. `__slots__` declares a
fixed set of attributes and drops the dict entirely:

```python
class Pixel:
    __slots__ = ("r", "g", "b")

p = Pixel()
p.r = 255
p.alpha = 1   # AttributeError — 'alpha' isn't a slot
```

Across thousands of objects this is a real memory win, and a common
interview question: *"how would you make this class cheaper to allocate a
million of?"*
""",
                    "prompt_md": """\
Write a class `Point` with `__slots__ = ("x", "y")` and an `__init__(self,
x, y)` that stores both. Slotted instances must reject any other attribute.
""",
                    "starter_code": "class Point:\n    ...\n",
                    "example_tests": """\
from solution import Point

def test_holds_coords():
    p = Point(1, 2)
    assert (p.x, p.y) == (1, 2)
""",
                    "hidden_tests": """\
import pytest
from solution import Point

def test_holds_coords():
    p = Point(1, 2)
    assert (p.x, p.y) == (1, 2)

def test_no_instance_dict():
    assert not hasattr(Point(0, 0), "__dict__")

def test_rejects_stray_attr():
    p = Point(1, 2)
    with pytest.raises(AttributeError):
        p.z = 3
""",
                    "solution_md": """\
```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

**Why:** listing the attributes in `__slots__` swaps the per-instance
`__dict__` for fixed C-level descriptors, so each `Point` is smaller and any
attribute outside the slot list raises `AttributeError`.
""",
                },
                {
                    "slug": "slots-record",
                    "title": "Boss: The Frozen Record",
                    "kind": "boss",
                    "xp": 120,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write a class `Record` with `__slots__ = ("id", "payload")` and
`__init__(self, id, payload)`. It must:

- store both fields and expose **no** `__dict__`,
- reject any attribute outside the slots,
- compare equal to another `Record` with the same `id` and `payload`, and
- be hashable (usable in a `set`), keyed on `(id, payload)`.
""",
                    "starter_code": "class Record:\n    ...\n",
                    "hidden_tests": """\
import pytest
from solution import Record

def test_fields():
    r = Record(1, "a")
    assert (r.id, r.payload) == (1, "a")

def test_no_dict():
    assert not hasattr(Record(1, "a"), "__dict__")

def test_rejects_stray_attr():
    with pytest.raises(AttributeError):
        Record(1, "a").extra = 9

def test_equality():
    assert Record(1, "a") == Record(1, "a")
    assert Record(1, "a") != Record(2, "a")

def test_hashable_in_set():
    s = {Record(1, "a"), Record(1, "a"), Record(2, "b")}
    assert len(s) == 2
""",
                    "solution_md": """\
```python
class Record:
    __slots__ = ("id", "payload")

    def __init__(self, id, payload):
        self.id = id
        self.payload = payload

    def __eq__(self, other):
        return (
            isinstance(other, Record)
            and (self.id, self.payload) == (other.id, other.payload)
        )

    def __hash__(self):
        return hash((self.id, self.payload))
```

**Why:** `__slots__` gives the compact, dict-free layout and blocks stray
attributes. Defining `__eq__` makes value equality work, and because
overriding `__eq__` normally drops hashability, we restore `__hash__` over
the same `(id, payload)` tuple so instances stay usable in sets and dict keys.
""",
                },
            ],
        },
        {
            "slug": "descriptors",
            "title": "The Descriptor Protocol",
            "description": "The mechanism behind every attribute, property, and method.",
            "badge": {"id": "descriptor-adept", "name": "Descriptor Adept", "icon": "🔬"},
            "quiz": [
                {
                    "prompt_md": "Which methods define the descriptor protocol?",
                    "options": [
                        "`__enter__` / `__exit__`",
                        "`__get__` / `__set__` / `__delete__`",
                        "`__iter__` / `__next__`",
                        "`__call__` only",
                    ],
                    "correct": 1,
                    "explanation_md": "A descriptor is any object implementing `__get__` (and optionally `__set__`/`__delete__`); it's how `property`, methods, and `classmethod` all work.",
                },
                {
                    "prompt_md": "Where must a descriptor instance live to take effect?",
                    "options": [
                        "In the instance's `__dict__`",
                        "As a **class** attribute",
                        "In a global variable",
                        "Inside `__init__`",
                    ],
                    "correct": 1,
                    "explanation_md": "Descriptors are invoked by the type machinery only when found on the class, not on the instance.",
                },
                {
                    "prompt_md": "What is `__set_name__(self, owner, name)` used for?",
                    "options": [
                        "Renaming the class",
                        "Automatically learning the attribute name the descriptor was assigned to",
                        "Setting the value",
                        "Deleting the attribute",
                    ],
                    "correct": 1,
                    "explanation_md": "Python calls `__set_name__` at class-creation time so the descriptor knows which name it's bound to (handy for choosing a backing-store key).",
                },
                {
                    "prompt_md": "A descriptor with `__set__` is a *data descriptor*. How does it interact with the instance dict?",
                    "options": [
                        "The instance dict wins",
                        "The data descriptor takes precedence over an instance-dict entry of the same name",
                        "They can't coexist",
                        "It raises an error",
                    ],
                    "correct": 1,
                    "explanation_md": "Data descriptors (those defining `__set__`/`__delete__`) override instance-dict entries — that's why `property` can't be shadowed by `self.x = ...`.",
                },
                {
                    "prompt_md": "Why store the value under a *different* key (e.g. `_x`) inside `__set__`?",
                    "options": [
                        "To make it public",
                        "To avoid infinitely recursing back into the descriptor",
                        "For faster hashing",
                        "It's required syntax",
                    ],
                    "correct": 1,
                    "explanation_md": "If the descriptor is bound to `x`, writing to `x` again would re-trigger `__set__` forever; a separate backing key breaks the loop.",
                },
            ],
            "missions": [
                {
                    "slug": "descriptors-positive",
                    "title": "A Positive Descriptor",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
A **descriptor** is an object that customises attribute access by
implementing `__get__`/`__set__`. Put one on a class and every read/write of
that attribute routes through it — this is how `property` works under the
hood:

```python
class Positive:
    def __set_name__(self, owner, name):
        self.key = "_" + name          # backing store, avoids recursion
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                 # accessed on the class itself
        return getattr(obj, self.key)
    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError("must be positive")
        setattr(obj, self.key, value)
```

The `obj is None` branch handles access on the class (`Cls.attr`) rather than
an instance.
""",
                    "prompt_md": """\
Write a data descriptor `Positive` (with `__set_name__`, `__get__`,
`__set__`) that only accepts values `> 0`, raising `ValueError` otherwise.
Store the value under `"_" + name` to avoid recursion.
""",
                    "starter_code": "class Positive:\n    ...\n",
                    "example_tests": """\
import pytest
from solution import Positive

class Account:
    balance = Positive()
    def __init__(self, balance):
        self.balance = balance

def test_accepts_positive():
    assert Account(100).balance == 100

def test_rejects_zero():
    with pytest.raises(ValueError):
        Account(0)
""",
                    "hidden_tests": """\
import pytest
from solution import Positive

class Account:
    balance = Positive()
    def __init__(self, balance):
        self.balance = balance

def test_accepts_positive():
    assert Account(100).balance == 100

def test_rejects_zero():
    with pytest.raises(ValueError):
        Account(0)

def test_rejects_negative():
    with pytest.raises(ValueError):
        Account(-5)

def test_reassignment_validates():
    a = Account(10)
    with pytest.raises(ValueError):
        a.balance = -1
    assert a.balance == 10
""",
                    "solution_md": """\
```python
class Positive:
    def __set_name__(self, owner, name):
        self.key = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.key)

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError("must be positive")
        setattr(obj, self.key, value)
```

**Why:** `__set_name__` captures the attribute name so the value can be
stashed under `_balance`, keeping `__set__` from recursing. Because `__set__`
is defined, this is a *data descriptor* — it intercepts every write, so an
invalid reassignment is rejected and the old value is preserved.
""",
                },
                {
                    "slug": "descriptors-typed",
                    "title": "Boss: The Type Guard",
                    "kind": "boss",
                    "xp": 130,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write a data descriptor `Typed` constructed as `Typed(expected_type)` that
rejects any assigned value not an instance of `expected_type` (raising
`TypeError`). Two `Typed` fields on the same class must stay independent.
""",
                    "starter_code": "class Typed:\n    ...\n",
                    "hidden_tests": """\
import pytest
from solution import Typed

class Person:
    name = Typed(str)
    age = Typed(int)
    def __init__(self, name, age):
        self.name = name
        self.age = age

def test_valid():
    p = Person("Ada", 36)
    assert (p.name, p.age) == ("Ada", 36)

def test_wrong_type_name():
    with pytest.raises(TypeError):
        Person(123, 36)

def test_wrong_type_age():
    with pytest.raises(TypeError):
        Person("Ada", "old")

def test_fields_independent():
    a = Person("A", 1)
    b = Person("B", 2)
    assert (a.name, a.age, b.name, b.age) == ("A", 1, "B", 2)
""",
                    "solution_md": """\
```python
class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.key = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.key)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"expected {self.expected_type.__name__}, got {type(value).__name__}"
            )
        setattr(obj, self.key, value)
```

**Why:** the descriptor stores its own `expected_type`, and `__set_name__`
gives each instance its own backing key (`_name`, `_age`) — so two `Typed`
fields on the same class never collide, and every assignment is type-checked
through `__set__`.
""",
                },
            ],
        },
        {
            "slug": "gc-weakref",
            "title": "Garbage Collection & weakref",
            "description": "Refcounts, cycles, and references that don't keep objects alive.",
            "badge": {"id": "cycle-breaker", "name": "Cycle Breaker", "icon": "♻️"},
            "quiz": [
                {
                    "prompt_md": "What is CPython's primary memory-reclamation mechanism?",
                    "options": [
                        "A mark-and-sweep pass every second",
                        "Reference counting — an object is freed the moment its refcount hits zero",
                        "Manual `free()` calls",
                        "The operating system",
                    ],
                    "correct": 1,
                    "explanation_md": "CPython frees objects immediately when their reference count reaches zero; the cyclic GC is a secondary collector for reference cycles.",
                },
                {
                    "prompt_md": "Why does CPython need a *cyclic* garbage collector on top of refcounting?",
                    "options": [
                        "To speed up attribute access",
                        "Because reference cycles keep each other's counts above zero and never get freed by refcounting alone",
                        "To compress memory",
                        "To handle threads",
                    ],
                    "correct": 1,
                    "explanation_md": "Two objects referencing each other keep both refcounts ≥ 1 forever; the cyclic GC detects and collects such unreachable cycles.",
                },
                {
                    "prompt_md": "What does a `weakref` reference do?",
                    "options": [
                        "Copies the object",
                        "Refers to an object **without** increasing its refcount, so it can still be collected",
                        "Locks the object in memory",
                        "Makes the object read-only",
                    ],
                    "correct": 1,
                    "explanation_md": "A weak reference lets you observe an object without keeping it alive — ideal for caches that shouldn't prevent cleanup.",
                },
                {
                    "prompt_md": "Calling a dead `weakref.ref` (whose target was collected) returns…",
                    "options": [
                        "The last value",
                        "`None`",
                        "Raises `KeyError`",
                        "An empty object",
                    ],
                    "correct": 1,
                    "explanation_md": "Once the referent is gone, calling the weakref returns `None`.",
                },
                {
                    "prompt_md": "Which values **cannot** be stored in a `WeakValueDictionary`?",
                    "options": [
                        "Custom class instances",
                        "Objects that don't support weak references, like plain `int` and `str`",
                        "Anything with a `__slots__`",
                        "Functions",
                    ],
                    "correct": 1,
                    "explanation_md": "Built-ins like `int`, `str`, and `tuple` aren't weakly referenceable, so they can't be weak-dict values; most custom objects can.",
                },
            ],
            "missions": [
                {
                    "slug": "weakref-cache",
                    "title": "A Cache That Lets Go",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
A normal dict *keeps its values alive* — a cache built on one can leak memory
forever. `weakref.WeakValueDictionary` holds its values weakly, so an entry
vanishes automatically once nothing else references the object:

```python
import weakref

cache = weakref.WeakValueDictionary()
cache["a"] = obj      # doesn't keep obj alive on its own
```

Note: values must be weakly referenceable, so custom objects work but plain
`int`/`str` do not.
""",
                    "prompt_md": """\
Write a class `WeakCache` wrapping a `weakref.WeakValueDictionary` with
`set(key, value)` and `get(key)` (returning `None` for a missing/collected
key). It must not keep its values alive on its own.
""",
                    "starter_code": "import weakref\n\n\nclass WeakCache:\n    ...\n",
                    "example_tests": """\
from solution import WeakCache

class Thing:
    pass

def test_get_live_value():
    c = WeakCache()
    t = Thing()
    c.set("a", t)
    assert c.get("a") is t
""",
                    "hidden_tests": """\
import gc
from solution import WeakCache

class Thing:
    pass

def test_get_live_value():
    c = WeakCache()
    t = Thing()
    c.set("a", t)
    assert c.get("a") is t

def test_missing_key():
    assert WeakCache().get("nope") is None

def test_value_collected_when_unreferenced():
    c = WeakCache()
    t = Thing()
    c.set("a", t)
    del t
    gc.collect()
    assert c.get("a") is None
""",
                    "solution_md": """\
```python
import weakref


class WeakCache:
    def __init__(self):
        self._data = weakref.WeakValueDictionary()

    def set(self, key, value):
        self._data[key] = value

    def get(self, key):
        return self._data.get(key)
```

**Why:** the `WeakValueDictionary` references its values weakly, so once the
last strong reference (`t`) is dropped the entry disappears on its own — the
cache never becomes the reason an object stays in memory.
""",
                },
                {
                    "slug": "weakref-registry",
                    "title": "Boss: The Live Registry",
                    "kind": "boss",
                    "xp": 130,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write a class `ObjectRegistry` that tracks objects **without** keeping them
alive:

- `register(name, obj)` — store a weak reference to `obj` under `name`,
- `get(name)` — return the object, or `None` if it was collected or never
  registered,
- `live_count()` — how many registered objects are still alive.
""",
                    "starter_code": "import weakref\n\n\nclass ObjectRegistry:\n    ...\n",
                    "hidden_tests": """\
import gc
from solution import ObjectRegistry

class Node:
    pass

def test_get_live():
    r = ObjectRegistry()
    n = Node()
    r.register("n", n)
    assert r.get("n") is n
    assert r.live_count() == 1

def test_missing():
    assert ObjectRegistry().get("nope") is None

def test_collected():
    r = ObjectRegistry()
    n = Node()
    r.register("n", n)
    del n
    gc.collect()
    assert r.get("n") is None
    assert r.live_count() == 0

def test_counts_only_live():
    r = ObjectRegistry()
    keep = Node()
    drop = Node()
    r.register("keep", keep)
    r.register("drop", drop)
    del drop
    gc.collect()
    assert r.live_count() == 1
    assert r.get("keep") is keep
""",
                    "solution_md": """\
```python
import weakref


class ObjectRegistry:
    def __init__(self):
        self._refs = {}

    def register(self, name, obj):
        self._refs[name] = weakref.ref(obj)

    def get(self, name):
        ref = self._refs.get(name)
        return ref() if ref is not None else None

    def live_count(self):
        return sum(1 for ref in self._refs.values() if ref() is not None)
```

**Why:** storing `weakref.ref(obj)` lets the registry observe objects without
bumping their refcount, so they're freed as soon as the outside world lets go.
Calling a dead ref returns `None`, which both `get` and `live_count` rely on
to report only still-living objects.
""",
                },
            ],
        },
        {
            "slug": "threading-locks",
            "title": "Threads, Locks & Queues",
            "description": "Shared-state safety with Lock and hand-off with queue.Queue.",
            "badge": {"id": "lock-keeper", "name": "Lock Keeper", "icon": "🔐"},
            "quiz": [
                {
                    "prompt_md": "What problem does a `threading.Lock` solve?",
                    "options": [
                        "It speeds up CPU-bound work",
                        "It prevents two threads from corrupting shared state by interleaving a read-modify-write",
                        "It creates new threads",
                        "It disables the GIL",
                    ],
                    "correct": 1,
                    "explanation_md": "A lock serialises access to shared mutable state so a non-atomic update (like `x += 1`) can't be split across threads.",
                },
                {
                    "prompt_md": "Even with the GIL, why can `counter += 1` from many threads still lose updates?",
                    "options": [
                        "The GIL only protects reads",
                        "`+=` is read-modify-write — the GIL can switch threads between the read and the write",
                        "Integers are immutable",
                        "It can't — the GIL makes it safe",
                    ],
                    "correct": 1,
                    "explanation_md": "The GIL guarantees single bytecode-op atomicity, but `+=` is several ops; a thread switch mid-sequence drops increments.",
                },
                {
                    "prompt_md": "What is the idiomatic way to hold a lock?",
                    "options": [
                        "`lock.acquire()` and hope",
                        "`with lock:` — a context manager that always releases",
                        "Never release it",
                        "Use a global flag",
                    ],
                    "correct": 1,
                    "explanation_md": "`with lock:` acquires on entry and releases on exit even if the body raises — no leaked locks.",
                },
                {
                    "prompt_md": "What does `queue.Queue` give you for producer/consumer designs?",
                    "options": [
                        "A faster list",
                        "A thread-safe hand-off structure — no manual locking needed to pass items between threads",
                        "A sorted collection",
                        "A way to share the GIL",
                    ],
                    "correct": 1,
                    "explanation_md": "`queue.Queue` is internally synchronised, so multiple threads can `put`/`get` safely without you managing a lock.",
                },
                {
                    "prompt_md": "Why call `thread.join()` before reading a result the thread produced?",
                    "options": [
                        "To start the thread",
                        "To block until the thread has finished, guaranteeing its work is done",
                        "To kill the thread",
                        "To lower its priority",
                    ],
                    "correct": 1,
                    "explanation_md": "`join()` waits for the thread to complete, so you don't read a half-finished result — the key to deterministic threaded tests.",
                },
            ],
            "missions": [
                {
                    "slug": "threading-counter",
                    "title": "A Thread-Safe Counter",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
`counter += 1` is a *read-modify-write*: three steps the interpreter can
interrupt between. Run it from several threads and increments vanish. A
`Lock` makes the update atomic:

```python
import threading

lock = threading.Lock()
with lock:
    counter += 1     # now indivisible w.r.t. other threads
```

To test threaded code deterministically, always `join()` every thread before
asserting — that guarantees all the work has actually happened.
""",
                    "prompt_md": """\
Write a class `Counter` with a `threading.Lock`, an `increment()` method that
safely does `+= 1` under the lock, and a `value` property returning the
current count. Concurrent increments must never be lost.
""",
                    "starter_code": "import threading\n\n\nclass Counter:\n    ...\n",
                    "example_tests": """\
from solution import Counter

def test_single_thread():
    c = Counter()
    for _ in range(10):
        c.increment()
    assert c.value == 10
""",
                    "hidden_tests": """\
import threading
from solution import Counter

def test_single_thread():
    c = Counter()
    for _ in range(10):
        c.increment()
    assert c.value == 10

def test_many_threads_lose_nothing():
    c = Counter()

    def work():
        for _ in range(1000):
            c.increment()

    threads = [threading.Thread(target=work) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert c.value == 4000
""",
                    "solution_md": """\
```python
import threading


class Counter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    @property
    def value(self):
        return self._value
```

**Why:** the lock makes each `+= 1` indivisible, so four threads doing 1000
increments each land exactly 4000 — no lost updates. `join()`ing every thread
before reading `value` is what makes the assertion deterministic.
""",
                },
                {
                    "slug": "threading-queue",
                    "title": "Boss: The Work Queue",
                    "kind": "boss",
                    "xp": 130,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write `parallel_sum(numbers, workers=4)` that sums `numbers` using a pool of
worker threads fed by a `queue.Queue`:

- load every number onto the queue,
- start `workers` threads that each drain the queue (use `get_nowait` and
  stop on `queue.Empty`), summing what they pull,
- `join` all threads and return the combined total.

It must return the correct sum for any input, including an empty list.
""",
                    "starter_code": "import threading\nimport queue\n\n\ndef parallel_sum(numbers, workers=4):\n    ...\n",
                    "hidden_tests": """\
from solution import parallel_sum

def test_basic_sum():
    assert parallel_sum(list(range(100))) == sum(range(100))

def test_empty():
    assert parallel_sum([]) == 0

def test_single_worker():
    assert parallel_sum([1, 2, 3, 4], workers=1) == 10

def test_negatives():
    assert parallel_sum([-1, -2, 3]) == 0
""",
                    "solution_md": """\
```python
import threading
import queue


def parallel_sum(numbers, workers=4):
    q = queue.Queue()
    for n in numbers:
        q.put(n)

    partials = []
    lock = threading.Lock()

    def consume():
        total = 0
        while True:
            try:
                total += q.get_nowait()
            except queue.Empty:
                break
        with lock:
            partials.append(total)

    threads = [threading.Thread(target=consume) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return sum(partials)
```

**Why:** `queue.Queue` is thread-safe, so workers pull items without a manual
lock; `get_nowait` + catching `queue.Empty` is the clean "drain until done"
pattern. Each worker keeps a private running total and appends it once (under
a lock, since `list.append` across threads plus the final read want a defined
order), and `join()` guarantees every worker finished before we sum the parts.
""",
                },
            ],
        },
        {
            "slug": "asyncio-coroutines",
            "title": "asyncio & Coroutines",
            "description": "async/await, gather, and bounding concurrency with a Semaphore.",
            "badge": {"id": "async-ace", "name": "Async Ace", "icon": "⚡"},
            "quiz": [
                {
                    "prompt_md": "What does calling an `async def` function return?",
                    "options": [
                        "Its result immediately",
                        "A coroutine object that does nothing until awaited or run on a loop",
                        "A thread",
                        "A generator of results",
                    ],
                    "correct": 1,
                    "explanation_md": "Calling a coroutine function just builds a coroutine object; it only executes when awaited or driven by an event loop (e.g. `asyncio.run`).",
                },
                {
                    "prompt_md": "What does `await asyncio.gather(*coros)` do?",
                    "options": [
                        "Runs them one after another",
                        "Schedules the coroutines concurrently and returns their results in order",
                        "Cancels them",
                        "Runs them in separate processes",
                    ],
                    "correct": 1,
                    "explanation_md": "`gather` runs the awaitables concurrently on the loop and collects results in the original order.",
                },
                {
                    "prompt_md": "When is `asyncio` the right concurrency tool?",
                    "options": [
                        "CPU-bound number crunching",
                        "I/O-bound work with lots of waiting (network, disk) on a single thread",
                        "Parallelising pure math across cores",
                        "Never — use threads always",
                    ],
                    "correct": 1,
                    "explanation_md": "async shines for I/O-bound workloads: while one task awaits, others run — all cooperatively on one thread. CPU-bound work wants multiprocessing.",
                },
                {
                    "prompt_md": "What does an `asyncio.Semaphore(n)` let you do?",
                    "options": [
                        "Speed up the loop",
                        "Limit how many coroutines run a protected section concurrently to at most `n`",
                        "Create `n` threads",
                        "Pause the whole program",
                    ],
                    "correct": 1,
                    "explanation_md": "`async with semaphore:` caps concurrency — useful to avoid, say, opening 10,000 sockets at once.",
                },
                {
                    "prompt_md": "Why does `await asyncio.sleep(0)` matter in cooperative code?",
                    "options": [
                        "It sleeps for a random time",
                        "It yields control to the loop so other ready tasks can run",
                        "It blocks all tasks",
                        "It has no effect",
                    ],
                    "correct": 1,
                    "explanation_md": "`sleep(0)` is a cooperative yield point — it lets the event loop switch to other tasks, which is exactly how concurrency interleaves.",
                },
            ],
            "missions": [
                {
                    "slug": "asyncio-gather",
                    "title": "Awaiting Many at Once",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
An `async def` function is a **coroutine** — calling it returns an object that
runs only when awaited. `asyncio.gather` runs several coroutines
concurrently and returns their results in order:

```python
import asyncio

async def double(x):
    await asyncio.sleep(0)     # a cooperative yield point
    return x * 2

async def main():
    return await asyncio.gather(double(1), double(2))   # [2, 4]

asyncio.run(main())
```

`asyncio.run` spins up an event loop, runs the coroutine to completion, and
tears the loop down.
""",
                    "prompt_md": """\
Write an `async def fetch_all(items)` that concurrently doubles every value
using `asyncio.gather`, returning a list of results in the original order.
(Give each doubling its own coroutine that `await asyncio.sleep(0)` before
returning.)
""",
                    "starter_code": "import asyncio\n\n\nasync def fetch_all(items):\n    ...\n",
                    "example_tests": """\
import asyncio
from solution import fetch_all

def test_doubles():
    assert asyncio.run(fetch_all([1, 2, 3])) == [2, 4, 6]
""",
                    "hidden_tests": """\
import asyncio
from solution import fetch_all

def test_doubles():
    assert asyncio.run(fetch_all([1, 2, 3])) == [2, 4, 6]

def test_empty():
    assert asyncio.run(fetch_all([])) == []

def test_order_preserved():
    assert asyncio.run(fetch_all([5, 1, 4, 2])) == [10, 2, 8, 4]
""",
                    "solution_md": """\
```python
import asyncio


async def fetch_all(items):
    async def double(x):
        await asyncio.sleep(0)
        return x * 2

    return await asyncio.gather(*(double(x) for x in items))
```

**Why:** each `double` is a coroutine that yields with `sleep(0)`, so they
interleave on the loop; `gather` schedules them all concurrently yet returns
results in the order the coroutines were passed — not the order they finished.
""",
                },
                {
                    "slug": "asyncio-bounded",
                    "title": "Boss: Bounded Concurrency",
                    "kind": "boss",
                    "xp": 140,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Write an `async def bounded_map(fn, items, limit)` that applies the async
function `fn` to every item with **at most `limit`** running concurrently,
returning results in the original order. Use an `asyncio.Semaphore` to cap
concurrency.
""",
                    "starter_code": "import asyncio\n\n\nasync def bounded_map(fn, items, limit):\n    ...\n",
                    "hidden_tests": """\
import asyncio
from solution import bounded_map

def test_results_in_order():
    async def fn(x):
        await asyncio.sleep(0)
        return x * 2

    async def main():
        return await bounded_map(fn, [1, 2, 3, 4, 5], 2)

    assert asyncio.run(main()) == [2, 4, 6, 8, 10]

def test_never_exceeds_limit():
    active = 0
    peak = 0

    async def fn(x):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0)
        active -= 1
        return x

    async def main():
        await bounded_map(fn, list(range(20)), 3)
        return peak

    assert asyncio.run(main()) <= 3

def test_empty():
    async def fn(x):
        return x

    assert asyncio.run(bounded_map(fn, [], 4)) == []
""",
                    "solution_md": """\
```python
import asyncio


async def bounded_map(fn, items, limit):
    sem = asyncio.Semaphore(limit)

    async def worker(item):
        async with sem:
            return await fn(item)

    return await asyncio.gather(*(worker(item) for item in items))
```

**Why:** every item gets a worker coroutine, but each must acquire the shared
`Semaphore` before calling `fn`, so no more than `limit` are ever inside the
protected section at once. `gather` still preserves input order in the
returned list regardless of finish order.
""",
                },
            ],
        },
        {
            "slug": "typing-internals",
            "title": "Typing at Runtime",
            "description": "get_type_hints, Protocols, and structural checks.",
            "badge": {"id": "type-theorist", "name": "Type Theorist", "icon": "📐"},
            "quiz": [
                {
                    "prompt_md": "Do Python's type hints affect execution by default?",
                    "options": [
                        "Yes, they enforce types at runtime",
                        "No — they're annotations; enforcement is opt-in via tools or explicit checks",
                        "Only in functions",
                        "Only with `mypy` installed",
                    ],
                    "correct": 1,
                    "explanation_md": "Annotations are stored, not enforced; static checkers (mypy) or runtime code (`get_type_hints`, `isinstance`) act on them if you choose.",
                },
                {
                    "prompt_md": "What does `typing.get_type_hints(func)` return?",
                    "options": [
                        "The function's source",
                        "A dict of resolved annotations, including `'return'` if annotated",
                        "The function's default arguments",
                        "A list of parameter names",
                    ],
                    "correct": 1,
                    "explanation_md": "It resolves the annotations (including string/forward references) into a `{name: type}` dict, with `'return'` for the return annotation.",
                },
                {
                    "prompt_md": "What is a `typing.Protocol`?",
                    "options": [
                        "A network protocol",
                        "A structural type — anything with the right methods matches, no explicit inheritance needed",
                        "An abstract base class you must subclass",
                        "A decorator",
                    ],
                    "correct": 1,
                    "explanation_md": "Protocols express *structural* (duck) typing: conformance is by shape, not by declared inheritance.",
                },
                {
                    "prompt_md": "What does `@runtime_checkable` add to a Protocol?",
                    "options": [
                        "Speed",
                        "The ability to use it with `isinstance()` (checking method presence)",
                        "Static-only checking",
                        "Automatic implementation",
                    ],
                    "correct": 1,
                    "explanation_md": "A `@runtime_checkable` Protocol supports `isinstance`, which checks for the presence of the required methods at runtime.",
                },
                {
                    "prompt_md": "What is `typing.Generic[T]` used to build?",
                    "options": [
                        "A faster list",
                        "Classes parameterised by a type variable, e.g. a `Stack[int]`",
                        "A runtime type enforcer",
                        "A metaclass",
                    ],
                    "correct": 1,
                    "explanation_md": "`Generic[T]` lets a container be parameterised over a type variable for static checkers, e.g. `class Stack(Generic[T])`.",
                },
            ],
            "missions": [
                {
                    "slug": "typing-hints",
                    "title": "Reading the Annotations",
                    "kind": "standard",
                    "xp": 70,
                    "lesson_md": """\
Type hints are just stored metadata. `typing.get_type_hints` resolves them
into a usable dict (handling forward references that live as strings):

```python
from typing import get_type_hints

def greet(name: str, times: int) -> str:
    ...

get_type_hints(greet)
# {'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}
```

A function with no annotations yields an empty dict.
""",
                    "prompt_md": """\
Write `param_types(func)` that returns the resolved annotation dict for
`func` using `get_type_hints` — mapping each annotated parameter (and
`'return'`, if annotated) to its type. An unannotated function returns `{}`.
""",
                    "starter_code": "from typing import get_type_hints\n\n\ndef param_types(func):\n    ...\n",
                    "example_tests": """\
from solution import param_types

def sample(x: int, y: str) -> bool:
    return True

def test_reads_hints():
    assert param_types(sample) == {"x": int, "y": str, "return": bool}
""",
                    "hidden_tests": """\
from solution import param_types

def sample(x: int, y: str) -> bool:
    return True

def test_reads_hints():
    assert param_types(sample) == {"x": int, "y": str, "return": bool}

def test_no_annotations():
    def bare(a, b):
        return a
    assert param_types(bare) == {}

def test_partial_annotations():
    def partial(a: int, b) -> None:
        return None
    assert param_types(partial) == {"a": int, "return": type(None)}
""",
                    "solution_md": """\
```python
from typing import get_type_hints


def param_types(func):
    return get_type_hints(func)
```

**Why:** `get_type_hints` does the real work — it resolves annotations
(including string forward-references) into a `{name: type}` dict and includes
`'return'` only when the return is annotated, so an unannotated function comes
back as `{}`.
""",
                },
                {
                    "slug": "typing-protocol",
                    "title": "Boss: The Structural Check",
                    "kind": "boss",
                    "xp": 130,
                    "prompt_md": """\
**Boss — hidden tests, no hints.**

Define a `@runtime_checkable` `Protocol` named `Sized` requiring a
`__len__(self) -> int` method, and write `total_length(items)` that sums
`len(x)` over only those items that are instances of `Sized` (ignoring the
rest). Use `isinstance` against the Protocol.
""",
                    "starter_code": "from typing import Protocol, runtime_checkable\n\n\n@runtime_checkable\nclass Sized(Protocol):\n    ...\n\n\ndef total_length(items):\n    ...\n",
                    "hidden_tests": """\
from solution import total_length

def test_sums_sized():
    assert total_length(["ab", [1, 2, 3], (1,)]) == 6

def test_ignores_unsized():
    assert total_length([1, 2, "ab", 3]) == 2

def test_all_unsized():
    assert total_length([1, 2.0, 3]) == 0

def test_empty():
    assert total_length([]) == 0
""",
                    "solution_md": """\
```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Sized(Protocol):
    def __len__(self) -> int: ...


def total_length(items):
    return sum(len(x) for x in items if isinstance(x, Sized))
```

**Why:** a `@runtime_checkable` Protocol lets `isinstance(x, Sized)` succeed
for anything exposing `__len__` — strings, lists, tuples — while `int`/`float`
have no length and are skipped. That's structural typing enforced at runtime:
conformance by shape, not by inheritance.
""",
                },
            ],
        },
        {
            "slug": "systems-crucible",
            "title": "Boss Battle: The Systems Crucible",
            "description": "Timed, hint-free, hidden tests — descriptors meet asyncio.",
            "is_boss_battle": True,
            "badge": {"id": "systems-sovereign", "name": "Systems Sovereign", "icon": "👑"},
            "missions": [
                {
                    "slug": "systems-crucible-boss",
                    "title": "The Systems Crucible",
                    "kind": "tier_boss",
                    "xp": 250,
                    "time_limit_seconds": 1200,
                    "prompt_md": """\
**⏱ Timed Boss Battle — 20 minutes, no hints, hidden test suite.**

Two trials, one submission:

1. A data descriptor `Bounded(lo, hi)` that only accepts values within the
   inclusive range `[lo, hi]`, raising `ValueError` otherwise. Two `Bounded`
   fields on one class must stay independent.
2. An `async def gather_doubled(values)` that concurrently doubles every value
   (each via its own coroutine that `await asyncio.sleep(0)`), returning
   results in order via `asyncio.gather`.
""",
                    "starter_code": (
                        "import asyncio\n\n\n"
                        "class Bounded:\n    ...\n\n\n"
                        "async def gather_doubled(values):\n    ...\n"
                    ),
                    "hidden_tests": """\
import asyncio
import pytest
from solution import Bounded, gather_doubled

class Dial:
    level = Bounded(0, 10)
    def __init__(self, level):
        self.level = level

def test_descriptor_accepts_in_range():
    assert Dial(5).level == 5

def test_descriptor_rejects_high():
    with pytest.raises(ValueError):
        Dial(11)

def test_descriptor_rejects_low():
    with pytest.raises(ValueError):
        Dial(-1)

def test_descriptor_fields_independent():
    a, b = Dial(1), Dial(9)
    assert (a.level, b.level) == (1, 9)

def test_async_doubles_in_order():
    assert asyncio.run(gather_doubled([1, 2, 3])) == [2, 4, 6]

def test_async_empty():
    assert asyncio.run(gather_doubled([])) == []
""",
                    "solution_md": """\
```python
import asyncio


class Bounded:
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

    def __set_name__(self, owner, name):
        self.key = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.key)

    def __set__(self, obj, value):
        if not (self.lo <= value <= self.hi):
            raise ValueError("out of range")
        setattr(obj, self.key, value)


async def gather_doubled(values):
    async def one(v):
        await asyncio.sleep(0)
        return v * 2

    return await asyncio.gather(*(one(v) for v in values))
```

**Why:** `Bounded` is a data descriptor — `__set_name__` gives each field its
own backing key so two dials don't collide, and `__set__` enforces the range
on every write. `gather_doubled` wraps each value in a coroutine that yields
with `sleep(0)`, so `gather` runs them concurrently but still returns results
in input order.
""",
                },
            ],
        },
    ],
}
