# Implementation Plan - Technical Review

## Overview
This document provides a step-by-step implementation plan for the technical improvements identified in TECHNICAL_REVIEW.md. Each task includes specific commands and expected outcomes.

**Branch:** `technical-review-nov2025`  
**Date:** November 25, 2025

---

## Phase 1: Critical Updates (Week 1) 🔴

### Task 1.1: Update Node.js Dependencies
**Time estimate:** 2-3 hours  
**Risk:** Medium (requires testing)

```bash
# Backup current state
git add -A && git commit -m "Checkpoint before dependency updates"

# Update dependencies one major version at a time
npm install css-loader@^7.0.0 --save-dev
npm install css-minimizer-webpack-plugin@^7.0.0 --save-dev
npm install sass-loader@^16.0.0 --save-dev
npm install webpack@^5.103.0 --save-dev
npm install webpack-cli@^6.0.0 --save-dev

# Update minor versions
npm install sass@latest --save-dev
npm install html-webpack-plugin@latest --save-dev
npm install webpack-dev-server@latest --save-dev
npm install dedent@latest --save-dev

# Test build
npm run build

# If successful, commit
git add package.json package-lock.json
git commit -m "Update npm dependencies to latest versions"
```

**Testing checklist:**
- [ ] `npm run build` completes without errors
- [ ] CSS output looks correct
- [ ] JS output is properly minified
- [ ] Source maps are generated
- [ ] File sizes are reasonable

---

### Task 1.2: Bundle External CDN Dependencies
**Time estimate:** 3-4 hours  
**Risk:** Medium

```bash
# Install dependencies
npm install @popperjs/core@^2.11.8 --save-dev
npm install tippy.js@^6.3.7 --save-dev
npm install feather-icons@^4.29.1 --save-dev

# Test that packages are installed
npm list @popperjs/core tippy.js feather-icons
```

**Update JavaScript** - `src/quantecon_book_theme/assets/scripts/index.js`:
```javascript
// Add at top of file (after CSS import)
import Popper from '@popperjs/core';
import tippy from 'tippy.js';
import feather from 'feather-icons';

// Make globally available (for compatibility)
window.Popper = Popper;
window.tippy = tippy;
window.feather = feather;
```

**Update template** - `src/quantecon_book_theme/theme/quantecon_book_theme/layout.html`:
```html
<!-- REMOVE these lines (around line 4-6): -->
<!-- <script src="https://unpkg.com/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script> -->
<!-- <script src="https://unpkg.com/tippy.js@6.3.1/dist/tippy-bundle.umd.js"></script> -->
<!-- <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script> -->
```

**Testing checklist:**
- [ ] Build completes successfully
- [ ] Bundle size is reasonable (should be slightly larger)
- [ ] Tooltips work (tippy.js)
- [ ] Icons render (feather-icons)
- [ ] No console errors
- [ ] Test offline functionality

---

### Task 1.3: Update Python Dependencies
**Time estimate:** 1 hour  
**Risk:** Low

Update `pyproject.toml`:
```toml
[project]
requires-python = ">=3.12"
dependencies = [
  "pyyaml>=6.0,<7.0",
  "sphinx>=7,<9",
  "docutils>=0.20,<0.22",
  "click>=8.0,<9.0",
  "sphinx_book_theme~=1.1.4",
  "beautifulsoup4>=4.12,<5.0",
]
```

**Note:** libsass removed - now using Node.js sass package exclusively.

**Testing checklist:**
- [ ] `pip install -e .` works
- [ ] Theme builds correctly
- [ ] Documentation builds
- [ ] Run test suite: `tox`

---

### Task 1.4: Security Audit & Fixes
**Time estimate:** 1 hour  
**Risk:** Low

```bash
# Check for vulnerabilities
npm audit

# Fix automatically fixable issues
npm audit fix

# Review and manually fix remaining issues
npm audit fix --force  # Only if safe to do so

# Python security check
pip install safety
safety check

# Commit fixes
git add package.json package-lock.json
git commit -m "Fix security vulnerabilities"
```

