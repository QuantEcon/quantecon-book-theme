"""Tests for the authors and translators attribution options."""

import json
import subprocess
import sys
import textwrap

import pytest
from bs4 import BeautifulSoup

from quantecon_book_theme import (
    _md_front_matter,
    _nb_front_matter,
    _normalise_people,
    _resolve_label,
    _resolve_people,
)


AUTHORS = [
    {"name": "Tom Sargent", "url": "https://tom.example.org"},
    {"name": "John Stachurski", "url": "https://john.example.org"},
]
TRANSLATORS = [
    {"name": "Zhang San", "url": "https://zhang.example.org"},
    {"name": "Li Si", "url": "https://li.example.org"},
]


class TestThemeOptionDefaults:
    """The four options must be declared in theme.conf, with safe defaults."""

    @pytest.fixture
    def option_lines(self, theme_dir):
        conf = (theme_dir / "theme.conf").read_text()
        return [line.strip() for line in conf.splitlines()]

    @pytest.mark.parametrize(
        "declaration",
        ["authors =", "authors_label =", "translators =", "translators_label ="],
    )
    def test_option_declared_once(self, option_lines, declaration):
        matches = [line for line in option_lines if line.startswith(declaration)]
        assert len(matches) == 1, f"expected one {declaration!r} line, got {matches}"

    def test_translators_label_default(self, option_lines):
        assert "translators_label = Translated by" in option_lines

    @pytest.mark.parametrize("option", ["authors", "authors_label", "translators"])
    def test_list_defaults_are_empty(self, option_lines, option):
        """An empty string is falsy in Jinja; the string "[]" is not.

        Declaring ``translators = []`` would put the two-character string "[]"
        in the template context, whose length is 2, and every page of every
        site would render an empty translators block.
        """
        assert f"{option} =" in option_lines


class TestTemplateMarkup:
    """Assertions about layout.html that the rendering tests cannot make."""

    @pytest.fixture
    def layout(self, theme_dir):
        return (theme_dir / "layout.html").read_text()

    def test_authors_links_are_marked_up_as_authors(self, layout):
        assert layout.count('rel="author"') == 3, "one per branch of the author loop"

    def test_translators_links_are_not_marked_up_as_authors(self, layout):
        translators_block = layout.split("<!-- Translators section -->")[1]
        translators_block = translators_block.split("{%- endif %}")[0]
        assert 'rel="author"' not in translators_block

    def test_suppression_guard_present(self, layout):
        """Without this the project ``author`` string leaks back onto a page
        that set ``authors: []`` in its front matter."""
        assert "{%- elif not authors_suppressed %}" in layout

    def test_translators_paragraph_has_no_font_size_attribute(self, layout):
        """``font-size`` is a non-standard attribute that only exists so
        page-header.js can read it back off the authors paragraph. It should
        not be copied onto new markup."""
        assert layout.count("font-size=") == 2, "the two authors paragraphs only"

    def test_translators_block_is_conditional(self, layout):
        assert "{%- if theme_translators | length > 0 %}" in layout
        # The section comment sits inside the conditional, so a site without
        # translators gets no stray comment on every page.
        marker = "{%- if theme_translators | length > 0 %}"
        assert layout.index(marker) < layout.index("<!-- Translators section -->")


