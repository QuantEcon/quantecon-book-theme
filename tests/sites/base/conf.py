# -- Project information -----------------------------------------------------

project = "Sphinx Book Theme"
copyright = "2020, Executable Book Project"
author = "Executable Book Project"

master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_nb", "sphinx_togglebutton", "sphinx_thebe"]
html_theme = "quantecon_book_theme"
html_baseurl = "https://sphinx-book-theme.readthedocs.org"
html_copy_source = True
html_sourcelink_suffix = ""
nb_execution_mode = "auto"

# Base options, we can add other key/vals later
html_theme_options = {
    "path_to_docs": "TESTPATH",
    "repository_url": "https://github.com/executablebooks/sphinx-book-theme",
    "nb_repository_url": "https://github.com/executablebooks/sphinx-book-theme",
    "navigation_with_keys": True,
    # "repository_branch": "main",  # Not using this, should default to main
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "jupyterhub_url": "https://datahub.berkeley.edu",
        "colab_url": "https://colab.research.google.com",
        "notebook_interface": "jupyterlab",
        "thebe": True,
    },
}
