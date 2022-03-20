from typing import Any, Callable, Optional

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

    def _display(
        self,
        parent,
        text: str,
        markdown: bool = False,
        tooltip: str = "",
    ) -> None:

        if markdown:
            mark, _ = mk.mark(text)
            html = mark
        else:
            html = text

        parent <= bh.SPAN()
        parent.children[-1].html = html

        if tooltip != "":
            parent.children[-1].attrs["class"] = "has-tooltip"
            parent.children[-1] <= bh.ARTICLE(tooltip)

    def display(
        self,
        text: str,
        markdown: bool = False,
        paragraph: bool = True,
        tooltips: Optional[list] = None,
    ) -> None:

        start: int = 0
        blocks: list[tuple[str, bool]] = []
        next_is_normal: bool = True
        while True:
            end = text.find("|", start)
            if end == -1:
                blocks.append((text[start:], next_is_normal))
                assert next_is_normal
                break
            if next_is_normal:
                blocks.append((text[start:end], next_is_normal))
            else:
                blocks.append((text[start:end], next_is_normal))
            start = end + 1
            next_is_normal = not next_is_normal

        nb_tooltips = len(list(filter(lambda b: not b[1], blocks)))
        if nb_tooltips > 0:
            assert tooltips is not None
            assert nb_tooltips == len(tooltips)

        print(blocks, nb_tooltips)

        if paragraph:
            self.target <= bh.P()
        else:
            self.target <= bh.SPAN()
        parent = self.target.children[-1]
        for i, (block_content, is_normal) in enumerate(blocks):
            if is_normal:
                tooltip = ""
            else:
                assert tooltips is not None
                tooltip = tooltips[int(i / 2)]
            self._display(parent, block_content, markdown, tooltip)

    def title(self, text) -> None:
        self.target <= bh.H1(text)

    def link(
        self, target_func: Callable, text: str, tooltip: str = "", **kwargs
    ) -> None:
        my_id = get_id()
        target_str = target_func.__name__
        if text == "":
            text = target_str

        self.target <= bh.A(text, href="javascript:void(0);", id=my_id)

        if tooltip != "":
            self.target.children[-1].attrs["class"] = "has-tooltip"
            self.target.children[-1] <= bh.ARTICLE(tooltip)

        self.target <= " "

        def result(
            _, func=target_func, func_args: dict[str, Any] = kwargs.copy()
        ) -> None:
            call_passage(func, **func_args)

        document[my_id].bind("click", result)

    def action_link(
        self, func: Callable, text: str, tooltip: str = "", **kwargs
    ) -> None:
        my_id = get_id()

        self.target <= bh.A(text, href="javascript:void(0);", id=my_id)

        if tooltip != "":
            self.target.children[-1].attrs["class"] = "has-tooltip"
            self.target.children[-1] <= bh.ARTICLE(tooltip)

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

    def radio_buttons(self, choices: list[str], tooltips=None) -> Radio:
        if tooltips is not None:
            assert len(tooltips) == len(choices), "Provide one tooltip per choice"

        my_id = get_id()

        self.target <= bh.FIELDSET()
        for i, choice in enumerate(choices):
            fieldset = self.target.children[-1]
            fieldset <= bh.LABEL() <= bh.INPUT(
                type="radio", name=my_id, value=choice
            ) + bh.SPAN(choice)

            if tooltips is not None:
                tooltip: str = tooltips[i]
                label_span = fieldset.children[-1].children[-1]
                label_span.attrs["class"] = "has-tooltip"
                label_span <= bh.ARTICLE(tooltip)

        self.target.select_one(f"input[name='{my_id}']").checked = "checked"

        return Radio(my_id)

    def dynamic_info(self, text="") -> DynamicInfo:
        my_id = get_id()
        self.target <= bh.P(id=my_id)
        return DynamicInfo(my_id, text)

    def cards(self, card_info: list[tuple[str, str, Optional[Callable]]]) -> None:
        grid_width = min(3, len(card_info))
        self.target <= bh.DIV(
            Class="card-grid",
            style="grid-template-columns: " + "1fr " * grid_width + ";",
        )
        grid = self.target.children[-1]
        for image, text, action in card_info:
            grid <= bh.DIV(Class="flip-card", style="width: min(23vw, 230px, 100%);")
            grid.children[-1] <= bh.DIV(Class="flip-card-inner")
            inner = grid.children[-1].children[-1]
            inner <= bh.DIV(
                Class="flip-card-front", style=f"background-image: url({image});"
            )
            inner <= bh.DIV(text, Class="flip-card-back")
            if action is not None:
                inner.bind("click", action)