**Testing checklist:**
- [ ] No high/critical vulnerabilities remain
- [ ] Application still functions correctly
- [ ] Tests pass

---

### Task 1.5: Add Linting Configuration
**Time estimate:** 2-3 hours  
**Risk:** Low

```bash
# Install linting tools
npm install eslint @eslint/js --save-dev
npm install stylelint stylelint-config-standard-scss --save-dev
npm install prettier --save-dev
```

**Create `.eslintrc.json`:**
```json
{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": ["eslint:recommended"],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  }
}
```

**Create `.stylelintrc.json`:**
```json
{
  "extends": ["stylelint-config-standard-scss"],
  "rules": {
    "max-nesting-depth": 4,
    "selector-class-pattern": null,
    "color-function-notation": "legacy",
    "alpha-value-notation": "number"
  }
}
```

**Create `.prettierrc.json`:**
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": false,
  "printWidth": 100,
  "tabWidth": 2
}
```

**Update `package.json` scripts:**
```json
{
  "scripts": {
    "build": "webpack",
    "lint": "npm run lint:js && npm run lint:css",
    "lint:js": "eslint 'src/**/*.js'",
    "lint:css": "stylelint 'src/**/*.scss'",
    "format": "prettier --write 'src/**/*.{js,scss,json}'",
    "format:check": "prettier --check 'src/**/*.{js,scss,json}'"
  }
}
```

**Update `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
  
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
  
  - repo: local
    hooks:
      - id: eslint
        name: eslint
        entry: npx eslint
        language: node
        types: [javascript]
        files: \.(js)$
      
      - id: prettier
        name: prettier
        entry: npx prettier --check
        language: node
        types_or: [javascript, scss, json]
        files: \.(js|scss|json)$
```

**Testing checklist:**
- [ ] `npm run lint` runs successfully
- [ ] Fix or document any linting errors
- [ ] `npm run format:check` passes
- [ ] Pre-commit hooks work

---

### Task 1.6: Quick Code Cleanup
**Time estimate:** 2-3 hours  
**Risk:** Low

**Remove console polyfill** from `src/quantecon_book_theme/assets/scripts/index.js`:
```javascript
// DELETE lines 8-44 (the console method polyfill)
// Modern browsers don't need this
```

**Fix webpack SASS output** in `webpack.config.js`:
```javascript
{
  loader: "sass-loader",
  options: {
    sassOptions: { 
      outputStyle: "compressed"  // Changed from "expanded"
    },
  },
}
```

**Remove commented code** from `src/quantecon_book_theme/assets/styles/index.scss`:
```scss
// DELETE lines 1973-2039 (commented collapse functionality)
// Keep in git history if needed
```

**Testing checklist:**
- [ ] Code still works without polyfill
- [ ] CSS is properly compressed
- [ ] No visual changes

---

## Phase 2: Code Organization (Week 2-3) 🟡

### Task 2.1: Refactor SCSS Structure
**Time estimate:** 8-10 hours  
**Risk:** Medium-High (visual testing required)

**Step 1: Create new directory structure**
```bash
cd src/quantecon_book_theme/assets/styles
mkdir -p base layout components themes utilities
```

**Step 2: Move existing partials**
```bash
# Move to appropriate directories
mv _colors.scss utilities/
mv _breakpoints.scss utilities/
mv _normalize.scss base/
mv _html5boilerplate.scss base/
mv _syntax.scss components/
mv _code.scss components/
mv _tippy-themes.scss components/
mv _margin.scss components/
mv _rtl.scss themes/
mv _dropdown.scss components/
```

**Step 3: Extract sections from index.scss**

Create new files and move content:

1. `base/_typography.scss` - fonts, headings, text styles
2. `base/_global.scss` - html, body, universal selectors
3. `layout/_toolbar.scss` - .qe-toolbar styles
4. `layout/_sidebar.scss` - .qe-sidebar styles
5. `layout/_page.scss` - .qe-page styles
6. `layout/_main.scss` - .qe-main, .qe-wrapper styles
7. `components/_buttons.scss` - button styles
8. `components/_tables.scss` - table styles
9. `components/_code-blocks.scss` - code block and collapse styles
10. `components/_admonitions.scss` - admonition styles
11. `components/_search.scss` - search form styles
12. `components/_modals.scss` - modal styles
13. `themes/_dark-theme.scss` - all .dark-theme styles

**Step 4: Create new index.scss**
```scss
/*
-----------------------------------
QuantEcon Book Theme - Main Stylesheet
-----------------------------------
*/

