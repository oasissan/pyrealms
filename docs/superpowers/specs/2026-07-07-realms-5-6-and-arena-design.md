# Realms 5 & 6 + Mock Interview Arena — Design

**Date:** 2026-07-07
**Status:** Approved, ready for implementation planning

## Goal

Replace the two hardcoded "Coming in Phase 2" placeholders on the world map
(`app/templates/map.html`) with two fully-built curriculum realms, and add
the Mock Interview Arena called for in the original design spec
(`docs/superpowers/specs/2026-07-05-python-zero-to-hero-design.md`, §5).

1. **Realm 5 — Systems & Performance** (Expert): real, CI-passing curriculum.
2. **Realm 6 — Hero's Trial** (Capstone/Endgame): design-pattern + "build" curriculum.
3. **Mock Interview Arena**: a first-class, timed, randomized practice subsystem.

## Guiding constraint

Everything auto-graded runs in `app/grading.py`'s real pytest subprocess:
**5-second timeout, no network, no guaranteed resource limits on Windows.**
Therefore:

- Concurrency (`threading`, `asyncio`) is tested via `join()` /
  `asyncio.sleep(0)` for determinism — **never wall-clock performance
  assertions**.
- The "async scraper / ORM" build bosses use **in-memory mock data sources**,
  never real HTTP.
- Big-O / GIL / memory-management concepts are taught in lessons and tested
  through *observable behavior* (`__slots__` rejecting attributes,
  `sys.getrefcount`, `gc`, `weakref`, correctness of an optimized algorithm),
  not timing.

