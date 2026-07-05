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

Every challenge's canonical solution must pass its own hidden suite, and
every Boss must stay fully hidden — `tests/test_content.py` enforces both
(CI runs it on every push). Run the whole suite locally:

```bash
pytest
```

`test_content.py` extracts the code from each mission's `solution_md` and
runs it against that mission's `hidden_tests` (and against the visible
`example_tests`), so a solution can never silently rot and example tests
can never diverge from reality.

## Adding a new challenge

Each mission is a dict in `app/content/tier{N}.py` with: `slug`, `title`,
`kind` (`standard` / `boss` / `tier_boss`), `xp`, `lesson_md`, `prompt_md`,
`starter_code`, `hidden_tests` (a full pytest file body that imports from
`solution`), and `solution_md` — the canonical answer as markdown with
**exactly one** ```python fenced block plus a short **Why:** note; it's
revealed to the learner once they pass. Standard (non-Boss) missions should
also include `example_tests`: a small, visible subset of assertions that
the same solution passes. Do **not** add `example_tests` to a Boss — they
stay hidden.

Quests that award a badge need a `badge` dict on the quest; the seeder
wires the achievement rule to that quest's boss mission automatically
(`app/seed.py`). A whole realm can be marked `"optional": True` on its tier
dict (like the Proving Grounds) — optional realms unlock on level alone and
never gate the main path.

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
