# Python Zero-to-Hero MVP Implementation Plan

> **For agentic workers:** Executed inline in the authoring session per user
> instruction ("implement based on the specification... no verification more
> than a terminal build"). Plan is architecture/task level; code lives in the
> repo, not duplicated here.

**Goal:** Build the MVP of the solo-use gamified Python learning platform from
`docs/superpowers/specs/2026-07-05-python-zero-to-hero-design.md`.

**Architecture:** FastAPI + Jinja2/HTMX server-rendered app, SQLite via
SQLAlchemy, subprocess-based pytest grading. Gamification state is
event-sourced (append-only XP ledger, freeze-token ledger, declarative
achievement rules) per the gamification implementation-patterns reference.

**Tech Stack:** Python 3, FastAPI, uvicorn, SQLAlchemy, Jinja2, HTMX (CDN),
Alpine.js (CDN), pytest, markdown.

## Global Constraints (from spec)

- Solo use, local only. No accounts, no auth, no public exposure.
- MVP scope: Tiers 1–3 curriculum; XP/levels; streak + freeze; badges;
  skill-tree map; subprocess grading (5s timeout, Unix memory cap).
- XP is `SUM(delta)` over an append-only ledger with `idempotency_key` —
  never a mutable counter.
- Streak evaluated lazily on qualifying actions using local dates; freeze
  tokens are earned (7-day streak), never purchased; own grant/consume ledger.
- Badges gate on passing boss challenges (hidden tests), not participation.
- Achievement rules are declarative rows (`trigger_event, condition, badge`),
  evaluated by one engine on submission events.
- Entire gamified HUD is toggle-able.
- No leaderboards, no monetization.

## File Structure

- `requirements.txt`, `run.py`, `.gitignore`, `README.md`
- `app/database.py` — engine, session, `get_db`
- `app/models.py` — Tier, Quest, Challenge, Submission, XpEvent,
  StreakState, FreezeEvent, AchievementRule, AchievementEarned, Settings
- `app/levels.py` — XP→level math
- `app/grading.py` — `run_hidden_tests(code, tests) -> GradeResult`
  (subprocess + pytest, timeout, `resource` caps)
- `app/services/xp.py` — `award_xp`, `total_xp`, level-up detection
- `app/services/streak.py` — `record_activity(db, today)`, freeze
  grant/consume, balance
- `app/services/achievements.py` — rule engine `evaluate(db, event, ctx)`
- `app/services/progress.py` — pass/unlock computation for tiers/quests/
  challenges, personal bests
- `app/content/tier{1,2,3}.py` — curriculum seed data (quests, missions,
  boss challenges, hidden pytest suites, badges, achievement rules)
- `app/seed.py` — idempotent DB seed
- `app/routers/pages.py` — map `/`, quest `/quest/{slug}`, mission
  `/mission/{slug}`
- `app/routers/actions.py` — `POST /challenge/{slug}/submit` (HTMX partial),
  `POST /settings/toggle-gamification`
- `app/main.py` — app wiring, static, templates, startup seed
- `app/templates/` — base, map, quest, mission + partials (result, hud)
- `app/static/style.css`

## Tasks

1. **Scaffold + data layer** — requirements, database, models, levels math.
2. **Grading engine** — subprocess pytest runner with timeout/memory cap,
   failing-test extraction.
3. **Gamification services** — XP ledger, streak+freeze, achievement rule
   engine, progress/unlock logic.
4. **Curriculum content + seed** — Tiers 1–3: 6 quests each (per spec topic
   list), each quest = 1 lesson mission + 1 boss mission (badge), plus a
   per-tier Boss Battle (timed, hint-free, gates next tier alongside a
   min-level requirement).
5. **Routes + templates** — skill-tree map with locked/unlocked realms and
   progress bars, quest and mission pages, HTMX submit flow with XP toast /
   level-up confetti / badge popup via OOB swaps, gamification toggle,
   personal-best display.
6. **Terminal build verification** — venv install, seed, boot uvicorn, curl
   the pages, POST passing/failing submissions, confirm XP/badge/streak
   events fire. Commit.
