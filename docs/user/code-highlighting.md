# Code Syntax Highlighting

By default, the theme uses custom QuantEcon syntax highlighting colors for code
blocks. You can switch to any Pygments built-in style instead.

```{contents}
:local:
:depth: 2
```

## Using Pygments Built-in Styles

To disable the custom code styling and use a Pygments theme:

```python
# conf.py

# Choose a Pygments style
pygments_style = 'friendly'  # or 'monokai', 'github-dark', 'default', etc.

html_theme_options = {
    ...
    "qetheme_code_style": False,
    ...
}
```

Available Pygments styles include: `default`, `friendly`, `monokai`,
`github-dark`, `github-light`, `tango`, `vim`, and many others. See the
[Pygments documentation](https://pygments.org/styles/) for a full list.

## Default Behavior

When `qetheme_code_style` is `True` (the default), the custom QuantEcon code
highlighting is used and the `pygments_style` setting is ignored. When set to
`False`, the theme respects your `pygments_style` configuration.

## Dark Mode Integration

When using the default QuantEcon code style, dark mode automatically applies a
VS Code Dark+ inspired syntax highlighting palette. See
[Dark Mode — Syntax Highlighting](dark-mode.md) for the
full color table.

If you use a custom Pygments style (`qetheme_code_style: False`), the dark mode
syntax colors are not applied and your Pygments configuration takes precedence.

## Inline Code Box Styling

By default, the theme removes the background box and border that
`pydata-sphinx-theme` applies to inline code literals (e.g., `` `x` `` or
`` `x = 42` ``). This keeps inline code visually consistent with the original
QuantEcon look.

To re-enable the box styling (background color, border, and padding) on inline
code elements:

```python
html_theme_options = {
    ...
    "inline_literal_box": True,
    ...
}
```

For Jupyter Book projects:

```yaml
sphinx:
  config:
    html_theme_options:
      inline_literal_box: true
```

When `inline_literal_box` is `False` (the default), inline code appears without
any visual container. When set to `True`, inline code elements display with a
subtle background and border provided by the parent theme.
