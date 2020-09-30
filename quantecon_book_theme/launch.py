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

    # First decide if we'll insert any links
    path = app.env.doc2path(pagename)

    # If so, insert the URLs depending on the configuration
    config_theme = app.config["html_theme_options"]
    launch_buttons = config_theme.get("launch_buttons", {})
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

def _is_notebook(app, pagename):
    return app.env.metadata[pagename].get("kernelspec")
