## Groupmate sprite animations
## Idle: PNG frame ATL. Other states: WebM in images/anims/

define GM_MOVIE_SIZE = (540, 1080)

init python:
    for _gm_channel in (
        "gm_angry",
        "gm_walking",
        "gm_shooting",
        "gm_jumpscare",
        "gm_punch",
    ):
        renpy.music.register_channel(_gm_channel, "music", loop=True, movie=True)

image groupmate angry = Movie(
    play="images/anims/angry.webm",
    loop=True,
    channel="gm_angry",
    size=GM_MOVIE_SIZE,
)
image groupmate walking = Movie(
    play="images/anims/walking.webm",
    loop=True,
    channel="gm_walking",
    size=GM_MOVIE_SIZE,
)
image groupmate shooting = Movie(
    play="images/anims/gunshooting.webm",
    loop=False,
    channel="gm_shooting",
    size=GM_MOVIE_SIZE,
)
image groupmate jumpscare = Movie(
    play="images/anims/fnaf.webm",
    loop=False,
    channel="gm_jumpscare",
    size=GM_MOVIE_SIZE,
)
image groupmate punch = Movie(
    play="images/anims/punching.webm",
    loop=False,
    channel="gm_punch",
    size=GM_MOVIE_SIZE,
)

image groupmate normal:
    zoom 0.8
    block:
        "images/groupmate_idle/frame0001.png"
        pause 0.041667
        "images/groupmate_idle/frame0002.png"
        pause 0.041667
        "images/groupmate_idle/frame0003.png"
        pause 0.041667
        "images/groupmate_idle/frame0004.png"
        pause 0.041667
        "images/groupmate_idle/frame0005.png"
        pause 0.041667
        "images/groupmate_idle/frame0006.png"
        pause 0.041667
        "images/groupmate_idle/frame0007.png"
        pause 0.041667
        "images/groupmate_idle/frame0008.png"
        pause 0.041667
        "images/groupmate_idle/frame0009.png"
        pause 0.041667
        "images/groupmate_idle/frame0010.png"
        pause 0.041667
        "images/groupmate_idle/frame0011.png"
        pause 0.041667
        "images/groupmate_idle/frame0012.png"
        pause 0.041667
        "images/groupmate_idle/frame0013.png"
        pause 0.041667
        "images/groupmate_idle/frame0014.png"
        pause 0.041667
        "images/groupmate_idle/frame0015.png"
        pause 0.041667
        "images/groupmate_idle/frame0016.png"
        pause 0.041667
        "images/groupmate_idle/frame0017.png"
        pause 0.041667
        "images/groupmate_idle/frame0018.png"
        pause 0.041667
        "images/groupmate_idle/frame0019.png"
        pause 0.041667
        "images/groupmate_idle/frame0020.png"
        pause 0.041667
        "images/groupmate_idle/frame0021.png"
        pause 0.041667
        "images/groupmate_idle/frame0022.png"
        pause 0.041667
        "images/groupmate_idle/frame0023.png"
        pause 0.041667
        "images/groupmate_idle/frame0024.png"
        pause 0.041667
        "images/groupmate_idle/frame0025.png"
        pause 0.041667
        "images/groupmate_idle/frame0026.png"
        pause 0.041667
        "images/groupmate_idle/frame0027.png"
        pause 0.041667
        "images/groupmate_idle/frame0028.png"
        pause 0.041667
        "images/groupmate_idle/frame0029.png"
        pause 0.041667
        "images/groupmate_idle/frame0030.png"
        pause 0.041667
        "images/groupmate_idle/frame0031.png"
        pause 0.041667
        "images/groupmate_idle/frame0032.png"
        pause 0.041667
        "images/groupmate_idle/frame0033.png"
        pause 0.041667
        "images/groupmate_idle/frame0034.png"
        pause 0.041667
        "images/groupmate_idle/frame0035.png"
        pause 0.041667
        "images/groupmate_idle/frame0036.png"
        pause 0.041667
        "images/groupmate_idle/frame0037.png"
        pause 0.041667
        "images/groupmate_idle/frame0038.png"
        pause 0.041667
        "images/groupmate_idle/frame0039.png"
        pause 0.041667
        "images/groupmate_idle/frame0040.png"
        pause 0.041667
        "images/groupmate_idle/frame0041.png"
        pause 0.041667
        "images/groupmate_idle/frame0042.png"
        pause 0.041667
        "images/groupmate_idle/frame0043.png"
        pause 0.041667
        "images/groupmate_idle/frame0044.png"
        pause 0.041667
        "images/groupmate_idle/frame0045.png"
        pause 0.041667
        "images/groupmate_idle/frame0046.png"
        pause 0.041667
        "images/groupmate_idle/frame0047.png"
        pause 0.041667
        "images/groupmate_idle/frame0048.png"
        pause 0.041667
        "images/groupmate_idle/frame0049.png"
        pause 0.041667
        "images/groupmate_idle/frame0050.png"
        pause 0.041667
        "images/groupmate_idle/frame0051.png"
        pause 0.041667
        "images/groupmate_idle/frame0052.png"
        pause 0.041667
        "images/groupmate_idle/frame0053.png"
        pause 0.041667
        "images/groupmate_idle/frame0054.png"
        pause 0.041667
        "images/groupmate_idle/frame0055.png"
        pause 0.041667
        "images/groupmate_idle/frame0056.png"
        pause 0.041667
        "images/groupmate_idle/frame0057.png"
        pause 0.041667
        "images/groupmate_idle/frame0058.png"
        pause 0.041667
        "images/groupmate_idle/frame0059.png"
        pause 0.041667
        "images/groupmate_idle/frame0060.png"
        pause 0.041667
        repeat
