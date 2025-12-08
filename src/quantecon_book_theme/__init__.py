"""A lightweight book theme based on the pydata sphinx theme."""

from pathlib import Path
import os
import hashlib
from functools import lru_cache
import subprocess
from datetime import datetime, timezone

from docutils import nodes
from sphinx.util import logging
from bs4 import BeautifulSoup as bs
from sphinx.util.fileutil import copy_asset
from sphinx.util.osutil import ensuredir

from .launch import add_hub_urls

__version__ = "0.15.0"
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
        outdir = app.outdir / "plugins"
        ensuredir(outdir)
        for i, asset in enumerate(app.config.html_theme_options["plugins_list"]):
            assetname = Path(asset).name
            copy_asset(app.confdir + "/" + asset, outdir)
            app.config.html_theme_options["plugins_list"][i] = "plugins/" + assetname


def get_git_last_modified(source_file, source_dir):
    """Get the last modified date for a source file from git.

    Args:
        source_file: The source file path relative to source_dir
        source_dir: The Sphinx source directory

    Returns:
        datetime object or None if git is not available
    """
    try:
        # Get the full path to the source file
        file_path = Path(source_dir) / source_file

        # Check if git is available and we're in a git repo
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=source_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None

        # Get the last commit date for this file
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--follow", "--", str(file_path)],
            cwd=source_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0 and result.stdout.strip():
            timestamp = int(result.stdout.strip())
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    except (
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
        ValueError,
        FileNotFoundError,
    ):
        pass

    return None


