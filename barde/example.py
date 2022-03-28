from dataclasses import dataclass, field
from barde import (
    passage,
    run,
    Output,
)
from barde.display import call_passage


@dataclass
class Inventory:
    apples: int = 0
    pies: int = 0


@dataclass
class MyState:
    inventory: Inventory = field(default_factory=Inventory)
    oven_is_on: bool = False


@passage(init_state=MyState())
def init(_body: Output, _sidebar: Output, state: MyState):
    state.inventory.apples = 0
    state.inventory.pies = 0
    state.oven_is_on = False

    call_passage(house)


def my_sidebar(sidebar: Output, state: MyState) -> None:
    sidebar.display(
        f"##### Inventory\n `{state.inventory.apples}`"
        f" apples<br/>`{state.inventory.pies}` pies",
        markdown=True,
    )


@passage
def house(body: Output, sidebar: Output, state: MyState):
    my_sidebar(sidebar, state)

    def turn_oven_on():
        print("voilà")
        state.oven_is_on = True
        print(f"state={state}")
        call_passage(house)

    def bake_pie():
        print("voilà")
        state.inventory.pies += 1
        state.inventory.apples -= 5
        call_passage(house)

    body.title("Your house")
    body.display("You are in your |house|.", tooltips=["A pretty building"])

    if state.oven_is_on:
        body.display("The oven is on")
        if state.inventory.apples >= 5:
            body.action_link(bake_pie, "Bake a pie", tooltip="Bake a yummy <b>pie</b>!")
            body.display(" - ", paragraph=False)
        else:
            body.display("You don't have enough apples to bake a pie!")
    else:
        body.display("The oven is off")

    if not state.oven_is_on:
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

    # body.display("<hr/>")
    # body.radio_buttons(
    #     ["pie cooking mode", "cookie cooking mode", "special mode"],
    #     tooltips=[
    #         "To bake delicious apple pies",
    #         "To bake wonderful cookies",
    #         "A mysterious mode for the adventurous cook",
    #     ],
    # )


@passage
def orchard(body: Output, sidebar: Output, state: MyState, new_apples: int = 0):
    state.inventory.apples += new_apples

    my_sidebar(sidebar, state)

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

    # body.cards(
    #     [
    #         (
    #             "https://grocycle.com/wp-content/uploads/2020/01/"
    #             "What-Is-A-Permaculture-Orchard-1024x400.jpg",
    #             "My card is the best card I love it<br/>Hello<b> there </b>"
    #             " it is so great yeah please help me <p> yuoupi",
    #             lambda: print("Youpi1"),
    #         ),
    #         (
    #             "https://grocycle.com/wp-content/uploads/2020/01/"
    #             "What-Is-A-Permaculture-Orchard-1024x400.jpg",
    #             "My card",
    #             None,
    #         ),
    #         (
    #             "https://grocycle.com/wp-content/uploads/2020/01/"
    #             "What-Is-A-Permaculture-Orchard-1024x400.jpg",
    #             "",
    #             lambda: print("Youpi3"),
    #         ),
    #         (
    #             "",
    #             "My <b>card</b>",
    #             lambda: print("Youpi4"),
    #         ),
    #     ]
    # )


if __name__ == "__main__":
    run()
