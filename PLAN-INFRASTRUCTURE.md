# Infrastructure Plan: Multilingual Hosting for QuantEcon Lecture Sites

**Date:** December 2024 (updated March 2026)
**Status:** Planning (deferred — not blocking theme work)

## Overview

This document captures hosting and infrastructure options for serving multiple language versions of QuantEcon lecture sites under unified URLs. This is **separate from the theme's language switcher feature**, which works with any hosting setup.

### Current State

| Language | Repository | Live URL |
|----------|-----------|----------|
| English (source) | `QuantEcon/lecture-python-programming` | `python-programming.quantecon.org` |
| Persian (Farsi) | `QuantEcon/lecture-python-programming.fa` | `quantecon.github.io/lecture-python-programming.fa` |
| Chinese (Simplified) | `QuantEcon/lecture-python-programming.zh-cn` | `quantecon.github.io/lecture-python-programming.zh-cn` |

Each repo deploys independently to GitHub Pages.

### Repository Naming Convention

```
lecture-python-programming         # English (source/base)
lecture-python-programming.fa      # Persian (Farsi)
lecture-python-programming.zh-cn   # Simplified Chinese
lecture-python-programming.zh-tw   # Traditional Chinese (if needed)
lecture-python-programming.ja      # Japanese (if needed)
```

---

## URL Structure Options

### Option A: Subdomain Pattern (Phase 1 — Recommended Start)

```
python-programming.quantecon.org/           # English (base, existing)
fa.python-programming.quantecon.org/        # Persian
zh.python-programming.quantecon.org/        # Chinese
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

**Setup required:**
- DNS CNAME records pointing to `quantecon.github.io`
- `CNAME` file in each translation repo
- Update `html_baseurl` in each repo's `_config.yml`

### Option B: Subdirectory Pattern via Reverse Proxy (Phase 2 — Optional Upgrade)

```
python-programming.quantecon.org/           # English
python-programming.quantecon.org/fa/        # Persian
python-programming.quantecon.org/zh-cn/     # Chinese
```

**Pros:**
- Clean, intuitive URL structure
- Single domain for all languages
- Better for SEO (consolidated domain authority)

**Cons:**
- Requires reverse proxy (Cloudflare Worker or similar)
- Additional infrastructure dependency
- Slightly more complex debugging

### Option C: Combined Deployment (Pure GitHub Pages)

Assemble all language builds into a single gh-pages deployment with subdirectory structure.

**Pros:**
- Pure GitHub Pages hosting — no external services
- True `/fa/` URL structure

**Cons:**
- Complex CI/CD orchestration across repos
- Build coordination overhead — all languages rebuild together
- Cross-repo tokens/permissions needed
- One language failure blocks all deployments

**Not recommended** due to CI/CD complexity and fragility.

---

## Hosting Comparison Matrix

| Feature | Subdomain (A) | Reverse Proxy (B) | Combined Deploy (C) |
|---------|:---:|:---:|:---:|
| Independent deployments | ✅ | ✅ | ❌ |
| Clean `/fa/` URLs | ❌ | ✅ | ✅ |
| Pure GitHub Pages | ✅ | ❌ | ✅ |
| Build failure isolation | ✅ | ✅ | ❌ |
| Single domain authority | ❌ | ✅ | ✅ |
| External dependencies | None | Cloudflare | None |
| Add new language effort | 🟢 Low | 🟢 Low | 🟡 Medium |
| CI/CD complexity | 🟢 Low | 🟢 Low | 🔴 High |
| Cost | Free | Free (Workers free tier) | Free |

---

## Recommended Upgrade Path

Phase 1 work is not wasted — subdomains become the backend origins for Phase 2.

```
Phase 1: Subdomain Pattern              Phase 2: Add Reverse Proxy
────────────────────────────            ────────────────────────────

fa.python-programming.org ──────┐
                                │       Cloudflare Worker routes:
python-programming.org ─────────┼──▶      /    → python-programming.org
                                │         /fa/ → fa.python-programming.org
zh.python-programming.org ──────┘         /zh/ → zh.python-programming.org

(Each repo deploys to gh-pages)         (Same backends, unified URLs)
```

### What Changes When Adding Reverse Proxy (Phase 1 → Phase 2)

| Aspect | Phase 1 (Subdomains) | Phase 2 (Reverse Proxy) |
|--------|---------------------|----------------------|
| DNS | Points to GitHub Pages | Points to Cloudflare |
| Subdomains | User-facing URLs | Backend origins (still exist) |
| `html_baseurl` | `https://fa.xxx.org/` | `https://xxx.org/fa/` |
| Theme language URLs | Update `url` values in config | Update `url` values in config |
| Repos & CI/CD | No change | No change ✅ |
| gh-pages deployment | No change | No change ✅ |

Migration is just: set up Cloudflare Worker (~20 lines JS), update DNS, update `html_baseurl` and language switcher URLs in each repo's `_config.yml`.

---

## Cloudflare Worker (Phase 2 Reference)

```javascript
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

  for (const [prefix, origin] of Object.entries(ROUTES)) {
    if (prefix !== '/' && path.startsWith(prefix)) {
      const newPath = path.slice(prefix.length - 1);
      const newUrl = origin + newPath + url.search;
      return fetch(newUrl, {
        headers: request.headers,
        method: request.method
      });
    }
  }

  return fetch(ROUTES['/'] + path + url.search);
}
```

---

## Subdomain DNS Setup (Phase 1 Reference)

```
# DNS Records
python-programming.quantecon.org      CNAME  quantecon.github.io
fa.python-programming.quantecon.org   CNAME  quantecon.github.io
zh.python-programming.quantecon.org   CNAME  quantecon.github.io
```

Each repo's `CNAME` file:
```
# lecture-python-programming/CNAME
python-programming.quantecon.org

# lecture-python-programming.fa/CNAME
fa.python-programming.quantecon.org

# lecture-python-programming.zh-cn/CNAME
zh.python-programming.quantecon.org
```

---

## Interaction with Theme Language Switcher

The theme's language switcher is **hosting-agnostic**. It renders links to whatever URLs are configured in `html_theme_options.languages[].url`. When the hosting setup changes, only the `url` values in each repo's `_config.yml` need updating — no theme code changes required.

**Current setup (no infrastructure changes):**
```yaml
languages:
  - code: en
    name: English
    url: https://python-programming.quantecon.org
  - code: fa
    name: فارسی
    url: https://quantecon.github.io/lecture-python-programming.fa
    rtl: true
```

**After Phase 1 (subdomains):**
```yaml
languages:
  - code: en
    name: English
    url: https://python-programming.quantecon.org
  - code: fa
    name: فارسی
    url: https://fa.python-programming.quantecon.org
    rtl: true
```

**After Phase 2 (reverse proxy):**
```yaml
languages:
  - code: en
    name: English
    url: https://python-programming.quantecon.org
  - code: fa
    name: فارسی
    url: https://python-programming.quantecon.org/fa
    rtl: true
```
