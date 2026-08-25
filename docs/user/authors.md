# Authors and Translators

The theme renders author credits below the page title, and translated editions can
credit their translators in the same place.

```{contents}
:local:
:depth: 1
```

## Basic usage

Both options take a list of `{name, url}` entries. A translator without a `url`
renders as plain text; an author without one still renders as a link, as it always
has.

```python
html_theme_options = {
    "authors": [
        {"name": "Thomas J. Sargent", "url": "http://www.tomsargent.com/"},
        {"name": "John Stachurski", "url": "https://johnstachurski.net/"},
    ],
    "translators": [
        {"name": "Zhang San", "url": "https://example.org/zhang"},
    ],
}
```

For Jupyter Book projects:

```yaml
sphinx:
  config:
    html_theme_options:
      authors:
        - name: Thomas J. Sargent
          url: http://www.tomsargent.com/
      translators:
        - name: Zhang San
          url: https://example.org/zhang
```

Authors and translators are rendered as separate lines so the two are never
confused. Author links carry `rel="author"`, which tells crawlers who wrote the
page; translator links deliberately do not.

## Labels

Translators are introduced by a label, because an unlabelled second list of names
below the authors would be ambiguous. Authors have no label by default — the names
directly under the title already read as the authors.

| Option | Default | Purpose |
|--------|---------|---------|
| `translators_label` | `Translated by` | Introduces the translators line |
| `authors_label` | *(empty)* | Adds a label to the authors line when set |

Set `translators_label` to render the credit in the edition's own language:

```python
html_theme_options = {
    "translators_label": "译者",
}
```

Setting `authors_label` to an empty string (the default) omits the authors label
entirely, which is how every existing site renders today.

## Per-page overrides

A page can set its own `authors` and `translators` in front matter. This matters for
a translated edition produced by a team, where each lecture is the work of a
different translator: the project-level option carries the default credit, and each
page names whoever actually did that lecture.

```yaml
---
translators:
  - name: Li Si
    url: https://example.org/li
---
```

A page value **replaces** the project value rather than merging with it, so a page
that wants to credit both a coordinator and its own translator must list both.

| Front matter | Result on that page |
|--------------|---------------------|
| key absent | inherits the project-level value |
| `translators: []` | the block is left out on that page |
| `translators: [{name: …}]` | replaces the project value entirely |
| any other shape | ignored — inherits the project-level value |

An explicit empty list is the way to mark a page that has no translator yet — an
untranslated or machine-translated page in an otherwise translated edition should
not carry a human's name.

`authors_label` and `translators_label` can be overridden per page in the same way.

Overrides must use the list-of-mappings form shown above. `authors` in particular is
shared ground — docutils treats it as a bibliographic field and nbformat defines it
in the notebook schema — so a page may already carry an `authors` value written for
something else. A value this theme cannot read is left alone rather than rendered
badly or treated as suppression, and the project-level credit still shows.

Overrides are read from the source file's front matter, so they work in MyST
markdown and Jupyter notebooks. In a notebook the keys go in the notebook-level
`metadata`, which means a notebook that already sets nbformat's standard
`metadata.authors` is taken at its word. reStructuredText field lists cannot express
a list of mappings, so `.rst` pages always inherit the project-level value.

:::{note}
Quote any date-like value inside front matter (`since: "2020-01-01"`). An unquoted
YAML date anywhere in a page's front matter fails the build inside MyST, before the
theme sees it.
:::

## When nothing is configured

With no `translators` set, no translators block is rendered and the generated HTML
is unchanged from previous versions of the theme. This is fully backwards
compatible.

With no `authors` set, the theme falls back to printing Sphinx's own `author`
configuration value in the authors slot. A page that sets `authors: []` in its front
matter suppresses that fallback too, so the page shows no attribution at all.

## Limitations

Translators are shown on content pages but not on the landing page, where only the
authors line is moved up beneath the title. The list connector (`, ` and ` and `) is
English regardless of the configured language; only the labels are localisable.