class TestNormalisePeople:
    """_normalise_people is the single gate every value passes through."""

    def test_documented_form_passes_through(self):
        assert _normalise_people(AUTHORS) == AUTHORS

    def test_missing_url_becomes_empty_string(self):
        assert _normalise_people([{"name": "Solo"}]) == [{"name": "Solo", "url": ""}]

    def test_null_url_becomes_empty_string(self):
        assert _normalise_people([{"name": "Solo", "url": None}]) == [
            {"name": "Solo", "url": ""}
        ]

    def test_entries_without_a_name_are_dropped(self):
        value = [{"url": "https://x.org"}, {"name": "  "}, {"name": "Real"}]
        assert _normalise_people(value) == [{"name": "Real", "url": ""}]

    def test_bare_string_becomes_one_person(self):
        """Previously a string was iterated character by character, emitting
        one empty anchor per character."""
        assert _normalise_people("Tom Sargent") == [{"name": "Tom Sargent", "url": ""}]

    def test_list_of_strings(self):
        assert _normalise_people(["Tom", "John"]) == [
            {"name": "Tom", "url": ""},
            {"name": "John", "url": ""},
        ]

    def test_single_dict(self):
        assert _normalise_people({"name": "Tom", "url": "https://tom.org"}) == [
            {"name": "Tom", "url": "https://tom.org"}
        ]

    @pytest.mark.parametrize("value", [None, "", [], (), 42, 3.5, True, object()])
    def test_values_without_people_become_empty(self, value):
        assert _normalise_people(value) == []

    def test_non_string_name_and_url_are_coerced(self):
        assert _normalise_people([{"name": 42, "url": 7}]) == [
            {"name": "42", "url": "7"}
        ]

    def test_non_mapping_entries_are_skipped(self):
        assert _normalise_people([["nested"], {"name": "Real"}]) == [
            {"name": "Real", "url": ""}
        ]

    def test_names_are_not_stripped(self):
        """Whitespace decides only whether an entry counts, never what renders,
        so projects already setting ``authors`` keep identical output."""
        assert _normalise_people([{"name": " Tom ", "url": ""}]) == [
            {"name": " Tom ", "url": ""}
        ]

    def test_input_is_not_mutated(self):
        original = [{"name": "Tom"}]
        _normalise_people(original)
        assert original == [{"name": "Tom"}]


class TestResolvePeople:
    """Page front matter replaces the project value; it never merges."""

    def test_absent_key_inherits_project_value(self):
        people, suppressed = _resolve_people({}, {"authors": AUTHORS}, "authors")
        assert people == AUTHORS
        assert suppressed is False

    def test_page_value_replaces_rather_than_merges(self):
        front_matter = {"authors": [{"name": "Page Author", "url": "https://p.org"}]}
        people, suppressed = _resolve_people(
            front_matter, {"authors": AUTHORS}, "authors"
        )
        assert people == [{"name": "Page Author", "url": "https://p.org"}]
        assert suppressed is False

    @pytest.mark.parametrize("empty", [None, "", [], ()])
    def test_any_explicitly_empty_value_suppresses(self, empty):
        """All of these say "nobody" rather than "I have nothing to say".
        ``None`` is what a bare ``authors:`` key parses to, and an empty string
        is what an interpolated template variable leaves behind."""
        people, suppressed = _resolve_people(
            {"authors": empty}, {"authors": AUTHORS}, "authors"
        )
        assert people == []
        assert suppressed is True

    def test_absent_key_with_no_project_value_is_not_suppressed(self):
        """Nothing configured anywhere must keep the existing fallback to
        Sphinx's own ``author`` setting."""
        people, suppressed = _resolve_people({}, {}, "authors")
        assert people == []
        assert suppressed is False

    def test_translators_resolve_independently_of_authors(self):
        config = {"authors": AUTHORS, "translators": TRANSLATORS}
        front_matter = {"authors": []}
        authors, authors_suppressed = _resolve_people(front_matter, config, "authors")
        translators, _ = _resolve_people(front_matter, config, "translators")
        assert authors == [] and authors_suppressed is True
        assert translators == TRANSLATORS

    @pytest.mark.parametrize(
        "value",
        [
            "Jane Doe, John Roe",  # docutils' own bibliographic field shape
            ["Jane Doe", "John Roe"],  # a list, but not of mappings
            [{"given": "Jane", "family": "Doe"}],  # mystmd's shape
            [{"name": "Real"}, {"url": "https://x.org"}],  # one unusable entry
            {"name": "Jane Doe"},  # a bare mapping rather than a list
            42,
        ],
    )
    def test_unreadable_front_matter_is_left_alone(self, value):
        """``authors`` is shared ground: docutils treats it as a bibliographic
        field and nbformat defines it in the notebook schema. A page carrying
        one written for something else must keep the project credit rather than
        rendering it badly or losing the byline."""
        people, suppressed = _resolve_people(
            {"authors": value}, {"authors": AUTHORS}, "authors"
        )
        assert people == AUTHORS
        assert suppressed is False

    def test_unreadable_front_matter_never_suppresses(self):
        """Suppression must mean "explicitly nobody", never "I could not read
        this" -- otherwise an unrecognised value silently deletes the byline."""
        _, suppressed = _resolve_people(
            {"authors": "Jane Doe, John Roe"}, {}, "authors"
        )
        assert suppressed is False


