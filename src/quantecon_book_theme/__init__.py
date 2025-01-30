"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
import os
import hashlib
from functools import lru_cache

from docutils import nodes
from sphinx.util import logging
from bs4 import BeautifulSoup as bs
from sphinx.util.fileutil import copy_asset
from sphinx.util.osutil import ensuredir

from .launch import add_hub_urls

__version__ = "0.8.1"
"""quantecon-book-theme version"""

SPHINX_LOGGER = logging.getLogger(__name__)
MESSAGE_CATALOG_NAME = "booktheme"


def get_html_theme_path():
    """Return list of HTML theme paths."""
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "quantecon_book_theme"
    return theme_path


def find_url_relative_to_root(pagename, relative_page, path_docs_source):
    """Given the current page (pagename), a relative page to it (relative_page),
    and a path to the docs source, return the path to `relative_page`, but now relative
    to the docs source (since this is what keys in Sphinx tend to use).
    """
    # In this case, the relative_page is the same as the pagename
    if relative_page == "":
        relative_page = Path(Path(pagename).name)

    # Convert everything to paths for use later
    path_rel = Path(relative_page).with_suffix("")
    path_parent = Path(pagename)  # pagename is relative to docs root
    source_dir = Path(path_docs_source)
    # This should be the path to `relative_page`, relative to `pagename`
    path_rel_from_page_dir = source_dir.joinpath(
        path_parent.parent.joinpath(path_rel.parent)
    )
    path_from_page_dir = path_rel_from_page_dir.resolve()
    page_rel_root = path_from_page_dir.relative_to(source_dir).joinpath(path_rel.name)
    return page_rel_root


def add_plugins_list(app):
    # copying plugins
    if "plugins_list" in app.config.html_theme_options:
        outdir = app.outdir + "/plugins"
        ensuredir(outdir)
        for i, asset in enumerate(app.config.html_theme_options["plugins_list"]):
            assetname = Path(asset).name
            copy_asset(app.confdir + "/" + asset, outdir)
            app.config.html_theme_options["plugins_list"][i] = "plugins/" + assetname


def add_to_context(app, pagename, templatename, context, doctree):
    """Functions and variable additions to context."""

    config_theme = app.config.html_theme_options

    def sbt_generate_toctree_html(
        level=1,
        include_item_names=False,
        with_home_page=False,
    ):
        # Config stuff
        if isinstance(with_home_page, str):
            with_home_page = with_home_page.lower() == "true"

        # Grab the raw toctree object and structure it so we can manipulate it
        toctree = context["generate_toctree_html"](
            startdepth=level - 1,
            maxdepth=level + 1,
            kind="sidebar",
            collapse=False,
            titles_only=True,
            includehidden=True,
        )
        # toctree = bs(toc_sphinx, "html.parser")

        # pair "current" with "active" since that's what we use w/ bootstrap
        for li in toctree("li", {"class": "current"}):
            li["class"].append("active")

        # Add the master_doc page as the first item if specified
        if with_home_page:
            master_title = master_doctree.traverse(nodes.title)[0].astext()
            if len(master_title) == 0:
                raise ValueError(f"Landing page missing a title: {master_doc}")
            li_class = "toctree-l1"
            if context["pagename"] == master_doc:
                li_class += " current"
            # Insert it into our toctree
            ul_home = bs(
                f"""
            <ul class="nav bd-sidenav">
                <li class="{li_class}">
                    <a href="{master_url}" class="reference internal">{master_title}</a>
                </li>
            </ul>""",
                "html.parser",
            )
            toctree.insert(0, ul_home("ul")[0])

        # Add an icon for external links
        for a_ext in toctree("a", attrs={"class": ["external"]}):
            a_ext.append(
                toctree.new_tag("i", attrs={"class": ["fas", "fa-external-link-alt"]})
            )

        # Add bootstrap classes for first `ul` items
        for ul in toctree("ul", recursive=False):
            ul.attrs["class"] = ul.attrs.get("class", []) + ["nav", "sidenav_l1"]

        return toctree.prettify()

    def generate_toc_html():
        """Return the within-page TOC links in HTML."""

        if not context.get("toc"):
            return ""

        soup = bs(context["toc"], "html.parser")

        # Add toc-hN classes
        def add_header_level_recursive(ul, level):
            for li in ul("li", recursive=False):
                li["class"] = li.get("class", []) + [f"toc-h{level}"]
                ul = li.find("ul", recursive=False)
                if ul:
                    add_header_level_recursive(ul, level + 1)

        add_header_level_recursive(soup.find("ul"), 1)

        # Add in CSS classes for bootstrap
        for ul in soup("ul"):
            ul["class"] = ul.get("class", []) + ["nav", "section-nav", "flex-column"]
        for li in soup("li"):
            li["class"] = li.get("class", []) + ["nav-item", "toc-entry"]
            if li.find("a"):
                a = li.find("a")
                a["class"] = a.get("class", []) + ["nav-link"]

        # Keep only the sub-sections of the title (so no title is shown)
        title = soup.find("a", attrs={"href": "#"})
        if title:
            title = title.parent
            # Only show if children of the title item exist
            if title.select("ul li"):
                out = title.find("ul").prettify()
            else:
                out = ""
        else:
            out = ""
        return out

    def get_github_src_folder(app):
        if "github_repo" in context:
            github_repo = context["github_repo"]
            if github_repo in app.srcdir:
                index = app.srcdir.rfind(github_repo)
                branch = config_theme.get("nb_branch", "")
                if branch == "":
                    branch = "main"
                folder = app.srcdir[index + len(github_repo) :]
                return "/blob/" + branch + folder
        return ""

    # Pull metadata about the master doc
    master_doc = app.config["master_doc"]
    master_doctree = app.env.get_doctree(master_doc)
    master_url = context["pathto"](master_doc)
    context["master_url"] = master_url

    context["sbt_generate_toctree_html"] = sbt_generate_toctree_html
    context["generate_toc_html"] = generate_toc_html

    # check if book pdf folder is present
    if os.path.isdir(app.outdir + "/_pdf"):
        if "pdf_book_name" not in context:
            context["pdf_book_name"] = app.config.latex_documents[0][1].replace(
                ".tex", ""
            )
        context["pdf_book_path"] = "/_pdf/" + context["pdf_book_name"] + ".pdf"

    # check if notebook folder is present
    if os.path.isdir(app.outdir + "/_notebooks"):
        context["notebook_path"] = "/_notebooks/" + context["pagename"] + ".ipynb"

    # Update the page title because HTML makes it into the page title occasionally
    if pagename in app.env.titles:
        title = app.env.titles[pagename]
        context["pagetitle"] = title.astext()

    # Add a shortened page text to the context using the sections text
    if not len(context["theme_description"]) > 0 and doctree:
        description = ""
        for section in doctree.traverse(nodes.section):
            description += section.astext().replace("\n", " ")
        description = description[:160]
        context["theme_description"] = description

    # Add the author if it exists
    if app.config.author != "unknown":
        context["author"] = app.config.author

    # Absolute URLs for logo if `html_baseurl` is given
    # pageurl will already be set by Sphinx if so
    if app.config.html_baseurl and app.config.html_logo:
        context["logourl"] = "/".join(
            (app.config.html_baseurl.rstrip("/"), context["logo_url"])
        )

    # Check mathjax version and set it in a variable
    if app.config["mathjax_path"] and "@3" in app.config["mathjax_path"]:
        context["mathjax_version"] = 3
    else:
        context["mathjax_version"] = 2
    # Add HTML context variables that the pydata theme uses that we configure elsewhere
    # For some reason the source_suffix sometimes isn't there even when doctree is
    if doctree and context.get("page_source_suffix"):
        repo_url = config_theme.get("repository_url", "")
        # Only add the edit button if `repository_url` is given
        if repo_url:
            branch = config_theme.get("repository_branch")
            if not branch:
                # Explicitly check in case branch is ""
                branch = "main"
            relpath = config_theme.get("path_to_docs", "")
            org, repo = repo_url.strip("/").split("/")[-2:]
            context.update(
                {
                    "github_user": org,
                    "github_repo": repo,
                    "github_version": branch,
                    "doc_path": relpath,
                }
            )
    else:
        # Disable using the button so we don't get errors
        context["theme_use_edit_page_button"] = False

    # default value is book.tex
    if "pdf_book_name" not in context:
        context["pdf_book_name"] = app.config.latex_documents[0][1].replace(".tex", "")
    context["github_sourcefolder"] = get_github_src_folder(app)

    # Make sure the context values are bool
    btns = [
        "theme_use_edit_page_button",
        "theme_use_repository_button",
        "theme_use_issues_button",
    ]
    for key in btns:
        if key in context:
            context[key] = _string_or_bool(context[key])


