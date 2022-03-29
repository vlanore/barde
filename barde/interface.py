from browser import document  # type:ignore ; pylint: disable=import-error

from barde.state import STORAGE


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


def open_restart_confirm(_event) -> None:
    document["restart-confirm"].showModal()


def close_restart_confirm(_event) -> None:
    document["restart-confirm"].close()