// Utilities (variables, functions, mixins)
@use "utilities/colors";
@use "utilities/breakpoints";

// Base styles (resets, typography, global)
@forward "base/normalize";
@forward "base/html5boilerplate";
@forward "base/global";
@forward "base/typography";

// Layout (structure, positioning)
@forward "layout/main";
@forward "layout/toolbar";
@forward "layout/sidebar";
@forward "layout/page";

// Components (reusable UI elements)
@forward "components/buttons";
@forward "components/tables";
@forward "components/code-blocks";
@forward "components/admonitions";
@forward "components/search";
@forward "components/modals";
@forward "components/syntax";
@forward "components/code";
@forward "components/tippy-themes";
@forward "components/margin";
@forward "components/dropdown";

// Themes (color schemes, variants)
@forward "themes/dark-theme";
@forward "themes/rtl";

// Google Fonts (consider moving to <link> in HTML)
@import url("https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,700;1,400&family=Source+Sans+Pro:ital,wght@0,400;0,700;1,400;1,700&display=swap");
```

**Step 5: Test thoroughly**
```bash
# Build
npm run build

# Visual testing checklist:
# - Test every page type
# - Test dark theme toggle
# - Test responsive breakpoints
# - Test RTL support
# - Compare with pre-refactor screenshots
```

**Testing checklist:**
- [ ] Build succeeds without errors
- [ ] Visual comparison shows no differences
- [ ] Dark theme works correctly
- [ ] All interactive elements function
- [ ] Responsive design works at all breakpoints

---

### Task 2.2: Modularize JavaScript
**Time estimate:** 6-8 hours  
**Risk:** Medium

**Step 1: Create module structure**
```bash
cd src/quantecon_book_theme/assets/scripts
mkdir -p modules utils
```

**Step 2: Create utility modules**

`utils/dom.js`:
```javascript
/**
 * Query selector shorthand
 */
export const $ = (selector, parent = document) => parent.querySelector(selector);
export const $$ = (selector, parent = document) => parent.querySelectorAll(selector);

/**
 * Wait for DOM to be ready
 */
export const onReady = (callback) => {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', callback);
  } else {
    callback();
  }
};
```

`utils/storage.js`:
```javascript
/**
 * Safe localStorage wrapper with error handling
 */
export const storage = {
  get(key, defaultValue = null) {
    try {
      const value = localStorage.getItem(key);
      return value !== null ? value : defaultValue;
    } catch (e) {
      console.warn('localStorage.getItem failed:', e);
      return defaultValue;
    }
  },
  
  set(key, value) {
    try {
      localStorage.setItem(key, value);
      return true;
    } catch (e) {
      console.warn('localStorage.setItem failed:', e);
      return false;
    }
  },
  
  getInt(key, defaultValue = 0) {
    return parseInt(this.get(key, defaultValue), 10);
  },
};
```

**Step 3: Extract feature modules**

Extract each major feature into its own module:
- `modules/theme-switcher.js` - dark/light theme toggle
- `modules/sidebar.js` - sidebar toggle and behavior
- `modules/toolbar.js` - toolbar initialization
- `modules/search.js` - search functionality
- `modules/font-sizer.js` - font size controls
- `modules/code-collapse.js` - collapsible code blocks
- `modules/launcher.js` - notebook launcher modal
- `modules/tooltips.js` - tippy.js initialization

**Step 4: Update index.js**
```javascript
import '../styles/index.scss';

