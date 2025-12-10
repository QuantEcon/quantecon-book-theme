# Architecture of the repository

This is a short overview of the general architecture and structure of the repository, to help you orient yourself.

This theme uses [sphinx-theme-builder](https://sphinx-theme-builder.readthedocs.io/en/latest/) as its build backend, and follows the [filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/filesystem-layout/) recommended by it.
See below for some more specific sections.

```{contents}
```

## `src/quantecon_book_theme/` - Theme source files

This folder contains all of the source files for this theme, and most changes to the theme are made somewhere inside this folder.

`__init__.py`
: The theme's Python module, which runs several configuration and set-up steps.
  This module sets up the `quantecon-book-theme` extension, inheriting features from `sphinx-book-theme`.
  It also inserts several variables into the Jinja template context that are then used in our HTML templates.
  Key functions include:
  - `setup_pygments_css()` - Generates Pygments CSS when custom code styling is disabled
  - `add_pygments_style_class()` - Adds CSS class to enable/disable custom code highlighting
  - `hash_assets_for_files()` - Adds cache-busting hashes to static assets

### `/theme/quantecon_book_theme/` - HTML templates

This is the actual theme source that is packaged and distributed via PyPI.
It contains HTML templates that make up the theme structure.

These follow the [`sphinx-basic-ng` template structure](https://sphinx-basic-ng.readthedocs.io/en/latest).

- `layout.html` inherits from the [pydata sphinx theme](https://pydata-sphinx-theme.readthedocs.io/) and modifies several sections.
  It includes:
  - **Preconnect hints** for CDN performance optimization
  - **SRI hashes** on external scripts for security
  - External library loading (Popper.js, Tippy.js, Feather Icons)
- `theme.conf` contains the Sphinx configuration file for this theme.
- `macros/` contains HTML templates that define Jinja macros.
- `sections/` contains HTML templates for major sections of the page.
- `components/` contains HTML templates for smaller, self-contained parts of the page.

### `/assets/scripts/` - JavaScript modules

Contains JavaScript files organized into feature-specific modules.
They are automatically compiled by webpack and bundled into a single file.

**Module Structure:**

| Module | Purpose | Exports |
|--------|---------|---------|
| `index.js` | Main entry point | Imports and initializes all modules |
| `theme-settings.js` | Dark mode, contrast, font size | `initThemeSettings`, `initFontSize` |
| `sidebar.js` | Sidebar toggle and navigation | `initSidebar` |
| `search.js` | Search functionality | `initSearch` |
| `navigation.js` | Fullscreen mode, back-to-top | `initFullscreen`, `initBackToTop` |
| `code-blocks.js` | Collapsible code, table containers | `initCollapsibleCode`, `initTableContainers` |
| `popups.js` | Tooltips and launcher settings | `initPopups`, `initLauncherSettings` |
| `page-header.js` | Page header and changelog | `initPageHeader`, `initChangelog` |
| `stderr-warnings.js` | Collapsible stderr output | `initStderrWarnings` |

Each module uses ES6 `export` syntax and is imported by `index.js`.

### `/assets/styles/` - SCSS modules

Contains SCSS files organized into logical modules.
They are compiled by webpack into a single CSS file.

**Module Structure:**

The main entry point is `index.scss`, which uses `@forward` directives to include all modules:

```scss
// Third-party and vendor styles
@forward "normalize";
@forward "html5boilerplate";
@forward "quantecon-defaults";
@forward "syntax";
@forward "code";
@forward "tippy-themes";
@forward "margin";
@forward "rtl";
@forward "dropdown";

// Component modules
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

**Key modules:**

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

Modules that need color variables use the modern `@use "colors"` syntax.

## `docs/` - Site documentation

The documentation for the theme, written as a Sphinx documentation site.

Here is a brief overview:

- `docs/*.md`: Contains several topic sections for the documentation (e.g., `configure.md` covers theme configuration options)
- `docs/contributing/`: Developer documentation including setup, architecture, and testing guides
- `docs/reference/`: Reference sections to demonstrate the look and feel of the theme
- `docs/features/`: Documentation for specific theme features like stderr warnings


## `webpack.config.js` and `package.json` - Asset compilation

`webpack.config.js` contains the compilation code to convert source files like SCSS and JS in `src/quantecon_book_theme/assets/*` into the production assets in `src/quantecon_book_theme/theme/quantecon_book_theme/static/`.

To compile assets during development:

```console
$ npm run build
```

**Key dependencies** (defined in `package.json`):
- `webpack` and `webpack-cli` - Module bundler
- `sass` and `sass-loader` - SCSS compilation
- `css-loader` and `css-minimizer-webpack-plugin` - CSS processing

## `tests/` - Testing infrastructure

Testing infrastructure that uses `pytest` along with `beautifulsoup` to validate
that the generated HTML is what we expect it to be.

Key test files:
- `conftest.py` - Shared pytest fixtures for directory paths
- `test_build.py` - HTML build and regression tests
- `test_module_structure.py` - Tests for modular SCSS/JS organization
- `test_rtl_functionality.py` - Right-to-left language support tests

See the [Testing Guide](testing.md) for detailed information about fixtures and tests.

## `.github/workflows/` - Continuous Integration and Deployment

Contains Continuous-integration (CI) workflows, run on commits/PRs to the GitHub repository.

The CI pipeline includes:
- **Pre-commit checks**: Code formatting (black) and linting (flake8)
- **Test suite**: Runs `tox` against Python 3.12 and 3.13
- **Documentation build**: Validates the docs build successfully

## External Dependencies

The theme loads several libraries from CDN for functionality:

| Library | Version | Purpose |
|---------|---------|---------|
| [Popper.js](https://popper.js.org/) | 2.9.2 | Tooltip positioning engine |
| [Tippy.js](https://atomiks.github.io/tippyjs/) | 6.3.1 | Tooltip library |
| [Feather Icons](https://feathericons.com/) | latest | Icon set |

These are loaded with **SRI (Subresource Integrity) hashes** for security.

## Parent theme - `pydata-sphinx-theme`

This theme inherits a lot of functionality and design rules from its parent theme, the [PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme).
This is a theme designed for the PyData community, with a similar look and feel to the book theme.
Over time, we try to upstream any improvements made here into the parent theme, as long as the look and feel is the same between the two.

If you come across something in the codebase and you're not sure where it comes from (an example is the `generate_toctree_html` function), you should [check the PyData Theme source files](https://github.com/pydata/pydata-sphinx-theme/tree/master/src/pydata_sphinx_theme) to see if it is defined there.
