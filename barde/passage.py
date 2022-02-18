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

def hide_sidebar(_event):
    document["open-sidebar"].style="display:block;"
    document["sidebar-box"].style="display:none;"
    document["hide-sidebar"].unbind("click")
    document["open-sidebar"].bind("click", open_sidebar)
    document["body"].style="grid-template-columns: 0 1fr min(95vw, 700px) 1fr 0;"


def open_sidebar(_event):
    document["open-sidebar"].style="display:none;"
    document["open-sidebar"].unbind("click")
    document["sidebar-box"].style="display:block;"
    document["hide-sidebar"].bind("click", hide_sidebar)
    document["body"].style="grid-template-columns: max(25vw, 140px) 1fr min(70vw, 700px) 1fr 0;"


def dark_mode(_event):
    """Toggle on dark mode."""
    document["theme-select"].clear()
    link = document["theme-select"] <= bh.A("light", href="javascript:void(0);")
    document["theme-select"] <= " - dark"
    link.unbind("click")
    print("1")
    link.bind("click", light_mode)
    document["stylesheet"].rel = "stylesheet alternate"
    document["stylesheet-dark"].rel = "stylesheet"
    document["html"].setAttribute("data-theme", "dark")
    STATE["style-mode"] = "dark"


def light_mode(_event):
    """Toggle on light mode."""
    document["theme-select"].clear()
    document["theme-select"] <= "light - "
    link = document["theme-select"] <= bh.A("dark", href="javascript:void(0);")
    link.unbind("click")
    print("1")
    link.bind("click", dark_mode)
    document["stylesheet"].rel = "stylesheet"
    document["stylesheet-dark"].rel = "stylesheet alternate"
    document["html"].setAttribute("data-theme", "light")
    STATE["style-mode"] = "light"


def select_style():
    """Select style mode (light or dark) based on stored data."""
    if "style-mode" in STATE.keys():
        match STATE["style-mode"]:
            case "light":
                light_mode(None)
            case "dark":
                dark_mode(None)
    else:
        light_mode(None)


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


def display_sidebar(content: str, markdown=False) -> None:
    if markdown:
        mark, _ = mk.mark(content)
        document["sidebar-content"].html += mark
    else:
        document["sidebar-content"].html += content


def link(target_func: Callable, text: str = "") -> None:
    target_str = target_func.__name__
    if text == "":
        text = target_str

    document["main"] <= bh.A(text, href="javascript:void(0);", id=target_str)
    document["main"] <= " "

    def result(_, func=target_func):
        clear_page()
        STATE["last_passage"] = target_str
        func()

    document[target_str].bind("click", result)


def image(src: str):
    document["main"] <= bh.IMG(src=src)


def restart(_event):
    document["main"].clear()
    document["sidebar-content"].clear()
    STATE.clear()
    run()


def run():
    document["hide-sidebar"].bind("click", hide_sidebar)

    select_style()
    document["restart"].bind("click", restart)

    if "last_passage" in STATE.keys():
        PASSAGES[STATE["last_passage"]]()
    elif START is not None:
        PASSAGES[START]()


if __name__ == "__main__":

    @passage(start=True)
    def init():
        STATE["a"] = 1
        display_sidebar("**Stats**<br/>Strenght: *3*<br/>Dex: *4*", markdown=True)
        hello()

    @passage
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
        markdown("uis nostrud exercitation ullamco labori\n " * 60)
        html(f"<i>Number: </i>{STATE['a']}<br/><br/>")
        link(tralala)
        link(youpi, "ioupi")

    @passage
    def youpi():
        title("Youpi")
        markdown("youpida")
        image(
            "https://upload.wikimedia.org/wikipedia/commons/8/87/Old_book_bindings.jpg"
        )

        STATE["a"] += 1

        link(hello)

    @passage
    def tralala():
        title("Tralala")
        markdown("trouloulala")
        link(youpi)
        link(hello)

    run()