class TestResolveLabel:
    def test_falls_back_to_the_configured_context_value(self):
        context = {"theme_translators_label": "Translated by"}
        assert _resolve_label({}, context, "translators_label") == "Translated by"

    def test_page_front_matter_wins(self):
        context = {"theme_translators_label": "Translated by"}
        front_matter = {"translators_label": "译者"}
        assert _resolve_label(front_matter, context, "translators_label") == "译者"

    def test_explicit_empty_removes_the_label(self):
        context = {"theme_translators_label": "Translated by"}
        assert (
            _resolve_label({"translators_label": ""}, context, "translators_label")
            == ""
        )

    def test_null_becomes_empty_rather_than_the_string_none(self):
        assert _resolve_label({"authors_label": None}, {}, "authors_label") == ""

    def test_missing_context_key_is_empty(self):
        assert _resolve_label({}, {}, "authors_label") == ""


class TestFrontMatterReaders:
    """Front matter is read from the source file rather than env.metadata.

    docutils treats ``authors`` as a bibliographic field, so a value routed
    through env.metadata comes back smart-quoted and split on commas -- and in
    a different shape again depending on the ``language`` setting, because not
    every locale lists ``authors`` among its bibliographic fields.
    """

    def test_reads_a_leading_yaml_block(self, tmp_path):
        page = tmp_path / "page.md"
        page.write_text(
            textwrap.dedent(
                """\
                ---
                translators:
                  - name: Zhang San
                    url: https://zhang.example.org
                ---

                # Title
                """
            )
        )
        assert _md_front_matter(str(page)) == {
            "translators": [{"name": "Zhang San", "url": "https://zhang.example.org"}]
        }

    def test_jupytext_markdown(self, tmp_path):
        """The shape QuantEcon lecture repos actually use."""
        page = tmp_path / "lecture.md"
        page.write_text(
            textwrap.dedent(
                """\
                ---
                jupytext:
                  text_representation:
                    extension: .md
                    format_name: myst
                kernelspec:
                  display_name: Python 3
                  name: python3
                translators:
                  - name: Li Si
                ---

                # Lecture
                """
            )
        )
        front_matter = _md_front_matter(str(page))
        assert front_matter["translators"] == [{"name": "Li Si"}]
        assert "kernelspec" in front_matter

    def test_unicode_names(self, tmp_path):
        page = tmp_path / "page.md"
        page.write_text(
            "---\ntranslators:\n  - name: 李四\n---\n\n# T\n", encoding="utf-8"
        )
        assert _md_front_matter(str(page))["translators"] == [{"name": "李四"}]

    def test_explicit_empty_list_survives(self, tmp_path):
        """An empty list must stay distinguishable from an absent key."""
        page = tmp_path / "page.md"
        page.write_text("---\ntranslators: []\n---\n\n# T\n")
        front_matter = _md_front_matter(str(page))
        assert front_matter == {"translators": []}
        assert "translators" in front_matter

    @pytest.mark.parametrize(
        "source",
        [
            "# No front matter\n",
            "\n---\ntranslators: []\n---\n",  # must start on the first line
            "---\ntranslators: []\n",  # unterminated
            "---\n\ttranslators: [\n---\n",  # malformed yaml
            "---\n- just\n- a list\n---\n",  # not a mapping
            "",
        ],
    )
    def test_sources_without_usable_front_matter(self, tmp_path, source):
        page = tmp_path / "page.md"
        page.write_text(source)
        assert _md_front_matter(str(page)) == {}

    def test_missing_file(self, tmp_path):
        assert _md_front_matter(str(tmp_path / "nope.md")) == {}
        assert _nb_front_matter(str(tmp_path / "nope.ipynb")) == {}

    def test_byte_order_mark_does_not_hide_front_matter(self, tmp_path):
        """Sphinx reads sources as utf-8-sig, so MyST parses a BOM'd page's
        front matter. Reading it as plain utf-8 here would leave the marker on
        the opening fence and silently drop every override on that page."""
        page = tmp_path / "page.md"
        page.write_text(
            "---\ntranslators:\n  - name: BOM Translator\n---\n\n# T\n",
            encoding="utf-8-sig",
        )
        assert page.read_bytes().startswith(b"\xef\xbb\xbf")
        assert _md_front_matter(str(page))["translators"] == [
            {"name": "BOM Translator"}
        ]

    def test_byte_order_mark_on_a_notebook(self, tmp_path):
        notebook = tmp_path / "page.ipynb"
        notebook.write_text(
            json.dumps({"cells": [], "metadata": {"translators": [{"name": "BOM"}]}}),
            encoding="utf-8-sig",
        )
        assert _nb_front_matter(str(notebook))["translators"] == [{"name": "BOM"}]

    @pytest.mark.parametrize("width", [3, 4, 8])
    def test_longer_dash_fences(self, tmp_path, width):
        """MyST accepts a fence of three or more dashes, closed by a run at
        least as long."""
        fence = "-" * width
        page = tmp_path / "page.md"
        page.write_text(f"{fence}\ntranslators:\n  - name: Fenced\n{fence}\n\n# T\n")
        assert _md_front_matter(str(page))["translators"] == [{"name": "Fenced"}]

    def test_closing_fence_may_be_longer_than_the_opening_one(self, tmp_path):
        page = tmp_path / "page.md"
        page.write_text("---\ntranslators:\n  - name: Fenced\n-----\n\n# T\n")
        assert _md_front_matter(str(page))["translators"] == [{"name": "Fenced"}]

    def test_closing_fence_may_not_be_shorter(self, tmp_path):
        page = tmp_path / "page.md"
        page.write_text("-----\ntranslators: []\n---\n\n# T\n")
        assert _md_front_matter(str(page)) == {}

    @pytest.mark.parametrize("opening", ["--", "---x", "- --", "***"])
    def test_lines_that_are_not_fences(self, tmp_path, opening):
        page = tmp_path / "page.md"
        page.write_text(f"{opening}\ntranslators: []\n{opening}\n\n# T\n")
        assert _md_front_matter(str(page)) == {}

    def test_notebook_metadata(self, tmp_path):
        notebook = tmp_path / "page.ipynb"
        notebook.write_text(
            json.dumps(
                {
                    "cells": [],
                    "metadata": {"translators": [{"name": "Wang Wu"}]},
                    "nbformat": 4,
                    "nbformat_minor": 5,
                }
            )
        )
        assert _nb_front_matter(str(notebook)) == {"translators": [{"name": "Wang Wu"}]}

    @pytest.mark.parametrize(
        "source", ["not json", "[]", '{"cells": []}', '{"metadata": []}']
    )
    def test_notebooks_without_usable_metadata(self, tmp_path, source):
        notebook = tmp_path / "page.ipynb"
        notebook.write_text(source)
        assert _nb_front_matter(str(notebook)) == {}


