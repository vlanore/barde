from typing import Callable

from browser import document  # type:ignore ; pylint: disable=import-error
from browser import html as bh  # type:ignore ; pylint: disable=import-error
from browser import markdown as mk  # type:ignore ; pylint: disable=import-error

from barde.state import STATE


NEXT_ID = 0


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

    def link(
        self, target_func: Callable, text: str, arg_func: Callable = lambda: {}
    ) -> None:
        target_str = target_func.__name__
        if text == "":
            text = target_str

        self.target <= bh.A(text, href="javascript:void(0);", id=target_str)
        self.target <= " "

        def result(_, func=target_func, arg_func=arg_func) -> None:
            kwargs = arg_func()

            print("Pouic")
            document["main"].clear()
            document["sidebar-content"].clear()

            STATE["last_passage"] = target_str
            STATE["last_passage_args"] = kwargs
            func(
                Output(document["main"]),
                Output(document["sidebar-content"]),
                **kwargs,
            )

        document[target_str].bind("click", result)
        document[target_str].id = ""

    def image(self, src: str) -> None:
        self.target <= bh.IMG(src=src)

    def text_input(self):
        global NEXT_ID
        my_id = NEXT_ID
        NEXT_ID += 1

        self.target <= bh.INPUT(type="text", id=f"id_{my_id}")

        return lambda: document[f"id_{my_id}"].value
