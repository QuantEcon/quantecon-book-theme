from setuptools import setup, find_packages
from pathlib import Path

lines = Path("quantecon_book_theme").joinpath("__init__.py")
for line in lines.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break

setup(
    name="quantecon-book-theme",
    version=version,
    python_requires=">=3.6",
    author="Project Jupyter Contributors",
    author_email="jupyter@googlegroups.com",
    # this should be a whitespace separated string of keywords, not a list
    keywords="reproducible science environments scholarship notebook",
    description="Theme for Quantecon lectures",
    long_description=Path("./README.md").read_text(),
    long_description_content_type="text/markdown",
    license="BSD",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "docutils>=0.15",
        "sphinx",
        "click",
        "setuptools",
        "libsass~=0.20.1",
        "sphinx_book_theme~=0.1.0",
        "beautifulsoup4",
        "web-compile",
        'importlib-resources>=3.0,<3.5; python_version < "3.7"',
    ],
    extras_require={
        "code_style": ["flake8<3.8.0,>=3.7.0", "black", "pre-commit~=2.7.0"],
        "sphinx": [
            "folium",
            "numpy",
            "matplotlib",
            "ipywidgets",
            "pandas",
            "nbclient",
            "myst-nb~=0.11.1",
            "sphinx-togglebutton>=0.2.1",
            "sphinx-copybutton",
            "plotly",
            "sphinxcontrib-bibtex~=2.2",
        ],
        "testing": [
            "myst_nb~=0.11.1",
            "coverage",
            "pytest~=6.0.1",
            "pytest-cov",
            "beautifulsoup4",
            "sphinx_thebe",
            "pytest-regressions~=2.0.1",
            "sphinx_copybutton",
        ],
    },
    entry_points={
        "sphinx.html_themes": ["quantecon_book_theme = quantecon_book_theme"]
    },
    package_data={
        "quantecon_book_theme": [
            "theme.conf",
            # Templates
            "*.html",
            "topbar/*.html",
            # Stylesheets
            "scss/*",
            # Other static files
            "static/*",
            "static/images/*",
        ]
    },
    include_package_data=True,
)
