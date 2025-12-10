# Visual Regression Tests

This directory contains Playwright-based visual regression tests for the quantecon-book-theme.

## Overview

These tests capture screenshots of key pages from a real lecture site build and compare them against baseline snapshots to detect unintended styling changes.

## Test Coverage

### Page Types
- **Homepage** - Main landing page layout
- **Lecture with code** - Code block styling, syntax highlighting
- **Lecture with math** - MathJax rendering
- **Intro pages** - Standard lecture content

### Theme Features
- Dark mode toggle
- Code block styling
- Math equation rendering
- Toolbar visibility
- Header and sidebar regions

### Viewports
- Desktop (1280x720)
- Mobile (Pixel 5)

## Running Tests

### Using tox (Recommended)

```bash
# Run visual tests
tox -e visual

# Update baselines after intentional changes
tox -e visual-update
```

### Manual Setup

If you prefer to run tests manually:

1. Build the lecture site first:
   ```bash
   git clone --branch quantecon-book-theme https://github.com/QuantEcon/lecture-python-programming.myst
   cd lecture-python-programming.myst
   pip install -r requirements.txt
   jb build lectures --path-output ./
   cd ..
   ```

2. Install Playwright:
   ```bash
   npm install
   npx playwright install chromium
   ```

3. Run tests:
   ```bash
   npm run test:visual
   ```

4. Update baselines:
   ```bash
   npm run test:visual:update
   ```

## CI Integration

Visual tests run automatically on every push and pull request via GitHub Actions:
1. Builds lecture site with current theme
2. Runs Playwright tests against the build
3. Uploads test results as artifacts
4. Posts a summary comment on PRs
5. Reports pass/fail status

### Platform-Specific Snapshots

Due to font rendering differences between macOS and Linux (ubuntu), snapshots are stored separately:

- `tests/visual/__snapshots__/` - **Ubuntu/CI baselines** (committed to repo)
- `tests/visual/macos/` - **macOS local baselines** (gitignored)

### First-Time CI Setup

To create the initial ubuntu baselines for CI:

1. Push your branch to GitHub
2. CI will fail (no baselines exist yet)
3. Comment `/update-new-snapshots` on the PR to trigger automatic snapshot generation
4. The workflow will commit the new baselines to your PR branch

**Note:** The `/update-new-snapshots` command only works after the workflow file exists on the `main` branch. For PRs that add this workflow, you'll need to use the manual method below.

#### Manual Method (Alternative)

If the `/update-new-snapshots` workflow isn't available yet:

1. Push your branch to GitHub
2. CI will fail (no baselines exist yet)
3. Download the `visual-test-diff` artifact
4. Extract and copy snapshots to `tests/visual/__snapshots__/`
5. Commit and push the snapshots

```bash
# After CI runs and fails, download and extract artifact, then:
mkdir -p tests/visual/__snapshots__
cp -r /path/to/extracted/artifact/* tests/visual/__snapshots__/
git add tests/visual/__snapshots__
git commit -m "Add ubuntu visual regression baselines"
git push
```

### Reviewing Failures

**On PRs:** Check the "🎭 Visual Regression Test Results" comment for a summary.

**For detailed analysis:**
1. Download the `playwright-report` artifact from the failed workflow
2. Open `index.html` to see visual diffs
3. If changes are intentional, update baselines:
   - For CI: Download new snapshots from `visual-test-diff` artifact and commit
   - For local: Run `tox -e visual-update`

## Baseline Snapshots

Baseline images are stored in different directories depending on the platform:

- **CI (ubuntu)**: `tests/visual/__snapshots__/` - committed to repository
- **Local (macOS via tox)**: `tests/visual/macos/` - gitignored

This separation allows local testing on macOS without interfering with CI baselines, since screenshot rendering differs between operating systems.

### Updating Baselines After Intentional Changes

When the theme styling intentionally changes:

1. **For new tests (CI baselines):**
   - Comment `/update-new-snapshots` on the PR
   - The workflow will generate and commit only the missing snapshots
   - This is safe - it won't overwrite existing baselines

2. **For existing tests that need updating:**
   - Push changes and let CI run
   - Download `visual-test-diff` artifact with new screenshots
   - Extract and copy to `tests/visual/__snapshots__/`
   - Commit and push

3. **For local baselines:**
   ```bash
   tox -e visual-update
   ```
