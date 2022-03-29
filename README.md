![](barde_banner.svg)

[![Pylint](https://github.com/vlanore/barde/actions/workflows/pylint.yml/badge.svg)](https://github.com/vlanore/barde/actions/workflows/pylint.yml)

**Barde** is a small python framework used to write simple text games and run them in your browser.
Barde is aimed at python beginners and people who don't want to bother building a complex UI.

Barde is heavily inspired by [Twine](https://twinery.org/) but is aimed at people who want to write simple programs instead of focusing on text.
Like twine, Barde runs fully in the browser so as to be easy to host and share.
Like sugarcube, Barde aims at providing some basic game features (saves, sidebar) out of the box so as to minimize the barrier to entry as much as possible.

Barde uses [Brython](https://brython.info/) to run python in the browser.

Barde uses [pico.css](https://picocss.com/) for its default CSS.

## Example
Here is an example of a simple Barde application that defines two passages with some formatting and a link between the two:
```python
from barde import passage, run

@passage(start=True)
def hello(doc, _):
    doc.title("Hello, world")
    doc.display(
        "Lorem ipsum **dolor sit amet**, "
        "consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore.",
        markdown=True
    )
    doc.link(hi, "Click me")

@passage
def hi(doc, _):
    doc.display("Barde says hi")
    
run()
```
