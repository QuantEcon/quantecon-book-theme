# Visual Regression Testing

Playwright-based tests capture screenshots of key pages from a real lecture
site build and compare them against baseline snapshots to detect unintended
styling changes.

```{contents}
:local:
:depth: 2
```

## Running Visual Tests

### Locally

```console
$ tox -e visual
```

This will:
1. Clone `lecture-python-programming.myst` (if not present)
2. Build the lecture site with Jupyter Book
3. Install Playwright and Chromium
4. Run visual regression tests

### Updating Local Baselines

```console
$ tox -e visual-update
```

Local baselines are stored in `tests/visual/macos/` (gitignored) and are
separate from CI baselines in `tests/visual/__snapshots__/`.

## CI Integration

Visual tests run as part of the `ci.yml` workflow on every push and PR.

### Updating CI Baselines via PR Comments

Two commands are available as PR comments:

| Command | Behavior |
|---|---|
| `/update-snapshots` | Regenerates **all** baselines — use for styling changes |
| `/update-new-snapshots` | Adds only **missing** baselines — use for new tests |

Both commands:
- Build the lecture site with the PR's theme changes
- Run Playwright on Ubuntu for platform-consistent snapshots
- Commit updated snapshots to the PR branch
- Post a summary comment on the PR

The `/update-snapshots` command also uploads a `snapshot-update-diff` artifact
with before/after images for review.

## Test Structure

```
tests/visual/
├── README.md
├── theme.spec.ts         # Playwright test specifications
├── __snapshots__/        # CI baseline images (Ubuntu)
└── macos/                # Local baseline images (gitignored)
```

## Configuration

Visual test configuration is in `playwright.config.ts` at the project root.
The `tox.ini` `[testenv:visual]` section contains the full environment setup
including dependencies like `jupyter-book`, `sphinx-exercise`, etc.