def build_site(tmp_path, theme_options, pages, bom_pages=()):
    """Build a throwaway site and return ``{pagename: BeautifulSoup}``.

    Options go through a generated ``conf.py`` rather than ``-D``, because
    Sphinx keeps a ``-D html_theme_options.authors=...`` value as a string.
    Names listed in ``bom_pages`` are written with a byte-order mark, which is
    what a Windows editor produces and what Sphinx's ``source_encoding``
    default expects to strip.
    """
    src = tmp_path / "src"
    src.mkdir()
    (src / "conf.py").write_text(
        "project = 'Attribution'\n"
        "author = 'Project Author'\n"
        "master_doc = 'index'\n"
        "extensions = ['myst_nb']\n"
        "html_theme = 'quantecon_book_theme'\n"
        f"html_theme_options = {json.dumps(theme_options)}\n"
    )
    toctree = "\n".join(sorted(pages))
    (src / "index.md").write_text(f"# Index\n\n```{{toctree}}\n{toctree}\n```\n")
    for name, source in pages.items():
        encoding = "utf-8-sig" if name in bom_pages else "utf-8"
        (src / f"{name}.md").write_text(source, encoding=encoding)

    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "-a", "-q", str(src), str(out)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(f"sphinx-build failed:\n{result.stdout}\n{result.stderr}")
    return {
        name: BeautifulSoup(
            (out / f"{name}.html").read_text(encoding="utf-8"), "html.parser"
        )
        for name in pages
    }


