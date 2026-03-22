# Multilingual Support Plan — Theme Features

**Date:** December 2024 (updated March 2026)
**Status:** Planning
**Scope:** Theme-level features only (see `PLAN-INFRASTRUCTURE.md` for hosting/DNS)

## Overview

This document defines the theme features needed to support multiple language versions of QuantEcon lecture sites. The theme provides a **hosting-agnostic language switcher** — it renders links to whatever URLs are configured, regardless of whether sites live on GitHub Pages, custom subdomains, or behind a reverse proxy.

### Design Principle

The theme does **not** know or care about hosting topology. Each lecture site configures explicit URLs for its language variants. When hosting changes (e.g., GitHub Pages → subdomains → Cloudflare proxy), only the `url` values in each site's `_config.yml` need updating — no theme code changes.

### Test Repositories

| Language | Repository | Current Live URL |
|----------|-----------|-----------------|
| English (source) | `QuantEcon/lecture-python-programming` | `python-programming.quantecon.org` |
| Persian (Farsi) | `QuantEcon/lecture-python-programming.fa` | `quantecon.github.io/lecture-python-programming.fa` |
| Chinese (Simplified) | `QuantEcon/lecture-python-programming.zh-cn` | `quantecon.github.io/lecture-python-programming.zh-cn` |

---

## Feature 1: Language Switcher Configuration

### New Theme Options

Two new options in `html_theme_options`:

- **`languages`** — list of available language variants with explicit URLs
- **`current_language`** — language code identifying the current build

### Configuration Example

Each language repo includes the **same `languages` list** but sets a different `current_language`:

```yaml
# lecture-python-programming/_config.yml (English — source)
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

```yaml
# lecture-python-programming.fa/_config.yml (Persian)
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

