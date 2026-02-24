# Testing Guide

The testing infrastructure uses `pytest` and `beautifulsoup4` to validate
generated HTML. Always run tests via `tox` for proper environment isolation.

```{contents}
:local:
:depth: 2
```

## Running Tests

```console
# Full test suite (Python 3.12 + 3.13, Sphinx 7)
$ tox

# Specific test file
$ tox -- tests/test_module_structure.py -v

# Tests matching a pattern
$ tox -- -k "test_scss"
```

## Test Structure

```
tests/
├── conftest.py              # Shared pytest fixtures
├── test_build.py            # HTML build and regression tests
├── test_module_structure.py # Module organization tests
├── test_custom_colors.py    # Color scheme tests
├── test_rtl_functionality.py # RTL language support tests
└── sites/                   # Test site configurations
    ├── base/                # Basic test site
    └── rtl_test/            # RTL-specific test site
```

## Fixtures

Defined in `conftest.py`:

| Fixture | Path | Purpose |
|---------|------|---------|
| `project_root` | Repository root | Access to top-level files |
| `src_dir` | `src/quantecon_book_theme/` | Python source directory |
| `assets_dir` | `src/.../assets/` | Source assets (SCSS/JS) |
| `theme_dir` | `src/.../theme/quantecon_book_theme/` | Sphinx theme templates |
| `styles_dir` | `src/.../assets/styles/` | SCSS source files |
| `scripts_dir` | `src/.../assets/scripts/` | JavaScript source files |

### Example

```python
def test_my_feature(styles_dir):
    """Example test using the styles_dir fixture."""
    index_scss = styles_dir / "index.scss"
    assert index_scss.exists()
    content = index_scss.read_text()
    assert "@forward" in content
```

## Module Structure Tests

`test_module_structure.py` validates the modular organization of SCSS and JS.

### SCSS tests

- **`test_all_scss_modules_exist`** — verifies all 23 expected SCSS files exist
- **`test_index_scss_imports_modules`** — verifies `@forward` directives for all 11 component modules
- **`test_scss_modules_use_sass_module_syntax`** — verifies modules use `@use` not `@import`

### JavaScript tests

- **`test_all_js_modules_exist`** — verifies all 9 expected JS files exist
- **`test_index_js_imports_all_modules`** — verifies all 8 feature modules are imported
- **`test_js_modules_export_functions`** — verifies each module exports expected functions
- **`test_no_console_polyfill`** — verifies obsolete IE8/9 polyfill is removed

### Layout template tests

- **`test_preconnect_hints_present`** — verifies `<link rel="preconnect">` hints for CDN domains
- **`test_sri_hashes_present`** — verifies SRI integrity attributes on CDN scripts
- **`test_external_scripts_loaded`** — verifies Popper.js, Tippy.js, and Feather Icons are loaded

## Build Tests

`test_build.py` builds actual Sphinx sites and validates the generated HTML.

### Regression testing

We use `pytest-regressions` to detect changes in HTML output:

```python
def test_build_book(file_regression):
    html = build_and_get_html()
    file_regression.check(html, extension=".html")
```

To update regression files after intentional changes:

```console
$ tox -- --force-regen
```

## Writing New Tests

### Guidelines

1. **Use fixtures** — avoid hardcoding paths
2. **Test one thing** — each test verifies a single behavior
3. **Descriptive names** — `test_feature_behavior_expected_result`
4. **Include docstrings** — explain what and why

### Example

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

Tests run on GitHub Actions for every push and pull request:

1. Pre-commit checks (black, flake8)
2. Full test suite with `tox`
3. Documentation build
4. Visual regression tests (see [Visual Testing](visual-testing.md))