def get_git_changelog(source_file, source_dir, max_entries=10):
    """Get the changelog for a source file from git.

    Args:
        source_file: The source file path relative to source_dir
        source_dir: The Sphinx source directory
        max_entries: Maximum number of changelog entries to return

    Returns:
        List of dicts with keys: hash, author, date, message, relative_time
        Empty list if git is not available
    """
    try:
        # Get the full path to the source file
        file_path = Path(source_dir) / source_file

        # Check if git is available and we're in a git repo
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=source_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return []

        # Get the changelog with format: hash|author|timestamp|subject
        result = subprocess.run(
            [
                "git",
                "log",
                f"-{max_entries}",
                "--format=%h|%an|%ct|%s",
                "--follow",
                "--",
                str(file_path),
            ],
            cwd=source_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return []

        changelog = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|", 3)
            if len(parts) == 4:
                commit_hash, author, timestamp, message = parts
                commit_time = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
                relative_time = get_relative_time(commit_time)

                changelog.append(
                    {
                        "hash": commit_hash,
                        "author": author,
                        "date": commit_time,
                        "message": message,
                        "relative_time": relative_time,
                    }
                )

        return changelog

    except (
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
        ValueError,
        FileNotFoundError,
    ):
        pass

    return []


def get_relative_time(past_date):
    """Convert a datetime to relative time string (e.g., '3 months ago')."""
    now = datetime.now(timezone.utc)
    # Ensure past_date is timezone-aware for comparison
    if past_date.tzinfo is None:
        past_date = past_date.replace(tzinfo=timezone.utc)
    diff = now - past_date

    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"


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
            if github_repo in str(app.srcdir):
                index = str(app.srcdir).rfind(github_repo)
                branch = config_theme.get("nb_branch", "")
                if branch == "":
                    branch = "main"
                folder = str(app.srcdir)[index + len(github_repo) :]
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
    if os.path.isdir(app.outdir / "_pdf"):
        if "pdf_book_name" not in context:
            context["pdf_book_name"] = app.config.latex_documents[0][1].replace(
                ".tex", ""
            )
        context["pdf_book_path"] = "/_pdf/" + context["pdf_book_name"] + ".pdf"

    # check if notebook folder is present
    if os.path.isdir(app.outdir / "_notebooks"):
        if "download_nb_path" in app.config.html_theme_options:
            context["notebook_path"] = (
                app.config.html_theme_options["download_nb_path"]
                + "/_notebooks/"
                + context["pagename"]
                + ".ipynb"
            )
        else:
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

    # Add git information (last modified date and changelog)
    if doctree and hasattr(app.env, "doc2path"):
        source_file = app.env.doc2path(pagename, base=False)
        source_dir = app.srcdir

        # Get last modified date
        last_modified = get_git_last_modified(source_file, source_dir)
        if last_modified:
            # Get date format from theme options, default to "%b %d, %Y"
            date_format = config_theme.get("last_modified_date_format", "%b %d, %Y")
            context["last_modified_date"] = last_modified.strftime(date_format)
            context["last_modified_iso"] = last_modified.isoformat()
        else:
            context["last_modified_date"] = None

        # Get changelog entries
        max_changelog_entries = config_theme.get("changelog_max_entries", 10)
        changelog = get_git_changelog(source_file, source_dir, max_changelog_entries)
        context["changelog_entries"] = changelog
        context["has_git_info"] = last_modified is not None and len(changelog) > 0

        # Add repository URL and source file for GitHub links
        repo_url = config_theme.get("repository_url", "")
        if repo_url:
            context["theme_repository_url"] = repo_url.rstrip("/")
            # Construct full path including path_to_docs
            path_to_docs = config_theme.get("path_to_docs", "")
            if path_to_docs:
                full_source_path = f"{path_to_docs}/{source_file}".replace("//", "/")
            else:
                full_source_path = source_file
            context["theme_source_file"] = full_source_path
        else:
            context["theme_repository_url"] = None
            context["theme_source_file"] = None
    else:
        context["last_modified_date"] = None
        context["changelog_entries"] = []
        context["has_git_info"] = False
        context["theme_repository_url"] = None
        context["theme_source_file"] = None

    # Make sure the context values are bool
    blns = [
        "theme_use_edit_page_button",
        "theme_use_repository_button",
        "theme_use_issues_button",
        "theme_enable_rtl",
    ]
    for key in blns:
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
            # Use .filename attribute to avoid deprecation warnings in Sphinx 9+
            for i, css_or_js in enumerate(context[asset_type]):
                filename = getattr(css_or_js, "filename", None)
                # Skip if filename attribute doesn't exist
                if filename is None:
                    continue
                if filename == asset_sphinx_link:
                    hash = _gen_hash(asset_source_path)
                    context[asset_type][i] = asset_sphinx_link + "?digest=" + hash
                    break


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


def add_pygments_style_class(app, pagename, templatename, context, doctree):
    """Add CSS class to root element if QuantEcon theme code style is disabled.

    When qetheme_code_style is False, adds 'use-pygments-style' class which
    disables the custom QuantEcon code token styles and allows Pygments
    built-in styles (configured via pygments_style) to be used.
    """
    config_theme = app.config.html_theme_options
    qetheme_code_style = config_theme.get("qetheme_code_style", True)

    # Convert string "false"/"true" to boolean if needed
    if isinstance(qetheme_code_style, str):
        qetheme_code_style = qetheme_code_style.lower() != "false"

    # Set a context variable that can be used in templates
    context["use_pygments_style"] = not qetheme_code_style


def setup_pygments_css(app):
    """Ensure Pygments CSS is included when using Pygments styles.

    This runs during builder-inited, after config is fully loaded.
    We generate our own unscoped pygments CSS file instead of using Sphinx's scoped version.
    """
    from pygments.formatters import HtmlFormatter

    # Access html_theme_options from app.config (it's a dict)
    config_theme = getattr(app.config, "html_theme_options", {})
    qetheme_code_style = config_theme.get("qetheme_code_style", True)

    # Convert string "false"/"true" to boolean if needed
    if isinstance(qetheme_code_style, str):
        qetheme_code_style = qetheme_code_style.lower() != "false"

    # When using Pygments styles, generate and include unscoped CSS
    if not qetheme_code_style:
        # Get the Pygments style name from config (default to 'default')
        pygments_style = getattr(app.config, "pygments_style", None) or "default"

        # Generate CSS without data-theme scoping
        formatter = HtmlFormatter(style=pygments_style)
        css_content = formatter.get_style_defs(".highlight")

        # Write CSS file to _static directory with a different name
        # This ensures it won't be overwritten by Sphinx or pydata-sphinx-theme
        static_dir = Path(app.outdir) / "_static"
        static_dir.mkdir(parents=True, exist_ok=True)
        pygments_css_path = static_dir / "pygments-quantecon.css"
        pygments_css_path.write_text(css_content)

        # Add the CSS file to the page (instead of the default pygments.css)
        app.add_css_file("pygments-quantecon.css")


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
    app.add_js_file("scripts/jquery.js")
    app.add_js_file("scripts/_sphinx_javascript_frameworks_compat.js")

    app.connect("html-page-context", add_hub_urls)
    app.connect("builder-inited", add_plugins_list)
    app.connect("builder-inited", setup_pygments_css)
    app.connect("html-page-context", hash_html_assets)
    app.connect("html-page-context", add_pygments_style_class)

    app.add_html_theme("quantecon_book_theme", get_html_theme_path())
    app.connect("html-page-context", add_to_context)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
