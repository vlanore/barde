import sys
from typing import Callable, Optional

from browser import document, html  # type:ignore ; pylint: disable=import-error


PASSAGES = {}

_state = {}

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
                print("yolo")
                global START
                global PASSAGES

                if start:
                    START = func.__name__
                PASSAGES[func.__name__] = func
                return func

            return result

        case _:
            sys.exit(1)


def display(text: str, end=None) -> None:
    document["main"] <= text
    if end is None:
        document["main"] <= html.BR()
    else:
        document["main"] <= end


def link(text: str, target=None, end=None) -> None:
    if target is None:
        target = text

    document["main"] <= html.A(text, href="javascript:void(0);", id=target)
    document["main"] <= " "

    def result(_, func=PASSAGES[target]):
        clear_page()
        func()

    document[target].bind("click", result)

    if end is None:
        document["main"] <= html.BR()
    else:
        document["main"] <= end


def run():
    if START is not None:
        PASSAGES[START]()


if __name__ == "__main__":

    @passage(start=True)
    def hello():
        display(html.H1("Hello, world"))
        display(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
            "tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris",
        )
        display(html.B("I'm bold"))

        link("tralala", end="")
        link("Y", "youpi")

    @passage
    def youpi():
        display("youpida")
        link("hello")

    @passage
    def tralala():
        display("trouloulala")
        link("youpi", end="")
        link("hello")

    run()
