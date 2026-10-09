"""
Tests for the toolbar's "View Source" button (#384).

Sphinx's generated pages (``genindex``, ``search``, and domain indices such as
sphinx-proof's ``prf-prf``) have no source document, so the theme sets no
repository URL for them. The button must then be left out rather than render
``href="None"``, which link checkers report as a missing file.
"""

import subprocess
import sys
from pathlib import Path
from shutil import copytree, ignore_patterns

import pytest
from bs4 import BeautifulSoup

SITE = Path(__file__).parent / "sites" / "base"
# html_theme_options["repository_url"] in sites/base/conf.py
REPOSITORY_URL = "https://github.com/executablebooks/sphinx-book-theme"
GENERATED_PAGES = ("genindex.html", "search.html")


@pytest.fixture(scope="module")
def pages(tmp_path_factory):
    """Build the base site and return ``{path: BeautifulSoup}`` for every page."""
    book = tmp_path_factory.mktemp("view_source") / "book"
    copytree(SITE, book, ignore=ignore_patterns("_build", "build_warnings.log"))
    out = book / "_build" / "html"
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "-a", "-W", "-q"]
        + [str(book), str(out)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(f"sphinx-build failed:\n{result.stdout}\n{result.stderr}")
    return {
        path.relative_to(out).as_posix(): BeautifulSoup(
            path.read_text(encoding="utf-8"), "html.parser"
        )
        for path in out.rglob("*.html")
        if "_static" not in path.relative_to(out).parts
    }


def view_source_hrefs(soup):
    """Return the href of each "View Source" toolbar link on a page."""
    return [a["href"] for a in soup.select('li[data-tippy-content="View Source"] a')]


@pytest.mark.build
class TestViewSource:
    def test_no_link_points_at_none(self, pages):
        broken = sorted(
            (name, a["href"])
            for name, soup in pages.items()
            for a in soup.find_all(href=True)
            if a["href"].startswith("None")
        )
        assert broken == []

    @pytest.mark.parametrize("name", GENERATED_PAGES)
    def test_generated_pages_have_no_button(self, pages, name):
        assert view_source_hrefs(pages[name]) == []

    def test_source_pages_keep_the_button(self, pages):
        source_pages = sorted(set(pages) - set(GENERATED_PAGES))
        assert "index.html" in source_pages
        assert "section1/ntbk.html" in source_pages
        hrefs = {name: view_source_hrefs(pages[name]) for name in source_pages}
        assert hrefs == {name: [REPOSITORY_URL] for name in source_pages}
