# The QuantEcon Book Theme

**An interactive book theme for Sphinx.**

A lightweight Sphinx theme designed to mimic the look-and-feel of an
interactive book. Key features:

* **[Dark mode](user/dark-mode.md)** — modern dark theme with full syntax highlighting, accessible colors, no flash on load
* **[Git-based metadata](user/git-metadata.md)** — automatic last-modified timestamps and interactive changelog per page
* **[Collapsible stderr warnings](user/features/stderr-warnings.md)** — wrap verbose notebook warnings in an expandable interface
* **[Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)** for visual elements
* **[Flexible content layout](user/layout.md)** inspired by [Edward Tufte CSS](https://edwardtufte.github.io/tufte-css/)
* **[Jupyter Notebook support](user/notebooks.md)** with visual classes for cell inputs, outputs, and interactivity
* **[Configurable code highlighting](user/code-highlighting.md)** — QuantEcon styles or Pygments built-in themes
* **[Launch buttons](user/launch.md)** — connect to BinderHub, JupyterHub, Colab, or Thebe for interactive content
* **[Text color schemes](user/text-color-schemes.md)** — Seoul256, Gruvbox, or custom colors for emphasis and bold
* **[RTL support](user/rtl-support.md)** — full right-to-left layout for Arabic, Hebrew, Persian, and more

## Quick Start

```bash
pip install quantecon-book-theme
```

```python
# conf.py
html_theme = "quantecon_book_theme"
```

## User Guide

Everything you need to install, configure, and use the theme.

```{toctree}
:maxdepth: 2
:caption: User Guide

user/index
```

## Developer Guide

Contributing, architecture, testing, and release processes.

```{toctree}
:maxdepth: 2
:caption: Developer Guide

developer/index
```

## Reference

```{toctree}
:caption: Reference
:maxdepth: 2

reference/index
api/index
```

## Acknowledgements

This theme is heavily inspired by (and dependent on)
[PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/) for its base
structure and configuration.
