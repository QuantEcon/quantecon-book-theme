# Contributing to QuantEcon Book Theme

Thank you for your interest in contributing to the QuantEcon Book Theme! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Node.js 18.18.0 or higher (see `.nvmrc`)
- Git

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/QuantEcon/quantecon-book-theme.git
cd quantecon-book-theme

# Install Node.js dependencies
npm install

# Install Python dependencies and development tools
pip install tox pre-commit

# Install pre-commit hooks
pre-commit install

# Build theme assets
npm run build

# Install theme in development mode
pip install -e .
```

### Building Documentation

```bash
# Build documentation once
tox -e docs-update

# Live reload development server (recommended for development)
tox -e docs-live
```

## Project Structure

```
quantecon-book-theme/
├── src/
│   └── quantecon_book_theme/
│       ├── __init__.py              # Main Python module
│       ├── launch.py                # Launcher utilities
│       ├── assets/                  # Source assets (SCSS, JS)
│       │   ├── scripts/             # JavaScript source
│       │   └── styles/              # SCSS source
│       └── theme/                   # Compiled theme
│           └── quantecon_book_theme/
│               ├── layout.html      # Main template
│               ├── theme.conf       # Theme configuration
│               └── static/          # Compiled CSS/JS
├── docs/                            # Documentation and examples
├── tests/                           # Test suite
├── webpack.config.js                # Webpack configuration
├── package.json                     # Node.js dependencies
└── pyproject.toml                   # Python package configuration
```

### Key Files

- **JavaScript Entry Point**: `src/quantecon_book_theme/assets/scripts/index.js`
- **SCSS Entry Point**: `src/quantecon_book_theme/assets/styles/index.scss`
- **Main Template**: `src/quantecon_book_theme/theme/quantecon_book_theme/layout.html`
- **Python Theme Module**: `src/quantecon_book_theme/__init__.py`

## Development Workflow

### Making Changes to Styles (SCSS)

1. Edit files in `src/quantecon_book_theme/assets/styles/`
2. Run `npm run build` to compile
3. Compiled CSS appears in `src/quantecon_book_theme/theme/quantecon_book_theme/static/styles/`
4. Test changes in documentation with `tox -e docs-live`

### Making Changes to JavaScript

1. Edit files in `src/quantecon_book_theme/assets/scripts/`
2. Run `npm run build` to compile
3. Compiled JS appears in `src/quantecon_book_theme/theme/quantecon_book_theme/static/scripts/`
4. Test changes in documentation with `tox -e docs-live`

### Making Changes to Templates

1. Edit `src/quantecon_book_theme/theme/quantecon_book_theme/layout.html`
2. Rebuild documentation to see changes: `tox -e docs-update`
3. Or use live reload: `tox -e docs-live`

### Making Changes to Python Code

1. Edit files in `src/quantecon_book_theme/`
2. Reinstall if needed: `pip install -e .`
3. Run tests: `tox`

## Code Style

### Python

- **Formatter**: Black
- **Linter**: Flake8
- **Line Length**: 88 characters (Black default)
- **Docstrings**: Google style

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input provided
    """
    pass
```

### JavaScript

- **Style**: ES6+ (const/let, arrow functions, template literals)
- **Linter**: ESLint (when configured)
- **Line Length**: 100 characters
- **Comments**: JSDoc style

```javascript
/**
 * Brief description of function
 * @param {string} param1 - Description
 * @param {number} param2 - Description
 * @returns {boolean} Description of return
 */
function exampleFunction(param1, param2) {
  // Implementation
}
```

### SCSS

- **Style**: Modern SCSS with @use/@forward
- **Linter**: Stylelint (when configured)
- **Naming**: BEM-inspired for classes
- **Nesting**: Maximum 3-4 levels

```scss
// Use modern @use instead of @import
@use "utilities/colors";

// BEM-style naming
.qe-component {
  &__element {
    property: value;
  }
  
  &--modifier {
    property: value;
  }
}
```

## Testing

### Running Tests

```bash
# Run full test suite (Python 3.12 and 3.13)
tox

# Run specific Python version
tox -e py312

# Run specific test file
pytest tests/test_build.py

# Run with coverage
pytest --cov=quantecon_book_theme
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test function names: `test_feature_behavior_expected_result`
- Use pytest fixtures for reusable test setup
- Include regression tests for bug fixes

Example test:
```python
def test_theme_loads_without_errors(test_app):
    """Test that theme initializes correctly."""
    app = test_app("basic")
    app.build()
    assert not app._warning.getvalue()
```

### Pre-commit Checks

Pre-commit hooks run automatically on `git commit`:
- Python formatting (Black)
- Python linting (Flake8)
- YAML/JSON validation
- Trailing whitespace removal

Run manually:
```bash
pre-commit run --all-files
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following code style guidelines

3. **Run tests**:
   ```bash
   tox
   ```

4. **Run pre-commit checks**:
   ```bash
   pre-commit run --all-files
   ```

5. **Build documentation** to verify visual changes:
   ```bash
   tox -e docs-update
   ```

6. **Commit your changes** with descriptive message:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

### Pull Request Guidelines

1. **Title**: Clear, descriptive title summarizing the change
2. **Description**: Explain what changed and why
3. **Testing**: Describe how you tested the changes
4. **Screenshots**: Include before/after screenshots for visual changes
5. **Breaking Changes**: Clearly document any breaking changes
6. **Documentation**: Update documentation if needed

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How were these changes tested?

## Screenshots
(If applicable)

## Checklist
- [ ] Tests pass locally
- [ ] Pre-commit checks pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Common Tasks

### Adding a New Feature

1. Plan the feature (discuss in issue if substantial)
2. Create feature branch
3. Implement feature with tests
4. Update documentation
5. Submit pull request

### Fixing a Bug

1. Create issue describing bug (if not already exists)
2. Create branch from issue
3. Write failing test reproducing bug
4. Fix bug
5. Verify test passes
6. Submit pull request referencing issue

### Updating Dependencies

```bash
# Node.js dependencies
npm outdated
npm update

# Python dependencies
# Edit pyproject.toml
pip install -e .
```

## Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: Search existing issues or create new one
- **Discussions**: Use GitHub Discussions for questions
- **Technical Review**: See `TECHNICAL_REVIEW.md` for architecture details

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions. We welcome contributors of all experience levels.

## License

By contributing, you agree that your contributions will be licensed under the BSD 3-Clause License.

## Questions?

If you have questions about contributing, please open a GitHub issue with the "question" label.
