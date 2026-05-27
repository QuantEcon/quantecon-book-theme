# Visual Regression Tests

Playwright-based visual regression tests for the quantecon-book-theme.

## Overview

These tests capture screenshots of pages from the
[`quantecon-book-theme-fixtures`](https://github.com/QuantEcon/quantecon-book-theme-fixtures)
site and compare them against baseline snapshots to detect unintended styling
changes. The fixtures repo is a curated, stable rendering target: the
landing page (`intro.html`), 12 synthetic pages (one per theme surface),
and real-world lecture captures that previously exposed theme bugs.

The fixtures repo is pinned in CI to a specific commit (`FIXTURES_SHA` in
`.github/workflows/ci.yml` and `.github/workflows/update-snapshots.yml`), so
the input doesn't move between theme PRs. To bump it, edit both workflow
files and `/update-snapshots` on the bump PR.

## Test Coverage

### Per-page (loop)
- Full-page screenshot
- Header region (`.qe-page__header`)
- Sidebar region (`.qe-sidebar`)

### Theme features
- Dark mode toggle
- Code block styling
- F-string interpolation styling (`.si` token regression)
- Math equation rendering (MathJax)
- Toolbar visibility

### Typography
- Bold / italic styling (light + dark)

### Definition lists
- `<dl>` rendering, glossary block

### Viewports
- Desktop (1280×720)
- Mobile (Pixel 5)

## Running Tests

### Using tox (Recommended)

```bash
# Run visual tests — clones fixtures repo to ./fixtures/ if not present
tox -e visual

# Update baselines after intentional changes
tox -e visual-update

# Pin to a specific fixtures commit for local testing
FIXTURES_REF=<sha> tox -e visual
```

### Manual setup

If you prefer to run things by hand:

1. Clone the fixtures repo as a sibling directory `fixtures/`:
   ```bash
   git clone https://github.com/QuantEcon/quantecon-book-theme-fixtures fixtures
   ```

2. Install fixtures build dependencies + this checkout of the theme:
   ```bash
   pip install -r fixtures/requirements.txt
   pip install -e .
   ```

3. Build the fixtures site:
   ```bash
   (cd fixtures && jb build .)
   ```

4. Install Playwright:
   ```bash
   npm install
   npx playwright install chromium
   ```

5. Run tests:
   ```bash
   npm run test:visual
   ```

6. Update baselines:
   ```bash
   npm run test:visual:update
   ```

## CI Integration

Visual tests run automatically on every push and pull request via
`.github/workflows/ci.yml`:

1. Checks out the fixtures repo at the pinned SHA.
2. Builds the fixtures site (`jb build . --warningiserror`).
3. Runs Playwright against the build.
4. Uploads test results as artifacts.
5. Posts a summary comment on PRs.
6. Deploys the fixtures site to Netlify as a preview — reviewers can click
   through the deploy link to eyeball every fixture page with this PR's
   theme applied.

### Platform-Specific Snapshots

Font rendering differs between macOS and Linux (ubuntu), so snapshots are
stored separately:

- `tests/visual/__snapshots__/` — **Ubuntu/CI baselines** (committed to repo)
- `tests/visual/macos/` — **macOS local baselines** (gitignored)

### First-Time CI Setup

To create the initial ubuntu baselines for CI:

1. Push your branch to GitHub.
2. CI will fail (no baselines exist yet).
3. Comment `/update-new-snapshots` on the PR to trigger automatic snapshot
   generation.
4. The workflow commits the new baselines to your PR branch.

### Reviewing Failures

**On PRs:** check the "🎭 Visual Regression Test Results" comment for a
summary.

**For detailed analysis:**
1. Download the `playwright-report` artifact from the failed workflow.
2. Open `index.html` to see visual diffs.
3. If changes are intentional, comment `/update-snapshots` on the PR to
   regenerate all baselines.
4. For local testing: `tox -e visual-update`.

## Baseline Snapshots

### Updating baselines after intentional changes

When the theme styling intentionally changes:

1. **Regenerate all snapshots (recommended for styling changes):**
   - Comment `/update-snapshots` on the PR.
   - The workflow regenerates ALL baselines using `--update-snapshots`.
   - Uploads a `snapshot-update-diff` artifact with before/after images for
     review.
   - Commits the new baselines to your PR branch.

2. **Add missing snapshots only (for new tests):**
   - Comment `/update-new-snapshots` on the PR.
   - Generates only MISSING snapshots — existing baselines are not
     overwritten.

3. **For local baselines:**
   ```bash
   tox -e visual-update
   ```

## Adding new fixture pages

To exercise a new theme surface (or capture a real-world lecture that
breaks):

1. Open a PR on
   [`quantecon-book-theme-fixtures`](https://github.com/QuantEcon/quantecon-book-theme-fixtures)
   adding the page. See its `real-world/README.md` for capture conventions.
2. Once merged, open a follow-up PR on this repo that bumps `FIXTURES_SHA`
   in both workflows and adds a corresponding test (if needed) in
   `theme.spec.ts`.
3. Comment `/update-new-snapshots` on that PR to seed baselines for the new
   page.
