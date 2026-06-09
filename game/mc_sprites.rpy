## MC sprite animations — WebM movies in images/anims/

define MC_MOVIE_SIZE = (540, 1080)

init python:
    for _mc_channel in (
        "mc_thinking",
        "mc_shocked",
        "mc_panicked",
        "mc_celebrate",
        "mc_running",
    ):
        renpy.music.register_channel(_mc_channel, "music", loop=True, movie=True)

image mc thinking = Movie(
    play="images/anims/MC_Thinking.webm",
    loop=True,
    channel="mc_thinking",
    size=MC_MOVIE_SIZE,
)
image mc shocked = Movie(
    play="images/anims/MC_Shocked.webm",
    loop=True,
    channel="mc_shocked",
    size=MC_MOVIE_SIZE,
)
image mc panicked = Movie(
    play="images/anims/MC_Scared.webm",
    loop=True,
    channel="mc_panicked",
    size=MC_MOVIE_SIZE,
)
image mc celebrate = Movie(
    play="images/anims/MC_Happy.webm",
    loop=True,
    channel="mc_celebrate",
    size=MC_MOVIE_SIZE,
)
image mc running = Movie(
    play="images/anims/jump.webm",
    loop=True,
    channel="mc_running",
    size=MC_MOVIE_SIZE,
)
