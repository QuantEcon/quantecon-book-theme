# Collapsible Stderr Warnings

The theme automatically detects and collapses stderr output in Jupyter notebook
cells, improving the reading experience when code produces verbose warnings.

```{contents}
:local:
:depth: 2
```

## How It Works

When a notebook cell produces stderr output (typically warnings), the theme:

1. Detects the stderr output in the cell
2. Wraps it in a collapsible interface
3. Displays a compact "⚠ Code warnings" button
4. Allows readers to expand/collapse the warnings

## Example

### Before (stderr visible by default)
```
model = create_js_with_sep_model()
...

W1123 10:15:26.780179   23830 cuda_executor.cc:1802] GPU interconnect information not available...
W1123 10:15:26.783637   23767 cuda_executor.cc:1802] GPU interconnect information not available...
```

### After (with collapsible feature)
```
model = create_js_with_sep_model()
...

[⚠ Code warnings ▶]  (click to expand)
```

## Benefits

- **Cleaner presentation** — verbose warnings don't disrupt reading flow
- **Information preserved** — warnings remain accessible when needed
- **Automatic** — no manual tagging or configuration required
- **User control** — readers can view warnings when troubleshooting

## Technical Details

- Runs on page load via `DOMContentLoaded` event
- Works with any number of stderr outputs per cell
- Compatible with dark mode
- Includes ARIA attributes for screen readers

## CSS Customization

Target these classes to customize the appearance:

- `.stderr-collapsible-wrapper` — the outer container
- `.stderr-toggle-button` — the clickable button
- `.stderr-content` — the expandable content area
- `.stderr-icon` — the warning icon
- `.stderr-label` — the "Warnings" text
- `.stderr-chevron` — the expand/collapse indicator
