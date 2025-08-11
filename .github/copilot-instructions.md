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
- **Run tests**: `tox` or `pytest --durations=10 --cov=quantecon_book_theme --cov-report=xml --cov-report=term-missing` (~5-15 minutes, NEVER CANCEL. Set timeout to 30+ minutes)
- **Pre-commit checks**: `pre-commit run --all-files` - All formatting and linting (~2-5 minutes, NEVER CANCEL. VALIDATED: flake8 and black work correctly)
- **Python 3.13 environment**: Tests are configured for Python 3.13 but will work with 3.12+
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
- **Full test suite**: `tox` (uses Python 3.13 environment if available)
- **Direct pytest**: `pytest` (requires manually installing test dependencies)
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
