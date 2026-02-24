# Layout and Page Elements

Control page structure, navigation, and content layout.

```{contents}
:local:
:depth: 2
```

## Sidebars

There are two kinds of sidebar-like content in `quantecon-book-theme`:
standard `{sidebar}` directives and a theme-specific `{margin}` directive.

```{tip}
Sidebar content will generally overlap with the right-hand TOC space.
When sidebar content scrolls into view, the TOC hides automatically.
```

### Margins

Content that pops out to the right margin at wide viewports (≥1200px):

````
```{margin} **My margin title**
Here is my margin content, it is pretty cool!
```
````

```{admonition} Margin example
:class: tip
In the quantecon-book-theme, this pops out to the right margin:

**Here is my margin content** — It is pretty cool!
```

### Content sidebars

In-line sidebars that allow page text to flow around them:

````
```{sidebar} **My sidebar title**
Here is my sidebar content, it is pretty cool!
```
````

Note how the content wraps around the sidebar. Some elements (notes, code
cells) may clash with sidebars — try `{margin}` instead if this happens.

````{sidebar} **My sidebar title**
```{note}
Here is my sidebar content, it is pretty cool!
```
![](../images/cool.jpg)
````

### Content in margins and sidebars

Sidebar/margin content supports code blocks:

````{admonition} Margin example — Code blocks
:class: tip
In the theme, this renders as a code block in the right margin:
```python
print("here is some python")
```
````

`````
````{margin} Code blocks in margins
```python
print("here is some python")
```
````
`````

As well as admonitions and images:

````{admonition} Margin example — Notes
:class: tip
In the theme, this renders as a note in the right margin:
```{note}
Wow, a note with an image in a margin!
![](../images/cool.jpg)
```
````

`````
````{margin} **Notes in margins**
```{note}
Wow, a note with an image in a margin!
![](../images/cool.jpg)
```
````
`````

### Margin figure captions

A figure with a caption to the right:

```{figure} ../images/cool.jpg
---
width: 60%
figclass: margin-caption
alt: My figure text
name: myfig5
---
And here is my figure caption
```

Reference with {ref}`myfig5` or {numref}`myfig5`.

A figure with caption below, placed in the margin:

```{figure} ../images/cool.jpg
---
figclass: margin
alt: My figure text
name: myfig4
---
And here is my figure caption
```

Reference with {ref}`myfig4` or {numref}`myfig4`.

## Full-Width Content

Extend content into the right margin by adding the `full-width` class:

````
```{note}
:class: full-width
This content will be full-width
```
````

```{note}
:class: full-width
This content will be full-width
```

```{tip} A note for ipynb users
If you are using a Jupyter Notebook as inputs to your documentation using the
[MyST-NB extension](https://myst-nb.readthedocs.io/en/latest/), you can trigger
this behavior with a code cell by adding a `full-width` tag to the cell.
```

## Quotations and Epigraphs

A standard quote:

> Here's my quote, it's pretty neat.
> I wonder how many lines I can create with
> a single stream-of-consciousness quote.
> I could try to add a list of ideas to talk about.
> I suppose I could just keep going on forever,
> but I'll stop here.

An epigraph draws more attention:

```{epigraph}
Here's my quote, it's pretty neat.
I wonder how many lines I can create with
a single stream-of-consciousness quote.
I could try to add a list of ideas to talk about.
I suppose I could just keep going on forever,
but I'll stop here.
```

With attribution:

```{epigraph}
Here's my quote, it's pretty neat.
I wonder how many lines I can create with
a single stream-of-consciousness quote.
I could try to add a list of ideas to talk about.
I suppose I could just keep going on forever,
but I'll stop here.

-- Jo the Jovyan, *[the jupyter book docs](https://jupyterbook.org/v1/)*
```

## Controlling the Left Navigation Bar

### Expand sections

Keep sub-sections permanently expanded:

```python
html_theme_options = {
    ...
    "expand_sections": ["list", "of", "pages"],
    ...
}
```

### Add a header to the TOC

Use `:caption: My header text` in your `toctree` directive.

### Show the home page in the TOC

```python
html_theme_options = {
    ...
    "home_page_in_toc": True,
    ...
}
```
