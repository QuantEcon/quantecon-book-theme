# Multilingual Support Plan

Architecture plan for supporting multiple language versions of QuantEcon lecture
sites.

```{contents}
:local:
:depth: 2
```

## Overview

**Status:** Planning
**Date:** December 2024

### Goals

1. Unified branding across all language versions
2. Easy translation management with separate repos per language
3. Simple sync workflow using `action-translation` for PR-based synchronization
4. Language switching — users can switch between available translations
5. SEO-friendly canonical URLs and hreflang tags

### Current State

- **English:** `github.com/QuantEcon/lecture-python-programming.myst`
- **Persian:** `github.com/QuantEcon/lecture-python-programming.fa`
- **Chinese:** Coming soon

## Architecture: Separate Repos per Language

| Aspect | Separate Repos | Single Repo with Branches |
|--------|---------------|---------------------------|
| Source organization | Clean, isolated per language | Complex branching |
| Translation workflow | Independent PRs | Branch management overhead |
| CI/CD | Own pipeline per repo | Complex conditional builds |
| Contributor access | Per-language team access | All-or-nothing |
| Build isolation | One failure doesn't block others | Shared failure risk |

### Naming Convention

```
lecture-python-programming.myst     # English (source)
lecture-python-programming.fa       # Persian (Farsi)
lecture-python-programming.zh-cn    # Simplified Chinese
lecture-python-programming.ja       # Japanese (if needed)
```

## URL Structure

### Recommended: Subdomain → Cloudflare Proxy upgrade path

**Phase 1** (simple): Subdomain pattern

```
fa.python-programming.quantecon.org   # Persian
zh.python-programming.quantecon.org   # Chinese
python-programming.quantecon.org      # English
```

**Phase 2** (optional): Add Cloudflare proxy for clean subdirectory URLs

```
python-programming.quantecon.org/fa/     # Persian
python-programming.quantecon.org/zh-cn/  # Chinese
python-programming.quantecon.org/        # English
```

## Theme Modifications

### Language Switcher Component

Configuration per-site `_config.yml`:

```yaml
sphinx:
  config:
    html_theme_options:
      languages:
        - name: English
          code: en
          url: https://python-programming.quantecon.org/
        - name: فارسی
          code: fa
          url: https://python-programming.quantecon.org/fa/
          rtl: true
        - name: 中文
          code: zh-cn
          url: https://python-programming.quantecon.org/zh-cn/
      current_language: en
```

### SEO: hreflang Tags

Alternate language links in `<head>`:

```html
<link rel="alternate" hreflang="fa" href=".../fa/page.html" />
<link rel="alternate" hreflang="zh-cn" href=".../zh-cn/page.html" />
<link rel="alternate" hreflang="x-default" href=".../page.html" />
```

### RTL Support

Persian sites should configure:

```yaml
sphinx:
  config:
    language: fa
    html_theme_options:
      enable_rtl: true
```

## Implementation Checklist

### Phase 1: Subdomain Setup

- [ ] Configure DNS for `fa.python-programming.quantecon.org`
- [ ] Add `CNAME` file to Persian repo
- [ ] Configure `html_baseurl` in Persian repo
- [ ] Enable RTL in Persian repo
- [ ] Add language switcher to theme
- [ ] Test cross-language navigation

### Phase 2: Theme Enhancements

- [ ] Implement language switcher dropdown component
- [ ] Add `languages` theme option
- [ ] Add hreflang meta tags
- [ ] Style language switcher (RTL-aware)
- [ ] Add documentation for multilingual configuration

### Phase 3: Additional Languages

- [ ] Create `lecture-python-programming.zh-cn` repo
- [ ] Set up Chinese translation workflow
- [ ] Configure DNS and deployment
- [ ] Update language switcher configuration

## Open Questions

1. **Page equivalence:** When switching languages, should the switcher link to the
   same page path (may 404), always link to the homepage, or fallback to homepage?
2. **Partial translations:** Show English version with notice? 404 with link? Hide option?
3. **Search:** Per-language or cross-language?
4. **URL canonicalization:** English at root `/` or `/en/`?

## References

- [Sphinx Internationalization](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)
- [pydata-sphinx-theme Localization](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/i18n.html)
- [Google hreflang Guidelines](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
