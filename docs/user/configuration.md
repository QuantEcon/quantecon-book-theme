# Configuration

Core configuration options for `quantecon-book-theme`. All options are set via
`html_theme_options` in your `conf.py` (or `_config.yml` for Jupyter Book).

```{contents}
:local:
:depth: 2
```

## Disabling QuantEcon Official Components

If you are a project using this theme but are not an official QuantEcon project,
set the following to remove the QuantEcon logo from the top toolbar and adjust
some default color styles:

```python
html_theme_options = {
    ...
    "quantecon_project": False,
    ...
}
```

## Source Repository Buttons

There are a collection of buttons that you can use to link back to your source
repository. All require the `repository_url` option:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    ...
}
```

### Add a link to your repository

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_repository_button": True,
    ...
}
```

### Add a button to open issues

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_issues_button": True,
    ...
}
```

### Add a button to suggest edits

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "use_edit_page_button": True,
    ...
}
```

By default, the edit button points to the `main` branch. To change this:

```python
html_theme_options = {
    ...
    "repository_branch": "{your-branch}",
    ...
}
```

If your documentation is in a sub-folder of the repository:

```python
html_theme_options = {
    ...
    "path_to_docs": "{path-relative-to-site-root}",
    ...
}
```

## Single-Page Mode

If your documentation only has a single page:

```python
html_theme_options = {
    ...
    "single_page": True,
    ...
}
```

This disables the left navigation bar.

## Add Authors

Display a list of authors just below the page title:

```python
html_theme_options = {
    ...
    "authors": [
        {"name": "author1", "url": "bio-link1"},
        {"name": "author2", "url": "bio-link2"},
    ],
    ...
}
```

## Plugins

Add custom JavaScript plugins to extend or modify theme features:

```python
html_theme_options = {
    ...
    "plugins_list": ["path-relative-to-config-file.js"],
    ...
}
```

## Logo Configuration

### Dark mode logo

Provide a dedicated dark mode variant of your logo. The image must be in
your `_static/` directory:

```python
html_theme_options = {
    ...
    "dark_logo": "name-of-dark-logo-image",
    ...
}
```

When no dark logo is provided, the theme automatically applies an inversion
filter to the site logo.

## Sticky Table of Contents

Enable a fixed right-hand table of contents with scroll spy and auto-expansion:

```python
html_theme_options = {
    ...
    "sticky_contents": True,
    ...
}
```

For Jupyter Book projects:

```yaml
sphinx:
  config:
    html_theme_options:
      sticky_contents: true
```

### Features

When enabled:
- **Fixed positioning** — the TOC stays visible while scrolling
- **Active section highlighting** — the current section is highlighted
- **Copy section link** — hover over a TOC entry to reveal a copy icon
- **Back to top button** — appears after scrolling down 300px
- **Auto-expand subsections** — subsections expand as you scroll

### Disable auto-expansion

```python
html_theme_options = {
    ...
    "sticky_contents": True,
    "contents_autoexpand": False,
    ...
}
```

When `contents_autoexpand` is `False`, only top-level section names are displayed.

## Customizing Toggle Buttons

### Toggle directives

Customize the button text for toggle directives:

```python
# conf.py
togglebutton_hint = "Show"
togglebutton_hint_hide = "Hide"
```

For Jupyter Book:

```yaml
sphinx:
  config:
    togglebutton_hint: "Show"
    togglebutton_hint_hide: "Hide"
```

### Dropdown admonitions

Dropdown admonitions (`:class: dropdown`) automatically display "Show"/"Hide"
instead of the default text. No additional configuration is needed.

**Example:**

````markdown
```{note}
:class: dropdown

This is a collapsible note.
```
````

Which renders:

```{note}
:class: dropdown

This is a collapsible note.
```

## Download Notebook Path

Specify a custom location for downloadable notebooks (useful for GitHub Pages
without a custom URL):

```python
html_theme_options = {
    ...
    "download_nb_path": "https://{{ GitHub Account }}.github.io/{{ repo }}/",
    ...
}
```

The default location is `/_notebooks/`.

## Open Graph Metadata

Generate OpenGraph preview tags by setting your site's base URL:

```python
html_baseurl = "https://<your-site-baseurl>"
```