All new content follows the existing mission-dict contract
(`CONTRIBUTING.md`): `slug`, `title`, `kind` (`standard`/`boss`/`tier_boss`),
`xp`, `lesson_md`, `prompt_md`, `starter_code`, `hidden_tests`,
`solution_md` (exactly one ```python fence), plus `example_tests` on
`standard` missions only. `test_content.py` enforces solution-vs-hidden-test
correctness and the no-visible-tests-on-boss rule in CI.

## Part 1 — Realm 5: Systems & Performance

`app/content/tier5.py`, registered in `ALL_TIERS`.

- `slug: "systems-performance"`, `order: 5`, `min_level: 8`, not optional.
- Gates behind Realm 3's tier boss (Realm 4 is optional and transparent to
  the gating chain — see `app/services/progress.py`), plus level ≥ 8.
  (`min_level` is tunable; level ~14 is reachable after realms 1-3.)

Six teaching quests (each: lesson + 5-question quiz + `standard` mission with
`example_tests` + `boss` mission with hidden tests + a `badge`), then a timed
tier-boss battle quest:

| Quest slug | Concept | Boss mission (hidden-tested) | Badge |
|---|---|---|---|
| `slots-memory` | `__slots__`, memory layout | class with `__slots__` that rejects stray attributes and exposes no `__dict__` | Slot Smith 🧩 |
| `descriptors` | descriptor protocol (`__get__`/`__set__`/`__set_name__`) | a validating typed descriptor (positive-number / type-checked field) | Descriptor Adept 🔬 |
| `gc-weakref` | refcounting, cycles, `gc`, `weakref` | a weak-value cache whose entries can be garbage-collected | Cycle Breaker ♻️ |
| `threading-locks` | threads, `Lock`, `queue.Queue` | a thread-safe producer/consumer that aggregates via a queue | Lock Keeper 🔐 |
| `asyncio-coroutines` | `async`/`await`, `gather`, `Semaphore` | a bounded-concurrency async runner (deterministic via `asyncio.sleep(0)`) | Async Ace ⚡ |
| `typing-internals` | `get_type_hints`, `Protocol`, `Generic` | a generic typed container / runtime structural check | Type Theorist 📐 |
| **boss battle** `systems-crucible` | combine | a descriptor **and** an async `gather` in one timed submission (`time_limit_seconds: 1200`) | Systems Sovereign 👑 |

## Part 2 — Realm 6: Hero's Trial

`app/content/tier6.py`, registered in `ALL_TIERS`.

- `slug: "heros-trial"`, `order: 6`, `min_level: 12`, not optional.
- Gates behind Realm 5's tier boss, plus level ≥ 12.

Design-pattern and "build" quests (same quest/mission shape as above):

| Quest slug | Concept | Boss build (hidden-tested) | Badge |
|---|---|---|---|
| `factory-registry` | Factory / registry pattern | a plugin registry that constructs objects by key | Pattern Smith 🏭 |
| `observer-pubsub` | Observer / pub-sub | an event emitter with subscribe / unsubscribe / emit | Signal Keeper 📡 |
| `strategy-command` | Strategy + Command/undo | a command stack supporting undo | Tactician ♟️ |
| `lru-cache` | build an LRU cache | a capacity-bounded LRU cache with correct eviction order | Cache Architect 🗃️ |
| `tiny-orm` | build an in-memory ORM | declare fields → insert → filter/query records | Data Smith 🛢️ |
| `async-pipeline` | async pipeline over a mock stream | a bounded-worker async pipeline over a fake async source | Flow Master 🌊 |
| **boss battle** `heros-capstone` | capstone | a multi-part build combining a pattern with a build (`time_limit_seconds: 1800`) | Python Hero 🦸 |

## Part 3 — Mock Interview Arena

A timed, randomized practice mode. **Reuses existing question banks** rather
than authoring arena-only content.

### Data model (new tables in `app/models.py`)

- `InterviewSession`: `id`, `created_at`, `finished_at` (nullable),
  `difficulty` (str), `num_questions` (int), `score` (int), `total` (int).
  Immutable once `finished_at` is set.
- `InterviewRound`: `id`, `session_id` (FK), `order`, `kind`
  (`"mcq"`/`"coding"`), `ref_id` (QuizQuestion.id or Challenge.id), `answer`
  (text/nullable), `correct` (bool), `points` (int), `elapsed_seconds`
  (float/nullable).

Score is computed from `InterviewRound` rows, not a mutable counter —
consistent with the project's append-only convention.

### Question pool

- **MCQ rounds** drawn randomly from the existing `QuizQuestion` bank.
- **Coding rounds** drawn from existing `boss`/`tier_boss` `Challenge` rows,
  graded through the **existing** `run_hidden_tests` — no new grading path.
- **Difficulty → source tiers:** *Standard* draws from tiers 2-3; *Expert*
  draws from tiers 4-6. Selection is randomized and seeded per session so a
  session is reproducible for display.

### Router (`app/routers/arena.py`)

- `GET /arena` — config form (difficulty, length), past sessions, personal best.
- `POST /arena/start` — create session, select & persist its rounds, redirect
  to the first round.
- `GET /arena/round/{session_id}` — render the current round (MCQ or coding)
  with a per-round Alpine countdown.
- `POST /arena/answer/{session_id}` — grade the round (MCQ: compare index;
  coding: `run_hidden_tests`), record it, advance; HTMX swaps in the next
  round or the results partial.
- `GET /arena/results/{session_id}` — final score, per-round breakdown,
  personal best.

### UI

- `templates/arena.html`, `partials/arena_round.html`,
  `partials/arena_result.html`.
- Arena entry in `base.html` nav, unlocked at level ≥ 8 (endgame gate).
- Small XP award per correct round via the XP ledger, idempotency key
  `arena:{session_id}:{round_order}` so replays never double-award.
- **No leaderboard** — personal-best only, matching the project's deliberate
  Achiever / anti-comparison stance.

## Wiring & cleanup

- Register `tier5.TIER`, `tier6.TIER` in `app/content/__init__.py:ALL_TIERS`
  (and the `from . import` line).
- Delete the two hardcoded placeholder `<section class="tier locked">` blocks
  in `app/templates/map.html` (Realm 5 & 6 "Coming in Phase 2").
- Reseed in dev by deleting `app.db`; seeding is idempotent and a no-op when
  any `Tier` row already exists. New `InterviewSession`/`InterviewRound`
  tables are created by `Base.metadata.create_all` on startup.

## Testing

- `tests/test_content.py` already auto-covers every new mission (solution vs
  its hidden tests; bosses carry no `example_tests`; quizzes well-formed).
- `tests/test_quiz_content.py` covers new quiz questions.
- New `tests/test_arena.py`: session creation, round selection by difficulty,
  MCQ + coding grading, score computation, idempotent XP, results.
- Full `pytest` must be green; then drive the running app (`python run.py`) to
  confirm the map shows Realms 5 & 6 unlocked at the right levels and an arena
  session plays through end to end.

## Build order

1. Realm 5 content (`tier5.py`) → `pytest tests/test_content.py -k tier5` green.
2. Realm 6 content (`tier6.py`) → `pytest -k tier6` green.
3. Wire `ALL_TIERS`, remove `map.html` placeholders, reseed → map renders.
4. Arena: models → service → router → templates → nav.
5. `tests/test_arena.py`, full `pytest` green, drive the app end to end.

## Out of scope

- Cosmetic unlocks (themes / map skins) from the original spec's endgame list.
- Spaced-repetition flashcards.
- Any monetization or leaderboard mechanics (explicitly excluded by project ethos).
