"""
Pytest configuration and shared fixtures for quantecon-book-theme tests.
"""

import pytest
from pathlib import Path


# Test paths
TESTS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = TESTS_DIR.parent
SRC_DIR = PROJECT_ROOT / "src" / "quantecon_book_theme"
ASSETS_DIR = SRC_DIR / "assets"
THEME_DIR = SRC_DIR / "theme" / "quantecon_book_theme"


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def src_dir():
    """Return the source directory."""
    return SRC_DIR


@pytest.fixture
def assets_dir():
    """Return the assets directory."""
    return ASSETS_DIR


@pytest.fixture
def theme_dir():
    """Return the theme directory."""
    return THEME_DIR


@pytest.fixture
def styles_dir(assets_dir):
    """Return the styles directory."""
    return assets_dir / "styles"


@pytest.fixture
def scripts_dir(assets_dir):
    """Return the scripts directory."""
    return assets_dir / "scripts"
