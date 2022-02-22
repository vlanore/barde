import sys
from typing import Callable, Optional

from browser import (  # type:ignore ; pylint: disable=import-error
    document,
    html as bh,
)
from browser.local_storage import storage  # type:ignore ; pylint: disable=import-error
from browser.object_storage import (  # type:ignore ; pylint: disable=import-error
    ObjectStorage,
)


PASSAGES = {}

STATE = ObjectStorage(storage)

START: Optional[str] = None


def hide_sidebar(_event):
    document["open-sidebar"].style = "display:block;"
    document["sidebar-box"].style = "display:none;"
    document["hide-sidebar"].unbind("click")
    document["open-sidebar"].bind("click", open_sidebar)
    document["body"].style = "grid-template-columns: 0 1fr min(95vw, 700px) 1fr;"


def open_sidebar(_event):
    document["open-sidebar"].style = "display:none;"
    document["open-sidebar"].unbind("click")
    document["sidebar-box"].style = "display:block;"
    document["hide-sidebar"].bind("click", hide_sidebar)
    document[
        "body"
    ].style = (
        "grid-template-columns: max(min(25vw, 300px), 140px) 1fr min(70vw, 700px) 1fr;"
    )


def dark_mode(_event):
    """Toggle on dark mode."""

    document["dark-mode"].html = "dark"
    document["dark-mode"].unbind("click")

    document["light-mode"].html = '<a href="javascript:void(0);">light</a>'
    document["light-mode"].bind("click", light_mode)

    document["html"].setAttribute("data-theme", "dark")

    STATE["style-mode"] = "dark"


def light_mode(_event):
    """Toggle on light mode."""

    document["light-mode"].html = "light"
    document["light-mode"].unbind("click")

    document["dark-mode"].html = '<a href="javascript:void(0);">dark</a>'
    document["dark-mode"].bind("click", dark_mode)

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
