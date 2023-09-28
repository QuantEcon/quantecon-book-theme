# Architecture of the repository

This is a short overview of the general architecture and structure of the repository, to help you orient yourself.

This theme uses [sphinx-theme-builder](https://sphinx-theme-builder.readthedocs.io/en/latest/) as its build backend, and follows the [filesystem layout](https://sphinx-theme-builder.readthedocs.io/en/latest/filesystem-layout/) recommended by it.
See below for some more specific sections

```{contents}
```

## `src/sphinx_book_theme/` - Theme source files

This folder contains all of the source files for this theme, and most changes to the theme are made somewhere inside this folder.

`__init__.py`
: The theme's Python module, which runs several configuration and set-up steps.
  This module does things like setup `sphinx-book-theme` extension. A lot of features of which is inherited here.
  It also inserts several variables into the Jinja template context that are then used in our HTML templates.

### `/theme/sphinx_book_theme/` - HTML templates

This is the actual theme source that is packaged and distributed via PyPI.
It contains HTML templates that make up the theme structure.

These follow the [`sphinx-basic-ng` template structure](https://sphinx-basic-ng.readthedocs.io/en/latest).

- `layout.html` inherits from the [pydata sphinx theme](https://pydata-sphinx-theme.readthedocs.io/) and modifies several sections.
- `theme.conf` contains the Sphinx configuration file for this theme.
- `macros/` contains HTML templates that define Jinja macros
- `sections/` contains HTML templates for major sections of the page.
- `components/` contains HTML templates for smaller, self-contained parts of the page.

### `/assets/scripts` - JavaScript assets

Contains JavaScript files for this theme. They are automatically compiled and inserted into the theme when new releases are made (or, via the command `stb compile`). They are **not checked in to `git` history**.

### `/assets/styles` - SCSS assets

Contains SCSS files for this theme.
These are compiled and bundled with the theme at build time.

## `docs/` - Site documentation

The documentation for the theme, written as a Sphinx documentation site.

Here is a brief overview:

- `docs/*.md`: Contains several topic sections for the documentation (e.g. `content-blocks.md` covers special content blocks for this theme)
- `docs/reference/`: Reference sections of the documentation, to demonstrate the look and feel of the theme.
  There are also other sections for theme-specific elements.


## `webpack.config.js` and `package.json` - Webpack and dependencies

`webpack.config.js` contains the compilation code to convert source files like SCSS and JS in `src/quantecon_book_theme/assets/*` into the production assets in `src/quantecon_book_theme/theme/quantecon_book_theme/static/` .
This compilation is called by default, during development commands (see below).

## `tests/` - Testing infrastructure

Testing infrastructure that uses `pytest` along with `beautifulsoup` to validate
that the generated HTML is what we expect it to be.
Much of these tests also use `pytest-regressions`, to check whether newly-generated HTML differs from previously-generated HTML.

## `.github/workflows/` - Continuous Integration and Deployment

Contains Continuous-integration (CI) workflows, run on commits/PRs to the GitHub repository.

## Parent theme - `pydata-sphinx-theme`

This theme inherits a lot of functionality and design rules from its parent theme, the [PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme).
This is a theme designed for the PyData community, with a similar look and feel to the book theme.
Over time, we try to upstream any improvements made here into the parent theme, as long as the look and feel is the same between the two.

If you come across something in the codebase and you're not sure where it comes from (an example is the `generate_toctree_html` function), you should [check the PyData Theme source files](https://github.com/pydata/pydata-sphinx-theme/tree/master/src/pydata_sphinx_theme) to see if it is defined there.
