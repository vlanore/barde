import sys
from typing import Callable, Optional

from browser import (  # type:ignore ; pylint: disable=import-error
    document,
    html as bhtml,
    markdown as mk,
)
from browser.local_storage import storage  # type:ignore ; pylint: disable=import-error
from browser.object_storage import (  # type:ignore ; pylint: disable=import-error
    ObjectStorage,
)


PASSAGES = {}

STATE = ObjectStorage(storage)

START: Optional[str] = None


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
    document["main"] <= bhtml.H1(text)


def link(text: str, target=None) -> None:
    if target is None:
        target = text

    document["main"] <= bhtml.A(text, href="javascript:void(0);", id=target)
    document["main"] <= " "

    def result(_, func=PASSAGES[target]):
        clear_page()
        func()

    document[target].bind("click", result)


def image(src: str):
    document["main"] <= bhtml.IMG(src=src)


def run():
    if START is not None:
        PASSAGES[START]()


if __name__ == "__main__":

    STATE["a"] = 1

    @passage(start=True)
    def hello():
        title("Hello, world")
        markdown(
            "Lorem ipsum **dolor sit amet**, "
            "consectetur adipiscing elit, sed do eiusmod "
            "tempor ~incididunt~ ut labore et "
            "dolore magna aliqua.:\n\n"
            f" * Ut enim ad minim veniam: `{STATE['a']} cm`\n"
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
            "https://upload.wikimedia.org/wikipedia/"
            "commons/c/c9/Lute_2%2C_MfM.Uni-Leipzig.jpg"
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
