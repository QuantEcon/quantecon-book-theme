# Announcement Banner

Display a dismissible announcement at the top of every page — useful for
site-wide notices such as a software upgrade, a link to changelog notes, or a
scheduled maintenance window.

```{contents}
:local:
:depth: 1
```

## Basic usage

Set the `announcement` option in `html_theme_options`. The value is an HTML
string, so you can include emphasis and a link:

```yaml
sphinx:
  config:
    html_theme_options:
      announcement: 'We upgraded to <strong>Anaconda 2026.06</strong> — see the <a href="/status.html">CHANGELOG</a>.'
```

For a `conf.py` project:

```python
html_theme_options = {
    "announcement": 'We upgraded to <strong>Anaconda 2026.06</strong> — see the <a href="/status.html">CHANGELOG</a>.',
}
```

Leave the option empty (the default) and no banner is shown.

## Dismissal

Readers can dismiss the banner with the `×` button. The dismissal is remembered
in the browser's `localStorage`, so it stays hidden on future visits.

Dismissal is keyed to the **content of the message**. When you change the
`announcement` text, the banner re-appears for everyone — including readers who
dismissed the previous message. This means you can reuse the banner for a new
notice without worrying that people who dismissed the last one will miss it.

## Expiry date

Add an optional `announcement_expires` date (ISO `YYYY-MM-DD`) to have the
banner disappear automatically. The banner shows **through the end of** that
day, in the reader's local timezone:

```yaml
sphinx:
  config:
    html_theme_options:
      announcement: 'We upgraded to <strong>Anaconda 2026.06</strong> — see the <a href="/status.html">CHANGELOG</a>.'
      announcement_expires: "2026-07-01"
```

The expiry is enforced two ways, so it works whether or not the site is rebuilt:

- **In the reader's browser** — the banner hides itself once the date passes,
  even if the published site has not been rebuilt since.
- **At build time** — if the date has already passed when the site is built, the
  banner is omitted from the generated HTML entirely.

If `announcement_expires` is not a valid `YYYY-MM-DD` date, the build logs a
warning and ignores the expiry (the banner keeps showing) — a typo will never
silently hide an active announcement.

## Per-page announcements

Per-page announcements (for example, flagging that a single lecture now uses a
newer library version) are not yet supported. Progress is tracked in
[issue #403](https://github.com/QuantEcon/quantecon-book-theme/issues/403); the
banner is built to accept per-page notices additively, so this can be added
without changing how the site-wide `announcement` option works.
