# QuantEcon Book Theme

QuantEcon Book Theme is a Sphinx theme specifically designed for Jupyter Book projects. It combines Python packaging with Node.js/webpack for asset compilation and includes comprehensive testing and documentation workflows.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Environment Setup
- **CRITICAL**: This project requires both Python 3.13+ and Node.js for full functionality
- Install required tools in this order:
  - `pip install tox` - Environment and task management
  - `pip install pre-commit` - Code quality hooks
  - `npm install` - Install webpack dependencies (~50 seconds, NEVER CANCEL)
  - `pre-commit install` - Install git hooks

### Build Commands and Timing
- **Asset compilation**: `npm run build` - Compiles CSS/JS with webpack (2.5-3 seconds, VALIDATED)
- **Theme compilation**: `tox -e compile` - Uses sphinx-theme-builder (~2-5 minutes, NEVER CANCEL. Set timeout to 10+ minutes)
- **Documentation build**: `tox -e docs-update` - Builds theme documentation (~5-15 minutes, NEVER CANCEL. Set timeout to 30+ minutes)
- **Live development**: `tox -e docs-live` - Auto-rebuilding development server (~5-10 minutes initial, NEVER CANCEL. Set timeout to 20+ minutes)
- **Install theme**: `pip install -e .` - Development installation (~3-10 minutes, NEVER CANCEL. Set timeout to 15+ minutes)

### Testing and Quality Assurance
- **Run tests**: `tox` - ALWAYS use tox for running tests (~5-15 minutes, NEVER CANCEL. Set timeout to 30+ minutes)
  - Tests run against Python 3.12 and 3.13 with Sphinx 7
  - DO NOT use `pytest` directly - always use `tox` for proper environment isolation
- **Pre-commit checks**: `pre-commit run --all-files` - All formatting and linting (~2-5 minutes, NEVER CANCEL. VALIDATED: flake8 and black work correctly)
- **Linting**: `flake8 src/` - Python linting (few seconds, VALIDATED)
- **Formatting**: `black --check src/` - Code formatting check (few seconds, VALIDATED)

### Network and Connectivity Issues
- **PyPI connectivity may fail** with timeout errors in sandboxed environments
- If `pip install` commands fail with ReadTimeoutError, document this limitation: "pip install fails due to network limitations"
- **WORKAROUND**: Use `pip install --timeout=120` for better reliability
- **DO NOT** skip commands that fail due to network issues - document them as environment limitations

## Validation Scenarios

After making changes, always test these scenarios:
- **Asset compilation**: Run `npm run build` and verify CSS/JS files are generated in `src/quantecon_book_theme/theme/quantecon_book_theme/static/`
- **Theme functionality**: Install the theme and test with a sample Jupyter Book project
- **Code quality**: Run `pre-commit run --all-files` to ensure formatting and linting pass
- **Documentation**: Run `tox -e docs-update` and verify HTML builds without errors

## Key Project Structure

### Build System Components
- `package.json` + `webpack.config.js` - Node.js asset compilation
- `pyproject.toml` - Python package configuration and dependencies
- `tox.ini` - Environment management and common tasks
- `.pre-commit-config.yaml` - Code quality automation

### Source Code Layout
```
src/quantecon_book_theme/
├── __init__.py              # Main theme module
├── assets/                  # Source CSS/JS (compiled by webpack)
├── launch.py                # Theme utilities
└── theme/                   # Sphinx theme files and compiled assets
```

### Important Files
- `src/quantecon_book_theme/assets/` - Edit SCSS and JavaScript source files here
- `src/quantecon_book_theme/theme/quantecon_book_theme/static/` - Compiled CSS/JS assets (do not edit directly)
- `tests/` - Pytest test suite with regression testing
- `docs/` - Theme documentation and examples

## Common Tasks

### Making Asset Changes
1. Edit source files in `src/quantecon_book_theme/assets/`
2. Run `npm run build` to compile changes
3. For development with auto-reload: `tox -e docs-live`
4. Always test changes with `tox -e docs-update`

