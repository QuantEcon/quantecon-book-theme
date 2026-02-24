# Development Setup

Set up a local development environment for `quantecon-book-theme`.

## Prerequisites

- **Python 3.12 or newer**
- **Node.js 18.18.0 or newer** — for compiling SCSS/JS assets with webpack
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
