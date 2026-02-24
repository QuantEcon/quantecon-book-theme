# User Guide

This guide covers everything you need to install, configure, and use the
**QuantEcon Book Theme** for your Sphinx or Jupyter Book project.

## Requirements

- **Python 3.12** or newer
- **Sphinx 7.0** or newer

## Installation

Install the theme with `pip`:

```bash
pip install quantecon-book-theme
```

## Quick Start

Activate the theme in your Sphinx configuration (`conf.py`):

```python
html_theme = "quantecon_book_theme"
```

For Jupyter Book projects, add to your `_config.yml`:

```yaml
sphinx:
  config:
    html_theme: quantecon_book_theme
```

A minimal configuration might look like:

```python
html_theme = "quantecon_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/{your-org}/{your-repo}",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
}
```

## What's in this guide

```{toctree}
:maxdepth: 2
:caption: User Guide

configuration
layout
notebooks
launch
dark-mode
code-highlighting
git-metadata
text-color-schemes
rtl-support
features/stderr-warnings
```
