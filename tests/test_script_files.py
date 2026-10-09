"""
Tests that every script a page requests is in the build (#454).

The theme calls ``setup_extension("sphinx_book_theme")`` for that package's
Python features, which also registers ``scripts/sphinx-book-theme.js``. The
file sits in sphinx_book_theme's static folder, which is only copied when that
is the active theme, so the theme drops the registration again.

The site is built with ``-W``, so a warning from sphinx_book_theme's asset
hashing, which still lists the script, would fail the build.
"""

import subprocess
import sys
from pathlib import Path
from shutil import copytree, ignore_patterns

import pytest
from bs4 import BeautifulSoup

SITE = Path(__file__).parent / "sites" / "base"


@pytest.fixture(scope="module", params=["theme", "jupyter-book"])
def site(request, tmp_path_factory):
    """Build the base site and return its output directory.

    Jupyter Book 1 lists ``sphinx_book_theme`` in its default ``extensions``,
    so there its ``setup()`` runs before this theme's rather than from inside
    it; the ``jupyter-book`` build reproduces that order.
    """
    book = tmp_path_factory.mktemp("scripts") / "book"
    copytree(SITE, book, ignore=ignore_patterns("_build", "build_warnings.log"))
    if request.param == "jupyter-book":
        with (book / "conf.py").open("a") as conf:
            conf.write('\nextensions.append("sphinx_book_theme")\n')
    out = book / "_build" / "html"
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "-a", "-W", "-q"]
        + [str(book), str(out)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(f"sphinx-build failed:\n{result.stdout}\n{result.stderr}")
    return out


@pytest.fixture(scope="module")
def scripts(site):
    """Return ``{page: [script src, ...]}`` for every page in the built site."""
    return {
        page.relative_to(site).as_posix(): [
            script["src"]
            for script in BeautifulSoup(
                page.read_text(encoding="utf-8"), "html.parser"
            ).find_all("script", src=True)
        ]
        for page in site.rglob("*.html")
        if "_static" not in page.relative_to(site).parts
    }


@pytest.mark.build
class TestScriptFiles:
    def test_sphinx_book_theme_script_is_not_requested(self, scripts):
        requesting = sorted(
            name
            for name, srcs in scripts.items()
            if any("scripts/sphinx-book-theme.js" in src for src in srcs)
        )
        assert requesting == []

    def test_quantecon_book_theme_script_is_still_loaded(self, scripts):
        assert "index.html" in scripts
        missing = sorted(
            name
            for name, srcs in scripts.items()
            if not any("scripts/quantecon-book-theme.js" in src for src in srcs)
        )
        assert missing == []

    def test_every_local_script_exists(self, site, scripts):
        missing = sorted(
            (name, src)
            for name, srcs in scripts.items()
            for src in srcs
            if "://" not in src
            and not (site / name).parent.joinpath(src.split("?")[0]).is_file()
        )
        assert missing == []
