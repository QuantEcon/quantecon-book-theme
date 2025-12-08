# Multilingual Support Plan for QuantEcon Lecture Sites

**Date:** December 2024  
**Status:** Planning  
**Author:** QuantEcon Team

## Overview

This document outlines the architecture for supporting multiple language versions of QuantEcon lecture sites (e.g., `lecture-python-programming.myst` with Persian, Chinese translations).

### Goals

1. **Unified branding** - All language versions feel like part of one integrated site
2. **Easy translation management** - Separate repos per language for clean source file organization
3. **Simple sync workflow** - Continue using `action-translation` for PR-based synchronization
4. **Language switching** - Users can easily switch between available translations
5. **SEO-friendly** - Proper canonical URLs and hreflang tags

### Current State

- **English:** `github.com/QuantEcon/lecture-python-programming.myst`
- **Persian:** `github.com/QuantEcon/lecture-python-programming.fa`
- **Chinese:** (Coming soon)

Each repo currently deploys independently to GitHub Pages.

---

## Architecture Decision: Separate Repos per Language

**Decision: Keep separate repositories for each language translation.**

### Rationale

| Aspect | Separate Repos ✅ | Single Repo with Branches |
|--------|------------------|---------------------------|
| Source organization | Clean, isolated per language | Complex branching strategy |
| Translation workflow | Independent PRs, easy review | Branch management overhead |
| CI/CD | Each repo has own pipeline | Complex conditional builds |
| Contributor access | Grant per-language team access | All-or-nothing access |
| `action-translation` sync | Works naturally with PRs | Would need adaptation |
| Build isolation | One language failure doesn't block others | Shared failure risk |

### Repository Naming Convention

```
lecture-python-programming.myst     # English (source/base)
lecture-python-programming.fa       # Persian (Farsi)
lecture-python-programming.zh-cn    # Simplified Chinese
lecture-python-programming.zh-tw    # Traditional Chinese (if needed)
lecture-python-programming.ja       # Japanese (if needed)
```

---

## URL Structure Options

### Option A: Subdirectory Pattern (Preferred)

```
https://python-programming.quantecon.org/           # English (base)
https://python-programming.quantecon.org/fa/        # Persian
https://python-programming.quantecon.org/zh-cn/     # Chinese
```

**Pros:**
- Clean, intuitive URL structure
- Single domain for all languages
- Better for SEO (consolidated domain authority)
- Matches common i18n patterns (Django, Next.js, etc.)

**Cons:**
- Requires either combined deployment OR reverse proxy
- Cannot be achieved with independent gh-pages hosting alone

### Option B: Subdomain Pattern

```
https://python-programming.quantecon.org/           # English
https://fa.python-programming.quantecon.org/        # Persian
https://zh.python-programming.quantecon.org/        # Chinese
```

**Pros:**
- Each repo deploys independently to gh-pages
- Simple DNS configuration (CNAME per subdomain)
- No deployment coordination needed
- Wikipedia uses this pattern successfully

**Cons:**
- Less "integrated" appearance
- Separate SSL certificates (or wildcard needed)
- Domain authority split across subdomains

---

## Hosting Implementation Comparison

### Feature Comparison Matrix

| Feature | Combined Deployment | Subdomain Pattern | Cloudflare Proxy |
|---------|:------------------:|:-----------------:|:----------------:|
| **URL Structure** | `/fa/` subdirectories ✅ | `fa.xxx.org` subdomains | `/fa/` subdirectories ✅ |
| **Pure GitHub Pages** | ✅ Yes | ✅ Yes | ❌ No (needs Cloudflare) |
| **Independent Deployments** | ❌ No (coordinated) | ✅ Yes | ✅ Yes |
| **CI/CD Complexity** | 🔴 High | 🟢 Low | 🟢 Low |
| **Add New Language** | 🟡 Medium (update workflow) | 🟢 Easy (new repo + DNS) | 🟢 Easy (update worker) |
| **Build Failure Isolation** | ❌ All languages affected | ✅ Independent | ✅ Independent |
| **Single Domain Authority** | ✅ Yes | ❌ Split across subdomains | ✅ Yes |
| **External Dependencies** | None | None | Cloudflare |
| **DNS Entries Required** | 1 | 1 per language | 1 + subdomains for origins |
| **SSL Certificates** | 1 | Wildcard or 1 per language | 1 (Cloudflare handles) |
| **Debugging Complexity** | 🟡 Medium | 🟢 Low | 🟡 Medium |
| **Cost** | Free | Free | Free (Workers free tier) |

### Decision Criteria

**Choose Combined Deployment if:**
- Clean `/fa/` URLs are essential
- You want to stay 100% on GitHub infrastructure
- You can accept coordinated builds and cross-repo CI complexity

