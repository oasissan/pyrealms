# Realms 5 & 6 + Mock Interview Arena — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship two full curriculum realms (Systems & Performance; Hero's Trial) plus a timed, randomized Mock Interview Arena, replacing the map's hardcoded "Coming in Phase 2" placeholders.

**Architecture:** New content lives as static dicts in `app/content/tier5.py` / `tier6.py`, registered in `ALL_TIERS` and loaded by the idempotent seeder — identical to tiers 1-4. The Arena is a new subsystem: two SQLAlchemy tables, a service that selects rounds from the existing quiz + boss-challenge banks and grades via the existing `run_hidden_tests`, an HTMX router, and Jinja templates.

**Tech Stack:** FastAPI, SQLAlchemy (SQLite), Jinja2, HTMX, Alpine.js. No new dependencies.

## Global Constraints

- Auto-graded code runs in `app/grading.py`'s pytest subprocess: **5s timeout, no network**. All hidden tests must be deterministic — no wall-clock timing assertions; `threading` tests `join()`; `asyncio` tests use `asyncio.sleep(0)`; async "scraper/ORM" bosses use in-memory mock sources.
- Every mission dict: `slug`, `title`, `kind` (`standard`/`boss`/`tier_boss`), `xp`, `prompt_md`, `starter_code`, `hidden_tests`, `solution_md` (**exactly one** ```python fence + a short `**Why:**` note). `standard` missions also get `lesson_md` and `example_tests`. `boss`/`tier_boss` missions **must not** have `example_tests`.
- Each teaching quest has a `badge` dict `{"id","name","icon"}` and a `quiz` list of 5 questions `{"prompt_md","options","correct","explanation_md"}`. The boss-battle quest has `is_boss_battle: True` and a `badge`, one `tier_boss` mission, and no quiz.
- No new dependencies (FastAPI, SQLAlchemy, Jinja2, HTMX, Alpine only). Follow the append-only ledger convention for XP.
- `tests/test_content.py` and `tests/test_quiz_content.py` are the CI gate for content correctness. `python -c "import app.main"` must succeed.

---

## Authoring template (reference for all content tasks)

Every teaching quest follows this exact shape. Use it verbatim as the pattern; only the concept, code, and tests change.

```python
{
    "slug": "slots-memory",
    "title": "__slots__ & Memory Layout",
    "description": "Trade per-instance dicts for fixed slots.",
    "badge": {"id": "slot-smith", "name": "Slot Smith", "icon": "🧩"},
    "quiz": [
        {
            "prompt_md": "What does defining `__slots__` on a class prevent?",
            "options": [
                "Subclassing",
                "Creating a per-instance `__dict__` (and thus arbitrary new attributes)",
                "Using `@property`",
                "Inheritance from `object`",
            ],
            "correct": 1,
            "explanation_md": "`__slots__` replaces the per-instance `__dict__` with a fixed set of descriptors, so instances can't grow new attributes and use less memory.",
        },
        # ...4 more, all `correct` pointing at the right index...
    ],
    "missions": [
        {
            "slug": "slots-point",
            "title": "A Slotted Point",
            "kind": "standard",
            "xp": 60,
            "lesson_md": """\
Prose lesson with a short ```python example```. Explain the *why*.
""",
            "prompt_md": "Write a class `Point` with `__slots__ = ('x', 'y')` ...",
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

def test_no_dict():
    assert not hasattr(Point(1, 2), "__dict__")

def test_rejects_new_attr():
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

**Why:** `__slots__` swaps the per-instance `__dict__` for fixed C-level
descriptors, so instances are smaller and reject stray attributes.
""",
        },
        {
            "slug": "slots-boss",
            "title": "Boss: The Frozen Record",
            "kind": "boss",
            "xp": 120,
            "prompt_md": "**Boss — hidden tests, no hints.** ...",
            "starter_code": "class Record:\n    ...\n",
            "hidden_tests": """\
# full pytest file importing from `solution`, deterministic
""",
            "solution_md": """\
```python
# canonical answer
```

**Why:** ...
""",
        },
    ],
}
```

The tier dict wraps quests plus a final boss-battle quest:

```python
TIER = {
    "slug": "systems-performance",
    "title": "Systems & Performance",
    "subtitle": "The Expert Realm",
    "order": 5,
    "min_level": 8,
    "quests": [ ...6 teaching quests..., {
        "slug": "systems-crucible",
        "title": "Boss Battle: The Systems Crucible",
        "description": "Timed, hint-free, hidden tests.",
        "is_boss_battle": True,
        "badge": {"id": "systems-sovereign", "name": "Systems Sovereign", "icon": "👑"},
        "missions": [{
            "slug": "systems-crucible-boss",
            "title": "The Systems Crucible",
            "kind": "tier_boss",
            "xp": 250,
            "time_limit_seconds": 1200,
            "prompt_md": "...",
            "starter_code": "...",
            "hidden_tests": "...",
            "solution_md": "...",
        }],
    }],
}
```

**Every mission's `solution_md` python must pass its own `hidden_tests`.** Verify each quest as you write it by running the extraction test (see verification step in each task).

---

## Task 1: Realm 5 content — `app/content/tier5.py`

**Files:**
- Create: `app/content/tier5.py`
- Test (existing gate): `tests/test_content.py`, `tests/test_quiz_content.py`

**Interfaces:**
- Produces: `tier5.TIER` — a tier dict with `slug="systems-performance"`, `order=5`, `min_level=8`, six teaching quests + one `is_boss_battle` quest, matching the authoring template above.

Quests to author (concept → boss deliverable → badge). Each = lesson + 5-Q quiz + `standard` mission (`example_tests`) + `boss` mission (hidden only):

1. `slots-memory` → slotted class rejecting stray attrs, no `__dict__` → Slot Smith 🧩
2. `descriptors` → validating typed descriptor (`__get__`/`__set__`/`__set_name__`, raises on bad type/value) → Descriptor Adept 🔬
3. `gc-weakref` → weak-value cache (`weakref.WeakValueDictionary`) whose entries drop when the referent is gone → Cycle Breaker ♻️
4. `threading-locks` → thread-safe counter/aggregator using `threading.Lock` or `queue.Queue`, threads `join()`ed → Lock Keeper 🔐
5. `asyncio-coroutines` → `async` function using `asyncio.gather`; boss adds a `Semaphore`-bounded runner, deterministic via `asyncio.sleep(0)` → Async Ace ⚡
6. `typing-internals` → use `typing.get_type_hints` / `Protocol`; boss: a `Generic[T]` container or `runtime_checkable` Protocol check → Type Theorist 📐

Boss battle `systems-crucible` → `tier_boss` `systems-crucible-boss`, `time_limit_seconds=1200`, combines a descriptor + an async `gather` → Systems Sovereign 👑.

- [ ] **Step 1: Write `tier5.py`** with the full `TIER` dict following the template. All hidden tests deterministic. Bosses carry no `example_tests`.

- [ ] **Step 2: Register temporarily for the content test.** In `app/content/__init__.py`, add `tier5` to the import and `ALL_TIERS` (Task 3 finalizes this; doing it now lets the content gate run).

- [ ] **Step 3: Run the content gate**

Run: `.venv/Scripts/python.exe -m pytest tests/test_content.py tests/test_quiz_content.py -q`
Expected: PASS (every tier5 solution passes its hidden tests; no boss has visible tests; quizzes well-formed).

- [ ] **Step 4: Fix any failing mission** — the failure names the mission slug and the assertion. Correct the solution or the test until green. Re-run Step 3.

- [ ] **Step 5: Commit**

```bash
git add app/content/tier5.py app/content/__init__.py
git commit -m "feat: add Realm 5 — Systems & Performance curriculum"
```

---

## Task 2: Realm 6 content — `app/content/tier6.py`

**Files:**
- Create: `app/content/tier6.py`
- Test: `tests/test_content.py`, `tests/test_quiz_content.py`

**Interfaces:**
- Produces: `tier6.TIER` — `slug="heros-trial"`, `order=6`, `min_level=12`, six teaching quests + boss battle.

Quests (all deterministic, no network):

1. `factory-registry` → a class-registry factory that constructs by string key, raises on unknown key → Pattern Smith 🏭
2. `observer-pubsub` → event emitter: `subscribe(cb)`, `unsubscribe(cb)`, `emit(*args)` fans out in order → Signal Keeper 📡
3. `strategy-command` → command stack: `do(cmd)` applies, `undo()` reverts last, on an in-memory state → Tactician ♟️
4. `lru-cache` → `LRUCache(capacity)` with `get`/`put`, evicts least-recently-used (use `collections.OrderedDict`) → Cache Architect 🗃️
5. `tiny-orm` → in-memory model: declare fields, `create(**kw)`, `filter(**kw)` returns matching records → Data Smith 🛢️
6. `async-pipeline` → `async` bounded-worker pipeline over a fake async generator source, results deterministic → Flow Master 🌊

Boss battle `heros-capstone` → `tier_boss` `heros-capstone-boss`, `time_limit_seconds=1800`, multi-part: e.g. an observable store with an LRU-cached query → Python Hero 🦸.

- [ ] **Step 1: Write `tier6.py`** following the template.
- [ ] **Step 2:** Add `tier6` to `app/content/__init__.py` import + `ALL_TIERS`.
- [ ] **Step 3: Run the gate** — `.venv/Scripts/python.exe -m pytest tests/test_content.py tests/test_quiz_content.py -q` → PASS.
- [ ] **Step 4:** Fix failing missions, re-run.
- [ ] **Step 5: Commit**

```bash
git add app/content/tier6.py app/content/__init__.py
git commit -m "feat: add Realm 6 — Hero's Trial curriculum"
```

---

## Task 3: Wire tiers & remove map placeholders

**Files:**
- Modify: `app/content/__init__.py` (finalize import + `ALL_TIERS = [tier1.TIER, tier2.TIER, tier3.TIER, tier4.TIER, tier5.TIER, tier6.TIER]`)
- Modify: `app/templates/map.html` (delete the two hardcoded `<section class="tier locked">` placeholder blocks, lines ~54-61)
- Delete (dev only): `app.db`

- [ ] **Step 1:** Confirm `app/content/__init__.py` line 3 is `from . import tier1, tier2, tier3, tier4, tier5, tier6` and `ALL_TIERS` lists all six.

- [ ] **Step 2:** In `map.html`, delete the two placeholder `<section>` blocks (Realm 5 "Systems & Performance … Coming in Phase 2" and Realm 6 "Hero's Trial … Coming in Phase 2"). Leave the `{% for ts in map_state %}` loop and the Badges section intact.

- [ ] **Step 3: Reseed.** Back up then remove the dev DB so the seeder rebuilds with the new tiers:

```bash
mv app.db app.db.pre-realms-bak 2>/dev/null; true
.venv/Scripts/python.exe -c "import app.main"
```
Expected: import succeeds; startup lifespan reseeds `app.db` with tiers 1-6.

- [ ] **Step 4: Verify seed count**

Run:
```bash
.venv/Scripts/python.exe -c "from app.database import SessionLocal; from app.models import Tier; db=SessionLocal(); print(sorted((t.order,t.slug) for t in db.query(Tier).all()))"
```
Expected: six tiers, orders 1-6 including `systems-performance` and `heros-trial`.

- [ ] **Step 5: Commit**

```bash
git add app/content/__init__.py app/templates/map.html
git commit -m "feat: register Realms 5 & 6, remove map placeholders"
```

---

## Task 4: Arena data model

**Files:**
- Modify: `app/models.py` (append two models)
- Test: `tests/test_arena.py` (create)

**Interfaces:**
- Produces: `InterviewSession(id, created_at, finished_at, difficulty, num_questions, score, total)` and `InterviewRound(id, session_id, order, kind, ref_id, answer, correct, points, elapsed_seconds)`; `InterviewSession.rounds` relationship ordered by `order`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_arena.py
from datetime import datetime
from app.database import Base, engine, SessionLocal
from app.models import InterviewSession, InterviewRound


def test_session_rounds_relationship():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    s = InterviewSession(difficulty="expert", num_questions=2, score=0, total=2)
    db.add(s); db.flush()
    db.add(InterviewRound(session_id=s.id, order=2, kind="mcq", ref_id=1, points=1))
    db.add(InterviewRound(session_id=s.id, order=1, kind="coding", ref_id=5, points=1))
    db.flush()
    assert [r.order for r in s.rounds] == [1, 2]
    db.rollback()
```

- [ ] **Step 2: Run it, expect failure** — `.venv/Scripts/python.exe -m pytest tests/test_arena.py::test_session_rounds_relationship -v` → FAIL (`ImportError: cannot import name 'InterviewSession'`).

- [ ] **Step 3: Add the models** to `app/models.py` (mirror existing style — `Mapped`/`mapped_column`, `datetime.utcnow` default like other tables):

```python
class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    difficulty: Mapped[str] = mapped_column(String)
    num_questions: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[int] = mapped_column(Integer, default=0)

    rounds: Mapped[list["InterviewRound"]] = relationship(
        back_populates="session", order_by="InterviewRound.order"
    )


class InterviewRound(Base):
    __tablename__ = "interview_rounds"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"))
    order: Mapped[int] = mapped_column(Integer)
    kind: Mapped[str] = mapped_column(String)  # "mcq" | "coding"
    ref_id: Mapped[int] = mapped_column(Integer)  # QuizQuestion.id or Challenge.id
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    correct: Mapped[bool] = mapped_column(Boolean, default=False)
    points: Mapped[int] = mapped_column(Integer, default=1)
    elapsed_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)

    session: Mapped[InterviewSession] = relationship(back_populates="rounds")
```

- [ ] **Step 4: Run test, expect pass** — same command → PASS.

- [ ] **Step 5: Commit**

```bash
git add app/models.py tests/test_arena.py
git commit -m "feat: add interview session/round models"
```

---

## Task 5: Arena service — round selection & grading

**Files:**
- Create: `app/services/arena.py`
- Modify: `tests/test_arena.py`

**Interfaces:**
- Consumes: `InterviewSession`, `InterviewRound` (Task 4); `QuizQuestion`, `Challenge` (existing); `run_hidden_tests` from `app/grading.py`; `award_xp` from `app/services/xp.py`.
- Produces:
  - `DIFFICULTY_TIERS: dict[str, list[int]]` — `{"standard": [2, 3], "expert": [4, 5, 6]}`.
  - `start_session(db, difficulty, num_questions) -> InterviewSession` — picks a random mix of MCQ (`QuizQuestion`) and coding (`Challenge` where `kind in ('boss','tier_boss')`) rounds from tiers in `DIFFICULTY_TIERS[difficulty]`, persists rounds ordered `1..n`, returns the session.
  - `current_round(db, session) -> InterviewRound | None` — first round with `correct is False and answer is None`, i.e. unanswered; `None` when done.
  - `grade_round(db, round, answer) -> bool` — MCQ: `int(answer) == QuizQuestion.correct_index`; coding: `run_hidden_tests(answer, challenge.hidden_tests).passed`. Sets `round.answer/correct/points`, awards XP idempotently (`arena:{session_id}:{order}`) on correct, returns correctness.
  - `finish_if_done(db, session) -> None` — when no unanswered rounds remain, set `finished_at`, recompute `score = sum(r.points for r in rounds if r.correct)`.
  - `personal_best(db) -> int | None` — max `score` among finished sessions.

- [ ] **Step 1: Write failing tests** covering: standard difficulty draws only tiers 2-3; MCQ grading with correct/incorrect index; coding grading via a trivial challenge; `finish_if_done` computes score. (Seed a minimal in-memory DB with one `QuizQuestion` and one boss `Challenge` whose hidden test is `from solution import f\n\ndef test(): assert f()==1` and solvable by `def f(): return 1`.)

```python
def test_mcq_grading(seeded_db):
    from app.services import arena
    s = arena.start_session(seeded_db, "standard", 1)
    r = arena.current_round(seeded_db, s)
    ok = arena.grade_round(seeded_db, r, str(r_expected_correct_index))
    assert ok is True
```

- [ ] **Step 2: Run, expect failure** (`ModuleNotFoundError: app.services.arena`).

- [ ] **Step 3: Implement `app/services/arena.py`** with the interface above. Use `random.sample`/`random.choice` over the candidate pools; guard against pools smaller than requested (fall back to `random.choices` or cap `num_questions`). Grade coding via `run_hidden_tests` (import lazily to avoid import cycles).

- [ ] **Step 4: Run tests, expect pass.**

- [ ] **Step 5: Commit**

```bash
git add app/services/arena.py tests/test_arena.py
git commit -m "feat: arena service — round selection and grading"
```

---

## Task 6: Arena router & templates

**Files:**
- Create: `app/routers/arena.py`, `app/templates/arena.html`, `app/templates/partials/arena_round.html`, `app/templates/partials/arena_result.html`
- Modify: `app/main.py` (register router), `app/templates/base.html` (nav link)

**Interfaces:**
- Consumes: `app/services/arena.py` (Task 5), `hud_context()` from `app/routers/pages.py`, the shared `templates` Jinja env.
- Produces routes: `GET /arena`, `POST /arena/start`, `GET /arena/round/{session_id}`, `POST /arena/answer/{session_id}`, `GET /arena/results/{session_id}`.

- [ ] **Step 1:** Read `app/routers/pages.py` and `app/routers/actions.py` to copy the exact `templates`/`hud_context`/DB-dependency wiring and HTMX partial-return conventions.

- [ ] **Step 2: Write `app/routers/arena.py`.** `GET /arena` renders `arena.html` (difficulty select, length, past sessions, `personal_best`). `POST /arena/start` calls `start_session`, redirects (303) to `/arena/round/{id}`. `GET /arena/round/{id}` renders `arena_round.html` for `current_round` (branch on `kind`: MCQ options vs a code textarea seeded from the challenge `starter_code`), including an Alpine per-round countdown. `POST /arena/answer/{id}` calls `grade_round` + `finish_if_done`, then returns the next `arena_round.html` partial or, when done, `arena_result.html` (HTMX swap). `GET /arena/results/{id}` renders full results.

- [ ] **Step 3: Write the three templates.** `arena.html extends base.html`. Round/result partials are bare fragments for HTMX swapping (match how `partials/result.html` is returned in `actions.py`). Coding rounds POST the textarea content as `answer`; MCQ rounds POST the chosen index.

- [ ] **Step 4: Register + link.** In `app/main.py`, `app.include_router(arena.router)`. In `base.html` nav, add an Arena link shown when `hud.level >= 8`.

- [ ] **Step 5: Smoke test the import & routes**

Run: `.venv/Scripts/python.exe -c "import app.main; print([r.path for r in app.main.app.routes if 'arena' in r.path])"`
Expected: the five `/arena...` paths listed.

- [ ] **Step 6: Commit**

```bash
git add app/routers/arena.py app/templates/arena.html app/templates/partials/arena_round.html app/templates/partials/arena_result.html app/main.py app/templates/base.html
git commit -m "feat: Mock Interview Arena router and UI"
```

---

## Task 7: End-to-end verification

**Files:** none (verification only)

- [ ] **Step 1: Full suite**

Run: `.venv/Scripts/python.exe -m pytest -q`
Expected: all green (content, quiz, arena, grading, seed).

- [ ] **Step 2: Import check (CI parity)**

Run: `.venv/Scripts/python.exe -c "import app.main"`
Expected: no error.

- [ ] **Step 3: Drive the app.** Start `python run.py`, load `/` — confirm Realms 5 & 6 render (locked or unlocked per level), no stale placeholders. Grant enough XP (or lower `min_level` temporarily) to open Realm 5, open a mission, submit its solution, confirm a pass. Open `/arena`, start an Expert session, answer an MCQ and a coding round, reach the results screen with a score. Use the `run` skill / browser tools to confirm.

- [ ] **Step 4: Restore dev DB note.** The reseeded `app.db` is the new baseline; the `app.db.pre-realms-bak` backup can be deleted once verified.

- [ ] **Step 5: Final commit / branch ready for PR**

```bash
git add -A
git commit -m "test: arena coverage + end-to-end verification" || true
```

---

## Self-Review

**Spec coverage:** Realm 5 (Task 1) ✓, Realm 6 (Task 2) ✓, wiring + placeholder removal (Task 3) ✓, Arena models/service/router/UI (Tasks 4-6) ✓, tests + drive-the-app (Task 7) ✓. Difficulty→tier mapping, XP idempotency, no-leaderboard, level-8 arena gate all present.

**Placeholder scan:** Content tasks intentionally specify each mission by concept + deliverable + exact badge/slug rather than inlining ~24 full missions here; the authoring template gives the complete concrete shape and `test_content.py` is the hard correctness gate. All Arena code (novel) is given in full. No TBD/TODO left.

**Type consistency:** `start_session`/`current_round`/`grade_round`/`finish_if_done`/`personal_best` signatures match between Task 5 (definition) and Task 6 (consumption). Model field names match between Task 4 and Task 5. `DIFFICULTY_TIERS` keys (`standard`/`expert`) match the router's difficulty select.
