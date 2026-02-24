# Release Process

Checklist for creating a new release of `quantecon-book-theme`.

```{contents}
:local:
:depth: 2
```

## 1. Pre-Release Validation

```bash
# Code quality
pre-commit run --all-files

# Full test suite
tox

# Documentation build
tox -e docs-update
```

Fix any issues before proceeding.

## 2. Version Updates

Update version numbers in these files:

### `src/quantecon_book_theme/__init__.py`

```python
__version__ = "X.Y.Z"
```

### `CHANGELOG.md`

Move unreleased changes to a new version section with today's date:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Changed
- ...

### Added
- ...

### Fixed
- ...
```

Add a comparison link at the bottom:

```markdown
[X.Y.Z]: https://github.com/QuantEcon/quantecon-book-theme/compare/vPREV...vX.Y.Z
```

## 3. Version Number Guidelines (SemVer)

- **Major (X.0.0)** — breaking changes, incompatible API changes
- **Minor (0.X.0)** — new features, significant refactoring
- **Patch (0.0.X)** — bug fixes, documentation updates, minor tweaks

## 4. Commit and Tag

```bash
git add src/quantecon_book_theme/__init__.py CHANGELOG.md
git commit -m "Release version X.Y.Z"

git tag -a vX.Y.Z -m "Version X.Y.Z - Brief description"

git push && git push origin vX.Y.Z
```

## 5. Create GitHub Release

Write release notes to a temp file, then create the release:

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z - Release Title" \
  --notes-file /tmp/release_notes.md
```

Creating the GitHub release triggers the PyPI publish workflow automatically.

## 6. Verify PyPI Publication

- Check GitHub Actions for successful publish workflow
- Verify on PyPI: <https://pypi.org/project/quantecon-book-theme/>
- Test: `pip install quantecon-book-theme==X.Y.Z`

## Common Issues

- **Pre-commit failures** — always run `pre-commit run --all-files` first
- **Duplicate version on PyPI** — PyPI rejects if version already exists
- **Missing CHANGELOG** — document all changes before release
- **Test failures** — fix all failures before release
