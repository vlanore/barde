import sys
from typing import Callable, Optional

from browser import (  # type:ignore ; pylint: disable=import-error
    document,
    html as bh,
    markdown as mk,
)
from browser.local_storage import storage  # type:ignore ; pylint: disable=import-error
from browser.object_storage import (  # type:ignore ; pylint: disable=import-error
    ObjectStorage,
)


PASSAGES = {}

STATE = ObjectStorage(storage)

START: Optional[str] = None


def night_mode(_event):
    """Toggle on night mode."""
    document["night-mode"].clear()
    link = document["night-mode"] <= bh.A("☀️", href="javascript:void(0);")
    link.bind("click", day_mode)
    document["stylesheet"].rel = "stylesheet alternate"
    document["stylesheet-dark"].rel = "stylesheet"
    STATE["style-mode"] = "night"


def day_mode(_event):
    """Toggle on day mode."""
    document["night-mode"].clear()
    link = document["night-mode"] <= bh.A("🌙", href="javascript:void(0);")
    link.bind("click", night_mode)
    document["stylesheet"].rel = "stylesheet"
    document["stylesheet-dark"].rel = "stylesheet alternate"
    STATE["style-mode"] = "day"


def select_style():
    """Select style mode (day or night) based on stored data."""
    if "style-mode" in STATE.keys():
        match STATE["style-mode"]:
            case "day":
                day_mode(None)
            case "night":
                night_mode(None)
    else:
        day_mode(None)


select_style()


def clear_page():
    document["main"].clear()


def passage(*args, **kwargs):
    """Decorator used to define a passage.

    Works without arguments, or with a single start(bool) arguments that denotes that
    this passage is the starting passage."""

    match args, kwargs:
        case [func], {} if callable(func):
            global PASSAGES
            PASSAGES[func.__name__] = func
            return func

        case ([start], {}) | ([], {"start": start}) if isinstance(start, bool):

            def result(func: Callable, start=start):
                global START
                global PASSAGES

                if start:
                    START = func.__name__
                PASSAGES[func.__name__] = func
                return func

            return result

        case _:
            sys.exit(1)


def markdown(text) -> None:
    mark, _ = mk.mark(text)
    document["main"].html += mark


def html(text) -> None:
    document["main"].html += text


def title(text) -> None:
    document["main"] <= bh.H1(text)


def link(text: str, target=None) -> None:
    if target is None:
        target = text

    document["main"] <= bh.A(text, href="javascript:void(0);", id=target)
    document["main"] <= " "

    def result(_, func=PASSAGES[target]):
        clear_page()
        STATE["last_passage"] = target
        func()

    document[target].bind("click", result)


def image(src: str):
    document["main"] <= bh.IMG(src=src)


def run():
    if "last_passage" in STATE.keys():
        PASSAGES[STATE["last_passage"]]()
    elif START is not None:
        PASSAGES[START]()


if __name__ == "__main__":

    @passage(start=True)
    def init():
        STATE["a"] = 1
        hello()

    @passage(start=True)
    def hello():
        title("Hello, world")
        markdown(
            "Lorem ipsum **dolor sit amet**, "
            "consectetur adipiscing elit, sed do eiusmod "
            "tempor <b>incididunt</b> ut labore et "
            "dolore magna aliqua.:\n\n"
            f" * Ut enim ad minim veniam: `{STATE['a']}cm`\n"
            " * quis nostrud exercitation ullamco laboris",
        )
        html(f"<i>Number: </i>{STATE['a']}<br/><br/>")
        link("tralala")
        link("Y", "youpi")

    @passage
    def youpi():
        title("Youpi")
        markdown("youpida")
        image(
            "https://upload.wikimedia.org/wikipedia/commons/8/87/Old_book_bindings.jpg"
        )

        STATE["a"] += 1

        link("hello")

    @passage
    def tralala():
        title("Tralala")
        markdown("trouloulala")
        link("youpi")
        link("hello")

    run()
