# Python Zero-to-Hero: Gamified Learning Platform — Design

## Purpose & Context

A solo-use, gamified Python learning website taking the user from absolute
basics to advanced concepts, weighted toward what actually gets asked in
**advanced Python technical interviews**. Building the site itself is also
intended as Python practice and a portfolio artifact — the codebase should be
something the user can discuss in an interview, not just the content inside
it.

- **Audience:** solo — just the site owner. No accounts, no multi-user
  features, no public traffic.
- **Deployment:** local machine only, or a GitHub-Actions-based flow. Never
  exposed to the public internet in the current scope.
- **Success criteria:** the user completes the curriculum (Tiers 1–5) and
  feels interview-ready on advanced Python concepts, with a working gamified
  app they can show off.

## Tech Stack & Architecture

- **Backend:** FastAPI (routes, Pydantic validation). Chosen over a
  JS/TS frontend because every route handler, decorator, generator, or async
  endpoint written to build the site doubles as advanced-Python practice.
- **UI:** Jinja2 templates + HTMX for server-driven interactivity (progress
  bars, XP toasts, quest-map unlocks via partial swaps) with a light
  Alpine.js sprinkle for pure client-side flourishes (confetti on level-up,
  animated counters). No React/Next.js build.
- **Database:** SQLite via SQLAlchemy — file-based, zero-ops, appropriate for
  solo use, and swappable to Postgres later without a rewrite.
- **Code execution:** submitted code runs via `subprocess` with a timeout
  (e.g. 5s) and, on Unix, a memory cap via the `resource` module. No
  Docker/sandbox hardening in this scope, since there's no untrusted public
  traffic — flagged as the one piece that would need rework if the site were
  ever exposed publicly.

## Curriculum

Content is organized as 5 Tiers ("Realms") on a skill-tree map. Each Tier
contains Quests (topics) made of bite-sized Missions (a short lesson +
auto-graded coding challenge). Later tiers skew hard toward advanced-interview
material.

1. **Foundations (Novice):** variables/types/operators, control flow,
   functions & scope, strings, core collections (list/tuple/dict/set), basic
   error handling.
2. **Core Craftsmanship (Apprentice):** comprehensions, `*args`/`**kwargs` &
   closures, OOP basics (classes, inheritance, dunder methods), file I/O &
   context managers, modules/packages/venvs, intro to `pytest`.
3. **Pythonic Mastery (Journeyman):** iterators & generators (`yield`),
   decorators (incl. `functools.wraps`), custom context managers, advanced
   OOP (ABCs, mixins, MRO, metaclasses intro), functional tools
   (`map`/`filter`/`reduce`, `itertools`, `functools`), exception chaining &
   custom exceptions.
4. **Systems & Performance (Expert)** — the interview-crusher tier: memory
   management & GC (refcounting, cycles), the GIL, threading vs.
   multiprocessing vs. `asyncio`, event loop & coroutines, Big-O applied in
   Python, descriptors & `__slots__`, type hints/`mypy`/typing internals,
   concurrency primitives (locks, queues).
5. **Hero's Trial (Capstone / Endgame):** design-pattern implementations,
   "Boss Battle" builds (e.g. a decorator-based cache, a mini async web
   scraper, a tiny ORM), a Mock Interview Arena (timed, randomized
   advanced-concept questions), and a final capstone project.

## Gamification Design

Solo use means mechanics lean on **Achiever** (mastery, interview stakes) and
**Free Spirit** (autonomy, customization) motivations. No Socialiser/
leaderboard mechanics — there is no one to compare against, and global
leaderboards are a known e-learning demotivator for anything short of the
top performer.

| Mechanic | Core Drive(s) | Phase | Purpose |
|---|---|---|---|
| XP + Levels | Development & Accomplishment | Onboarding→Scaffolding | Every completed lesson/challenge awards XP; leveling up unlocks the next Tier, keeping the full curriculum from being visible/overwhelming at once |
| Skill-tree world map | Epic Meaning + Ownership | All | Visualizes the whole journey; progress bars get more granular near tier completion (goal-gradient effect) |
| Badges (e.g. "Decorator Wizard", "GIL Whisperer") | Ownership & Possession | Scaffolding→Endgame | Awarded only for passing a concept's boss challenge — tied to demonstrated skill, not participation |
| Daily streak + freeze token | Loss & Avoidance | Scaffolding | Freeze earned through consistent practice (not purchased); mandatory safety valve — Duolingo data shows freeze users retain ~48% longer past day 7 |
| Personal-best tracking | Achiever (competition substitute) | Scaffolding→Endgame | Compete against your own past solve time/attempts, since there's no other player to compare against |
| Boss Battles (end of each tier) | Hard Fun / mastery | Gates progression | Timed, hint-free, hidden test suite — a real mastery checkpoint |
| Mock Interview Arena | Hard Fun + Unpredictability | Endgame | Randomized advanced-concept questions under time pressure |
| Spaced-repetition flashcards | Curiosity | Scaffolding | Lightweight variable-reward review for retention, not a compulsive-checking loop |
| Cosmetic unlocks (themes, map skins) | Ownership | Endgame | Free Spirit payoff for long-term engagement; purely cosmetic, no pay-to-win (no monetization exists) |

**Ethics check (passed):**
- Streak has a grace/freeze mechanic — no single missed day erases long-term
  progress.
- No leaderboard — avoids the e-learning comparison-anxiety trap.
- The entire gamified layer is toggle-able (XP/streak UI can be hidden).
- Badges gate on passing hidden tests (real mastery), not on participation —
  avoids rewarding motion over competence.
- No monetization, no purchasable power-ups, no manufactured scarcity.

## Data Model

Core tables (SQLAlchemy + SQLite):

- `tiers`, `quests`, `lessons`, `challenges` — static curriculum content,
  seeded rather than user-generated.
- `submissions` — each code attempt: challenge_id, code, pass/fail, hidden
  test results, timestamp.
- `xp_ledger` — **append-only** event log
  (`event_type, delta, idempotency_key, created_at, metadata`). Current XP is
  `SUM(delta)`, not a mutable counter — avoids double-award bugs and gives an
  auditable history.
- `streak_state` — `last_active_local_date`, `current_streak`,
  `longest_streak`. Evaluated lazily on each qualifying action (not a
  midnight cron job) to sidestep timezone/day-boundary bugs.
- `freeze_tokens` — its own grant/consumption ledger, same pattern as XP.
- `achievement_rules` (`trigger_event, condition, badge_id`) +
  `achievements_earned` — a declarative rule engine evaluated on each
  submission event, rather than scattered `if` checks in the grading code.

## Code Execution / Auto-Grading Flow

1. User submits code for a challenge in the browser.
2. FastAPI writes it to a temp file, runs it via `subprocess` against that
   challenge's hidden `pytest` suite, with a timeout and memory cap.
3. Result (pass/fail, failing test names, stdout/stderr) returns to the UI
   via an HTMX partial swap — no full page reload, so the reward moment (XP
   toast, progress tick, badge popup) feels instant.
4. On pass, an event fires into the XP ledger and the achievement-rule
   engine.

## MVP vs. Stretch Scope

**MVP:**
- Curriculum Tiers 1–3
- XP/levels, streak + freeze, badges, skill-tree map
- Local subprocess-based grading

**Stretch (Phase 2):**
- Curriculum Tiers 4–5
- Mock Interview Arena
- GitHub-Actions-based grading as an alternate execution backend
  (push-to-grade workflow tied to a real commit graph) — deferred because it
  adds real complexity (repo scaffolding, webhook/API auth, polling for run
  results) beyond what MVP needs
- Cosmetic unlocks
