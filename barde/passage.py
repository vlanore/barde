from typing import Callable, Optional
from browser import document, html

_passages = {}

_state = {}

_start: Optional[str] = None


def clear_page():
    document.clear()


def passage(*args, **kwargs):
    """Decorator used to define a passage.

    Works without arguments, or with a single start(bool) arguments that denotes that
    this passage is the starting passage."""

    match args, kwargs:
        case [func], {} if callable(func):
            global _passages
            _passages[func.__name__] = func
            return func

        case ([start], {}) | ([], {"start": start}) if type(start) == bool:

            def result(func: Callable, start=start):
                print("yolo")
                global _start
                global _passages

                if start:
                    _start = func.__name__
                _passages[func.__name__] = func
                return func

            return result

        case _:
            exit(1)


def display(text: str, end=None) -> None:
    document <= text
    if end is None:
        document <= html.BR()
    else:
        document <= end


def link(text: str, target=None, end=None) -> None:
    if target is None:
        target = text

    document <= html.A(text, href="javascript:void(0);", id=target)
    document <= " "

    def result(_, f=_passages[target]):
        clear_page()
        f()

    document[target].bind("click", result)

    if end is None:
        document <= html.BR()
    else:
        document <= end


def run():
    if _start is not None:
        _passages[_start]()


if __name__ == "__main__":

    @passage(start=True)
    def hello():
        display("Hello", end="")
        display(" world")
        display("Hi there")

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
