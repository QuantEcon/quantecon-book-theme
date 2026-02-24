# -- Project information -----------------------------------------------------

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
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "RTL_SUPPORT.md"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
nitpick_ignore = [
    ("py:class", "docutils.nodes.document"),
    ("py:class", "docutils.parsers.rst.directives.body.Sidebar"),
]

numfig = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
# We use pydata-sphinx-theme for the documentation site itself, while
# quantecon_book_theme is the theme being documented.
html_theme = "pydata_sphinx_theme"
html_logo = "_static/qe-logo.png"
html_title = "QuantEcon Book Theme"
html_copy_source = True
html_sourcelink_suffix = ""
html_favicon = "_static/qe-logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
nb_execution_mode = "auto"

# -- Togglebutton configuration ----------------------------------------------
togglebutton_hint = "Show"
togglebutton_hint_hide = "Hide"

html_theme_options = {
    "github_url": "https://github.com/QuantEcon/quantecon-book-theme",
    "use_edit_page_button": True,
    "show_prev_next": True,
    "navigation_with_keys": False,
    "header_links_before_dropdown": 6,
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/quantecon-book-theme/",
            "icon": "fas fa-box",
        },
    ],
}

html_context = {
    "github_user": "QuantEcon",
    "github_repo": "quantecon-book-theme",
    "github_version": "main",
    "doc_path": "docs",
}

bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"
