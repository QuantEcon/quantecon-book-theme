# Testing Guide

This guide explains the testing infrastructure for `quantecon-book-theme`, including test fixtures, what each test validates, and how to run and extend the test suite.

## Running Tests

Always use `tox` to run tests, which ensures proper environment isolation:

```console
$ tox
```

This runs the full test suite against Python 3.12 and 3.13 with Sphinx 7.

To run a specific test file:

```console
$ tox -- tests/test_module_structure.py -v
```

To run tests matching a pattern:

```console
$ tox -- -k "test_scss"
```

## Test Structure

Tests are located in the `tests/` directory:

```
tests/
├── conftest.py              # Shared pytest fixtures
├── test_build.py            # HTML build and regression tests
├── test_module_structure.py # Module organization tests
├── test_rtl_functionality.py # RTL language support tests
└── sites/                   # Test site configurations
    ├── base/                # Basic test site
    └── rtl_test/            # RTL-specific test site
```

## Test Fixtures

Fixtures are defined in `tests/conftest.py` and provide consistent paths to key directories:

| Fixture | Path | Purpose |
|---------|------|---------|
| `project_root` | Repository root | Access to top-level files |
| `src_dir` | `src/quantecon_book_theme/` | Python source directory |
| `assets_dir` | `src/quantecon_book_theme/assets/` | Source assets (SCSS/JS) |
| `theme_dir` | `src/quantecon_book_theme/theme/quantecon_book_theme/` | Sphinx theme templates |
| `styles_dir` | `src/quantecon_book_theme/assets/styles/` | SCSS source files |
| `scripts_dir` | `src/quantecon_book_theme/assets/scripts/` | JavaScript source files |

### Example Usage

```python
def test_my_feature(styles_dir):
    """Example test using the styles_dir fixture."""
    index_scss = styles_dir / "index.scss"
    assert index_scss.exists()
    content = index_scss.read_text()
    assert "@forward" in content
```

## Module Structure Tests

The `test_module_structure.py` file validates the modular organization of SCSS and JavaScript files. These tests ensure maintainability and proper code structure.

### SCSS Module Tests

#### `test_all_scss_modules_exist`

**Purpose**: Verifies that all 23 expected SCSS module files exist in `assets/styles/`.

**What it checks**:
- Partial modules (prefixed with `_`): `_base.scss`, `_dark-theme.scss`, `_toolbar.scss`, etc.
- Main entry point: `index.scss`

**Why it matters**: Ensures no modules were accidentally deleted or renamed during refactoring.

---

#### `test_index_scss_imports_modules`

**Purpose**: Verifies that `index.scss` uses `@forward` directives to include all 11 component modules.

**What it checks**:
```scss
@forward "base";
@forward "dark-theme";
@forward "toolbar";
@forward "sidebar";
@forward "page";
@forward "content";
@forward "admonitions";
@forward "footnotes";
@forward "stderr";
@forward "modals";
@forward "autodoc";
```

**Why it matters**: The `@forward` directive is the modern Sass way to expose module contents. This ensures all styles are included in the final compiled CSS.

---

#### `test_scss_modules_use_sass_module_syntax`

**Purpose**: Verifies that SCSS modules use modern `@use` syntax instead of deprecated `@import`.

**What it checks**:
- Modules that reference color variables should have `@use "colors"`
- Not the deprecated `@import "colors"`

**Why it matters**: The `@use` rule is the modern Sass module system, providing better encapsulation and avoiding global namespace pollution.

### JavaScript Module Tests

#### `test_all_js_modules_exist`

**Purpose**: Verifies that all 9 expected JavaScript module files exist in `assets/scripts/`.

**What it checks**:
- Feature modules: `theme-settings.js`, `sidebar.js`, `search.js`, `navigation.js`, `code-blocks.js`, `popups.js`, `page-header.js`, `stderr-warnings.js`
- Main entry point: `index.js`

---

#### `test_index_js_imports_all_modules`

**Purpose**: Verifies that `index.js` imports all 8 feature modules.

**What it checks**:
```javascript
import { initThemeSettings, initFontSize } from "./theme-settings.js";
import { initSidebar } from "./sidebar.js";
// ... etc
```