@lru_cache(maxsize=None)
def _gen_hash(path: str) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def hash_assets_for_files(assets: list, theme_static: Path, context):
    """Generate a hash for assets, and append to its entry in context.

    assets: a list of assets to hash, each path should be relative to
         the theme's static folder.

    theme_static: a path to the theme's static folder.

    context: the Sphinx context object where asset links are stored. These are:
        `css_files` and `script_files` keys.
    """
    for asset in assets:
        # CSS assets are stored in css_files, JS assets in script_files
        asset_type = "css_files" if asset.endswith(".css") else "script_files"
        if asset_type in context:
            # Define paths to the original asset file, and its linked file in Sphinx
            asset_sphinx_link = f"_static/{asset}"
            asset_source_path = theme_static / asset
            if not asset_source_path.exists():
                SPHINX_LOGGER.warning(
                    f"Asset {asset_source_path} does not exist, not linking."
                )
            # Find this asset in context, and update it to include the digest
            if asset_sphinx_link in context[asset_type]:
                hash = _gen_hash(asset_source_path)
                ix = context[asset_type].index(asset_sphinx_link)
                context[asset_type][ix] = asset_sphinx_link + "?digest=" + hash


def hash_html_assets(app, pagename, templatename, context, doctree):
    """Add ?digest={hash} to assets in order to bust cache when changes are made.

    The source files are in `static` while the built HTML is in `_static`.
    """
    assets = ["scripts/quantecon-book-theme.js"]
    # Only append the book theme CSS if it's explicitly this theme. Sub-themes
    # will define their own CSS file, so if a sub-theme is used, this code is
    # run but the book theme CSS file won't be linked in Sphinx.
    if app.config.html_theme == "quantecon_book_theme":
        assets.append("styles/quantecon-book-theme.css")
    hash_assets_for_files(assets, get_html_theme_path() / "static", context)


def _string_or_bool(var):
    if isinstance(var, str):
        return var.lower() == "true"
    elif isinstance(var, bool):
        return var
    else:
        return var is None


def setup(app):
    # Configuration for Juypter Book
    app.setup_extension("sphinx_book_theme")
    app.add_js_file("scripts/quantecon-book-theme.js")

    app.connect("html-page-context", add_hub_urls)
    app.connect("builder-inited", add_plugins_list)
    app.connect("html-page-context", hash_html_assets)

    app.add_html_theme("quantecon_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
