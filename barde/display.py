from typing import Callable

from browser import document  # type:ignore ; pylint: disable=import-error
from browser import html as bh  # type:ignore ; pylint: disable=import-error
from browser import markdown as mk  # type:ignore ; pylint: disable=import-error

from barde.state import STATE


class Output:
    def __init__(self, target) -> None:
        self.target = target

    def clear_page(self):
        self.target.clear()

    def display(self, text, markdown=True) -> None:
        if markdown:
            mark, _ = mk.mark(text)
            self.target.html += mark
        else:
            self.target.html += text

    def title(self, text) -> None:
        self.target <= bh.H1(text)

    def link(self, target_func: Callable, text: str, **kwargs) -> None:
        target_str = target_func.__name__
        if text == "":
            text = target_str

        self.target <= bh.A(text, href="javascript:void(0);", id=target_str)
        self.target <= " "

        def result(_, func=target_func, func_args=kwargs.copy()):
            print("Pouic")
            document["main"].clear()
            document["sidebar-content"].clear()

            STATE["last_passage"] = target_str
            STATE["last_passage_args"] = kwargs
            func(
                Output(document["main"]),
                Output(document["sidebar-content"]),
                **func_args
            )

        document[target_str].bind("click", result)
        document[target_str].id = ""

    def image(self, src: str):
        self.target <= bh.IMG(src=src)
