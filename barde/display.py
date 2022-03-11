from typing import Any, Callable

from browser import document  # type:ignore ; pylint: disable=import-error
from browser import html as bh  # type:ignore ; pylint: disable=import-error
from browser import markdown as mk  # type:ignore ; pylint: disable=import-error

from barde.state import STATE


NEXT_ID = 0


def get_id() -> str:
    global NEXT_ID
    my_id = NEXT_ID
    NEXT_ID += 1
    return f"id_{my_id}"


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

        def result(
            _, func=target_func, func_args: dict[str, Any] = kwargs.copy()
        ) -> None:
            for key, value in func_args.items():
                if callable(value):
                    func_args[key] = value()

            print("Pouic")
            document["main"].clear()
            document["sidebar-content"].clear()

            STATE["last_passage"] = target_str
            STATE["last_passage_args"] = func_args
            func(
                Output(document["main"]),
                Output(document["sidebar-content"]),
                **func_args,
            )

        document[target_str].bind("click", result)
        document[target_str].id = ""

    def image(self, src: str) -> None:
        self.target <= bh.IMG(src=src)

    def text_input(self):
        my_id = get_id()

        self.target <= bh.INPUT(type="text", id=my_id)

        return lambda: document[my_id].value
