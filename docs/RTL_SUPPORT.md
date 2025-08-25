# RTL (Right-to-Left) Script Support

The QuantEcon Book Theme now supports RTL (Right-to-Left) scripts including Arabic, Hebrew, Persian, and other RTL languages.

## Usage

To enable RTL support in your Sphinx configuration, add the following to your `conf.py`:

```python
html_theme = "quantecon_book_theme"

html_theme_options = {
    "enable_rtl": True,  # Enable RTL support
    # ... other theme options
}
```

## Configuration

- **Option**: `enable_rtl`
- **Type**: Boolean
- **Default**: `False`
- **Description**: When set to `True`, enables right-to-left text direction and adjusts the entire layout for RTL languages.

## Features

When RTL mode is enabled, the theme automatically adjusts:

### Layout Changes
- **Text Direction**: All text flows from right to left
- **Sidebar Position**: Moves from left to right side
- **Navigation**: Toolbar elements are reversed for RTL flow
- **Margins and Padding**: Adjusted for RTL reading patterns
- **Blockquotes**: Border appears on the right side instead of left

### Preserved Elements
For optimal readability, these elements remain in LTR (Left-to-Right) direction:
- **Code blocks** and syntax highlighting
- **Mathematical equations** and formulas
- **URLs** and technical content

## Example

```python
# conf.py for an Arabic documentation site
project = "دليل البرمجة"
language = "ar"  # Arabic language code

html_theme = "quantecon_book_theme"
html_theme_options = {
    "enable_rtl": True,
    "repository_url": "https://github.com/your-repo/arabic-docs",
    # ... other options
}
```

## Supported Languages

This RTL implementation supports all RTL scripts including:
- **Arabic** (العربية)
- **Hebrew** (עברית)
- **Persian/Farsi** (فارسی)
- **Urdu** (اردو)
- **Pashto** (پښتو)
- And other RTL writing systems

## Testing

You can test the RTL functionality by:

1. Setting `enable_rtl = True` in your theme options
2. Building your Sphinx documentation
3. Viewing the generated HTML to see the RTL layout adjustments

The theme includes comprehensive test files demonstrating both LTR and RTL modes side by side.

## Implementation Details

- RTL styles are implemented using CSS `[dir="rtl"]` selectors
- The `dir="rtl"` attribute is conditionally added to the `<body>` element
- Layout adjustments use CSS flexbox and positioning for proper RTL flow
- All changes are backward compatible with existing LTR documents
