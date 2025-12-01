# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.11.0...HEAD
[0.11.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.10.1...v0.11.0
[0.10.1]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.3...v0.10.0
[0.9.3]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.2...v0.9.3
[0.9.2]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.1...v0.9.2
[0.9.1]: https://github.com/QuantEcon/quantecon-book-theme/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/QuantEcon/quantecon-book-theme/releases/tag/v0.9.0