```yaml
# lecture-python-programming.zh-cn/_config.yml (Chinese)
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

### URL Construction

When a user clicks a language link, the switcher navigates to:

```
{lang.url}/{pagename}.html
```

For example, on the `intro` page of the English site, clicking "فارسی" navigates to:

```
https://quantecon.github.io/lecture-python-programming.fa/intro.html
```

This works because all translation repos mirror the source repo's page structure (via `action-translation`).

### Graceful Behavior

- **No `languages` configured** → no switcher rendered (backwards compatible)
- **Single language configured** → no switcher rendered (nothing to switch to)
- **Page doesn't exist in target language** → user sees a 404 on the target site (acceptable for Phase 1; translation repos should mirror source structure)

---

## Feature 2: Language Switcher UI Component

### Placement

A globe icon button at the **far right** of the bottom toolbar (`qe-toolbar__links`), after the GitHub source link:

```
[TOC] [Home] [Logo]     ...     [Search] [Fullscreen] [A+] [A-] [◐] [⬇] [▶] [PDF] [GitHub] [🌐]
```

This prominent position signals that language switching is a site-level action, and pairs naturally with the GitHub icon as a "meta/external" control.

### Behavior

- **Click** opens a dropdown/popover listing available languages
- **Current language** is visually marked (e.g., bold, checkmark, or highlighted)
- **RTL languages** display their name in the correct direction (the `dir` attribute on the link handles this)
- **Dropdown position** is RTL-aware (flips side when `enable_rtl` is active)

### Template (`layout.html`)

```jinja
{# Language Switcher — only rendered when multiple languages are configured #}
{% if theme_languages and theme_languages | length > 1 %}
<li class="btn__language">
  <div class="language-switcher">
    <button class="language-switcher__toggle" aria-label="Switch language"
            aria-expanded="false" aria-haspopup="true">
      <svg><!-- globe icon --></svg>
    </button>
    <ul class="language-switcher__menu" role="menu">
      {% for lang in theme_languages %}
      <li role="menuitem">
        <a href="{{ lang.url }}/{{ pagename }}.html"
           hreflang="{{ lang.code }}"
           {% if lang.code == theme_current_language %}aria-current="true"{% endif %}
           {% if lang.rtl %}dir="rtl"{% endif %}>
          {{ lang.name }}
        </a>
      </li>
      {% endfor %}
    </ul>
  </div>
</li>
{% endif %}
```

### Styling

New SCSS partial: `_language-switcher.scss`

Key design requirements:
- Matches existing toolbar button style (consistent with search, font size, etc.)
- Dropdown appears above the toolbar (since toolbar is at the bottom)
- RTL-aware positioning (flip when `body[dir="rtl"]`)
- Language names use appropriate font/direction for each script
- Current language is visually distinguished
- Accessible: keyboard navigable, proper ARIA roles

---

## Feature 3: SEO — hreflang Tags

### Purpose

Tell search engines that each page has equivalent content in other languages. This prevents duplicate content penalties and helps serve the right language in search results.

### Template (`layout.html` — inside `<head>`)

```jinja
{% if theme_languages and theme_languages | length > 1 %}
{% for lang in theme_languages %}
<link rel="alternate" hreflang="{{ lang.code }}"
      href="{{ lang.url }}/{{ pagename }}.html" />
{% endfor %}
<link rel="alternate" hreflang="x-default"
      href="{{ theme_languages[0].url }}/{{ pagename }}.html" />
{% endif %}
```

The `x-default` tag points to the first language in the list (English, by convention) as the fallback for unmatched locales.

---

## Feature 4: RTL Integration (Already Implemented)

The theme already supports RTL layout via `enable_rtl: true`. Persian and Arabic sites use:

```yaml
html_theme_options:
  enable_rtl: true
```

The language switcher adds one additional RTL concern: its dropdown styling must respect `body[dir="rtl"]`. This is handled in `_rtl.scss` alongside existing RTL adjustments.

### Localized UI Strings

Sphinx and the parent theme (pydata-sphinx-theme) handle UI string localization (e.g., "Next", "Previous", "Search") when `language` is set in the Sphinx config. The quantecon-book-theme does **not** need its own translation catalogs.

```yaml
sphinx:
  config:
    language: fa  # Sphinx handles translating built-in UI strings
```

---

## Implementation Plan

### Theme Changes Required

| Step | Description | Files Modified |
|------|-------------|---------------|
| 1 | Register `languages` and `current_language` theme options | `theme.conf`, `__init__.py` |
| 2 | Process language list in `add_to_context()` | `__init__.py` |
| 3 | Add language switcher template markup | `layout.html` |
| 4 | Add `hreflang` tags to `<head>` | `layout.html` |
| 5 | Create language switcher styles | `_language-switcher.scss`, `index.scss` |
| 6 | Add RTL-aware switcher styles | `_rtl.scss` |
| 7 | Add switcher toggle JavaScript | `assets/scripts/` |
| 8 | Compile assets | `npm run build` |
| 9 | Write documentation | `docs/developer/multilingual.md` |
| 10 | Add tests | `tests/` |

### Per-Site Configuration (Not Theme Work)

Each lecture repo needs these changes in `_config.yml` (done by site maintainers, not the theme):

```yaml
sphinx:
  config:
    language: fa                    # Sphinx built-in — localizes UI strings
    html_theme_options:
      enable_rtl: true              # For RTL languages (fa, ar, he, ur)
      languages: [...]              # Language list with URLs
      current_language: fa          # This build's language code
```

---

## Design Decisions

### Decided

| Question | Decision | Rationale |
|----------|----------|-----------|
| Page linking | Link to same `pagename` in target language | Translation repos mirror source structure via `action-translation` |
| No translation available | User sees 404 on target site | Acceptable for Phase 1; repos should mirror structure |
| Search | Per-language (each site has own search index) | Cross-language search is unnecessary complexity |
| English URL | Remains at root `/` (no `/en/` prefix) | Breaking existing links is not worth it |
| UI string localization | Handled by Sphinx via `language` config | No need for theme-level translation catalogs |
| Hosting topology | Theme is agnostic — uses explicit URLs | Decouples theme from infrastructure decisions |

### Open for Discussion

1. **Switcher placement** — Bottom toolbar (proposed) vs. top header area? The toolbar is consistent with other controls but may be less discoverable.

2. **Language label format** — Show native name only ("فارسی") or native + English ("فارسی / Persian")? Native-only is cleaner; dual labels help users who might not recognize a script.

3. **Visual design** — Globe icon dropdown (proposed) or inline flag/text links? Globe icon is compact and internationally recognized; flags are controversial (languages ≠ countries).

---

## References

- [Google hreflang Guidelines](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [pydata-sphinx-theme Localization](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/i18n.html)
- [Sphinx Internationalization](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)
- [W3C Language Tags](https://www.w3.org/International/articles/language-tags/)
- Hosting and infrastructure options → see `PLAN-INFRASTRUCTURE.md`
