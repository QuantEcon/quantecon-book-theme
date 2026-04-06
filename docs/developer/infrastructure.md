# Infrastructure: Hosting Multilingual Sites

This guide describes how to host multiple language versions of a QuantEcon
lecture site, with each language in its own Git repository, and tie them
together with the theme's language switcher.

```{contents}
:local:
:depth: 2
```

## Architecture Overview

Each language version lives in a **separate repository** and deploys
independently. The theme's language switcher links between them using explicit
URLs configured in each site's `_config.yml`.

```text
┌──────────────────────────┐
│  lecture-python-programming  (English — source)
│  → python-programming.quantecon.org
└──────────────────────────┘
┌──────────────────────────┐
│  lecture-python-programming.fa  (Persian)
│  → quantecon.github.io/lecture-python-programming.fa
└──────────────────────────┘
┌──────────────────────────┐
│  lecture-python-programming.zh-cn  (Chinese)
│  → quantecon.github.io/lecture-python-programming.zh-cn
└──────────────────────────┘
```

Each repo has its own CI/CD pipeline, builds independently, and deploys to
GitHub Pages. No cross-repo coordination is required for deployment.

### Repository Naming Convention

```text
lecture-python-programming         # English (source)
lecture-python-programming.fa      # Persian (Farsi)
lecture-python-programming.zh-cn   # Simplified Chinese
lecture-python-programming.ja      # Japanese (if needed)
```