**Why it matters**: Ensures all features are loaded when the theme initializes.

---

#### `test_js_modules_export_functions`

**Purpose**: Verifies that each JavaScript module exports its expected functions.

**What it checks**:

| Module | Expected Exports |
|--------|-----------------|
| `theme-settings.js` | `initThemeSettings`, `initFontSize` |
| `sidebar.js` | `initSidebar` |
| `search.js` | `initSearch` |
| `navigation.js` | `initFullscreen`, `initBackToTop` |
| `code-blocks.js` | `initCollapsibleCode`, `initTableContainers` |
| `popups.js` | `initPopups`, `initLauncherSettings` |
| `page-header.js` | `initPageHeader`, `initChangelog` |
| `stderr-warnings.js` | `initStderrWarnings` |

**Why it matters**: Ensures proper ES6 module encapsulation and that `index.js` can import all required functions.

---

#### `test_no_console_polyfill`

**Purpose**: Verifies that the obsolete console polyfill has been removed.

**What it checks**:
- `window.console = window.console || {}` is NOT present
- `var noop = function () {}` is NOT present

**Why it matters**: This polyfill was needed for IE8/9 but is unnecessary for modern browsers. Removing it reduces bundle size and maintenance burden.

### Layout Template Tests

#### `test_preconnect_hints_present`

**Purpose**: Verifies that `layout.html` includes `<link rel="preconnect">` hints for CDN domains.

**What it checks**:
```html
<link rel="preconnect" href="https://unpkg.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

**Why it matters**: Preconnect hints tell browsers to establish early connections to external domains, reducing latency when loading CDN resources.

---

#### `test_sri_hashes_present`

**Purpose**: Verifies that CDN scripts include Subresource Integrity (SRI) hashes.

**What it checks**:
- `integrity="sha384-..."` attribute present
- `crossorigin="anonymous"` attribute present

**Why it matters**: SRI is a security feature that ensures external scripts haven't been tampered with. If a CDN is compromised, the browser will refuse to execute scripts that don't match the expected hash.

---

#### `test_external_scripts_loaded`

**Purpose**: Verifies that the 3 external scripts are loaded from CDN.

**What it checks**:
- `@popperjs/core` - Positioning engine for tooltips
- `tippy.js` - Tooltip library
- `feather-icons` - Icon set

**Why it matters**: These libraries are loaded from CDN rather than bundled to reduce our bundle size. This test ensures they're properly referenced.

## Build Tests

The `test_build.py` file contains tests that build actual Sphinx sites and validate the generated HTML.

### Key Tests

- **`test_build_book`**: Builds a test site and validates the HTML structure
- **Regression tests**: Compare generated HTML against golden files to detect unintended changes

### Regression Testing

We use `pytest-regressions` to detect changes in HTML output:

```python
def test_build_book(file_regression):
    # Build site and get HTML
    html = build_and_get_html()
    # Compare against stored reference
    file_regression.check(html, extension=".html")
```

To update regression files after intentional changes:

```console
$ tox -- --force-regen
```

## Writing New Tests

### Guidelines

1. **Use fixtures**: Always use the provided fixtures rather than hardcoding paths
2. **Test one thing**: Each test should verify a single behavior
3. **Descriptive names**: Test names should describe what they verify
4. **Include docstrings**: Explain what the test checks and why

### Example Test

```python
class TestNewFeature:
    """Tests for the new feature."""

    def test_feature_file_exists(self, scripts_dir):
        """Verify the new feature module exists."""
        module_path = scripts_dir / "new-feature.js"
        assert module_path.exists(), "Missing new-feature.js module"

    def test_feature_exports_init_function(self, scripts_dir):
        """Verify the module exports its init function."""
        content = (scripts_dir / "new-feature.js").read_text()
        assert "export function initNewFeature" in content
```

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Every push to the repository
- Every pull request

The CI workflow runs:
1. Pre-commit checks (black, flake8, etc.)
2. Full test suite with `tox`
3. Documentation build

See `.github/workflows/` for the CI configuration.
