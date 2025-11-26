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

Visual tests run automatically on every push via GitHub Actions:
1. Builds lecture site with current theme
2. Runs Playwright tests against the build
3. Uploads test results as artifacts
4. Reports pass/fail status

### Reviewing Failures
1. Download the `playwright-report` artifact from the failed workflow
2. Open `index.html` to see visual diffs
3. If changes are intentional, update baselines with `npm run test:visual:update`

## Baseline Snapshots

Baseline images are stored in different directories depending on the platform:

- **CI (ubuntu)**: `tests/visual/__snapshots__/` - committed to repository
- **Local (macOS via tox)**: `tests/visual/macos/` - gitignored

This separation allows local testing on macOS without interfering with CI baselines, since screenshot rendering differs between operating systems.

When the theme styling intentionally changes:
1. Update CI baselines by running tests in CI with `--update-snapshots`
2. Download the updated snapshots from CI artifacts
3. Commit the new baselines to `tests/visual/__snapshots__/`
