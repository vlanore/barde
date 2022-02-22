from typing import Callable

from browser import document  # type:ignore ; pylint: disable=import-error
from browser import html as bh  # type:ignore ; pylint: disable=import-error
from browser import markdown as mk  # type:ignore ; pylint: disable=import-error

from barde.passage import STATE


def clear_page():
    document["main"].clear()


def display(text, markdown=True) -> None:
    if markdown:
        mark, _ = mk.mark(text)
        document["main"].html += mark
    else:
        document["main"].html += text


def title(text) -> None:
    document["main"] <= bh.H1(text)


def display_sidebar(content: str, markdown=True) -> None:
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