### Running Tests
- **Full test suite**: `tox` - ALWAYS use tox (runs tests in Python 3.12 and 3.13 environments)
- **NEVER use pytest directly** - tox provides proper environment isolation and multi-version testing
- **Regression tests**: Tests compare generated HTML against golden files in `tests/test_build/`

### Code Quality Workflow
- Always run `pre-commit run --all-files` before committing
- Pre-commit includes: black (formatting), flake8 (linting), YAML/JSON validation
- CI will fail if pre-commit checks don't pass

## Troubleshooting

### Network/PyPI Issues
- **Symptom**: ReadTimeoutError during pip install
- **Solution**: Document as "fails due to network limitations" in instructions
- **Alternative**: Try `pip install --timeout=120` for longer timeout

### GitHub CLI (gh) Issues
- **Shell Escaping**: zsh has many issues with shell escaping, heredocs, and multiline strings. **ALWAYS** use the `create_file` tool to write content to a temporary file first, then pass it to `gh` with the `--body-file` flag. **NEVER** pass multiline body content directly via `--body` in the terminal.
  - Example workflow for updating a PR description:
    1. Use `create_file` to write the body to `/tmp/pr_body.md`
    2. Run: `gh pr edit 123 --body-file /tmp/pr_body.md`
  - Example workflow for creating a release:
    1. Use `create_file` to write release notes to `/tmp/release_notes.md`
    2. Run: `gh release create vX.Y.Z --title "Title" --notes-file /tmp/release_notes.md`
- **Output Capture**: Always write gh output to `/tmp` file for reliable capture: `gh pr view 123 2>&1 | tee /tmp/gh_output.txt`

### Missing Python 3.13
- **Symptom**: `tox` skips environments with "could not find python interpreter"
- **Solution**: Tests will work with Python 3.12+ even if configured for 3.13

### Webpack Build Issues
- **Symptom**: CSS/JS files not updating after changes
- **Solution**: Run `npm run build` explicitly before testing
- **Check**: Verify compiled files exist in `src/quantecon_book_theme/theme/quantecon_book_theme/static/`

### Test Failures
- **Regression tests**: If HTML output changes, update test fixtures by deleting files in `tests/test_build/` and re-running pytest
- **Missing dependencies**: Install test dependencies with `pip install -e .[test]`

## Command Reference

### Frequently Used Commands
```bash
# Setup
pip install tox pre-commit
npm install
pre-commit install

# Development workflow
npm run build                    # Compile assets (2.5-3 seconds, VALIDATED)
tox -e docs-live                # Live development server (5-10 minutes)
pre-commit run --all-files      # Code quality checks (2-5 minutes, VALIDATED)
flake8 src/                     # Python linting (few seconds, VALIDATED)
black --check src/              # Formatting check (few seconds, VALIDATED)

# Testing and CI
tox                             # Full test suite (5-15 minutes)
tox -e docs-update              # Build documentation (5-15 minutes)
```

### Directory Listing
```
ls -la [repo-root]:
.binder/
.flake8
.git/
.github/
.gitignore
.pre-commit-config.yaml
LICENSE
README.md
codecov.yml
docs/
node_modules/
package-lock.json
package.json
pyproject.toml
src/
tests/
tox.ini
webpack.config.js
```

### Package.json Content
```json
{
    "name": "quantecon_book_theme",
    "repository": "https://github.com/QuantEcon/quantecon-book-theme",
    "scripts": {
      "build": "webpack"
    },
    "devDependencies": {
      "css-loader": "^6.8.1",
      "css-minimizer-webpack-plugin": "^4.2.2",
      "webpack": "^5.0.0",
      "webpack-cli": "^5.0.0",
      "sass": "^1.59.3",
      "sass-loader": "^10.3.1"
    }
}
```

## Validation Checklist

The following commands have been verified to work in this environment:

