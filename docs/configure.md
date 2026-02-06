# Configuration

A few configuration options for this theme

```{note}
This documentation and the examples below are written with MyST Markdown, a form
of markdown that works with Sphinx. For more information about MyST markdown, and
to use MyST markdown with your Sphinx website,
see [the MyST-parser documentation](https://myst-parser.readthedocs.io/)
```

## Disabling QuantEcon Official Components

If you are a project using this theme please use

```python
html_theme_options = {
    ...
    "quantecon_project": False,
    ...
}
```

as this will remove the QuantEcon logo from the top toolbar.

This will also override some colors styles for a slightly different look
for the theme.

## Source repository buttons

There are a collection of buttons that you can use to link back to your source
repository. This lets users browse the repository, or take actions like suggest
an edit or open an issue. In each case, they require the following configuration
to exist:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    ...
}
```

### Add a link to your repository

To add a link to your repository, add the following configuration:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_repository_button": True,
    ...
}
```

### Add a button to open issues

To add a button to open an issue about the current page, use the following
configuration:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_issues_button": True,
    ...
}
```

### Add a button to suggest edits

You can add a button to each page that will allow users to edit the page text
directly and submit a pull request to update the documentation. To include this
button, use the following configuration:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_edit_page_button": True,
    ...
}
```

By default, the edit button will point to the `main` branch, but if you'd like
to change this, use the following configuration:

```python
html_theme_options = {
    ...
    "repository_branch": "{your-branch}",
    ...
}
```

By default, the edit button will point to the root of the repository. If your
documentation is hosted in a sub-folder, use the following configuration:

```python
html_theme_options = {
    ...
    "path_to_docs": "{path-relative-to-site-root}",
    ...
}
```

## Use a single-page version of this theme

If your documentation only has a single page, and you don't need the left
navigation bar, then you may configure `quantecon-book-theme` to run in **single page mode**
with the following configuration:

```python
html_theme_options = {
    ...
    "single_page": True
    ...
}
```

## Add authors to your documentation

If you'd like to add a list of authors to your documentation, you can do so with the following configuration:

```python
html_theme_options = {
    ...
    "authors": [
        {"name": "author1", "url": "bio-link1"},
        {"name": "author2", "url": "bio-link2"},
    ]
}
```

Authors with there bio links will be displayed just below the title of the page.

## Use plugins to add/extend features

If you want some extra features in your documentation website or modify an existing one, you can add a list of plugins
in javascript format, to suit your needs:

```python
html_theme_options = {
    ...
    "plugins_list": ["path-relative-to-config-file.js"]
    ...
}
```

## Add a dark mode version of your logo

To optimize your branding for dark mode, consider creating a dedicated dark mode variant of your logo.
Then, configure the theme settings to display this variant when dark mode is active, using the following configuration:

```python
html_theme_options = {
    ...
    "dark_logo": "name-of-dark-logo-image"
    ...
}
```

The image is expected to be in the `_static` folder of your source repository.

## Specifying the hosting location for Download Notebooks

While this location is auto-configured to be `/_notebooks/` (which works in most deployment cases) this option
enables you to specify a different location for more complex url structures such as those found when using
GitHub pages (without a custom URL)

```python
html_theme_options = {
    ...
    "download_nb_path" : https://{{ GitHub Account}}.github.io/{{ repo }}/
    ...
}
```

## Custom Code Syntax Highlighting

By default, the theme uses custom QuantEcon syntax highlighting colors for code blocks. If you'd prefer to use Pygments' built-in syntax highlighting styles instead, you can disable the custom code styling:

```python
# conf.py

# Set the Pygments style you want to use
pygments_style = 'friendly'  # or 'monokai', 'github-dark', 'default', etc.

html_theme_options = {
    ...
    "qetheme_code_style": False,
    ...
}
```

