# -- Project information -----------------------------------------------------
import os

project = "Quantecon Book Theme"
copyright = "2020"
author = "The Quantecon Project"

master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinxcontrib.bibtex",
    "sphinx_thebe",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "pst": ("https://pydata-sphinx-theme.readthedocs.io/en/latest/", None),
}
nitpick_ignore = [
    ("py:class", "docutils.nodes.document"),
    ("py:class", "docutils.parsers.rst.directives.body.Sidebar"),
]

suppress_warnings = ["myst.domains", "ref.ref"]

numfig = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "quantecon_book_theme"
html_logo = "_static/qe-logo.png"
html_title = "Quantecon Book Theme"
html_copy_source = True
html_sourcelink_suffix = ""
html_favicon = "_static/qe-logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
nb_execution_mode = "cache"
thebe_config = {
    "repository_url": "https://github.com/binder-examples/jupyter-stacks-datascience",
    "repository_branch": "master",
}

html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/QuantEcon/quantecon-book-theme",
    # "repository_branch": "gh-pages",  # For testing
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        # "jupyterhub_url": "https://datahub.berkeley.edu",  # For testing
        "colab_url": "https://colab.research.google.com/",
        "notebook_interface": "jupyterlab",
        "thebe": True,
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "expand_sections": ["reference/index"],
    # For testing
    # "home_page_in_toc": True,
    # "single_page": True
    # "extra_footer": "<a href='https://google.com'>Test</a>",
    # "extra_navbar": "<a href='https://google.com'>Test</a>",
}
bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"


def setup(app):
    # -- To demonstrate ReadTheDocs switcher -------------------------------------
    # This links a few JS and CSS files that mimic the environment that RTD uses
    # so that we can test RTD-like behavior. We don't need to run it on RTD and we
    # don't wanted it loaded in GitHub Actions because it messes up the lighthouse
    # results.
    if not os.environ.get("READTHEDOCS") and not os.environ.get("GITHUB_ACTIONS"):
        app.add_css_file(
            "https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css"
        )
        app.add_css_file("https://assets.readthedocs.org/static/css/badge_only.css")

        # Create the dummy data file so we can link it
        # ref: https://github.com/readthedocs/readthedocs.org/blob/bc3e147770e5740314a8e8c33fec5d111c850498/readthedocs/core/static-src/core/js/doc-embed/footer.js  # noqa: E501
        app.add_js_file("rtd-data.js")
        app.add_js_file(
            "https://assets.readthedocs.org/static/javascript/readthedocs-doc-embed.js",
            priority=501,
        )