def attribution(soup, kind):
    """Return the rendered text of the authors or translators paragraph."""
    paragraph = soup.select_one(f"p.qe-page__header-{kind}")
    return None if paragraph is None else " ".join(paragraph.get_text().split())


@pytest.mark.build
class TestRendering:
    """End-to-end rendering of both blocks through a real Sphinx build."""

    @pytest.fixture(scope="class")
    def pages(self, tmp_path_factory):
        return build_site(
            tmp_path_factory.mktemp("attribution"),
            {"authors": AUTHORS, "translators": TRANSLATORS},
            {
                "inherit": "# Inherit\n",
                "override": (
                    "---\n"
                    "authors:\n"
                    "  - name: Page Author\n"
                    "    url: https://page.example.org\n"
                    "translators:\n"
                    "  - name: Solo Translator\n"
                    "    url: https://solo.example.org\n"
                    "---\n\n# Override\n"
                ),
                "suppress": "---\nauthors: []\ntranslators: []\n---\n\n# Suppress\n",
                "labels": (
                    "---\nauthors_label: 作者\ntranslators_label: 译者\n---\n\n# Labels\n"
                ),
                "nourl": "---\ntranslators:\n  - name: No Url\n---\n\n# No url\n",
                "docinfo": "---\nauthors: Jane Doe, John Roe\n---\n\n# Docinfo\n",
                "bom": "---\ntranslators:\n  - name: BOM Translator\n---\n\n# Bom\n",
            },
            bom_pages=("bom",),
        )

    def test_project_values_render_on_a_plain_page(self, pages):
        soup = pages["inherit"]
        assert attribution(soup, "authors") == "Tom Sargent and John Stachurski"
        assert attribution(soup, "translators") == "Translated by Zhang San and Li Si"

    def test_only_authors_are_marked_up_for_crawlers(self, pages):
        soup = pages["inherit"]
        assert len(soup.select("p.qe-page__header-authors a[rel=author]")) == 2
        assert soup.select("p.qe-page__header-translators a[rel=author]") == []

    def test_page_front_matter_replaces_both_lists(self, pages):
        soup = pages["override"]
        assert attribution(soup, "authors") == "Page Author"
        assert attribution(soup, "translators") == "Translated by Solo Translator"

    def test_explicit_empty_lists_suppress_both_blocks(self, pages):
        soup = pages["suppress"]
        assert attribution(soup, "authors") is None
        assert attribution(soup, "translators") is None

    def test_suppressed_authors_do_not_fall_back_to_the_project_author(self, pages):
        """The template's fallback prints Sphinx's own ``author`` setting; a
        page that suppressed its authors must not get it instead."""
        assert "Project Author" not in pages["suppress"].get_text()

    def test_labels_are_overridable_per_page(self, pages):
        soup = pages["labels"]
        assert attribution(soup, "authors").startswith("作者")
        assert attribution(soup, "translators").startswith("译者")
        assert soup.select_one("span.qe-page__header-translators-label").text == "译者"

    def test_default_authors_label_is_empty(self, pages):
        """Authors keep their label-free rendering unless a label is set."""
        assert pages["inherit"].select("span.qe-page__header-authors-label") == []

    def test_translator_without_a_url_renders_as_plain_text(self, pages):
        soup = pages["nourl"]
        assert attribution(soup, "translators") == "Translated by No Url"
        assert soup.select("p.qe-page__header-translators a") == []

    def test_a_docutils_style_authors_field_leaves_the_byline_alone(self, pages):
        """A page carrying `authors:` as docutils' bibliographic field must keep
        the project byline rather than collapsing both names into one bad link
        or losing the byline entirely."""
        assert attribution(pages["docinfo"], "authors") == (
            "Tom Sargent and John Stachurski"
        )

    def test_front_matter_survives_a_byte_order_mark(self, pages):
        """Sphinx reads sources as utf-8-sig, so MyST honours this page's front
        matter; the theme must not disagree with the parser about the same
        file and silently credit the wrong people."""
        assert attribution(pages["bom"], "translators") == (
            "Translated by BOM Translator"
        )


