from typing import Any, Callable

from browser import document  # type: ignore # pylint: disable=import-error

from barde.display import call_passage
from barde.state import STORAGE, State
from barde.interface import (
    hide_sidebar,
    select_style,
    open_restart_confirm,
    close_restart_confirm,
)
from barde.save import close_save_menu, open_save_menu, render_save_list
import barde.globals as globs

StateType = Any
Passage = Callable[..., None]


def passage(func: Passage) -> Passage:
    globs.PASSAGES[func.__name__] = func
    return func


def start_passage(init_state: Callable[[], StateType]) -> Callable[[Passage], Passage]:
    def result(
        func: Passage, init_state: Callable[[], StateType] = init_state
    ) -> Passage:
        globs.START = func.__name__  # type: ignore
        globs.INIT_STATE = init_state()  # type: ignore
        globs.PASSAGES[func.__name__] = func
        return func

    return result


def restart(_event: Any) -> None:
    document["main"].clear()
    document["sidebar-content"].clear()

    for key in STORAGE.keys():
        if "save__" not in key:
            STORAGE.pop(key)

    document["hide-sidebar"].unbind("click")
    document["restart"].unbind("click")
    run()
    close_restart_confirm(None)


def run() -> None:
    # bond save menu and sidebar buttons
    document["close-save-menu"].bind("click", close_save_menu)
    document["saves"].bind("click", open_save_menu)
    document["hide-sidebar"].bind("click", hide_sidebar)

    # restart
    document["restart"].bind("click", open_restart_confirm)
    document["restart-yes"].bind("click", restart)
    document["restart-no"].bind("click", close_restart_confirm)

    select_style()

    # start from the last open page, or from scratch
    if "last_passage" in STORAGE.keys():
        assert isinstance(globs.INIT_STATE, State)
        state_type = type(globs.INIT_STATE)
        state_dict = STORAGE["state_before_last_passage"]
        init_state = state_type.from_dict(state_dict)
        call_passage(
            globs.PASSAGES[STORAGE["last_passage"]],
            _init_state=init_state,
            **STORAGE["last_passage_args"],
        )

    elif globs.START is not None:
        init_state = globs.INIT_STATE
        call_passage(globs.PASSAGES[globs.START], _init_state=init_state)

    # remove loading screen and display app
    document["main"].style = "visibility: visible;"
    document["sidebar"].style = "visibility: visible;"
    document["loading"].style = "display: none;"

    # populate loading menu
    render_save_list()
