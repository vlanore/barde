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
    print("yo")
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
        "Aliquam pretium libero vel orci viverra, ac viverra tellus tempus. Vestibulum "
        "in condimentum felis. Donec dapibus velit ac ligula congue aliquet. Maecenas"
        " lorem est, tempus ut felis ac, molestie euismod nibh. Morbi id neque ut odio"
        " sodales efficitur. Cras eget scelerisque libero, non pulvinar magna. "
        "Phasellus placerat nunc eros, a pellentesque dolor consectetur quis."
        " Vestibulum sed efficitur nulla. Morbi venenatis leo id nisi lacinia "
        "vulputate. Morbi non ullamcorper metus. Morbi non dapibus urna, at bibendum"
        " dolor. Etiam bibendum consectetur libero ut scelerisque. Nunc sit amet dolor"
        " at lectus dapibus mattis vitae ac mi. Curabitur feugiat lobortis leo, vel "
        "accumsan mi feugiat a.\n\n Fusce nec magna blandit, consequat leo euismod,"
        " molestie nunc. Cras a leo sed odio ultrices semper finibus non nisl."
        "Proin laoreet felis ut tincidunt rhoncus. Proin laoreet vel erat a mattis."
        " Curabitur porttitor sed elit tristique lacinia. Praesent ullamcorper id"
        " tellus sit amet dapibus. Etiam urna urna, sagittis in feugiat id, ultrices"
        " auctor mi. Morbi placerat non magna sit amet consectetur. Morbi at cursus"
        " nunc. Integer lobortis sit amet est ut tincidunt."
        "Duis urna ante, pellentesque scelerisque urna aliquam, fermentum bibendum"
        " ligula. Nunc viverra ex non pharetra mattis. Ut eget diam vel risus laoreet"
        " elementum vitae in nisi. Sed tempor orci ac nisi euismod, in pretium eros"
        " efficitur. Aliquam sed enim quam. Interdum et malesuada fames ac ante ipsum "
        "primis in faucibus. Cras ac nibh id mauris porttitor mollis. In tincidunt"
        " magna diam, id porta ante lacinia in. Suspendisse porta ante non convallis"
        " tincidunt.\n\n"
        "Integer dignissim enim nec dui rhoncus, sit amet molestie ex sagittis."
        " Aenean nec risus diam. Morbi ac eleifend libero. Aliquam quis pretium orci."
        " In hac habitasse platea dictumst. Nam lobortis, dui at molestie congue, lacus"
        " tortor hendrerit turpis, et imperdiet sem erat ut metus. Phasellus urna "
        "lorem, pretium et nisl ac, ultricies venenatis mi. Donec id erat tristique, "
        "facilisis orci non, vestibulum lacus. Quisque leo sapien, maximus in elit"
        " in, aliquet condimentum enim. Maecenas lobortis maximus felis at efficitur."
        " In feugiat metus nec felis tincidunt lobortis."
        "Ut aliquam ullamcorper placerat. Cras scelerisque rutrum neque et malesuada."
        " Cras et laoreet augue. Duis eget nisi eu magna tristique convallis sit amet"
        " sit amet libero. Nunc ut fringilla libero, sit amet dignissim massa. Aenean"
        " eget orci magna. Mauris pellentesque nibh at lectus accumsan, nec sodales "
        "augue commodo. Vestibulum eget ante eu ligula cursus faucibus. Integer "
        "tempor magna justo, eget maximus odio egestas vel.",
        markdown=False,
    )
    display(f"<i>Number: </i>{STATE['a']}<br/><br/>")
    link(tralala, "tralala")
    link(youpi, "ioupi")


@passage
def youpi():
    title("Youpi")
    display("youpida")
    image("https://upload.wikimedia.org/wikipedia/commons/8/87/Old_book_bindings.jpg")

    STATE["a"] += 1

    link(hello, "hello")


@passage
def tralala():
    title("Tralala")
    display("trouloulala")
    link(youpi, "youpi")
    link(hello, "hello")


run()
