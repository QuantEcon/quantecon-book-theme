# Set up your development workflow

The following instructions will help you set up a basic development environment so that you can begin experimenting with changes.
This covers the basics, and see the other sections of the Contributing Guide for more details.

## Prerequisites

This project requires both **Python** and **Node.js** for full functionality:

- **Python 3.12 or newer** - For the Sphinx theme and testing
- **Node.js 18.18.0 or newer** - For compiling SCSS/JS assets with webpack

## Set up your development environment

First we'll install the necessary tools that you can use to begin making changes.
Follow these steps:

1. **Get the source code** using git:

   ```bash
   git clone https://github.com/QuantEcon/quantecon-book-theme
   cd quantecon-book-theme
   ```

2. **Install Python tools** (`tox` and `pre-commit`):

   ```console
   $ pip install tox pre-commit
   ```

3. **Install Node.js dependencies**:

   ```console
   $ npm install
   ```

   This installs webpack and other build tools needed for asset compilation.

4. **Install pre-commit hooks**:

   ```console
   $ pre-commit install
   ```

   This ensures code meets quality standards on every commit.

   :::{margin}
   You can manually run all `pre-commit` jobs:

   ```console
   $ pre-commit run --all-files
   ```
   :::

The rest of these instructions use `tox` to automate the installation and commands necessary to do many common things.

## Build the documentation

Now that you've installed the necessary tools, try building the documentation for this theme locally.
To do so, run the following `tox` command:

```console
$ tox -e docs-update
```

This will build the documentation using the latest version of the theme and put the outputs in `docs/_build/html`.
You may then preview them by opening one of the HTML files.

## Update the theme's assets (CSS/JS)

Now that you've previewed the documentation, try making changes to this theme's assets and see how they affect the documentation builds.
This is an easy way to preview the effect that your changes will make.

First, **make your changes in `src/quantecon_book_theme/assets/`**.
This folder contains all of the SCSS and JavaScript that are used in this site.

- **SCSS files** are in `assets/styles/` - organized into modular partials
- **JavaScript files** are in `assets/scripts/` - organized into feature modules

For example, edit one of the `.scss` files to add or modify a style rule.

Next, **compile the changes** using webpack:

```console
$ npm run build
```

This compiles SCSS to CSS and bundles JavaScript modules. The output goes to `src/quantecon_book_theme/theme/quantecon_book_theme/static/`.

:::{note}
You can also use `tox -e compile` which runs the [Sphinx Theme Builder](https://sphinx-theme-builder.readthedocs.io/), but `npm run build` is faster for quick iterations during development.
:::

Finally, **re-build the documentation** to preview your changes:

```console
$ rm -rf docs/_build/html
$ tox -e docs-update
```

When you open the HTML files for the documentation, your changes should be reflected.

## Auto-build the docs when you make changes

You can bundle both of the steps above into a single command, which also opens a live server that watches for changes to the theme's assets and documentation, and automatically compiles changes + re-builds the theme.

To do so, use this `tox` command:

```console
$ tox -e docs-live
```

This will do the following:

- Generate the theme's documentation (similar to running `tox -e docs-update`)
- Start a development server on an available port `127.0.0.1:xxxx`
- Open it in your default browser
- Watch for changes and automagically regenerate the documentation and auto-reload your browser when a change is made.

With this, you can modify the theme in an editor, and see how those modifications render on the browser.

## Run the tests

Once you've made a change to the theme, you should confirm that the tests still pass, and potentially add or modify a test for your changes.

To run the test suite, use `tox`:

```console
$ tox
```

This will run `pytest` against all of the files in `tests/` and display the result. Tests run against Python 3.12 and 3.13.

You can pass arguments to `pytest` like so:

```console
$ tox -- -k test_match
```

Anything passed after `--` will be passed directly to `pytest`.

:::{tip}
See the [Testing Guide](testing.md) for detailed information about test fixtures, what each test validates, and how to write new tests.
:::
