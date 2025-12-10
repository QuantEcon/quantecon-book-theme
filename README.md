# quantecon-book-theme
A Jupyter Book Theme for QuantEcon Book Style Projects

## Features

- **Clean, professional design** optimized for technical and academic documentation
- **Git-based metadata** - Automatic display of last modified dates and interactive changelog with commit history
- **Collapsible stderr warnings** - Automatically wraps verbose warnings in notebook cells with an expandable interface
- **Jupyter Notebook support** with visual classes for cell inputs, outputs, and interactive functionality
- **Configurable code syntax highlighting** - Choose between custom QuantEcon styles or Pygments built-in themes
- **Launch buttons** for online interactivity via BinderHub
- **Flexible content layout** inspired by beautiful online books
- **Bootstrap 4** for visual elements and functionality
- **Built on PyData Sphinx Theme** inheriting robust features and design patterns

## Usage

To use this theme in [Jupyter Book](https://github.com/executablebooks/jupyter-book):

1. Install the theme

  ```bash
  pip install quantecon-book-theme
  ```

2. Add the theme to your `_config.yml` file:

  ```yaml
  sphinx:
      config:
          html_theme: quantecon_book_theme
  ```

### Configuration Options

The theme supports various configuration options in your `conf.py` or `_config.yml`:

```python
html_theme_options = {
    "repository_url": "https://github.com/{your-org}/{your-repo}",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,

    # Git metadata (new in v0.12.0)
    "last_modified_date_format": "%b %d, %Y",  # Date format for last modified
    "changelog_max_entries": 10,  # Number of commits to show in changelog

    # Code highlighting (new in v0.10.0)
    "qetheme_code_style": True,  # False to use Pygments built-in styles
}

# When using Pygments styles
pygments_style = 'friendly'  # or 'monokai', 'github-dark', etc.
```

See the [full documentation](https://quantecon-book-theme.readthedocs.io/) for all configuration options.

## Development

### Testing

This project uses `tox` for running tests across multiple Python versions:

```bash
# Run full test suite
tox

# Run pre-commit checks
pre-commit run --all-files
```

**Important**: Always use `tox` instead of running `pytest` directly to ensure proper environment isolation and multi-version testing.

## Updating Fixtures for Tests

### Updating test regression files on layout changes

It is advisable to update the test files for file regression checks when releavant layout files change.

For example, at present we have a sidebar file-regression check to validate html across tests.
The file which it compares against is `tests/test_build/test_build_book.html`.

If updating the sidebar html, then one of the easier steps to update this test file is:

1. Delete the file `tests/test_build/test_build_book.html`.
2. Run `pytest` in your command line, which will then generate a new file. Check if the file is at par with your expectations, contains elements which you added/modified.

Now future pytests will test against this file, and the subsequent tests should pass.

## Contributing Guide

The docs for the contributing guide of this repository: https://github.com/QuantEcon/quantecon-book-theme/blob/master/docs/contributing/index.md