### ✅ VALIDATED COMMANDS
- `npm install` - Installs webpack dependencies (~50 seconds)
- `npm run build` - Compiles assets successfully (2.5-3 seconds)
- `pip install tox pre-commit flake8 black` - Basic tooling installation works
- `pre-commit install` - Git hooks installation works
- `tox` - Full test suite with Python 3.12 and 3.13 environments (ALWAYS use this for testing)
- `flake8 src/` - Python linting works and finds issues as expected
- `black --check src/` - Code formatting check works
- Asset compilation produces expected files in `src/quantecon_book_theme/theme/quantecon_book_theme/static/`

### ⚠️ NETWORK-LIMITED COMMANDS
These commands may fail with ReadTimeoutError in sandboxed environments:
- `pip install -e .` - Theme installation (dependency download issues)
- `tox -e compile` - Sphinx theme builder installation (dependency download issues)
- `tox -e docs-update` - Documentation building (dependency download issues)
- `tox` - Test execution (dependency download issues)

### 💡 RECOMMENDED APPROACH
1. Always try commands first as documented
2. If pip commands fail with network timeouts, document as "fails due to network limitations"
3. Use `--timeout=120` flag with pip for better reliability
4. Focus on webpack builds and basic linting which work reliably

## Release Process

When creating a new release, follow this checklist in order:

### 1. Pre-Release Validation
- **Run pre-commit checks**: `pre-commit run --all-files`
  - Fix any trailing whitespace, formatting, or linting issues
  - Commit any fixes before proceeding
- **Run full test suite**: `tox`
  - Ensure all tests pass in Python 3.12 and 3.13 environments
  - Fix any test failures before proceeding
- **Build documentation**: `tox -e docs-update`
  - Verify documentation builds without errors
  - Check that any new features are documented

### 2. Version Updates
Update version numbers in these locations:
- **`src/quantecon_book_theme/__init__.py`**: Update `__version__ = "X.Y.Z"`
- **`CHANGELOG.md`**: Move unreleased changes to new version section with today's date
  - Use format: `## [X.Y.Z] - YYYY-MM-DD`
  - Organize changes under: Changed, Added, Fixed, Deprecated, Removed, Security
  - Add comparison links at bottom: `[X.Y.Z]: https://github.com/QuantEcon/quantecon-book-theme/compare/vPREV...vX.Y.Z`

### 3. Version Number Guidelines (Semantic Versioning)
- **Major (X.0.0)**: Breaking changes, incompatible API changes
- **Minor (0.X.0)**: New features, significant refactoring, non-breaking changes
- **Patch (0.0.X)**: Bug fixes, documentation updates, minor tweaks

### 4. Commit and Tag
```bash
# Commit version updates
git add src/quantecon_book_theme/__init__.py CHANGELOG.md
git commit -m "Release version X.Y.Z"

# Create annotated tag
git tag -a vX.Y.Z -m "Version X.Y.Z - Brief description"

# Push commit and tag
git push && git push origin vX.Y.Z
```

### 5. Create GitHub Release
```bash
# Write release notes to a temp file first (use create_file tool)
# Then create the release using --notes-file
gh release create vX.Y.Z \
  --title "vX.Y.Z - Release Title" \
  --notes-file /tmp/release_notes.md
```

**IMPORTANT**: Always use `--notes-file` with a temp file instead of `--notes` to avoid zsh shell escaping issues. Creating the GitHub release triggers the PyPI publish workflow automatically.

### 6. Verify PyPI Publication
- Check GitHub Actions for successful PyPI publish workflow
- Verify package appears on PyPI: https://pypi.org/project/quantecon-book-theme/
- Test installation: `pip install quantecon-book-theme==X.Y.Z`

### Common Release Issues
- **Pre-commit failures**: Always run `pre-commit run --all-files` before creating release
- **Wrong version in `__init__.py`**: PyPI will reject if version already exists
- **Missing CHANGELOG entry**: Document all changes before release
- **Test failures**: Fix all test failures before proceeding with release
