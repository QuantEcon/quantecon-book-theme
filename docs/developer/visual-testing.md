# Visual Regression Testing

Playwright-based tests capture screenshots of pages from the
[`quantecon-book-theme-fixtures`](https://github.com/QuantEcon/quantecon-book-theme-fixtures)
site and compare them against baseline snapshots to detect unintended
styling changes. The fixtures repo is a curated, stable rendering target:
the landing page, 12 synthetic pages (one per theme surface), and
real-world lecture captures that previously exposed theme bugs.

The fixtures repo is **pinned to a specific commit** in the theme's CI
workflows (`FIXTURES_SHA` in `.github/workflows/ci.yml` and
`.github/workflows/update-snapshots.yml`), so the test input doesn't move
between theme PRs.

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
1. Clone `quantecon-book-theme-fixtures` (if not present)
2. Check out the requested ref — defaults to `main`, overridable via the
   `FIXTURES_REF` env var (accepts SHA, branch, or tag)
3. Build the fixtures site with `jb build .`
4. Install Playwright and Chromium
5. Run visual regression tests against the build

To pin to the same fixtures commit as CI for local testing:

```console
$ FIXTURES_REF=<sha-from-ci.yml> tox -e visual
```

### Updating Local Baselines

```console
$ tox -e visual-update
```

Local baselines are stored in `tests/visual/macos/` (gitignored) and are
separate from CI baselines in `tests/visual/__snapshots__/`, since
screenshot rendering differs between macOS and Linux.

## CI Integration

Visual tests run as part of the `ci.yml` workflow on every push and PR:

1. Checks out the fixtures repo at `FIXTURES_SHA`
2. Installs build deps via `pip install -r fixtures/requirements.txt`
3. Installs the PR's theme via `pip install .`
4. Builds the fixtures site with `jb build . --warningiserror`
5. Runs Playwright against the build
6. Deploys the fixtures site to Netlify as a PR preview (reviewers can
   click through every fixture page with this PR's theme applied)

### Updating CI Baselines via PR Comments

Two commands are available as PR comments:

| Command | Behavior |
|---|---|
| `/update-snapshots` | Regenerates **all** baselines — use for styling changes |
| `/update-new-snapshots` | Adds only **missing** baselines — use for new tests |

Both commands:
- Check out the fixtures repo at the pin read from this PR branch's `ci.yml`
- Build the fixtures site with the PR's theme applied
- Run Playwright on Ubuntu for platform-consistent snapshots
- Re-run the suite against the freshly written baselines to confirm they
  reproduce (see below)
- Commit updated snapshots to the PR branch
- Post a summary comment on the PR

Both are restricted to users with an `OWNER`, `MEMBER`, or `COLLABORATOR`
association — they check out and execute PR-branch code under a token with
write access.

The `/update-snapshots` command also uploads a `snapshot-update-diff` artifact
with before/after images for review.

### Baselines are re-checked before the commit

After regenerating, the workflow runs the suite once more *without*
`--update-snapshots`, against the same built site that produced the images. The
summary comment reports the outcome either way, so a bad regeneration is visible
immediately instead of surfacing later on `main`. Note this reports; it does not
gate — the commit and push happen regardless, so the images are always available
to inspect.

What a failure means depends on which command you ran:

- After `/update-snapshots`, every baseline was rewritten, so a failure means
  the images just written don't reproduce against the same build — that is,
  the render is not deterministic.
- After `/update-new-snapshots`, only *missing* baselines were created and
  existing ones were left untouched, while the verify run covers the whole
  suite. A failure there may be in what was just added, or in an existing
  baseline the PR legitimately invalidated. The comment says so rather than
  guessing; use `/update-snapshots` if the latter.

The verify run writes to its own `test-results-verify/` directory. This matters:
Playwright clears its output directory at the start of every run, so sharing
`test-results/` would erase the regeneration images that the
`snapshot-update-diff` artifact exists to carry.

### Making the bot's commit trigger CI

Commits pushed with the default `GITHUB_TOKEN` do **not** raise `push` or
`pull_request` events — GitHub's loop-prevention rule. So by default the
regenerated baselines land while the PR's `visual` check still shows its
previous, now-stale failure, and you have to push an empty commit to re-run it.

To make this automatic, add a repository secret named `SNAPSHOT_BOT_TOKEN`
holding a fine-grained personal access token (or GitHub App installation token)
with **Contents: read and write** on this repository. The workflow picks it up
automatically and pushes with it; CI then re-runs on the PR without any manual
step. If the secret is absent the workflow falls back to `GITHUB_TOKEN` and
still works — the summary comment just tells you to push the empty commit.

```{note}
`issue_comment` workflows always load the workflow file from the **default
branch**, not from the PR branch. If a PR changes `update-snapshots.yml`
itself, the new workflow takes effect only after that change has been
merged to `main`.

The fixtures pin is the deliberate exception: the workflow re-reads
`FIXTURES_SHA` out of the checked-out branch's `ci.yml`, so a PR that bumps
the pin regenerates against the fixtures it actually tests against. Without
that, such a PR regenerates against `main`'s fixtures, gets byte-identical
baselines, commits nothing, and can never go green.
```

## Bumping the fixtures pin

To consume new fixtures (e.g. after a real-world capture is added to the
fixtures repo):

1. Open a PR on
   [`quantecon-book-theme-fixtures`](https://github.com/QuantEcon/quantecon-book-theme-fixtures)
   adding the page. See its `real-world/README.md` for capture conventions.
2. Once merged, open a follow-up PR on this repo that bumps `FIXTURES_SHA`
   in `ci.yml` (the source of truth — `update-snapshots.yml` reads it from
   there, and its own copy is only a fallback) and, if needed, adds a
   corresponding test entry in `theme.spec.ts`.
3. Comment `/update-new-snapshots` on that PR to seed baselines for any
   newly tested pages.

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
The `tox.ini` `[testenv:visual]` and `[testenv:visual-update]` sections
contain the full environment setup including the fixtures-repo clone +
checkout dance and dependencies like `jupyter-book`, `sphinx-exercise`,
etc.