**Choose Subdomain Pattern if:**
- Simplicity is the priority
- Each translation team needs full autonomy
- You're okay with `fa.xxx.org` URL structure
- You want the fastest path to deployment

**Choose Cloudflare Proxy if:**
- Clean `/fa/` URLs are essential
- You want independent deployments per language
- You're comfortable with Cloudflare as a dependency
- You want CDN benefits (caching, DDoS protection)

### Recommended Upgrade Path

The **Subdomain Pattern → Cloudflare Proxy** path is recommended because Phase 1 work is not wasted—it becomes the foundation for Phase 2.

```
Phase 1: Subdomain Pattern              Phase 2: Add Cloudflare Proxy
────────────────────────────────        ────────────────────────────────

fa.python-programming.org ──────┐       
                                │       Cloudflare Worker routes:
python-programming.org ─────────┼──▶      /    → python-programming.org
                                │         /fa/ → fa.python-programming.org
zh.python-programming.org ──────┘         /zh/ → zh.python-programming.org

(Each repo deploys to gh-pages)         (Same backends, unified URLs)
```

#### What Changes When Adding Cloudflare (Phase 1 → Phase 2)

| Aspect | Phase 1 (Subdomains) | Phase 2 (Cloudflare) |
|--------|---------------------|----------------------|
| DNS | Points to GitHub Pages | Points to Cloudflare |
| Subdomains | User-facing URLs | Backend origins (still exist) |
| `html_baseurl` | `https://fa.xxx.org/` | `https://xxx.org/fa/` |
| Repos & CI/CD | No change | No change ✅ |
| gh-pages deployment | No change | No change ✅ |

#### Migration Steps (Phase 1 → Phase 2)

1. **Set up Cloudflare** (if not already using for DNS)
2. **Create Worker script** (~20 lines of JavaScript)
3. **Update DNS** to route through Cloudflare
4. **Update `html_baseurl`** in each translation repo's `_config.yml`
5. **Update language switcher URLs** in theme configuration

**Key benefit:** All the repo setup, CI/CD pipelines, and gh-pages deployments from Phase 1 remain unchanged. Only the "front door" (DNS + URL routing) changes.

### Recommendation Summary

| Phase | Approach | URLs | Effort |
|-------|----------|------|--------|
| **Phase 1** | Subdomain Pattern | `fa.python-programming.org` | 🟢 Low |
| **Phase 2** (optional) | Add Cloudflare Proxy | `python-programming.org/fa/` | 🟢 Low (incremental) |

---

## Hosting Implementation Options

### Implementation 1: Combined Deployment (Pure GitHub Pages)

Assemble all language builds into a single gh-pages deployment with subdirectory structure.

#### Why This Works: Relative Links

Jupyter Book (via Sphinx) generates **relative paths** for internal navigation by default:

```html
<!-- Example generated HTML -->
<a href="getting_started.html">Getting Started</a>
<a href="../chapter2/intro.html">Chapter 2 Intro</a>
<a href="_static/custom.css">Stylesheet</a>
```

This means internal links work correctly regardless of subdirectory:

```
# English site at root
/index.html links to → ./getting_started.html ✅

# Persian site in /fa/
/fa/index.html links to → ./getting_started.html → resolves to /fa/getting_started.html ✅
```

**What needs explicit configuration:**

| Link Type | Format | Needs Configuration? |
|-----------|--------|---------------------|
| Internal page links | Relative (`./page.html`) | ❌ No |
| Navigation (prev/next) | Relative | ❌ No |
| Static assets | Relative (`_static/`) | ❌ No |
| Table of contents | Relative | ❌ No |
| Canonical URL | Absolute | ✅ Set `html_baseurl` |
| Social meta tags | Absolute | ✅ Set `html_baseurl` |
| Language switcher | Absolute | ✅ Must configure |
| Sitemap | Absolute | ✅ Set `html_baseurl` |

Each language build should set its `html_baseurl` appropriately:

```yaml
# lecture-python-programming.fa/_config.yml
sphinx:
  config:
    html_baseurl: https://python-programming.quantecon.org/fa/
```

#### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Coordinator Repository                        │
│              (or workflow in main English repo)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │  English Repo │ │  Persian Repo │ │  Chinese Repo │
    │   (source)    │ │     (.fa)     │ │   (.zh-cn)    │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                 │                 │
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │  Build HTML   │ │  Build HTML   │ │  Build HTML   │
    │  (artifact)   │ │  (artifact)   │ │  (artifact)   │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                    ┌─────────────────┐
                    │ Assemble into   │
                    │ single gh-pages │
                    │                 │
                    │ /index.html     │
                    │ /fa/index.html  │
                    │ /zh-cn/index.html│
                    └─────────────────┘
```

#### GitHub Actions Workflow (Conceptual)

```yaml
# .github/workflows/deploy-multilingual.yml
name: Deploy Multilingual Site

