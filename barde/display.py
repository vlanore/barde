from typing import Any, Callable

from browser import document  # type:ignore ; pylint: disable=import-error
from browser import html as bh  # type:ignore ; pylint: disable=import-error
from browser import markdown as mk  # type:ignore ; pylint: disable=import-error

from barde.state import STATE

NEXT_ID = 0


def call_passage(passage: Callable, **params: dict[str, Any]) -> None:
    document["main"].clear()
    document["sidebar-content"].clear()

    STATE["last_passage"] = passage.__name__
    STATE["last_passage_args"] = params
    passage(
        Output(document["main"]),
        Output(document["sidebar-content"]),
        **params,
    )


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

    def display(
        self, text: str, markdown: bool = False, paragraph: bool = True
    ) -> None:
        if markdown:
            mark, _ = mk.mark(text)
            html = mark
        else:
            html = text
        if paragraph:
            self.target <= bh.P()
            self.target.children[-1].html = html
        else:
            self.target.html += html

    def title(self, text) -> None:
        self.target <= bh.H1(text)

    def link(self, target_func: Callable, text: str, **kwargs) -> None:
        my_id = get_id()
        target_str = target_func.__name__
        if text == "":
            text = target_str

        self.target <= bh.A(text, href="javascript:void(0);", id=my_id)
        self.target <= " "

        def result(
            _, func=target_func, func_args: dict[str, Any] = kwargs.copy()
        ) -> None:
            call_passage(func, **func_args)

        document[my_id].bind("click", result)

    def action_link(self, func: Callable, text: str, **kwargs) -> None:
        my_id = get_id()

        self.target <= bh.A(text, href="javascript:void(0);", id=my_id)
        self.target <= " "

        document[my_id].bind("click", lambda _, args=kwargs.copy(): func(**args))

    def image(self, src: str) -> None:
        self.target <= bh.IMG(src=src)

    def text_input(self, label: str = "") -> Callable:
        my_id = get_id()

        self.target <= bh.LABEL(label) <= bh.INPUT(type="text", id=my_id)

        return lambda: document[my_id].value

    def int_input(self, label: str = "", default: int = 0) -> Callable:
        my_id = get_id()

        self.target <= bh.LABEL(label) <= bh.INPUT(
            value=default, type="number", id=my_id
        )

        return lambda: int(document[my_id].value)

    def radio_buttons(self, choices: list[str]) -> Callable:
        name = get_id()

        self.target <= bh.FIELDSET()
        for choice in choices:
            self.target.children[-1] <= bh.LABEL() <= bh.INPUT(
                type="radio", name=name, value=choice
            ) + choice

        self.target.select_one(f"input[name='{name}']").checked = "checked"

        return lambda: document.select_one(f"input[name='{name}']:checked").value
