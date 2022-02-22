from barde import (
    STATE,
    display,
    display_sidebar,
    image,
    link,
    passage,
    run,
    title,
)


@passage(start=True)
def init():
    STATE["a"] = 1
    display_sidebar("**Stats**<br/>Strenght: *3*<br/>Dex: *4*", markdown=True)
    hello()


@passage
def hello():
    title("Hello, world")
    display(
        "Lorem ipsum **dolor sit amet**, "
        "consectetur adipiscing elit, sed do eiusmod "
        "tempor <b>incididunt</b> ut labore et "
        "dolore magna aliqua.:\n\n"
        f" * Ut enim ad minim veniam: `{STATE['a']}cm`\n"
        " * quis nostrud exercitation ullamco laboris",
        markdown=True,
    )
    display(
        " ".join(
            [
                "uis nostrud exercitation ullamco labori\n "[(i % 15) : -(i % 4)]
                for i in range(100)
            ]
        )
    )
    display(f"<i>Number: </i>{STATE['a']}<br/><br/>")
    link(tralala)
    link(youpi, "ioupi")


@passage
def youpi():
    title("Youpi")
    display("youpida")
    image("https://upload.wikimedia.org/wikipedia/commons/8/87/Old_book_bindings.jpg")

    STATE["a"] += 1

    link(hello)


@passage
def tralala():
    title("Tralala")
    display("trouloulala")
    link(youpi)
    link(hello)


run()
