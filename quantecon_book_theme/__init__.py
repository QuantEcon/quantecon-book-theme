"""A lightweight book theme based on the pydata sphinx theme."""
from pathlib import Path
import os

from docutils import nodes
from sphinx.util import logging
from bs4 import BeautifulSoup as bs
from sphinx.util.fileutil import copy_asset
from sphinx.util.osutil import ensuredir

from .launch import add_hub_urls

__version__ = "0.2.3"
"""quantecon-book-theme version"""

SPHINX_LOGGER = logging.getLogger(__name__)
MESSAGE_CATALOG_NAME = "booktheme"


def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = str(Path(__file__).parent.absolute())
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


def add_static_path(app):
    """Ensure CSS/JS is loaded."""
    static_path = Path(__file__).parent.joinpath("static").absolute()
    app.config.html_static_path.append(str(static_path))

    # copying plugins
    if "plugins_list" in app.config.html_theme_options:
        outdir = app.outdir + "/plugins"
        ensuredir(outdir)
        for i, asset in enumerate(app.config.html_theme_options["plugins_list"]):
            assetname = Path(asset).name
            copy_asset(app.confdir + "/" + asset, outdir)
            app.config.html_theme_options["plugins_list"][i] = "plugins/" + assetname

    # Javascript
    for fname in static_path.iterdir():
        if ".js" in fname.suffix:
            app.add_js_file(fname.name)


def add_to_context(app, pagename, templatename, context, doctree):
    """ Functions and variable additions to context."""

    def sbt_generate_nav_html(
        level=1,
        include_item_names=False,
        with_home_page=False,
    ):
        # Config stuff
        if isinstance(with_home_page, str):
            with_home_page = with_home_page.lower() == "true"

        # Grab the raw toctree object and structure it so we can manipulate it
        toc_sphinx = context["generate_nav_html"](
            startdepth=level - 1,
            maxdepth=level + 1,
            kind="sidebar",
            collapse=False,
            titles_only=True,
            includehidden=True,
        )
        toctree = bs(toc_sphinx, "html.parser")

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
                branch = context["github_version"]
                folder = app.srcdir[index + len(github_repo) :]
                return "/tree/" + branch + folder
        return ""

    # Pull metadata about the master doc
    master_doc = app.config["master_doc"]
    master_doctree = app.env.get_doctree(master_doc)
    master_url = context["pathto"](master_doc)
    context["master_url"] = master_url

    # default value is book.tex
    context["pdf_book_name"] = app.config.latex_documents[0][1].replace(".tex", "")
    context["github_sourcefolder"] = get_github_src_folder(app)

    context["sbt_generate_nav_html"] = sbt_generate_nav_html
    context["generate_toc_html"] = generate_toc_html

    # check if book pdf folder is present
    if os.path.isdir(app.outdir + "/_pdf"):
        context["pdf_book_path"] = "_pdf/" + context["pdf_book_name"] + ".pdf"

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
            (app.config.html_baseurl.rstrip("/"), "_static/" + context["logo"])
        )

    # Add HTML context variables that the pydata theme uses that we configure elsewhere
    # For some reason the source_suffix sometimes isn't there even when doctree is
    if doctree and context.get("page_source_suffix"):
        config_theme = app.config.html_theme_options
        repo_url = config_theme.get("repository_url", "")
        # Only add the edit button if `repository_url` is given
        if repo_url:
            branch = config_theme.get("repository_branch")
            if not branch:
                # Explicitly check in cae branch is ""
                branch = "master"
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

    # Make sure the context values are bool
    btns = [
        "theme_use_edit_page_button",
        "theme_use_repository_button",
        "theme_use_issues_button",
    ]
    for key in btns:
        if key in context:
            context[key] = _string_or_bool(context[key])


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

    app.connect("html-page-context", add_hub_urls)
    app.connect("builder-inited", add_static_path)

    app.add_html_theme("quantecon_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