// Import dependencies
import tippy from 'tippy.js';
import feather from 'feather-icons';

// Import utilities
import { onReady } from './utils/dom.js';

// Import feature modules
import { initThemeSwitcher } from './modules/theme-switcher.js';
import { initSidebar } from './modules/sidebar.js';
import { initToolbar } from './modules/toolbar.js';
import { initSearch } from './modules/search.js';
import { initFontSizer } from './modules/font-sizer.js';
import { initCodeCollapse } from './modules/code-collapse.js';
import { initLauncher } from './modules/launcher.js';
import { initTooltips } from './modules/tooltips.js';

// Make dependencies globally available
window.tippy = tippy;
window.feather = feather;

// Initialize when DOM is ready
onReady(() => {
  // Replace feather icon placeholders
  feather.replace();
  
  // Initialize features
  initThemeSwitcher();
  initSidebar();
  initToolbar();
  initSearch();
  initFontSizer();
  initCodeCollapse();
  initLauncher();
  initTooltips();
});
```

**Testing checklist:**
- [ ] All features work identically
- [ ] No console errors
- [ ] Bundle size is reasonable
- [ ] Code is more readable

---

### Task 2.3: Template Refactoring
**Time estimate:** 4-5 hours  
**Risk:** Medium

**Step 1: Create includes directory**
```bash
mkdir -p src/quantecon_book_theme/theme/quantecon_book_theme/includes
mkdir -p src/quantecon_book_theme/theme/quantecon_book_theme/includes/modals
```

**Step 2: Extract sections**

Create these include files:
- `includes/meta-tags.html` - SEO and social meta tags
- `includes/toolbar.html` - Toolbar markup
- `includes/sidebar.html` - Sidebar markup
- `includes/modals/settings-modal.html` - Launcher modal
- `includes/modals/download-modal.html` - Download PDF modal

**Step 3: Update layout.html**
```html
{%- extends "pydata_sphinx_theme/layout.html" %}

{% block extrahead %}
{% include "includes/meta-tags.html" %}
{% endblock %}

