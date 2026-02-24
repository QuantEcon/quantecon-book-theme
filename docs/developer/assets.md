# Asset Compilation

The theme's CSS and JavaScript are compiled from source files in
`src/quantecon_book_theme/assets/` using webpack.

```{contents}
:local:
:depth: 2
```

## Quick Reference

```bash
# Compile SCSS and JS
npm run build

# Install webpack and dependencies
npm install
```

## Workflow

1. **Edit source files** in `src/quantecon_book_theme/assets/`
   - SCSS files in `assets/styles/`
   - JavaScript files in `assets/scripts/`

2. **Compile** with webpack:

   ```console
   $ npm run build
   ```

   Output goes to `src/quantecon_book_theme/theme/quantecon_book_theme/static/`.

3. **Preview** by rebuilding the docs:

   ```console
   $ rm -rf docs/_build/html
   $ tox -e docs-update
   ```

   Or use the live-reload server:

   ```console
   $ tox -e docs-live
   ```

:::{note}
You can also use `tox -e compile` which runs the
[Sphinx Theme Builder](https://sphinx-theme-builder.readthedocs.io/), but
`npm run build` is faster for quick iterations.
:::

## Build Dependencies

Defined in `package.json`:

| Package | Purpose |
|---------|---------|
| `webpack` + `webpack-cli` | Module bundler |
| `sass` + `sass-loader` | SCSS compilation |
| `css-loader` | CSS processing |
| `css-minimizer-webpack-plugin` | CSS minification |

## SCSS Architecture

The entry point is `assets/styles/index.scss`. It uses `@forward` to include
all modules. See [Architecture — SCSS Modules](architecture.md)
for the full module list.

When adding a new SCSS module:
1. Create `_my-module.scss` in `assets/styles/`
2. Add `@forward "my-module";` to `index.scss`
3. Run `npm run build`
4. Update the test in `test_module_structure.py`

## JavaScript Architecture

The entry point is `assets/scripts/index.js`. It imports all feature modules.
See [Architecture — JavaScript Modules](architecture.md)
for the full module list.

When adding a new JS module:
1. Create `my-feature.js` in `assets/scripts/`
2. Export an `initMyFeature` function
3. Import and call it from `index.js`
4. Run `npm run build`
5. Update the test in `test_module_structure.py`
