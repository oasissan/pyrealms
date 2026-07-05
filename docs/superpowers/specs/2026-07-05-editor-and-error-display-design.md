# Code Editor & Readable Test Errors — Design

Date: 2026-07-05
Status: Approved (user selected both recommended options)

## Goal

Replace the bare `<textarea>` editor with a real code editor, and replace raw
pytest output with beginner-readable, per-test failure cards showing the call
that was made, the expected value, and what the learner's code actually
returned or raised.

## Decisions (user-approved)

1. **Editor:** CodeMirror 6 loaded from a CDN (esm.sh), matching the
   existing no-build-step convention (htmx/Alpine via unpkg). Progressive
   enhancement: the `<textarea name="code">` stays as the source of truth, so
   the page still works if the CDN is unreachable.
2. **Error detail:** failed tests reveal inputs + expected vs got. Each
   failed test renders as a card: `Called`, `Expected`, `Got`, or a crash
   panel with the exception type, message, and the offending line of the
   learner's own code.

## Architecture

### 1. Structured grading (`app/grading.py`)

- **Syntax pre-check:** before spawning pytest, `compile(code,
  "solution.py", "exec")` in the parent (compile only — never executed).
  A `SyntaxError` returns immediately with structured line/offset/text for a
  caret-pointer display. Faster and cleaner than letting collection fail.
- **Reporter plugin:** grading writes a `conftest.py` into the tempdir
  alongside `solution.py` and `test_solution.py`. A
  `pytest_runtest_makereport` hookwrapper captures, per test:
  - name, outcome
  - for `AssertionError`: pytest's rewritten explanation (e.g.
    `assert 5 == 6\n + where 5 = solve([1, 2, 3])`) parsed into
    `got` / `expected` / `call`
  - for other exceptions: type, message, and the deepest traceback frame
    inside `solution.py` (line number + source line)
  and writes `report.json` in the tempdir.
- **New dataclasses:** `TestCaseResult` (name, outcome, call, expected, got,
  error_type, error_message, user_line_no, user_line, detail) and extended
  `GradeResult` (adds `tests`, `syntax_error`, counts). Raw output is kept
  (ANSI-stripped) as a fallback and for `Submission.output` storage.
- **Fallbacks:** if `report.json` is missing/empty but pytest failed (e.g.
  import-time crash at module level), show the cleaned raw output.

### 2. Result partial (`partials/result.html` + CSS)

- Summary bar: "3 / 5 tests passed" with a mini progress bar.
- Passed tests as compact green chips; failed tests as cards per the
  approved mockup (Called / Expected / Got, or 💥 crash panel with the
  learner's offending line).
- Syntax error panel with the source line and a caret pointing at the
  offset.
- Timeout panel styled consistently.

### 3. Editor (`mission.html`, `style.css`)

- `<script type="module">` importing `codemirror` (basicSetup),
  `@codemirror/lang-python`, and the One Dark theme from esm.sh.
- The CodeMirror view is created from the textarea's content; the textarea
  is hidden. On `htmx:configRequest` (and native submit) the doc is synced
  back to the textarea, so form serialization is unchanged.
- If the module import fails (offline), the textarea remains visible and
  keeps the existing Tab-to-indent handler.

## Testing

- New `tests/test_grading.py` (TDD): passing run, assertion failure parsed
  into call/expected/got, exception with learner line extraction, syntax
  error pre-check, isinstance-style assertion fallback to detail text,
  timeout (with patched `TIMEOUT_SECONDS`).
- Template/editor verified by running the app.

## Out of scope

- Sandboxing changes, storing structured reports in the DB, editor
  autocomplete/linting.
