import json
import sys
import datetime
from typing import Callable, Optional, Any

from browser import document  # type:ignore ; pylint: disable=import-error
from browser import html as bh  # type:ignore ; pylint: disable=import-error

from barde.display import call_passage
from barde.state import STORAGE


PASSAGES = {}

START = None

INIT_STATE = None


def hide_sidebar(_event):
    document["open-sidebar"].style = "display:block;"
    document["sidebar-box"].style = "display:none;"
    document["hide-sidebar"].unbind("click")
    document["open-sidebar"].bind("click", open_sidebar)
    document["body"].style = "grid-template-columns: 0 1fr min(95vw, 700px) 1fr;"


def open_sidebar(_event):
    document["open-sidebar"].style = "display:none;"
    document["open-sidebar"].unbind("click")
    document["sidebar-box"].style = "display:block;"
    document["hide-sidebar"].bind("click", hide_sidebar)
    document[
        "body"
    ].style = (
        "grid-template-columns: max(min(25vw, 300px), 140px) 1fr min(70vw, 700px) 1fr;"
    )


def dark_mode(_event):
    """Toggle on dark mode."""

    document["dark-mode"].html = "dark"
    document["dark-mode"].unbind("click")

    document["light-mode"].html = '<a href="javascript:void(0);">light</a>'
    document["light-mode"].bind("click", light_mode)

    document["html"].setAttribute("data-theme", "dark")

    STORAGE["style-mode"] = "dark"


def light_mode(_event):
    """Toggle on light mode."""

    document["light-mode"].html = "light"
    document["light-mode"].unbind("click")

    document["dark-mode"].html = '<a href="javascript:void(0);">dark</a>'
    document["dark-mode"].bind("click", dark_mode)

    document["html"].setAttribute("data-theme", "light")

    STORAGE["style-mode"] = "light"


def select_style():
    """Select style mode (light or dark) based on stored data."""
    if "style-mode" in STORAGE.keys():
        match STORAGE["style-mode"]:
            case "light":
                light_mode(None)
            case "dark":
                dark_mode(None)
    else:
        light_mode(None)


def passage(*args, **kwargs):
    """Decorator used to define a passage.

    Works without arguments, or with a single start(bool) arguments that denotes that
    this passage is the starting passage."""

    match args, kwargs:
        case [func], {} if callable(func):
            global PASSAGES
            PASSAGES[func.__name__] = func
            return func

        case ([init_state], {}) | ([], {"init_state": init_state}):

            def result(func: Callable, init_state=init_state):
                global START
                global PASSAGES
                global INIT_STATE

                START = func.__name__
                INIT_STATE = init_state
                PASSAGES[func.__name__] = func
                return func

            return result

        case _:
            sys.exit(1)


def open_restart_confirm(_event) -> None:
    document["restart-confirm"].showModal()


def close_restart_confirm(_event) -> None:
    document["restart-confirm"].close()


def restart(_event):
    document["main"].clear()
    document["sidebar-content"].clear()

    for key in STORAGE.keys():
        if "save__" not in key:
            STORAGE.pop(key)

    document["hide-sidebar"].unbind("click")
    document["restart"].unbind("click")
    run()
    close_restart_confirm(None)


def open_save_menu(_event) -> None:
    document["save-menu"].showModal()


def close_save_menu(_event) -> None:
    document["save-menu"].close()


def render_save_list() -> None:
    document["save-menu-list"].clear()
    for i in range(5):
        if f"save__{i}__savetime" in STORAGE.keys():
            savetime: str = STORAGE[f"save__{i}__savetime"]
        else:
            savetime: str = " ___ "

        if f"save__{i}__name" in STORAGE.keys():
            name: str = STORAGE[f"save__{i}__name"]
        else:
            name: str = " ___ "

        save_block = document["save-menu-list"] <= bh.TR()
        save_block <= bh.TH(i + 1, scope="row") + bh.TD(savetime) + bh.TD(name)

        save_block <= bh.TD() <= bh.A(
            "Save", href="javascript:void(0);", id=f"save_slot_{i}"
        ) + " - " + bh.A(
            "Load", href="javascript:void(0);", id=f"load_slot_{i}"
        ) + " - " + bh.A(
            "Clear", href="javascript:void(0);", id=f"clear_slot_{i}"
        )

        document[f"save_slot_{i}"].bind("click", lambda _, nb=i: save_to(nb))
        document[f"load_slot_{i}"].bind("click", lambda _, nb=i: load_from(nb))
        document[f"clear_slot_{i}"].bind("click", lambda _, nb=i: clear_slot(nb))


def clear_slot(slot: int) -> None:
    for key in STORAGE.keys():
        if f"save__{slot}__" in key:
            STORAGE.pop(key)
    render_save_list()


def save_to(slot: int) -> None:
    STORAGE[f"save__{slot}__savetime"] = str(datetime.datetime.now())
    STORAGE[f"save__{slot}__name"] = STORAGE["last_passage"]
    STORAGE[f"save__{slot}__last_passage"] = STORAGE["last_passage"]
    STORAGE[f"save__{slot}__last_passage_args"] = STORAGE["last_passage_args"]
    STORAGE[f"save__{slot}__state"] = STORAGE["state_before_last_passage"]

    render_save_list()


def load_from(slot: int) -> None:
    document["main"].clear()
    document["sidebar-content"].clear()

    state_type = type(INIT_STATE)
    state_dict = json.loads(STORAGE[f"save__{slot}__state"])
    print(state_dict)
    state_before_last_passage = state_type(**state_dict)
    print(init_state)
    last_passage = STORAGE[f"save__{slot}__last_passage"]
    last_passage_args = STORAGE[f"save__{slot}__last_passage_args"]

    call_passage(
        PASSAGES[last_passage],
        _init_state=state_before_last_passage,
        **last_passage_args,
    )
    close_save_menu(None)


def run():
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
        state_type = type(INIT_STATE)
        state_dict = json.loads(STORAGE["state_before_last_passage"])
        print(state_dict)
        init_state = state_type(**state_dict)
        print(init_state)
        call_passage(
            PASSAGES[STORAGE["last_passage"]],
            _init_state=init_state,
            **STORAGE["last_passage_args"],
        )

    elif START is not None:
        init_state = INIT_STATE
        call_passage(PASSAGES[START], _init_state=init_state)

    # remove loading screen and display app
    document["main"].style = "visibility: visible;"
    document["sidebar"].style = "visibility: visible;"
    document["loading"].style = "display: none;"

    # populate loading menu
    render_save_list()
