# Contributing to PyRealms

Thanks for considering a contribution! This started as a personal learning
project, but it's built to be genuinely useful (and forkable) for anyone
studying Python.

## Getting set up

```bash
git clone https://github.com/<you>/pyrealms.git
cd pyrealms
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py            # http://127.0.0.1:8000
```

The SQLite database (`app.db`) is created and seeded automatically on first
run. Delete it any time to reseed from scratch.

## Before opening a PR

Every challenge's hidden test suite must stay solvable — CI checks this on
every push. Run the same check locally:

```bash
python -c "
from app.content import ALL_TIERS
for tier in ALL_TIERS:
    for quest in tier['quests']:
        for m in quest['missions']:
            print(m['slug'])
"
```

If you add or edit a challenge in `app/content/tier{1,2,3}.py`, write a
reference solution and confirm it passes the `hidden_tests` you wrote via
`app/grading.run_hidden_tests(solution_code, hidden_tests)` — a broken
hidden-test suite silently locks learners out of that mission.

## Adding a new challenge

Each mission is a dict in `app/content/tier{N}.py` with: `slug`, `title`,
`kind` (`standard` / `boss` / `tier_boss`), `xp`, `lesson_md`, `prompt_md`,
`starter_code`, and `hidden_tests` (a full pytest file body that imports
from `solution`). Quests that award a badge need a `badge` dict on the
quest; the seeder wires the achievement rule to that quest's boss mission
automatically (`app/seed.py`).

## Code style

- No comments explaining *what* code does — only *why*, when it's
  non-obvious (a workaround, an invariant, a subtle constraint).
- Keep new dependencies out unless they earn their place — this project
  intentionally stays small (FastAPI, SQLAlchemy, Jinja2, HTMX, Alpine).
- Match the existing service-layer pattern (`app/services/`) for anything
  touching XP, streaks, or achievements — those are append-only ledgers by
  design (see `README.md`); don't reintroduce mutable counters.

## Reporting bugs / suggesting features

Open a GitHub issue. Include repro steps for bugs (which mission, what you
submitted, what you expected).

## License

By contributing, you agree your contributions are licensed under this
project's [MIT License](LICENSE).
