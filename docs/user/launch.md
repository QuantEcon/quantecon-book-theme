# Launch Buttons for Interactivity

Add buttons that allow users to interact with your book's content in the cloud
— via BinderHub, JupyterHub, Google Colab, or Thebe live code cells.

```{contents}
:local:
:depth: 2
```

## Prerequisites

All launch buttons require a configured repository URL:

```python
html_theme_options = {
    ...
    "repository_url": "https://github.com/{your-docs-url}",
    "nb_branch": "{your-branch}",
    "path_to_docs": "{path-relative-to-site-root}",
    ...
}
```

```{margin} Paired ipynb files
If you're using [Jupytext](https://jupytext.readthedocs.io/en/latest/) to
pair an ipynb file with your text files, and that ipynb file is in the same
folder as your content, then Binder/JupyterHub links will point to the ipynb
file instead of the text file.
```

## Binder / BinderHub

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "binderhub_url": "https://{your-binderhub-url}"
    },
    ...
}
```

## JupyterHub

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "jupyterhub_url": "https://{your-jupyterhub-url}"
    },
    ...
}
```

## Google Colab

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "colab_url": "https://{your-colab-url}"
    },
    ...
}
```

### Separate Notebook Repository

If your notebooks live in a separate repository from your documentation:

```python
html_theme_options = {
    ...
    "nb_repository_url": "https://github.com/{your-notebook-repo-url}",
    "nb_branch": "{notebook-repo-branch}",
    "nb_path_to_notebooks": "",  # empty for flat repos, or "notebooks/"
    ...
}
```

## Live Code Cells with Thebe

[Thebe](http://thebe.readthedocs.org/) converts static code blocks into
*interactive* code blocks powered by a Jupyter kernel. Users can run code
on your page without leaving it.

### Setup

Install and enable the [`sphinx-thebe`](https://sphinx-thebe.readthedocs.io/)
extension:

```python
extensions = [
    ...
    "sphinx_thebe",
    ...
]
```

Then activate the UI elements:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "thebe": True,
    },
    ...
}
```

If you also specify a `repository_url`, `sphinx-thebe` will use that repository
for its environment.

```{tip}
You can customize Thebe with the `thebe_config` dictionary in `conf.py`.
This overrides any configuration pulled from `html_theme_options`. See the
[`sphinx-thebe` documentation](https://sphinx-thebe.readthedocs.io/) for details.
```

## Interface Configuration

Control which JupyterLab or Notebook interface is opened:

```python
html_theme_options = {
    ...
    "launch_buttons": {
        "notebook_interface": "jupyterlab",
    },
    ...
}
```

Set the relative path to your documentation:

```python
html_theme_options = {
    ...
    "path_to_docs": "{path-relative-to-repo-root}",
    ...
}
```
