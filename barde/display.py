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


class DynamicInfo:
    def __init__(self, my_id: str, text: str = "") -> None:
        self.my_id = my_id
        self.set(text)

    def set(self, text: str) -> None:
        document[self.my_id].clear()
        document[self.my_id] <= text


class Input:
    def __init__(self, my_id: str, convert: Callable = str) -> None:
        self.my_id = my_id
        self.convert = convert

    def get(self) -> Any:
        return self.convert(document[self.my_id].value)

    def on_change(self, func: Callable) -> None:
        document[self.my_id].bind("input", lambda _, func=func: func())


class Radio:
    def __init__(self, my_id: str) -> None:
        self.my_id = my_id

    def get(self) -> Any:
        return document.select_one(f"input[name='{self.my_id}']:checked").value

    def on_change(self, func: Callable) -> None:
        for element in document.select(f"input[name='{self.my_id}']"):
            element.bind("input", lambda _, func=func: func())


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

    def text_input(self, label: str = "") -> Input:
        my_id = get_id()

        self.target <= bh.LABEL(label) <= bh.INPUT(type="text", id=my_id)

        return Input(my_id)

    def int_input(self, label: str = "", default: int = 0) -> Input:
        my_id = get_id()

        self.target <= bh.LABEL(label) <= bh.INPUT(
            value=default, type="number", id=my_id
        )

        return Input(my_id, int)

    def radio_buttons(self, choices: list[str]) -> Radio:
        my_id = get_id()

        self.target <= bh.FIELDSET()
        for choice in choices:
            self.target.children[-1] <= bh.LABEL() <= bh.INPUT(
                type="radio", name=my_id, value=choice
            ) + choice

        self.target.select_one(f"input[name='{my_id}']").checked = "checked"

        return Radio(my_id)

    def dynamic_info(self, text="") -> DynamicInfo:
        my_id = get_id()
        self.target <= bh.P(id=my_id)
        return DynamicInfo(my_id, text)
