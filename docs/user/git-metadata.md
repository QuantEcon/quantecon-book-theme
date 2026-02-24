# Git-Based Metadata

The theme automatically displays git-based metadata for each page, including the
last modified timestamp and an interactive changelog dropdown.

```{contents}
:local:
:depth: 2
```

## Requirements

1. Your documentation source files must be tracked in a git repository
2. A configured `repository_url` in your theme options

## Automatic Features

When available, the theme displays:

- **Last modified timestamp** — when the file was last changed in git
- **Changelog dropdown** — interactive button showing the last 10 commits affecting the file
- **Clickable commit hashes** — each links directly to the GitHub commit page
- **Full history link** — links to the complete commit history on GitHub

## Configuration

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-org}/{your-repo}",
    "repository_branch": "main",  # default: "main"
    "path_to_docs": "docs",  # if docs are in a subfolder

    # Git metadata customization
    "last_modified_date_format": "%b %d, %Y",  # default: "%b %d, %Y"
    "changelog_max_entries": 10,  # default: 10
    ...
}
```

For Jupyter Book projects:

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

## Date Format Options

The `last_modified_date_format` option accepts Python `strftime` format codes:

- `%b %d, %Y` → "Nov 22, 2025" (default)
- `%Y-%m-%d` → "2025-11-22"
- `%B %d, %Y` → "November 22, 2025"
- `%m/%d/%Y` → "11/22/2025"

See the [Python strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
for all format codes.

## Disabling

Git metadata features are automatically disabled if:
- The source file is not tracked in a git repository
- The `repository_url` is not configured
- The git commands fail or timeout

No additional configuration is needed.