on:
  workflow_dispatch:
  repository_dispatch:
    types: [translation-updated]
  push:
    branches: [main]

jobs:
  build-english:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build English site
        run: jupyter-book build lectures/
      - uses: actions/upload-artifact@v4
        with:
          name: site-en
          path: lectures/_build/html/

  build-persian:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          repository: QuantEcon/lecture-python-programming.fa
      - name: Build Persian site
        run: jupyter-book build lectures/
      - uses: actions/upload-artifact@v4
        with:
          name: site-fa
          path: lectures/_build/html/

  build-chinese:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          repository: QuantEcon/lecture-python-programming.zh-cn
      - name: Build Chinese site
        run: jupyter-book build lectures/
      - uses: actions/upload-artifact@v4
        with:
          name: site-zh-cn
          path: lectures/_build/html/

  deploy:
    needs: [build-english, build-persian, build-chinese]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: site-en
          path: combined/
      - uses: actions/download-artifact@v4
        with:
          name: site-fa
          path: combined/fa/
      - uses: actions/download-artifact@v4
        with:
          name: site-zh-cn
          path: combined/zh-cn/
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./combined
```

#### Triggering Cross-Repo Builds

Each translation repo notifies the coordinator when updated:

```yaml
# In lecture-python-programming.fa/.github/workflows/notify.yml
name: Notify Coordinator

on:
  push:
    branches: [main]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger multilingual deploy
        uses: peter-evans/repository-dispatch@v2
        with:
          token: ${{ secrets.CROSS_REPO_TOKEN }}
          repository: QuantEcon/lecture-python-programming.myst
          event-type: translation-updated
          client-payload: '{"language": "fa"}'
```

#### Pros & Cons

| Pros | Cons |
|------|------|
| Pure GitHub Pages hosting | Complex CI/CD orchestration |
| True `/fa/` URL structure | Build coordination overhead |
| Single deployment target | All languages rebuild together |
| No external services needed | Need cross-repo tokens/permissions |

---

### Implementation 2: Subdomain with Independent Hosting

Each language repo deploys to its own subdomain independently.

#### DNS Configuration

```
# DNS Records (Cloudflare, Route53, etc.)
python-programming.quantecon.org      CNAME  quantecon.github.io
fa.python-programming.quantecon.org   CNAME  quantecon.github.io
zh.python-programming.quantecon.org   CNAME  quantecon.github.io
```

#### GitHub Pages Configuration

Each repo's `CNAME` file:

```
# lecture-python-programming.myst/CNAME
python-programming.quantecon.org

# lecture-python-programming.fa/CNAME
fa.python-programming.quantecon.org

# lecture-python-programming.zh-cn/CNAME
zh.python-programming.quantecon.org
```

#### Jupyter Book Configuration

```yaml
# lecture-python-programming.fa/lectures/_config.yml
sphinx:
  config:
    language: fa
    html_baseurl: https://fa.python-programming.quantecon.org/
