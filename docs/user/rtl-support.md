# RTL (Right-to-Left) Support

The theme supports RTL scripts including Arabic, Hebrew, Persian, and other
right-to-left languages.

```{contents}
:local:
:depth: 2
```

## Enabling RTL

Add the following to your `conf.py`:

```python
html_theme = "quantecon_book_theme"

html_theme_options = {
    "enable_rtl": True,
}
```

## Configuration

- **Option**: `enable_rtl`
- **Type**: Boolean
- **Default**: `False`

## Layout Changes

When RTL mode is enabled, the theme automatically adjusts:

- **Text direction** — all text flows right-to-left
- **Sidebar position** — moves from left to right side
- **Navigation** — toolbar elements are reversed for RTL flow
- **Margins and padding** — adjusted for RTL reading patterns
- **Blockquotes** — border appears on the right side

### Preserved elements

For optimal readability, these remain in LTR direction:

- **Code blocks** and syntax highlighting
- **Mathematical equations** and formulas
- **URLs** and technical content

## Example

```python
# conf.py for an Arabic documentation site
project = "دليل البرمجة"
language = "ar"

html_theme = "quantecon_book_theme"
html_theme_options = {
    "enable_rtl": True,
    "repository_url": "https://github.com/your-repo/arabic-docs",
}
```

## Supported Languages

- **Arabic** (العربية)
- **Hebrew** (עברית)
- **Persian/Farsi** (فارسی)
- **Urdu** (اردو)
- **Pashto** (پښتو)
- And other RTL writing systems

## Implementation

- RTL styles use CSS `[dir="rtl"]` selectors
- The `dir="rtl"` attribute is conditionally added to `<body>`
- Layout adjustments use CSS flexbox and positioning
- All changes are backward compatible with existing LTR documents
