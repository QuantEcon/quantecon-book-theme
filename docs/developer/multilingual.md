# Multilingual Support

The theme supports a language switcher for sites that have translated versions
hosted in separate repositories.

```{contents}
:local:
:depth: 2
```

## Overview

The language switcher is a **hosting-agnostic** dropdown in the bottom toolbar
that links to equivalent pages on other language versions of a site. It works
with any URL structure — GitHub Pages, custom subdomains, reverse proxies, or
any combination.

Each site configures explicit URLs for its language variants. When hosting
changes, only the `url` values in each site's `_config.yml` need updating — no
theme code changes required.

## Configuration

Add two options to `html_theme_options`:

- **`languages`** — list of available language variants
- **`current_language`** — the language code for this build

### Required Fields per Language Entry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | yes | Language code (e.g., `en`, `fa`, `zh-cn`) |
| `name` | string | yes | Display name in native script (e.g., `فارسی`) |
| `url` | string | yes | Base URL of the language version (no trailing slash) |
| `rtl` | boolean | no | Set `true` for right-to-left languages |

### Example: English Site (Source)

```yaml
# lecture-python-programming/_config.yml
sphinx:
  config:
    html_theme_options:
      languages:
        - code: en
          name: English
          url: https://python-programming.quantecon.org
        - code: fa
          name: فارسی
          url: https://quantecon.github.io/lecture-python-programming.fa
          rtl: true
        - code: zh-cn
          name: 中文
          url: https://quantecon.github.io/lecture-python-programming.zh-cn
      current_language: en
```

### Example: Persian Site (RTL Translation)

```yaml
# lecture-python-programming.fa/_config.yml
sphinx:
  config:
    language: fa
    html_theme_options:
      enable_rtl: true
      languages:
        - code: en
          name: English
          url: https://python-programming.quantecon.org
        - code: fa
          name: فارسی
          url: https://quantecon.github.io/lecture-python-programming.fa
          rtl: true
        - code: zh-cn
          name: 中文
          url: https://quantecon.github.io/lecture-python-programming.zh-cn
      current_language: fa
```

### Example: Chinese Site (LTR Translation)

```yaml
# lecture-python-programming.zh-cn/_config.yml
sphinx:
  config:
    language: zh-cn
    html_theme_options:
      languages:
        - code: en
          name: English
          url: https://python-programming.quantecon.org
        - code: fa
          name: فارسی
          url: https://quantecon.github.io/lecture-python-programming.fa
          rtl: true
        - code: zh-cn
          name: 中文
          url: https://quantecon.github.io/lecture-python-programming.zh-cn
      current_language: zh-cn
```

## Behavior

### Language Switcher

- Appears as a **globe icon** at the far right of the bottom toolbar, after the GitHub icon
- Only renders when **2 or more languages** are configured
- Clicking opens a dropdown listing all available languages
- The current language is **bold** in the dropdown
- RTL language names display with correct text direction
- Clicking a language navigates to `{lang.url}/{pagename}.html`
- Closes when clicking outside or pressing Escape

### hreflang Tags (SEO)

When multiple languages are configured, the theme automatically injects
`<link rel="alternate" hreflang="...">` tags in the `<head>` for each language,
plus an `x-default` tag pointing to the first language in the list. This tells
search engines about equivalent content in other languages.

### No Languages Configured

When `languages` is empty, has only one entry, or is not set, the switcher is
not rendered and no hreflang tags are emitted. This is fully backwards
compatible.

## RTL Integration

For right-to-left languages (Persian, Arabic, Hebrew, etc.), configure both:

```yaml
html_theme_options:
  enable_rtl: true    # Activates RTL layout for the entire site
  current_language: fa
  languages:
    - code: fa
      name: فارسی
      url: https://...
      rtl: true       # Marks this language as RTL in the switcher dropdown
```

The `enable_rtl` option controls the page layout direction. The `rtl: true`
field on a language entry only affects how that language's name is displayed
in the dropdown (via `dir="rtl"` on the link).

## Localized UI Strings

Sphinx and the parent theme (pydata-sphinx-theme) handle translating built-in
UI strings like "Next", "Previous", and "Search" when `language` is set in the
Sphinx configuration:

```yaml
sphinx:
  config:
    language: fa  # Triggers Sphinx's built-in translations
```

The quantecon-book-theme does not need its own translation catalogs.

## Infrastructure

The language switcher renders plain `<a href="...">` links to whatever URLs you
configure. It does not fetch, proxy, or iframe content.

For guidance on hosting translated sites (GitHub Pages, subdomains, reverse
proxies), see the [Infrastructure](infrastructure.md) documentation.

## Architecture

### Files Modified

| File | Purpose |
|------|---------|
| `theme.conf` | `languages` and `current_language` option defaults |
| `__init__.py` | Process language list in `add_to_context()` |
| `layout.html` | Language switcher markup + hreflang tags |
| `_language-switcher.scss` | Switcher dropdown styles |
| `_rtl.scss` | RTL-aware adjustments for the switcher |
| `language-switcher.js` | Toggle open/close, keyboard nav, click-outside |
| `index.js` | Import and initialize the switcher module |
| `index.scss` | Import the new SCSS partial |
