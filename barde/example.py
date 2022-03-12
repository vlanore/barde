from barde import (
    STATE,
    passage,
    run,
    Output,
)
from barde.display import call_passage


@passage(start=True)
def init(_body: Output, _sidebar: Output):
    STATE["apples"] = 0
    STATE["pies"] = 0
    STATE["oven_is_on"] = False

    call_passage(house)


def my_sidebar(sidebar: Output) -> None:
    sidebar.display("You have:")
    sidebar.display(f"{STATE['apples']} apples")
    sidebar.display(f"{STATE['pies']} pies")


@passage
def house(body: Output, sidebar: Output):
    my_sidebar(sidebar)

    def turn_oven_on():
        STATE["oven_is_on"] = True
        call_passage(house)

    def bake_pie():
        STATE["pies"] += 1
        STATE["apples"] -= 5
        call_passage(house)

    body.title("Your house")
    body.display("You are in your house.")

    if STATE["oven_is_on"]:
        body.display("The oven is on")
        if STATE["apples"] >= 5:
            body.action_link(bake_pie, "Bake a pie")
            body.display("<br/>", paragraph=False)
        else:
            body.display("You don't have enough apples to bake a pie!")
    else:
        body.display("The oven is off")

    if not STATE["oven_is_on"]:
        body.action_link(turn_oven_on, "Turn on the oven")
        body.display("<br/>", paragraph=False)
    body.link(orchard, "Go to the orchard")


@passage
def orchard(body: Output, sidebar: Output, new_apples: int = 0):
    STATE["apples"] += new_apples

    my_sidebar(sidebar)

    body.title("Orchard")
    if new_apples > 0:
        body.display(f"You gather {new_apples} apples")
    else:
        body.display("You are in the orchard.")

    nb_apples = body.int_input("How many apples:", 1)
    body.action_link(
        lambda: call_passage(orchard, new_apples=nb_apples.get()), "Gather!"
    )
    body.display("<br/>", paragraph=False)
    body.link(house, "Go to your house")


run()