The language suffix matches the [IETF language tag](https://www.w3.org/International/articles/language-tags/).

## Option 1: GitHub Pages (Default)

This is the simplest setup. Each repo deploys to its default GitHub Pages URL.

### URLs

```text
https://python-programming.quantecon.org/       # English (custom domain)
https://quantecon.github.io/lecture-python-programming.fa/    # Persian
https://quantecon.github.io/lecture-python-programming.zh-cn/ # Chinese
```

### Setup Steps

1. **Each repo** deploys to GitHub Pages via its own CI workflow.
2. The English repo uses a custom domain (`python-programming.quantecon.org`).
3. Translation repos use the default `quantecon.github.io/repo-name/` URL.
4. Configure the language switcher in each repo's `_config.yml` with the full URLs.

### Language Switcher Config

```yaml
# In every repo's _config.yml — same languages list, different current_language
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
      current_language: en  # or fa, zh-cn depending on the repo
```

### Pros & Cons

| Pros | Cons |
|------|------|
| Zero infrastructure setup | URLs include `quantecon.github.io` prefix |
| Each repo fully independent | No unified domain |
| No DNS changes needed | SEO authority split across domains |
| Works today with no changes | |

## Option 2: Subdomains (Upgraded)

Each language repo gets a custom subdomain.

### URLs

```text
https://python-programming.quantecon.org/        # English
https://fa.python-programming.quantecon.org/      # Persian
https://zh.python-programming.quantecon.org/      # Chinese
```

### Setup Steps

**1. Add DNS Records**

Create CNAME records pointing each subdomain to GitHub Pages:

```text
python-programming.quantecon.org      CNAME  quantecon.github.io
fa.python-programming.quantecon.org   CNAME  quantecon.github.io
zh.python-programming.quantecon.org   CNAME  quantecon.github.io
```

**2. Add CNAME Files**

Each repo needs a `CNAME` file in the branch deployed to GitHub Pages:

```text
# lecture-python-programming/CNAME
python-programming.quantecon.org

# lecture-python-programming.fa/CNAME
fa.python-programming.quantecon.org

# lecture-python-programming.zh-cn/CNAME
zh.python-programming.quantecon.org
```

**3. Enable HTTPS**

In each repo's Settings → Pages, enable "Enforce HTTPS". GitHub provisions
SSL certificates automatically for custom domains.

**4. Set `html_baseurl`**

```yaml
# lecture-python-programming.fa/_config.yml
html:
  baseurl: https://fa.python-programming.quantecon.org/
```

**5. Update Language Switcher URLs**

```yaml
languages:
  - code: en
    name: English
    url: https://python-programming.quantecon.org
  - code: fa
    name: فارسی
    url: https://fa.python-programming.quantecon.org
    rtl: true
  - code: zh-cn
    name: 中文
    url: https://zh.python-programming.quantecon.org
```

### Pros & Cons

| Pros | Cons |
|------|------|
| Clean, professional URLs | DNS configuration required per language |
| Each repo deploys independently | SSL certificate per subdomain (auto-provisioned) |
| No build coordination needed | Domain authority split across subdomains |
| Easy to add new languages | |

## Option 3: Reverse Proxy with Subdirectory URLs (Advanced)

Use a reverse proxy (e.g., Cloudflare Workers) to serve all languages under
a single domain with subdirectory URLs, while each repo continues to deploy
independently.

### URLs

```text
https://python-programming.quantecon.org/         # English
https://python-programming.quantecon.org/fa/       # Persian
https://python-programming.quantecon.org/zh-cn/    # Chinese
```

### How It Works

A reverse proxy sits between the user and GitHub Pages. When a request comes
in for `/fa/intro.html`, the proxy fetches it from the Persian site's origin
and serves it back under the main domain.

```text
User → python-programming.quantecon.org/fa/intro.html
  ↓
Cloudflare Worker (routes by path prefix)
  ↓
fa.python-programming.quantecon.org/intro.html (origin)
```

The user sees `python-programming.quantecon.org/fa/intro.html` in their
browser, but the content is actually served from the Persian site's GitHub
Pages deployment.

### Setup Steps

**Prerequisite:** Complete Option 2 first. The subdomains become backend
origins for the proxy.

**1. Set Up Cloudflare**

- Add the domain to Cloudflare (if not already using it for DNS).
- Create a Cloudflare Worker with the routing logic below.

**2. Cloudflare Worker**

```javascript
const ROUTES = {
  "/fa/": "https://fa.python-programming.quantecon.org",
  "/zh-cn/": "https://zh.python-programming.quantecon.org",
  "/": "https://python-programming.quantecon.org",
};

addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  for (const [prefix, origin] of Object.entries(ROUTES)) {
    if (prefix !== "/" && path.startsWith(prefix)) {
      const newPath = path.slice(prefix.length - 1);
      return fetch(origin + newPath + url.search, {
        headers: request.headers,
        method: request.method,
      });
    }
  }

  return fetch(ROUTES["/"] + path + url.search);
}
```

**3. Add Worker Route**

In Cloudflare → Workers → Routes, add:

```text
python-programming.quantecon.org/*  →  your-worker-name
```

**4. Update `html_baseurl`**

```yaml
# lecture-python-programming.fa/_config.yml
html:
  baseurl: https://python-programming.quantecon.org/fa/
```

**5. Update Language Switcher URLs**

```yaml
languages:
  - code: en
    name: English
    url: https://python-programming.quantecon.org
  - code: fa
    name: فارسی
    url: https://python-programming.quantecon.org/fa
    rtl: true
  - code: zh-cn
    name: 中文
    url: https://python-programming.quantecon.org/zh-cn
```

### Pros & Cons

| Pros | Cons |
|------|------|
| Single domain, clean `/fa/` URLs | Requires Cloudflare (free tier works) |
| Best for SEO (consolidated authority) | Additional infrastructure to maintain |
| Each repo still deploys independently | Slightly more complex debugging |
| CDN benefits (caching, DDoS protection) | |

## Upgrade Path

The options above form a natural progression. Work done at each stage is
preserved in the next:

```text
Option 1 (GitHub Pages)  →  Option 2 (Subdomains)  →  Option 3 (Reverse Proxy)
─────────────────────────────────────────────────────────────────────────────────
Theme config: update URLs    DNS + CNAME files        Cloudflare Worker + DNS
No infra changes             Simple DNS setup          Subdomains become origins
```

At each stage, the only theme-level change is updating the `url` values in
each repo's `_config.yml`. The theme code does not change.

## Adding a New Language

Regardless of which hosting option you use, the process is:

1. **Create the repository** — e.g., `lecture-python-programming.ja` for Japanese.
2. **Set up the translation workflow** — configure `action-translation` to sync from the source repo.
3. **Configure the site** — add `_config.yml` with `language`, `html_baseurl`, and `html_theme_options` (including `languages` list).
4. **Deploy to GitHub Pages** — set up CI/CD.
5. **Update all repos** — add the new language entry to the `languages` list in every repo's `_config.yml`.
6. **DNS/infra** (if using Option 2 or 3) — add DNS record and/or update the Cloudflare Worker.

### RTL Languages

For right-to-left languages (Arabic, Persian, Hebrew, Urdu, Pashto):

```yaml
sphinx:
  config:
    language: fa
    html_theme_options:
      enable_rtl: true
```

See the [RTL Support documentation](../RTL_SUPPORT.md) for details.

## Translation Sync Workflow

QuantEcon uses [action-translation](https://github.com/QuantEcon/action-translation)
to synchronize source content to translation repos via automated pull requests.

```text
Source repo (English)
  │
  ├─ push to main
  │
  ├──→ action-translation PR → lecture-python-programming.fa
  └──→ action-translation PR → lecture-python-programming.zh-cn
```

Translation teams review PRs, translate content, and merge. Each repo builds
and deploys independently after merge.

## Reference

- [GitHub Pages Custom Domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Cloudflare Workers](https://developers.cloudflare.com/workers/)
- [Google hreflang Guidelines](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [IETF Language Tags](https://www.w3.org/International/articles/language-tags/)
