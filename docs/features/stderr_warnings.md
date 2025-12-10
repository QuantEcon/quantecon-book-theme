# Collapsible Stderr Warnings Feature

## Overview

The QuantEcon Book Theme now includes automatic detection and collapsing of stderr output in Jupyter notebook cells. This feature helps improve the reading experience when code produces verbose warnings from upstream packages.

## How It Works

When a notebook cell produces stderr output (typically warnings), the theme automatically:

1. Detects the stderr output in the cell
2. Wraps it in a collapsible interface
3. Displays a compact "⚠ Code warnings" button
4. Allows readers to expand/collapse the warnings as needed

## Example

Here's what a cell with stderr output looks like:

### Before (stderr visible by default):
```
model = create_js_with_sep_model()
...

W1123 10:15:26.780179   23830 cuda_executor.cc:1802] GPU interconnect information not available: INTERNAL: NVML doesn't support extracting fabric info or NVLink is not used by the device.
W1123 10:15:26.783637   23767 cuda_executor.cc:1802] GPU interconnect information not available: INTERNAL: NVML doesn't support extracting fabric info or NVLink is not used by the device.
```

### After (with collapsible feature):
```
model = create_js_with_sep_model()
...

[⚠ Code warnings ▶]  (click to expand)
```

## Benefits

- **Cleaner presentation**: Verbose warnings don't disrupt the reading flow
- **Information preserved**: Warnings are still accessible when needed
- **Automatic**: No manual tagging or configuration required
- **User control**: Readers can choose to view warnings when troubleshooting

## Implementation Details

The feature is implemented using:

- **JavaScript**: Automatically detects `.cell_output` elements containing `.output.stderr`
- **CSS**: Styled with yellow/amber colors to indicate warnings
- **Accessibility**: Includes ARIA attributes for screen readers

## Technical Notes

- The feature runs on page load via `DOMContentLoaded` event
- Works with any number of stderr outputs per cell
- Compatible with dark theme
- No configuration needed - works automatically

## Testing

To test the feature, create a Jupyter notebook with code that produces stderr warnings, build it with Jupyter Book using this theme, and verify that:

1. Stderr outputs show the collapsible "⚠ Warnings" button
2. Clicking the button expands/collapses the warnings
3. The styling matches the theme
4. Regular (non-stderr) outputs display normally

## Customization

The feature can be customized via CSS by targeting these classes:

- `.stderr-collapsible-wrapper` - The outer container
- `.stderr-toggle-button` - The clickable button
- `.stderr-content` - The expandable content area
- `.stderr-icon` - The warning icon
- `.stderr-label` - The "Warnings" text
- `.stderr-chevron` - The expand/collapse indicator
