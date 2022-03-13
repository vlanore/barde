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
    sidebar.display(
        f"##### Inventory\n `{STATE['apples']}` apples<br/>`{STATE['pies']}` pies",
        markdown=True,
    )


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
    body.display("You are in your |house|.", tooltips=["A pretty building"])

    if STATE["oven_is_on"]:
        body.display("The oven is on")
        if STATE["apples"] >= 5:
            body.action_link(bake_pie, "Bake a pie", tooltip="Bake a yummy <b>pie</b>!")
            body.display(" - ", paragraph=False)
        else:
            body.display("You don't have enough apples to bake a pie!")
    else:
        body.display("The oven is off")

    if not STATE["oven_is_on"]:
        body.action_link(
            turn_oven_on,
            "Turn on the oven",
            tooltip="Turning on the <b>oven</b> might help with cooking <b>pies</b>.",
        )
        body.display(" - ", paragraph=False)

    body.link(
        orchard,
        "Go to the orchard",
        tooltip=(
            "The <b>orchard</b> is a place with big apple trees. "
            "You might find <b>apples</b> there."
        ),
    )

    body.display("<hr/>")
    body.radio_buttons(
        ["pie cooking mode", "cookie cooking mode", "special mode"],
        tooltips=[
            "To bake delicious apple pies",
            "To bake wonderful cookies",
            "A mysterious mode for the adventurous cook",
        ],
    )


@passage
def orchard(body: Output, sidebar: Output, new_apples: int = 0):
    STATE["apples"] += new_apples

    my_sidebar(sidebar)

    body.title("Orchard")
    body.image(
        "https://grocycle.com/wp-content/uploads/2020/01/"
        "What-Is-A-Permaculture-Orchard-1024x400.jpg"
    )

    if new_apples > 0:
        body.display(
            f"You gather {new_apples} |apples|",
            tooltips=["It's a fruit used to make <b>pies</b>"],
        )
    else:
        body.display("You are in the orchard.")

    nb_apples = body.int_input("How many apples:", 1)
    body.action_link(
        lambda: call_passage(orchard, new_apples=nb_apples.get()),
        "Gather!",
        tooltip="Gather them <b>apples</b>!",
    )
    body.display(" - ", paragraph=False)
    body.link(
        house,
        "Go to your house",
        tooltip=(
            "Your <b>house</b> is a place with a big <b>oven</b>"
            " which might be linked to <b>pie</b> cooking"
        ),
    )


run()
