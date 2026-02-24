# Text Color Schemes

The theme applies colors to the `em` (emphasis) element, bold/strong, and definition list
terms using a built-in color scheme system.

```{contents}
:local:
:depth: 2
```

## Built-in Schemes

| Scheme | Description |
|---|---|
| `seoul256` (default) | Dark teal for emphasis, dark amber for strong — with matching light variants for dark mode |
| `gruvbox` | Earthy aqua for emphasis, warm orange for strong — with light variants for dark mode |
| `none` | Restores standard typography — italic for `em`, bold for `strong`, no color |

## Selecting a Scheme

In `conf.py`:

```python
html_theme_options = {
    ...
    "color_scheme": "seoul256",  # or "gruvbox" or "none"
    ...
}
```

For Jupyter Book projects:

```yaml
sphinx:
  config:
    html_theme_options:
      color_scheme: "seoul256"
```

## Seoul256 Colors

| Element | Light Mode | Dark Mode |
|---|---|---|
| **Emphasis** (`em`) | `#005f5f` dark teal | `#5fafaf` medium-light teal |
| **Bold/Strong** (`strong`, `b`) | `#875f00` dark amber | `#d7af5f` light amber-gold |
| **Definitions** (`dl dt`) | Inherits from bold/strong | Inherits from bold/strong |

```css
/* Seoul256 — Light Mode */
em       { color: #005f5f; }  /* dark teal */
strong   { color: #875f00; }  /* dark amber */
dl dt    { color: #875f00; }  /* inherits from strong */

/* Seoul256 — Dark Mode */
em       { color: #5fafaf; }  /* medium-light teal */
strong   { color: #d7af5f; }  /* light amber-gold */
dl dt    { color: #d7af5f; }  /* inherits from strong */
```

## Gruvbox Colors

| Element | Light Mode | Dark Mode |
|---|---|---|
| **Emphasis** (`em`) | `#427b58` earthy aqua | `#8ec07c` light aqua |
| **Bold/Strong** (`strong`, `b`) | `#af3a03` warm orange | `#fe8019` bright orange |
| **Definitions** (`dl dt`) | Inherits from bold/strong | Inherits from bold/strong |

```css
/* Gruvbox — Light Mode */
em       { color: #427b58; }  /* earthy aqua */
strong   { color: #af3a03; }  /* warm orange */
dl dt    { color: #af3a03; }  /* inherits from strong */

/* Gruvbox — Dark Mode */
em       { color: #8ec07c; }  /* light aqua */
strong   { color: #fe8019; }  /* bright orange */
dl dt    { color: #fe8019; }  /* inherits from strong */
```

## Custom Color Scheme

Place a `custom_color_scheme.css` file in your project's `_static/` directory.
The theme will automatically detect and include it:

```css
/* _static/custom_color_scheme.css */
:root {
  --qe-emphasis-color: #005f5f;
  --qe-strong-color: #875f00;
  --qe-definition-color: #875f00;
}
body.dark-theme {
  --qe-emphasis-color: #5fafaf;
  --qe-strong-color: #d7af5f;
  --qe-definition-color: #d7af5f;
}
```

```{note}
The `color_scheme` option is validated at build time. Invalid scheme names
fall back to `seoul256` with a warning. When using `custom_color_scheme.css`,
the base scheme still applies — your CSS overrides take precedence.
```
