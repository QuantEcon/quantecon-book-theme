# Development Setup

Set up a local development environment for `quantecon-book-theme`.

## Prerequisites

- **Python 3.12 or newer**
- **Node.js 24 or newer** — for compiling SCSS/JS assets with webpack
- **Git**

## Initial Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/QuantEcon/quantecon-book-theme.git
   cd quantecon-book-theme
   ```

2. **Install Python tools** (`tox` and `pre-commit`):

   ```console
   $ pip install tox pre-commit
   ```

3. **Install Node.js dependencies**:

   ```console
   $ npm install
   ```

4. **Install pre-commit hooks**:

   ```console
   $ pre-commit install
   ```

   :::{margin}
   Run all `pre-commit` jobs manually:

   ```console
   $ pre-commit run --all-files
   ```
   :::

## Build the Documentation

```console
$ tox -e docs-update
```

This builds the docs and puts the output in `docs/_build/html`.

## Auto-rebuild During Development

```console
$ tox -e docs-live
```

This starts a live-reload development server that watches for changes and
automatically rebuilds. It will open in your default browser.

## Run Tests

```console
$ tox
```

This runs `pytest` against Python 3.12 and 3.13. Pass arguments to pytest:

```console
$ tox -- -k test_match
```

:::{tip}
See [Testing](testing.md) for detailed information about test fixtures and
writing new tests.
:::

### Everything stays repo-local

`tox` keeps the toolchain isolated to this repository — it builds its
virtualenvs under `.tox/` and installs the package plus its `[test]` extras
there, never into your base/global Python. The theme's SCSS/JS assets are
compiled by `sphinx-theme-builder`, which provisions its own Node.js into an
in-repo `.nodeenv/` (with `node_modules/` for `npm`). All three directories are
git-ignored, so nothing leaks system-wide and the environment can always be
rebuilt from scratch by deleting them.

## Code Style

### Python

- **Formatter**: Black (88 char line length)
- **Linter**: Flake8
- **Docstrings**: Google style

### JavaScript

- ES6+ (const/let, arrow functions, template literals)
- JSDoc comments
- 100 char line length

### SCSS

- Modern `@use` / `@forward` syntax (not `@import`)
- BEM-inspired class naming
- Maximum 3–4 levels of nesting

## Troubleshooting

### `nodeenv-version-mismatch` when running `tox` or installing

If `tox` (or a `pip install -e .`) fails with something like:

```text
× The `nodeenv` for this project is unhealthy.
╰─> There is a mismatch between what is present in the environment (v18.18.0)
    and the expected version of NodeJS (v20.18.0).
```

your in-repo `.nodeenv/` is stale — it was provisioned against an older pinned
Node.js version and never refreshed. `sphinx-theme-builder` rebuilds it
automatically once it's removed:

```console
$ rm -rf .nodeenv
$ tox
```

The pinned version lives under `[tool.sphinx-theme-builder]` (`node-version`)
in `pyproject.toml`; deleting `.nodeenv/` is always safe since it is git-ignored
and regenerated on the next build.
