from pathlib import Path
from typing import Any, Dict, Optional

from docutils.nodes import document
from sphinx.application import Sphinx
from sphinx.util import logging
from shutil import copy2


SPHINX_LOGGER = logging.getLogger(__name__)


def add_hub_urls(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: Optional[document],
):
    """Builds a binder link and inserts it in HTML context for use in templating.

    This is a ``html-page-context`` sphinx event (see :ref:`sphinx:events`).

    :param pagename: The sphinx docname related to the page
    :param context: A dictionary of values that are given to the template engine,
        to render the page and can be modified to include custom values.
    :param doctree: A doctree when the page is created from a reST documents;
        it will be None when the page is created from an HTML template alone.

    """

    # If so, insert the URLs depending on the configuration
    config_theme = app.config["html_theme_options"]
    launch_buttons = config_theme.get("launch_buttons", {})

    repo_url = _get_repo_url(config_theme)

    # Parse the repo parts from the URL
    org, repo = _split_repo_url(repo_url)

    context["binder_url"] = (
        f"{config_theme['binderhub_url']}/v2/gh/{org}/{repo}/master?"
        f"urlpath=tree/{ pagename }.ipynb"
    )

    if org is None and repo is None:
        # Skip the rest because the repo_url isn't right
        return

    if not launch_buttons or not _is_notebook(app, pagename):
        return

    # Check if we have a markdown notebook, and if so then add a link to the context
    if (
        _is_notebook(app, pagename)
        and "sourcename" in context
        and context["sourcename"].endswith(".md")
    ):
        # Figure out the folders we want
        build_dir = Path(app.outdir).parent
        ntbk_dir = build_dir.joinpath("jupyter_execute")
        sources_dir = build_dir.joinpath("html", "_sources")
        # Paths to old and new notebooks
        path_ntbk = ntbk_dir.joinpath(pagename).with_suffix(".ipynb")
        path_new_notebook = sources_dir.joinpath(pagename).with_suffix(".ipynb")
        # Copy the notebook to `_sources` dir so it can be downloaded
        path_new_notebook.parent.mkdir(exist_ok=True, parents=True)
        copy2(path_ntbk, path_new_notebook)
        context["ipynb_source"] = pagename + ".ipynb"

    # Add thebe flag in context
    if launch_buttons.get("thebe", False):
        context["use_thebe"] = True


def _split_repo_url(url):
    """Split a repository URL into an org / repo combination."""
    if "github.com/" in url:
        end = url.split("github.com/")[-1]
        org, repo = end.split("/")[:2]
    else:
        SPHINX_LOGGER.warning(
            f"Currently Binder/JupyterHub repositories must be on GitHub, got {url}"
        )
        org = repo = None
    return org, repo


def _get_repo_url(config):
    repo_url = config.get("nb_repository_url")
    if not repo_url:
        raise ValueError(
            "You must provide the key: `repository_url` to use launch buttons."
        )
    return repo_url


def _is_notebook(app, pagename):
    return app.env.metadata[pagename].get("kernelspec")