```

#### Pros & Cons

| Pros | Cons |
|------|------|
| Simple, independent deployments | Subdomain URLs less elegant |
| No coordination needed | Multiple DNS entries |
| Each repo fully autonomous | Domain authority fragmented |
| Easy to add new languages | Wildcard SSL or per-subdomain certs |

---

### Implementation 3: Cloudflare Reverse Proxy (Hybrid)

Use Cloudflare Workers or Page Rules to route subdirectory paths to different gh-pages origins.

#### Architecture

```
                         ┌─────────────────┐
    User Request ───────▶│   Cloudflare    │
    /fa/intro.html       │   (DNS + CDN)   │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │     Cloudflare Worker     │
                    │   (Path-based routing)    │
                    └─────────────┬─────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
   /fa/* → fa.xxx.org       /* → xxx.org         /zh-cn/* → zh.xxx.org
   (Persian gh-pages)       (English gh-pages)   (Chinese gh-pages)
```

#### Cloudflare Worker Code

```javascript
// Cloudflare Worker for path-based routing
const ROUTES = {
  '/fa/': 'https://fa.python-programming.quantecon.org',
  '/zh-cn/': 'https://zh.python-programming.quantecon.org',
  '/': 'https://python-programming.quantecon.org'
};

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;
  
  // Find matching route
  for (const [prefix, origin] of Object.entries(ROUTES)) {
    if (prefix !== '/' && path.startsWith(prefix)) {
      // Rewrite to origin, preserving rest of path
      const newPath = path.slice(prefix.length - 1); // Keep leading /
      const newUrl = origin + newPath + url.search;
      return fetch(newUrl, {
        headers: request.headers,
        method: request.method
      });
    }
  }
  
  // Default to English
  return fetch(ROUTES['/'] + path + url.search);
}
```

#### Pros & Cons

| Pros | Cons |
|------|------|
| Clean `/fa/` URLs | Requires Cloudflare (free tier works) |
| Independent repo deployments | Additional infrastructure layer |
| Easy to add languages | Slightly more complex debugging |
| CDN benefits included | Cloudflare dependency |

---

## Theme Modifications for Language Support

### 1. Language Switcher Component

Add a dropdown to the theme navbar allowing users to switch languages.

#### Configuration (per-site `_config.yml`)

```yaml
html:
  extra_navbar: ""
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
      current_language: en  # or fa, zh-cn
```

#### Template Addition (`layout.html`)

```jinja
{# Language Switcher Component #}
{% if theme_languages %}
<div class="language-switcher dropdown">
  <button class="btn btn-sm dropdown-toggle" type="button" 
          id="languageDropdown" data-bs-toggle="dropdown" aria-expanded="false">
    🌐 {{ theme_current_language_name }}
  </button>
  <ul class="dropdown-menu" aria-labelledby="languageDropdown">
    {% for lang in theme_languages %}
    <li>
      <a class="dropdown-item {% if lang.code == theme_current_language %}active{% endif %}"
         href="{{ lang.url }}{{ pagename }}.html"
         hreflang="{{ lang.code }}"
         {% if lang.rtl %}dir="rtl"{% endif %}>
        {{ lang.name }}
      </a>
    </li>
    {% endfor %}
  </ul>
</div>
{% endif %}
```

### 2. RTL Support (Already Implemented)

The theme already supports RTL via `enable_rtl` option. Persian sites should configure:

```yaml
# lecture-python-programming.fa/_config.yml
sphinx:
  config:
    language: fa
    html_theme_options:
      enable_rtl: true
```

### 3. SEO: hreflang Tags

Add alternate language links to `<head>` for SEO:

```jinja
{# In layout.html <head> section #}
{% if theme_languages %}
{% for lang in theme_languages %}
<link rel="alternate" hreflang="{{ lang.code }}" 
      href="{{ lang.url }}{{ pagename }}.html" />
{% endfor %}
<link rel="alternate" hreflang="x-default" 
      href="{{ theme_languages[0].url }}{{ pagename }}.html" />
{% endif %}
```

### 4. Localized Theme Strings

The parent theme (pydata-sphinx-theme) already supports localized UI strings. Ensure the language is set correctly:

```yaml
sphinx:
  config:
    language: fa  # Triggers Persian translations for "Next", "Previous", etc.
```

---

## Recommended Approach

### For Immediate Implementation (Phase 1)

**Use Implementation 2: Subdomain Pattern**

1. ✅ Simplest to set up
2. ✅ Each repo remains fully independent
3. ✅ No CI/CD coordination needed
4. ✅ Works with existing gh-pages setup
5. ✅ Language switcher links to subdomains

### For Future Enhancement (Phase 2)

**Migrate to Implementation 1 or 3**

If unified `/fa/` URLs become important:
- **Option 1 (Combined Deployment)** if you want to stay pure GitHub
- **Option 3 (Cloudflare)** if you want independent deploys + clean URLs

---

## Implementation Checklist

### Phase 1: Subdomain Setup

- [ ] Configure DNS for `fa.python-programming.quantecon.org`
- [ ] Add `CNAME` file to Persian repo
- [ ] Configure `html_baseurl` in Persian repo's `_config.yml`
- [ ] Enable RTL in Persian repo's theme options
- [ ] Add language switcher to theme
- [ ] Test cross-language navigation

### Phase 2: Theme Enhancements

- [ ] Implement language switcher dropdown component
- [ ] Add `languages` theme option
- [ ] Add hreflang meta tags
- [ ] Style language switcher (including RTL-aware positioning)
- [ ] Add documentation for multilingual configuration

### Phase 3: Additional Languages

- [ ] Create `lecture-python-programming.zh-cn` repo
- [ ] Set up Chinese translation workflow
- [ ] Configure DNS and deployment
- [ ] Update language switcher configuration

---

## Open Questions

1. **Page equivalence:** When switching languages, should the switcher:
   - (a) Link to the same page path in other language (may 404 if not translated)
   - (b) Always link to homepage of other language
   - (c) Link to same page with fallback to homepage

2. **Partial translations:** How to handle pages that aren't translated yet?
   - Show English version with notice?
   - 404 with link to English?
   - Hide language option for untranslated pages?

3. **Search:** Should search be per-language or cross-language?

4. **URL canonicalization:** Should English site be at root `/` or `/en/`?

---

## References

- [Sphinx Internationalization](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)
- [Jupyter Book i18n Discussion](https://github.com/executablebooks/jupyter-book/issues/1234)
- [pydata-sphinx-theme Localization](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/i18n.html)
- [Google hreflang Guidelines](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