Available Pygments styles include: `default`, `friendly`, `monokai`, `github-dark`, `github-light`, `tango`, `vim`, and many others. See the [Pygments documentation](https://pygments.org/styles/) for a full list.

When `qetheme_code_style` is `True` (the default), the custom QuantEcon code highlighting is used and the `pygments_style` setting is ignored. When set to `False`, the theme will respect your `pygments_style` configuration.

## Git-Based Metadata

The theme automatically displays git-based metadata for each page, including the last modified timestamp and an interactive changelog dropdown. This feature requires:

1. Your documentation source files to be tracked in a git repository
2. A configured `repository_url` in your theme options

### Automatic Features

When available, the theme displays:

- **Last modified timestamp**: Shows when the current file was last changed in git
- **Changelog dropdown**: Interactive button showing the last 10 commits affecting the current file
- **Clickable commit hashes**: Each commit hash links directly to the GitHub commit page
- **Full history link**: Links to the complete commit history for the file on GitHub

### Configuration Options

You can customize the git metadata display in your `conf.py`:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-org}/{your-repo}",
    "repository_branch": "main",  # default: "main"
    "path_to_docs": "docs",  # if your docs are in a subfolder

    # Git metadata customization
    "last_modified_date_format": "%b %d, %Y",  # default: "%b %d, %Y"
    "changelog_max_entries": 10,  # default: 10
    ...
}
```

For Jupyter Book projects, add to your `_config.yml`:

```yaml
sphinx:
  config:
    html_theme_options:
      repository_url: "https://github.com/{your-org}/{your-repo}"
      repository_branch: "main"
      path_to_docs: "docs"
      last_modified_date_format: "%b %d, %Y"
      changelog_max_entries: 10
```

### Date Format Options

The `last_modified_date_format` option accepts Python `strftime` format codes:

- `%b %d, %Y` → "Nov 22, 2025" (default)
- `%Y-%m-%d` → "2025-11-22"
- `%B %d, %Y` → "November 22, 2025"
- `%m/%d/%Y` → "11/22/2025"

See the [Python strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) for all format codes.

### Disabling Git Metadata

The git metadata features are automatically disabled if:
- The source file is not tracked in a git repository
- The `repository_url` is not configured
- The git commands fail or timeout

No additional configuration is needed to handle these cases.

## Customizing Toggle Button Text

The theme supports collapsible content via the `sphinx-togglebutton` extension, which provides two mechanisms for creating expandable sections:

1. **Toggle directives** - Created with `` ```{toggle} `` syntax
2. **Dropdown admonitions** - Created by adding `:class: dropdown` to admonitions

### Customizing Toggle Directive Text

To customize the button text for toggle directives, add the following to your Sphinx configuration:

```python
# conf.py

# Customize toggle button text
togglebutton_hint = "Show"
togglebutton_hint_hide = "Hide"
```

For Jupyter Book projects, add to your `_config.yml`:

```yaml
# _config.yml

sphinx:
  config:
    togglebutton_hint: "Show"
    togglebutton_hint_hide: "Hide"
```

### Dropdown Admonitions

The theme automatically customizes dropdown admonitions (those with `:class: dropdown`) to display "Show"/"Hide" instead of the default "Click to show"/"Click to hide". This styling is built into the theme and requires no additional configuration.

**Example usage:**

````markdown
```{note}
:class: dropdown

This is a collapsible note that will show "Show" when collapsed and "Hide" when expanded.
```

```{toggle}
This is a toggle directive that will use the configured button text.
```
````
which renders:

```{note}
:class: dropdown

This is a collapsible note that will show "Show" when collapsed and "Hide" when expanded.
```

```{toggle}
This is a toggle directive that will use the configured button text.
```

## Customizing Emphasis and Definition Colors

The theme applies custom colors to emphasis (italic) and bold/strong text. By default:

- **Emphasis** (`em`): Green (`#2d9f42`) in light mode, lighter green (`#66bb6a`) in dark mode
- **Bold/Strong** (`strong`, `b`): Brown (`#8b4513`) in light mode, lighter brown (`#cd853f`) in dark mode

You can override these colors using `html_theme_options`:

```python
html_theme_options = {
    ...
    "emphasis_color": "#1a73e8",
    "emphasis_color_dark": "#8ab4f8",
    "definition_color": "#d93025",
    "definition_color_dark": "#f28b82",
    ...
}
```

For Jupyter Book projects, add to your `_config.yml`:

```yaml
sphinx:
  config:
    html_theme_options:
      emphasis_color: "#1a73e8"
      emphasis_color_dark: "#8ab4f8"
      definition_color: "#d93025"
      definition_color_dark: "#f28b82"
```

| Option | Description | Default |
|---|---|---|
| `emphasis_color` | Color for `em` tags in light mode | `#2d9f42` (green) |
| `emphasis_color_dark` | Color for `em` tags in dark mode | `#66bb6a` (light green) |
| `definition_color` | Color for `strong`/`b` tags in light mode | `#8b4513` (brown) |
| `definition_color_dark` | Color for `strong`/`b` tags in dark mode | `#cd853f` (peru) |

Any option left empty will use the theme's built-in default color.
