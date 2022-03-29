import datetime
from typing import Type

from browser import document  # type:ignore # pylint: disable=import-error
from browser import html as bh  # type:ignore # pylint: disable=import-error

from barde.state import STORAGE, State
from barde.display import call_passage
import barde.globals as globs


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

    assert isinstance(globs.INIT_STATE, State)
    state_type: Type[State] = type(globs.INIT_STATE)
    state_dict = STORAGE[f"save__{slot}__state"]
    state_before_last_passage = state_type.from_dict(state_dict)
    last_passage = STORAGE[f"save__{slot}__last_passage"]
    last_passage_args = STORAGE[f"save__{slot}__last_passage_args"]

    call_passage(
        globs.PASSAGES[last_passage],
        _init_state=state_before_last_passage,
        **last_passage_args,
    )
    close_save_menu(None)