@pytest.mark.build
class TestRenderingWithoutTranslators:
    """A site that configures nothing new must render as it always has."""

    @pytest.fixture(scope="class")
    def pages(self, tmp_path_factory):
        return build_site(
            tmp_path_factory.mktemp("plain"),
            {"authors": AUTHORS},
            {"plain": "# Plain\n"},
        )

    def test_no_translators_block(self, pages):
        assert pages["plain"].select("p.qe-page__header-translators") == []

    def test_no_translators_comment_left_behind(self, pages):
        assert "Translators section" not in str(pages["plain"])

    def test_authors_still_render(self, pages):
        assert attribution(pages["plain"], "authors") == (
            "Tom Sargent and John Stachurski"
        )


@pytest.mark.build
class TestJoinFormatting:
    """The translators list joins exactly like the authors list does."""

    @pytest.fixture(scope="class")
    def pages(self, tmp_path_factory):
        people = [
            {"name": "One", "url": "https://one.example.org"},
            {"name": "Two", "url": "https://two.example.org"},
            {"name": "Three", "url": "https://three.example.org"},
            {"name": "Four", "url": "https://four.example.org"},
        ]
        return build_site(
            tmp_path_factory.mktemp("join"),
            {"authors": people, "translators": people},
            {
                f"n{count}": (
                    "---\ntranslators:\n"
                    + "".join(
                        f"  - name: {p['name']}\n    url: {p['url']}\n"
                        for p in people[:count]
                    )
                    + "authors:\n"
                    + "".join(
                        f"  - name: {p['name']}\n    url: {p['url']}\n"
                        for p in people[:count]
                    )
                    + f"---\n\n# {count}\n"
                )
                for count in (1, 2, 3, 4)
            },
        )

    @pytest.mark.parametrize(
        "count,expected",
        [
            (1, "One"),
            (2, "One and Two"),
            (3, "One, Two, and Three"),
            (4, "One, Two, Three, and Four"),
        ],
    )
    def test_translators_join(self, pages, count, expected):
        assert attribution(pages[f"n{count}"], "translators") == (
            f"Translated by {expected}"
        )

    @pytest.mark.parametrize(
        "count,expected",
        [
            (1, "One"),
            (2, "One and Two"),
            (3, "One, Two, and Three"),
            (4, "One, Two, Three, and Four"),
        ],
    )
    def test_authors_join_is_unchanged(self, pages, count, expected):
        assert attribution(pages[f"n{count}"], "authors") == expected
