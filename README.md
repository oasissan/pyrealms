# 🐍 PyRealms

**Python Zero-to-Hero** — a gamified path from your first script to
interview-ready, built as a real app you run yourself.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/oasissan/pyrealms/actions/workflows/deploy.yml/badge.svg)](https://github.com/oasissan/pyrealms/actions/workflows/deploy.yml)

Five tiered "Realms" of quests and missions, auto-graded by hidden pytest
suites, with XP, levels, streaks, freeze tokens, badges, and timed Boss
Battles. Built with FastAPI + Jinja2 + HTMX + SQLite — no build step, no
JS framework, no account system. The codebase itself is meant to double as
advanced-Python practice for anyone reading it.

Design spec: [`docs/superpowers/specs/2026-07-05-python-zero-to-hero-design.md`](docs/superpowers/specs/2026-07-05-python-zero-to-hero-design.md)

## Quick start

```bash
git clone https://github.com/oasissan/pyrealms.git
cd pyrealms
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py            # http://127.0.0.1:8000
```

The SQLite database (`app.db`) is created and seeded with the Tier 1–3
curriculum on first startup. It's gitignored — delete it any time to
reset your progress and reseed from scratch.

## Features

- **21 quests, 39 challenges** across 3 realms (Foundations, Core
  Craftsmanship, Pythonic Mastery), each a short lesson + a coding
  challenge auto-graded against a hidden pytest suite
- **XP & levels** — an append-only ledger (never a mutable counter), with
  levels gating access to later realms
- **Streaks with freeze tokens** — evaluated lazily on local dates, no
  midnight-cron timezone bugs; freeze tokens are *earned* (7-day streak),
  never bought
- **Badges** on a declarative rule engine, gated on passing a boss
  challenge — never on participation alone
- **Timed, hint-free Boss Battles** at the end of each realm
- **Personal-best tracking** (attempts-to-first-pass, fastest solve) —
  since there's no leaderboard, you compete against your own past runs
- **One-click toggle** to hide the entire gamified layer if you just want
  the curriculum
- No accounts, no leaderboards, no monetization — see the design spec's
  ethics check for why

## How it works

- **Curriculum** — `app/content/tier{1,2,3}.py` are the seed data: each
  mission is a dict with a lesson, a prompt, starter code, and a hidden
  pytest suite. `app/seed.py` loads them into SQLite on first boot.
- **Grading** — `app/grading.py` writes your submission to a temp dir and
  runs the hidden suite via `subprocess`, with a 5s timeout and a Unix
  memory cap. ⚠️ **Not a security sandbox** — fine for running on your own
  machine; if you deploy it somewhere reachable by others, put it behind
  auth (see `app/auth.py` — set `APP_USERNAME`/`APP_PASSWORD` env vars).
- **XP** — `app/services/xp.py`; current XP is `SUM(delta)` over
  `xp_ledger`, with idempotency keys so re-passing a challenge never
  double-awards.
- **Streaks & freezes** — `app/services/streak.py`.
- **Achievements** — `app/services/achievements.py`, a small rule engine
  evaluated on submission/streak events instead of scattered `if` checks.
- **Progress/unlocks** — `app/services/progress.py` computes what's
  unlocked on every request from submission history — no separate
  "progress" state to drift out of sync.

## Deploying it yourself

This is designed to run locally, but if you want it reachable elsewhere
(e.g. as a portfolio demo), see [`DEPLOY.md`](DEPLOY.md) for a free-tier
Oracle Cloud VM walkthrough with GitHub Actions auto-deploy on push. Set
`APP_USERNAME`/`APP_PASSWORD` before making it public — see the grading
caveat above.

## Roadmap

MVP (done): Tiers 1–3, full gamification loop, local subprocess grading.

Stretch (not yet built): Tiers 4–5 (systems/performance, capstone), a Mock
Interview Arena, an alternate GitHub-Actions-based grading backend,
cosmetic unlocks.

## Contributing

Contributions welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup
and how challenges are structured. Please follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE) — use it, fork it, adapt it for your own curriculum.
