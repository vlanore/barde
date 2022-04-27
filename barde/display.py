from dataclasses import dataclass, field
from math import cos, radians, sin
from typing import Any, Callable, Optional

from browser import document, window  # type:ignore # pylint: disable=import-error
from browser import html as bh  # type:ignore # pylint: disable=import-error
from browser import markdown as mk  # type:ignore # pylint: disable=import-error

from barde.state import STORAGE, State

Passage = Callable[..., None]


_NEXT_ID = 0

STATE = None


def set_page_title(new_title: str) -> None:
    document.title = new_title


def call_passage(
    passage: Callable,
    _init_state: Optional[State] = None,
    scroll_to_top: bool = True,
    **params: dict[str, Any],
) -> None:

    global STATE
    if _init_state is not None:
        STATE = _init_state
    assert isinstance(STATE, State)

    document["main"].clear()
    document["sidebar-content"].clear()

    STORAGE["last_passage"] = passage.__name__
    STORAGE["last_passage_args"] = params
    STORAGE["state_before_last_passage"] = STATE.to_dict()
    passage(
        Output(document["main"]),
        Output(document["sidebar-content"]),
        STATE,
        **params,
    )
    if scroll_to_top:
        window.scrollTo(0, 0)


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
        document[self.my_id].bind("input", lambda _: func())


class Radio:
    def __init__(self, my_id: str) -> None:
        self.my_id = my_id

    def get(self) -> Any:
        return document.select_one(f"input[name='{self.my_id}']:checked").value

    def on_change(self, func: Callable) -> None:
        for element in document.select(f"input[name='{self.my_id}']"):
            element.bind("input", lambda _: func())


def get_id() -> str:
    global _NEXT_ID
    my_id = _NEXT_ID
    _NEXT_ID += 1
    return f"id_{my_id}"


@dataclass
class HexCellInfo:
    text: str = ""
    tooltip: Optional[str] = None
    action: Optional[Callable] = None
    cls: Optional[str] = None  # CSS class
    borders: dict[int, str] = field(default_factory=dict)  # orientation, class


BrTarget = Any
BrEvent = Any


class Output:
    def __init__(self, target: BrTarget) -> None:
        self.target = target

    def clear_page(self) -> None:
        self.target.clear()

    def _display(
        self,
        parent: BrTarget,
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

    def title(self, text: str) -> None:
        self.target <= bh.H1(text)

    def link(
        self,
        target_func: Passage,
        text: str,
        tooltip: str = "",
        **kwargs: Any,
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
            _: BrEvent,
            func: Passage = target_func,
            func_args: dict[str, Any] = kwargs.copy(),
        ) -> None:
            call_passage(func, **func_args)

        document[my_id].bind("click", result)

    def action_link(
        self, func: Callable, text: str, tooltip: str = "", **kwargs: Any
    ) -> None:
        my_id = get_id()

        self.target <= bh.A(text, href="javascript:void(0);", id=my_id)

        if tooltip != "":
            self.target.children[-1].attrs["class"] = "has-tooltip"
            self.target.children[-1] <= bh.ARTICLE(tooltip)

        self.target <= " "

        document[my_id].bind("click", lambda _, kwargs=kwargs.copy(): func(*kwargs))

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

    def radio_buttons(
        self, choices: list[str], tooltips: Optional[list[str]] = None
    ) -> Radio:
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

    def dynamic_info(self, text: str = "") -> DynamicInfo:
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
            cls = "card-action" if action is not None else ""

            if text != "" and image != "":
                grid <= bh.DIV(Class="flip-card")
                grid.children[-1] <= bh.DIV(Class="flip-card-inner")
                inner = grid.children[-1].children[-1]
                inner <= bh.DIV(
                    Class="flip-card-front",
                    style=f"background-image: url({image});",
                )
                inner <= bh.DIV(text, Class="flip-card-back")
                to_bind = inner

            elif image != "":
                grid <= bh.DIV(
                    Class=cls + " single-card",
                    style=f"background-image: url({image});",
                )
                to_bind = grid.children[-1]

            elif text != "":
                grid <= bh.DIV(
                    text,
                    Class=cls + " single-card",
                )
                to_bind = grid.children[-1]

            else:
                raise ValueError("Need text or image")

            to_bind.bind("click", lambda _, action=action: action())

    def hex_grid(
        self,
        cells: list[list[Optional[HexCellInfo]]],
        cell_size: int = 100,
        gap: int = 15,
    ) -> None:
        """Displays a hex grid.

        First line is shifted left. Missing cells should be set to None."""

        # create container
        nb_lines = len(cells)
        nb_cols = max(len(line) for line in cells)
        line_height = cell_size * (1.1547 - 0.289)
        border_clip_ratio = float(gap) / (cell_size + gap) / 2.0
        style = (
            f"--hexgrid-cell-size: {cell_size}px;"
            f"--hexgrid-gap: {gap}px;"
            f"--border-clip-ratio: {border_clip_ratio};"
            f"grid-template-columns: repeat({nb_cols}, {cell_size}px);"
            f"grid-template-rows: repeat({nb_lines}, {line_height}px);"
            f"width: {(nb_cols + 0.5) * (gap + cell_size)}px"
        )
        self.target <= bh.DIV(Class="hexgrid-container", style=style)
        container = self.target.children[-1]

        # create cells
        for line_index, line in enumerate(cells):

            # create all cells in line
            for cell_index, cell in enumerate(line):
                coordinates = (
                    f"grid-column-start: {cell_index+1};"
                    f"grid-row-start: {line_index+1};"
                )
                offset = (
                    f"margin-left:-{(cell_size + gap)/2}px;"
                    if line_index % 2 == 0
                    else ""
                )
                style = offset + coordinates
                cls = "hexgrid-cell"

                if cell is not None:
                    if cell.cls is not None:
                        cls += " " + cell.cls
                    if cell.action is not None:
                        cls += " hexgrid-action"

                    container <= bh.DIV(Class="hexgrid-cell-wrap", style=style)
                    cell_div = container.children[-1]

                    # border classes
                    for side, bdr_cls in cell.borders.items():
                        assert side in range(6)
                        border_transforms = []
                        angle = 30 + 60 * side
                        border_transforms.append(  # move left corner to hex center
                            f"translate({cell_size / 2.}px, {(gap + cell_size) / 2.}px)"
                        )
                        border_transforms.append(  # center on top of hex
                            f"translate({(cell_size + gap) / -4. * 1.1547}px, "
                            f"{gap / -4.}px)"
                        )
                        distance_to_center = 0.25 * gap + 0.5 * cell_size
                        border_transforms.append(
                            f"translate({-distance_to_center * sin(radians(angle))}px, "
                            f"{-distance_to_center * cos(radians(angle))}px)"
                        )
                        border_transforms.append(f"rotate(-{angle}deg)")
                        cell_div <= bh.DIV(
                            Class=f"hexgrid-cell-border {bdr_cls}",
                            style=f"transform:{' '.join(border_transforms)};",
                        )

                    cell_div <= bh.DIV(cell.text, Class=cls)
                    if cell.action is not None:
                        cell_div.bind("click", lambda _, action=cell.action: action())
