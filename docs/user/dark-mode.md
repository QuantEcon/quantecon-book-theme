# Dark Mode

The theme includes a built-in dark mode that users can toggle via the sun/moon
icon in the toolbar.

```{contents}
:local:
:depth: 2
```

## How It Works

- **Toggle**: Users click the contrast button (sun icon) in the toolbar
- **Persistence**: The preference is saved in `localStorage` and applied on subsequent visits
- **No flash**: Dark mode is applied before the page renders (no FOUC)

## Color Palette

The dark mode uses a modern navy-charcoal palette designed for readability:

| Role | Color | Usage |
|------|-------|-------|
| Background | `#1a1a2e` | Page background |
| Surface | `#252540` | Sidebar, cards, admonitions |
| Surface Alt | `#2d2d4a` | Tooltips, hover states |
| Text | `#d4d4e4` | Primary body text |
| Muted Text | `#9898b0` | Secondary text, TOC links |
| Links | `#6cb6ff` | Hyperlinks |
| Link Hover | `#91cdff` | Hovered links |
| Link Visited | `#a08fff` | Previously visited links |
| Borders | `#3a3a5c` | Dividers, input borders |
| Code Background | `#1e1e32` | Code blocks, inputs |

## Syntax Highlighting

Code blocks use a VS Code Dark+ inspired palette:

| Token | Color | Example |
|-------|-------|---------|
| Keywords | `#c586c0` (purple) | `import`, `def`, `return` |
| Strings | `#ce9178` (warm orange) | `"hello"`, `'world'` |
| Numbers | `#b5cea8` (light green) | `42`, `3.14` |
| Functions | `#dcdcaa` (yellow) | `print()`, `len()` |
| Builtins/Classes | `#4ec9b0` (teal) | `list`, `dict`, `int` |
| Comments | `#7c8a9e` (muted blue-gray) | `# comment` |
| Variables | `#9cdcfe` (light blue) | `x`, `result` |
| Operators | `#d4d4e4` (text color) | `=`, `+`, `:` |

If you use a custom Pygments style (via `qetheme_code_style: False`), the dark
mode syntax colors are not applied and your Pygments configuration takes precedence.

## Admonitions

Admonitions automatically adapt with type-specific accent colors:

| Admonition Type | Accent Color |
|----------------|-------------|
| Note, See Also | Blue (`#6cb6ff`) |
| Warning, Caution, Attention | Amber (`#d4a017`) |
| Danger, Error | Red (`#e06060`) |
| Tip, Hint | Green (`#50b880`) |
| Important | Blue (`#6cb6ff`) |

## Image Handling

Images display with a subtle opacity reduction (88%) rather than color
inversion. Hovering over an image restores full brightness.

For projects with a dedicated dark mode logo, see the
[dark logo configuration](configuration.md).
When no dark logo is provided, the theme applies an inversion filter to the
site logo.

## Customizing Dark Mode Colors

Override CSS custom properties in a stylesheet in your `_static/` directory:

```css
/* _static/custom_dark.css */
body.dark-theme {
  --qe-dark-link: #58a6ff;
  --qe-dark-bg: #1e1e2e;
}
```

### Available custom properties

| Variable | Default | Description |
|----------|---------|-------------|
| `--qe-dark-bg` | `#1a1a2e` | Page background |
| `--qe-dark-surface` | `#252540` | Cards, sidebars, elevated surfaces |
| `--qe-dark-surface-alt` | `#2d2d4a` | Toolbar, inputs, alternate surfaces |
| `--qe-dark-border` | `#3a3a5c` | Borders |
| `--qe-dark-text` | `#d4d4e4` | Primary body text |
| `--qe-dark-text-muted` | `#9898b0` | Secondary/muted text |
| `--qe-dark-heading` | `#e8e8f0` | Heading text (h2–h5) |
| `--qe-dark-heading-top` | `#f0f0f8` | Top-level heading (h1) |
| `--qe-dark-text-light` | `#b8b8d0` | Light text (sidebar nav) |
| `--qe-dark-link` | `#6cb6ff` | Link color |
| `--qe-dark-link-hover` | `#91cdff` | Link hover color |
| `--qe-dark-link-visited` | `#a08fff` | Visited link color |
| `--qe-dark-code-bg` | `#1e1e32` | Code block background |
| `--qe-dark-inline-code` | `#e0b0ff` | Inline code text color |
| `--qe-dark-accent` | `#0072bc` | Primary accent (buttons) |
| `--qe-dark-accent-dark` | `#005a96` | Accent hover state |

```{note}
Dark mode works with all other theme features including the sticky TOC,
text color schemes (Seoul256, Gruvbox), and git-based metadata.
```
