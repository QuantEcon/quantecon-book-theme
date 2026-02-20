# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Complete dark theme overhaul** (#365) — rewrote the dark theme for a modern, consistent, and readable experience
  - Replaced ad-hoc grays (`#222`/`#333`/`#444`) with a cohesive navy-charcoal palette (`#1a1a2e` background, `#252540` surfaces, `#d4d4e4` text, `#6cb6ff` links)
  - Images now use subtle opacity reduction instead of aggressive CSS inversion
- **CSS custom properties for dark theme** (#365) — all 16 palette colors declared as overridable `--qe-dark-*` custom properties; downstream projects can now customize colors without duplicating selectors

### Added
- **Dark mode syntax highlighting** (#365) — complete token colors for all ~40 Pygments syntax classes using a VS Code Dark+ inspired palette
- **FOUC prevention** (#365) — early inline script applies dark mode class before first paint, eliminating the flash of white on page load
- **Dark mode documentation** (#365) — new "Dark Mode" section in `configure.md` covering palette, syntax highlighting, admonitions, image handling, and CSS customization with full reference table of all overridable custom properties
- **Dark mode coverage for unstyled elements** (#365) — modals, admonitions (type-specific accents), homepage elements, collapse/toggle bars, tooltips, autodoc, footnotes, and non-QuantEcon project overrides

### Fixed
- **Double logo in dark theme** (#365) — when a dedicated dark logo is configured, both light and dark logos were shown; fixed `:only-child` selector to check the `<a>` wrapper instead of the `<img>`
- **Page header unreadable in dark mode** (#365) — title link, authors, "Last changed" button, and changelog dropdown used `#444` text on dark backgrounds
- **Unreadable table text in dark mode** (#365) — table rows used `#333` text on dark backgrounds
- **Indistinguishable links in dark mode** (#365) — all links were `#fff`, same as body text
- **Inline code light border in dark mode** (#365) — code spans retained light-theme borders
- **Sidebar search white in dark mode** (#365) — search input area remained white
- **Toolbar border in dark mode** (#365) — toolbar border remained light gray
- **Syntax highlighting gaps** (#365) — only 3 of ~40 token types had dark mode overrides
- **Stderr warnings in dark mode** (#365) — updated to use amber accents matching the new palette

## [0.17.1] - 2026-02-19

### Fixed
- **Horizontal scrollbar on sticky TOC** (#363) — added `overflow-x: hidden` to the sticky "On this page" sidebar to prevent an unwanted horizontal scrollbar when long section titles wrap
- **npm security vulnerabilities** (#364) — resolved 9 dependency vulnerabilities (5 high, 3 moderate, 1 low) via `npm audit fix`, updating webpack, node-forge, qs, lodash, cross-spawn, ajv, and nanoid

## [0.17.0] - 2026-02-19

### Breaking Changes
- **Removed individual color options** — the following `html_theme_options` have been removed:
  `emphasis_color`, `emphasis_color_dark`, `strong_color`, `strong_color_dark`, `definition_color`, `definition_color_dark`.
  These are replaced by the new `color_scheme` option (see Changed below). Projects using the old options should migrate to either the built-in `seoul256` scheme or a `custom_color_scheme.css` file.

### Added
- **Sticky table of contents with scroll highlighting** (#350, #133)
  - New `sticky_contents` option enables a fixed-position RHS TOC that tracks scroll position
  - Scroll spy highlights the currently visible section in the TOC
  - Auto-expand subsections show the active hierarchy (configurable via `contents_autoexpand`)
  - Copy section link: hover over any TOC entry to copy the full URL with anchor
  - Back to top button appears after scrolling down 300px
  - New `scrollspy.js` module with `requestAnimationFrame` throttling
  - Full documentation in `docs/configure.md`
- **CI: `/update-snapshots` command** (#362)
  - PR comment command to regenerate all Playwright visual baselines

### Changed
- **Text color scheme system** (#360) — replaces individual color options with scheme-based approach
  - New `color_scheme` theme option (`seoul256` default, `gruvbox`, `none` to disable)
  - Seoul256-inspired palette: dark teal (`#005f5f`) for emphasis, dark amber (`#875f00`) for strong (light mode); medium-light teal (`#5fafaf`) and light amber-gold (`#d7af5f`) for dark mode
  - Gruvbox palette: earthy aqua (`#427b58`) for emphasis, warm orange (`#af3a03`) for strong (light mode); light aqua (`#8ec07c`) and bright orange (`#fe8019`) for dark mode
  - Custom override via `custom_color_scheme.css` in project `_static/` (auto-detected)
  - New `_color-schemes.scss` module for built-in scheme definitions

### Fixed
- **Math equation visual test stability** (#361)
  - Regenerated stale snapshots for consistent cross-environment rendering
  - Increased tolerance with `maxDiffPixelRatio: 0.15` for MathJax font variance

## [0.16.0] - 2026-02-06

### Added
- **Customizable emphasis and bold text colors** (#355, #356)
  - Six new `html_theme_options`: `emphasis_color`, `emphasis_color_dark`, `strong_color`, `strong_color_dark`, `definition_color`, `definition_color_dark`
  - Allows per-site color customization of italic (`<em>`), bold (`<strong>`/`<b>`), and definition list (`<dt>`) elements
  - Supports light and dark mode independently
  - CSS custom properties (`--qe-emphasis-color`, `--qe-strong-color`, `--qe-definition-color`) with SCSS fallbacks
  - Server-side validation of color values to prevent CSS injection
  - Comprehensive documentation in `docs/configure.md` with examples

### Fixed
- **Math equation visual test stability** (#357)
  - Replaced fixed 1000ms timeout with `MathJax.startup.promise` for reliable math rendering detection
  - Captures paragraph container instead of tiny MathJax element to avoid dimension mismatches
- **Update-snapshots workflow** (#357)
  - Added `continue-on-error: true` to handle missing snapshot exit codes gracefully

### Changed
- **Dependency updates** (Dependabot)
  - Bump codecov/codecov-action from 5.5.1 to 5.5.2 (#351)
  - Bump actions/upload-artifact from 5 to 6 (#352)

## [0.15.1] - 2025-12-11

### Fixed
- **Notebook launch URLs with `path_to_docs`** (#345)
  - Fixed bug where `path_to_docs` prefix was incorrectly included in notebook URLs
  - When docs are in a subdirectory (e.g., `lectures/`) but notebooks are in a flat repo structure, launch buttons (Colab, JupyterHub, Binder) now generate correct URLs
  - Added comprehensive test coverage including backward compatibility tests
- **Visual regression test stability** (#350)
  - Fixed flaky MathJax visual regression test by using `maxDiffPixels` instead of `maxDiffPixelRatio`
  - Handles minor rendering variations across different environments

### Changed
- **Dependency updates** (Dependabot)
  - Bump actions/github-script from 7 to 8 (#348)
  - Bump actions/upload-artifact from 4 to 5 (#347)
  - Bump actions/setup-node from 4 to 6 (#346)

## [0.15.0] - 2025-12-08

### Changed
- **Major refactoring and modernization** (#335)
  - Updated Node.js from 16.13.2 (EOL) to 18.18.0 LTS
  - Modularized SCSS: Split 2038-line monolithic stylesheet into 11 focused modules
  - Modularized JavaScript: Organized 565 lines into 8 feature-specific modules
  - Updated npm dependencies: sass (1.94.2), sass-loader (16.0.6), css-loader (7.1.2), webpack (5.103.0), and more
  - Updated Python dependencies: Added version constraints for pyyaml, docutils, beautifulsoup4
  - Updated flake8 constraint from <3.8.0 to >=7.0.0
  - Removed unused `click` dependency

### Added
- Performance optimizations (#335)
  - Preconnect hints for CDN resources (unpkg.com, cdn.jsdelivr.net, fonts.googleapis.com)
  - Reduces connection time by 100-300ms per CDN
- Security improvements (#335)
  - Fixed 2 npm vulnerabilities (cross-spawn HIGH severity, nanoid MODERATE severity)
  - Added SRI (Subresource Integrity) hashes to all CDN-loaded scripts
- Testing improvements (#335)
  - New test infrastructure with conftest.py and shared fixtures
  - Added test_module_structure.py with 10 new tests (13→23 total tests)
  - Validates SCSS module structure, JavaScript module exports, layout template configuration
- Documentation improvements (#335)
  - Comprehensive CONTRIBUTING.md with development guide
  - New testing guide at docs/contributing/testing.md
  - AI-assisted development guide at .github/copilot-instructions.md
  - Added .editorconfig for consistent code formatting
  - Added .nvmrc for Node.js version pinning

### Fixed
- Deprecation warnings (#335)
  - Fixed deprecated `datetime.utcnow()` → `datetime.now(timezone.utc)`
  - Fixed deprecated `datetime.utcfromtimestamp()` → `datetime.fromtimestamp(..., tz=timezone.utc)`
  - All 19 deprecation warnings resolved
- Removed obsolete console polyfill for IE8/9 (#335)
  - Reduces JavaScript bundle size from 8.91 KiB to 8.73 KiB

## [0.14.0] - 2025-12-01

### Added
- Visual regression testing with Playwright (#339)
  - Automated screenshot comparison for theme styling
  - Tests for code blocks, dark mode, math equations, headers, sidebars
  - Desktop and mobile viewport coverage
  - CI integration with GitHub Actions
- New `/update-new-snapshots` PR comment command (#340)
  - Automatically generates baseline snapshots for new visual tests
  - Only creates missing snapshots (won't overwrite existing baselines)
  - Documents workflow in tests/visual/README.md

### Fixed
- Removed italic formatting from f-string interpolation tokens (#324, #329)
  - F-string placeholders like `{variable}` now render in consistent monospace
  - Improves code readability by matching terminal/REPL output style

## [0.13.2] - 2025-11-25

### Fixed
- Updated Jupyter Book links to avoid redirects (#337)
  - Footer "Powered by Jupyter Book" link now points directly to jupyterbook.org/v1/
  - Eliminates redirect warnings in lecture linkcheckers

## [0.13.1] - 2025-11-25

### Fixed
- Colab launch button now correctly generates URLs for flat notebook repositories (#336)
  - Added `nb_path_to_notebooks` configuration option to specify notebook path independently from `path_to_docs`
  - Defaults to empty string for flat repositories, fixing incorrect URL generation

## [0.13.0] - 2024-11-24

### Added
- Collapsible stderr warnings feature (#333)
  - Automatically detects and wraps stderr output in notebook cells with a collapsible interface
  - Displays a compact "⚠ Code warnings" button for cleaner presentation
  - Improves readability when code produces verbose warnings from upstream packages
  - Includes dark theme support and accessibility features (ARIA labels)
  - Works seamlessly with myst-nb's `merge_streams` configuration option

## [0.12.0] - 2025-11-23

### Added
- Git-based metadata integration for lecture pages (#328, #331)
  - Last modified timestamp displayed below authors
  - Interactive changelog dropdown showing last 10 commits (configurable)
  - Clickable commit hashes linking to GitHub commit pages
  - Full commit history link for each document
  - Configuration options: `last_modified_date_format` and `changelog_max_entries`

### Changed
- Improved lecture header layout (#328, #331)
  - Removed redundant title display from page headers
  - Increased lecture series heading font size by 44%
  - Increased author names font size by 20%
  - Repositioned metadata elements for better visual hierarchy

## [0.11.0] - 2025-11-20

### Added
- Color-based emphasis system for `<em>` and `<strong>` tags (#327)
  - `<em>` tags now render with distinctive color emphasis instead of italics
  - `<strong>` tags render with both color emphasis and bold weight
  - New SCSS color variables for consistent emphasis styling

### Changed
- Visual treatment of emphasized text now uses color rather than italics for improved readability

## [0.10.1] - 2024-XX-XX

### Fixed
- Customized toggle button text to display 'Show'/'Hide' instead of default text (#322)

## [0.10.0] - 2024-XX-XX

### Added
- Optional custom code style feature (#319)
  - Users can now choose between custom QuantEcon syntax highlighting styles or Pygments built-in themes
  - Configuration option `quantecon_book_theme_code_style` in `conf.py`

## [0.9.3] - 2024-XX-XX

### Fixed
- Collapse functionality bugs: CSS selectors, height parsing, and toggle bar creation (#300)

### Changed
- Increased page max-width to accommodate 80-character code lines (#309)

## [0.9.2] - 2024-XX-XX

### Fixed
- Reference error in index.js (#311)

### Changed
- Fixed coverage warnings in RTL functionality tests (#313)

## [0.9.1] - 2024-XX-XX

### Changed
- Updated Jupyter Book footer link to reduce redirects (#303)

## [0.9.0] - 2024-XX-XX

### Added
- Initial stable release with core theme features

[Unreleased]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.17.0...HEAD
[0.17.1]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.17.0...v0.17.1
[0.17.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.15.1...v0.16.0
[0.15.1]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.15.0...v0.15.1
[0.15.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.13.2...v0.14.0
[0.13.2]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.13.1...v0.13.2
[0.13.1]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.10.1...v0.11.0
[0.10.1]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.3...v0.10.0
[0.9.3]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.2...v0.9.3
[0.9.2]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.1...v0.9.2
[0.9.1]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/QuantEcon/quantecon-book-theme/releases/tag/v0.9.0
