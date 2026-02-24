# Repository Architecture

Overview of the project structure and how the major components fit together.

```{contents}
:local:
:depth: 2
```

## Build System

The project uses two build systems:
- **Node.js** (webpack) — compiles SCSS and JS source assets into production files
- **Python** (sphinx-theme-builder) — packages and distributes the Sphinx theme

Key build config files:
- `package.json` + `webpack.config.js` — Node.js asset compilation
- `pyproject.toml` — Python package configuration
- `tox.ini` — Environment management and task automation
- `.pre-commit-config.yaml` — Code quality hooks

## `src/quantecon_book_theme/` — Theme Source

This is where most changes are made.

### `__init__.py` — Python Module

The main theme module. Sets up the `quantecon-book-theme` extension, inheriting
from `sphinx-book-theme`. Key functions:

- `setup_pygments_css()` — generates Pygments CSS when custom code styling is disabled
- `add_pygments_style_class()` — adds CSS class to enable/disable custom highlighting
- `hash_assets_for_files()` — adds cache-busting hashes to static assets

### `/theme/quantecon_book_theme/` — HTML Templates

The actual Sphinx theme distributed via PyPI. Follows the
[`sphinx-basic-ng` template structure](https://sphinx-basic-ng.readthedocs.io/en/latest).

- `layout.html` — inherits from [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/). Includes preconnect hints, SRI hashes, and external library loading
- `theme.conf` — Sphinx theme configuration file
- `macros/` — Jinja macros
- `sections/` — HTML templates for major page sections
- `components/` — HTML templates for self-contained page components

### `/assets/scripts/` — JavaScript Modules

ES6 modules organized by feature, compiled by webpack into a single bundle:

| Module | Purpose | Exports |
|--------|---------|---------|
| `index.js` | Entry point | Imports all modules |
| `theme-settings.js` | Dark mode, contrast, font size | `initThemeSettings`, `initFontSize` |
| `sidebar.js` | Sidebar toggle and navigation | `initSidebar` |
| `search.js` | Search functionality | `initSearch` |
| `navigation.js` | Fullscreen, back-to-top | `initFullscreen`, `initBackToTop` |
| `code-blocks.js` | Collapsible code, table containers | `initCollapsibleCode`, `initTableContainers` |
| `popups.js` | Tooltips and launcher settings | `initPopups`, `initLauncherSettings` |
| `page-header.js` | Page header and changelog | `initPageHeader`, `initChangelog` |
| `stderr-warnings.js` | Collapsible stderr output | `initStderrWarnings` |

### `/assets/styles/` — SCSS Modules

Compiled by webpack into a single CSS file. Entry point is `index.scss` using
`@forward` directives:

| Module | Purpose |
|--------|---------|
| `_base.scss` | Typography, HTML elements, resets |
| `_dark-theme.scss` | Dark mode color overrides |
| `_toolbar.scss` | Top navigation bar |
| `_sidebar.scss` | Left sidebar navigation |
| `_page.scss` | Main content area layout |
| `_content.scss` | Content typography and spacing |
| `_admonitions.scss` | Note/warning/tip boxes |
| `_footnotes.scss` | Footnote styling |
| `_stderr.scss` | Stderr warning collapsible styling |
| `_modals.scss` | Modal dialog styles |
| `_autodoc.scss` | API documentation styles |
| `_colors.scss` | Color variable definitions |

Modules that need color variables use `@use "colors"` syntax.

## `docs/` — Documentation

The theme's own documentation, structured into User Guide and Developer Guide:

- `docs/user/` — Configuration and usage documentation for theme users
- `docs/developer/` — Contributing, architecture, and testing guides
- `docs/reference/` — Visual demos of theme elements
- `docs/api/` — Python API autodoc

## `tests/` — Testing

Uses `pytest` with `beautifulsoup` to validate generated HTML:

- `conftest.py` — shared fixtures for directory paths
- `test_build.py` — HTML build and regression tests
- `test_module_structure.py` — modular SCSS/JS organization tests
- `test_rtl_functionality.py` — RTL language support tests
- `test_custom_colors.py` — color scheme tests

## External Dependencies (CDN)

| Library | Version | Purpose |
|---------|---------|---------|
| [Popper.js](https://popper.js.org/) | 2.9.2 | Tooltip positioning engine |
| [Tippy.js](https://atomiks.github.io/tippyjs/) | 6.3.1 | Tooltip library |
| [Feather Icons](https://feathericons.com/) | latest | Icon set |

Loaded with **SRI (Subresource Integrity) hashes** for security.

## Parent Theme

This theme inherits from the
[PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme). If you
encounter unfamiliar code, check the
[PyData Theme source files](https://github.com/pydata/pydata-sphinx-theme/tree/master/src/pydata_sphinx_theme).
