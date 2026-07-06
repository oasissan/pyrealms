# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

PyRealms — a gamified, self-hosted Python curriculum. FastAPI + Jinja2 +
HTMX + SQLite, no JS framework, no build step, no accounts. Learners work
through tiered "Realms" of quests/challenges, auto-graded against hidden
pytest suites, earning XP/levels/streaks/badges. Full feature rationale is
in `README.md`; the original design spec is
`docs/superpowers/specs/2026-07-05-python-zero-to-hero-design.md`.

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py                 # serves on http://127.0.0.1:8000, auto-reload

pytest                        # full suite
pytest tests/test_grading.py  # one file
pytest tests/test_grading.py::test_timeout   # one test
pytest tests/test_content.py -k tier1        # every mission whose id contains "tier1"
```

There's no lint/format/typecheck command configured — CI (`.github/workflows/deploy.yml`)
only does `python -c "import app.main"` and `pytest -q`.

The SQLite file `app.db` is created and seeded on first app startup (see
`app/seed.py`, called from the FastAPI `lifespan` in `app/main.py`).
Seeding is a no-op if any `Tier` row already exists — delete `app.db` to
force a reseed after editing curriculum content. Tests don't touch
`app.db`; they call `run_hidden_tests` / content helpers directly.

## Architecture

**Content vs. database.** The curriculum lives as plain Python dicts in
`app/content/tier{1,2,3,4}.py` (tier4 is the optional "Proving Grounds"
DSA realm — see `optional: True` on its tier dict). `app/seed.py` loads
this static content into SQLAlchemy rows (`Tier` → `Quest` → `Challenge`)
once, idempotently. To change curriculum content, edit the tier files and
delete `app.db`; don't hand-edit rows.

**Solution rot is prevented by tests, not review.** Every mission's
`solution_md` (canonical answer shown after passing) has its Python
extracted (`app/content/__init__.py:solution_code`, first ```python
fence) and run against that same mission's `hidden_tests` in
`tests/test_content.py`. This is the test suite's main job — if you add
or edit a mission, this is what will catch a broken example. Boss/tier_boss
missions must never have `example_tests` (visible tests are only for
standard missions); this is also asserted in `test_content.py`.

**Grading is a real subprocess, not a sandbox.** `app/grading.py` writes
the learner's code + the hidden test file + an injected `conftest.py`
reporter plugin into a temp dir and runs real pytest via `subprocess`,
with a 5s timeout and (POSIX-only) an `RLIMIT_AS`/`RLIMIT_CPU` cap. The
reporter plugin captures structured per-test outcomes (call/expected/got,
or crash type + the learner's own line) into `report.json`, which
`_build_test_results` turns into `TestCaseResult` objects — this is what
lets the UI show a readable diff instead of raw pytest output. This is
explicitly **not** a security boundary; see the warnings in `README.md`,
`DEPLOY.md`, and `app/auth.py` before exposing the app beyond localhost.

**Progress/unlocks are computed, not stored.** `app/services/progress.py`
(`build_map`) derives the entire unlock state — which tiers/quests/
challenges are open — from `Submission` history plus current level, on
every request. There's no separate mutable "unlocked" flag to drift out
of sync. Unlock rules: Tier 1 is always open; tier N unlocks once tier
N-1's boss is passed *and* the learner's level meets `min_level`
(`optional` tiers skip the boss-gate and only check level). Inside a
tier, regular quests are open immediately; a tier's boss quest unlocks
once every other quest in the tier is complete. Inside a quest, challenges
unlock sequentially.

**XP, streaks, and freeze tokens are append-only ledgers**, never mutable
counters — this is a deliberate project convention (see `CONTRIBUTING.md`).
`app/services/xp.py`: current XP is `SUM(delta)` over `XpEvent`, keyed by
`idempotency_key` so re-passing a challenge never double-awards.
`app/services/streak.py`: streak state (`StreakState`) is evaluated
lazily against local dates on each qualifying action (no midnight cron);
`FreezeEvent` is a separate grant/consume ledger — freeze tokens are
earned every 7-day streak (capped at `MAX_FREEZE_BALANCE`), never bought.
Follow this ledger pattern for anything touching XP/streaks/achievements
rather than adding a mutable counter column.

**Achievements are a declarative rule engine**
(`app/services/achievements.py`), evaluated against `AchievementRule` rows
seeded from quest `badge` dicts (gated on that quest's boss challenge) plus
`META_ACHIEVEMENTS` in `app/content/__init__.py`. `evaluate(db, trigger_event,
context)` is called from the submit-challenge route after a pass; add new
badge conditions by extending `_condition_met`'s shape dispatch, not by
adding ad-hoc `if` checks in the router.

**Routers**: `app/routers/pages.py` serves full HTML pages (world map,
quest page, mission page) via `hud_context()` (XP/level/streak, shared
across every page). `app/routers/actions.py` handles HTMX POSTs — challenge
submission (the reward moment: grade → award XP → record streak → evaluate
achievements → return `partials/result.html`) and solution reveal
("give up" — records a `SolutionReveal`, no XP, doesn't mark the challenge
passed). `app/routers/chatbot.py` is a separate, mostly independent
subsystem (see below).

**Gemini Copilot chatbot** (`app/services/gemini_web.py`,
`app/routers/chatbot.py`) is a from-scratch reverse-engineered client for
the Gemini web UI, not a real API. It reuses the learner's own
browser-session cookies (`__Secure-1PSID`/`__Secure-1PSIDTS`), auto-detected
via `browser-cookie3` from Chrome/Edge/Firefox on the local machine
(`autodetect_cookies`), or configured manually and stored on the singleton
`Settings` row. It scrapes tokens (`SNlM0e`/`cfb2h`/`FdrFJe`) out of
`gemini.google.com/app`'s HTML and POSTs to Gemini's internal
`StreamGenerate` endpoint — brittle by nature (Gemini can change its page
format at any time) and entirely separate from the grading/curriculum
logic. Local-only in practice: cookie auto-detection reads OS browser
credential stores.

**Auth**: `app/auth.py`'s `BasicAuthMiddleware` is a no-op unless both
`APP_USERNAME` and `APP_PASSWORD` env vars are set — required before
exposing the app beyond localhost, since grading has no sandbox.

## Adding a curriculum challenge

See `CONTRIBUTING.md` for the full mission dict shape
(`slug`/`kind`/`hidden_tests`/`solution_md`/etc.) and badge wiring. The
short version: add a mission dict to the right tier file, give it a
`solution_md` with exactly one ```python fence, and make sure it passes
its own `hidden_tests` — `tests/test_content.py` will enforce this in CI.
