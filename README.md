# 🐍 Python Zero-to-Hero

A solo-use, gamified Python learning platform: 5 tiered "Realms" of quests
and missions, auto-graded by hidden pytest suites, with XP, levels, streaks,
freeze tokens, badges, and boss battles. Built with FastAPI + Jinja2 + HTMX +
SQLite — the codebase itself doubles as advanced-Python practice.

Design spec: `docs/superpowers/specs/2026-07-05-python-zero-to-hero-design.md`

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py            # http://127.0.0.1:8000
```

The SQLite database (`app.db`) is created and seeded with the Tier 1–3
curriculum on first startup.

## How it works

- **Curriculum** — `app/content/tier{1,2,3}.py` seed 21 quests / 39
  challenges. Each mission is a short lesson + a coding challenge graded
  against a hidden pytest suite. Quest bosses award badges; each realm ends
  in a timed Boss Battle that (with a level requirement) gates the next
  realm.
- **Grading** — `app/grading.py` writes your code to a temp dir and runs the
  hidden suite via `subprocess` with a 5s timeout and a Unix memory cap.
  ⚠️ Not a security sandbox — local solo use only, never expose publicly.
- **XP** — append-only ledger (`xp_ledger`) with idempotency keys; current XP
  is `SUM(delta)`. Levels unlock realms.
- **Streak** — evaluated lazily on each passing submission using local
  dates; freeze tokens (earned every 7-day streak, max 2 banked) cover a
  single missed day.
- **Badges** — declarative rules (`achievement_rules`) evaluated by one
  engine on submission events.
- **Ethics** — no leaderboards, no monetization, streak freezes exist, and
  the whole game layer can be hidden with one click in the header.

## Scope

MVP = Tiers 1–3 + full gamification loop. Phase 2 (per spec): Tiers 4–5,
Mock Interview Arena, GitHub-Actions grading backend, cosmetic unlocks.