{# Main content block #}
{%- block content %}
  {% include "includes/toolbar.html" %}
  
  <div class="qe-wrapper">
    <div class="qe-main">
      {% include "includes/sidebar.html" %}
      
      <div class="qe-page">
        {# Page content #}
      </div>
    </div>
  </div>
  
  {% include "includes/modals/settings-modal.html" %}
  {% include "includes/modals/download-modal.html" %}
{%- endblock %}
```

**Testing checklist:**
- [ ] Theme renders correctly
- [ ] All includes are found
- [ ] No missing variables
- [ ] Modals work correctly

---

## Phase 3: Performance Optimization (Week 4) ⚡

### Task 3.1: Webpack Optimization
**Time estimate:** 3-4 hours  
**Risk:** Low

Update `webpack.config.js`:

```javascript
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  mode: "production",
  devtool: "source-map",
  
  entry: {
    "quantecon-book-theme": [
      "./src/quantecon_book_theme/assets/scripts/index.js",
    ],
  },
  
  output: {
    filename: "scripts/[name].js",
    path: staticPath,
    clean: true, // Clean output directory
  },
  
  optimization: {
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true, // Remove console.logs in production
          },
        },
      }),
      new CssMinimizerPlugin(),
    ],
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
        },
      },
    },
  },
  
  cache: {
    type: 'filesystem',
    buildDependencies: {
      config: [__filename],
    },
  },
  
  // ... rest of config
};
```

**Install Terser:**
```bash
npm install terser-webpack-plugin --save-dev
```

**Testing checklist:**
- [ ] Build time improves (measure before/after)
- [ ] Bundle sizes reduce
- [ ] Functionality intact

---

### Task 3.2: Font Loading Optimization
**Time estimate:** 2 hours  
**Risk:** Low

**Replace** `@import` in SCSS with `<link>` in template head:

In `layout.html`:
```html
{% block css %}
  <!-- Preconnect to Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  
  <!-- Load fonts with display=swap for better performance -->
  <link href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,700;1,400&family=Source+Sans+Pro:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
  
  {{ super() }}
{% endblock %}
```

Remove from `index.scss`:
```scss
// DELETE this line:
// @import url("https://fonts.googleapis.com/css2?family=PT+Serif...");
```

**Testing checklist:**
- [ ] Fonts load correctly
- [ ] No FOIT (flash of invisible text)
- [ ] Lighthouse score improves

---

## Phase 4: Testing & Documentation (Week 5) 📝

### Task 4.1: Add JavaScript Tests
**Time estimate:** 8-10 hours  
**Risk:** Low

```bash
# Install testing framework
npm install --save-dev vitest @vitest/ui jsdom
```

**Create test files:**
- `tests/javascript/utils/storage.test.js`
- `tests/javascript/utils/dom.test.js`
- `tests/javascript/modules/theme-switcher.test.js`

**Add to package.json:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

---

### Task 4.2: Add Documentation Files
**Time estimate:** 4-6 hours  
**Risk:** None

Create these files:
1. `CONTRIBUTING.md` - How to contribute
2. `ARCHITECTURE.md` - System architecture
3. `.editorconfig` - Editor configuration
4. `.nvmrc` - Node.js version
5. Update `README.md` with badges and links

---

## Quick Wins Checklist ✅

These can be done immediately (1-2 hours total):

```bash
# 1. Add .nvmrc
echo "18.18.0" > .nvmrc

# 2. Add .editorconfig
cat > .editorconfig << 'EOF'
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
EOF

# 3. Run npm audit fix
npm audit fix

# 4. Update webpack sass output
# (manually edit webpack.config.js as shown above)

# 5. Remove console polyfill
# (manually edit index.js as shown above)

# Commit all quick wins
git add .
git commit -m "Quick wins: Add .nvmrc, .editorconfig, fix security issues, optimize webpack"
```

---

## Progress Tracking

Use this checklist to track progress:

**Phase 1: Critical Updates**
- [ ] Task 1.1: Update Node.js dependencies
- [ ] Task 1.2: Bundle CDN dependencies
- [ ] Task 1.3: Update Python dependencies
- [ ] Task 1.4: Security audit
- [ ] Task 1.5: Add linting
- [ ] Task 1.6: Code cleanup

**Phase 2: Code Organization**
- [ ] Task 2.1: Refactor SCSS
- [ ] Task 2.2: Modularize JavaScript
- [ ] Task 2.3: Template refactoring

**Phase 3: Performance**
- [ ] Task 3.1: Webpack optimization
- [ ] Task 3.2: Font loading optimization

**Phase 4: Testing & Docs**
- [ ] Task 4.1: JavaScript tests
- [ ] Task 4.2: Documentation

---

## Success Metrics

Track these metrics before and after each phase:

```bash
# Bundle sizes
ls -lh src/quantecon_book_theme/theme/quantecon_book_theme/static/scripts/
ls -lh src/quantecon_book_theme/theme/quantecon_book_theme/static/styles/

# Build time
time npm run build

# Test coverage
npm run test:coverage

# Lighthouse score
# Run on built documentation
```

**Target Improvements:**
- Build time: -30%
- Bundle size: -20%
- Test coverage: 80%+
- Lighthouse: 90+

---

## Support & Questions

If you encounter issues:
1. Check TECHNICAL_REVIEW.md for context
2. Review error messages carefully
3. Test incrementally
4. Commit working states frequently
5. Document any deviations from this plan
