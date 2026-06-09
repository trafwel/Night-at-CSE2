## ============================================================
##  Night at CSE2 — QTE / Timed Challenge System
## ============================================================

# ── Quick-Time Event: single dodge prompt ────────────────────
# Usage:
#   call screen qte_dodge(prompt="The groupmate turns the corner—", time_limit=3.0)
#   if _return == "success": ...
#
screen qte_dodge(prompt="DODGE!", time_limit=3.5):
    modal True
    zorder 50

    timer time_limit action Return("fail")

    # Red vignette border
    frame:
        xfill True yfill True
        background "#cc000033"

    frame:
        xalign 0.5
        yalign 0.62
        background Frame("#000000dd", 12, 12)
        padding (50, 30)

        vbox:
            spacing 18
            xalign 0.5

            text prompt:
                size 26
                color "#ffdddd"
                xalign 0.5
                text_align 0.5

            # Countdown bar
            bar:
                value AnimatedValue(0, time_limit, time_limit)
                range time_limit
                xsize 420
                ysize 18
                xalign 0.5
                left_bar  Frame("#ff4444", 0, 0)
                right_bar Frame("#441111", 0, 0)
                thumb      None

            textbutton "  !! DODGE !!  ":
                xalign 0.5
                action Return("success")
                text_style "qte_btn_text"
                background "#cc2222"
                hover_background "#ff4444"
                padding (30, 14)

style qte_btn_text:
    size 24
    color "#ffffff"
    bold True


# ── Timed cooking challenge ───────────────────────────────────
# Usage:
#   call screen qte_cook
#   if _return == "success": ...
#
screen qte_cook():
    modal True
    zorder 50

    default step = 0
    default correct = 0

    timer 10.0 action Return("fail")

    frame:
        xfill True yfill True
        background "#33220011"

    frame:
        xalign 0.5
        yalign 0.5
        background Frame("#1a1000ee", 12, 12)
        padding (50, 30)
        minimum (600, 300)

        vbox:
            spacing 16
            xalign 0.5

            text "TENDON KOHAKU SET — QUICK-FIRE!":
                size 22 color "#ffcc44" xalign 0.5 bold True

            if step == 0:
                text "Step 1: Pick the broth base!" size 18 color "#ffeeaa" xalign 0.5
                hbox:
                    spacing 20 xalign 0.5
                    textbutton "Dashi stock"    action [SetScreenVariable("step",1), SetScreenVariable("correct", correct+1)]
                    textbutton "Tap water"      action [SetScreenVariable("step",1)]
                    textbutton "Energy drink"   action [SetScreenVariable("step",1)]
            elif step == 1:
                text "Step 2: Tempura fry time?" size 18 color "#ffeeaa" xalign 0.5
                hbox:
                    spacing 20 xalign 0.5
                    textbutton "2 minutes"      action [SetScreenVariable("step",2)]
                    textbutton "90 seconds"     action [SetScreenVariable("step",2), SetScreenVariable("correct", correct+1)]
                    textbutton "Until vibes"    action [SetScreenVariable("step",2)]
            elif step == 2:
                text "Step 3: Sauce how much tsuyu?" size 18 color "#ffeeaa" xalign 0.5
                hbox:
                    spacing 20 xalign 0.5
                    textbutton "A little"       action [SetScreenVariable("step",3)]
                    textbutton "A lot"          action [SetScreenVariable("step",3)]
                    textbutton "Just right"     action [SetScreenVariable("step",3), SetScreenVariable("correct", correct+1)]
            elif step == 3:
                if correct >= 2:
                    $ renpy.run(Return("success"))
                else:
                    $ renpy.run(Return("fail"))

            bar:
                value AnimatedValue(0, 10.0, 10.0)
                range 10.0
                xsize 480 ysize 12 xalign 0.5
                left_bar  Frame("#ffaa00", 0, 0)
                right_bar Frame("#332200", 0, 0)
                thumb None


# ── Timed room-search screen ─────────────────────────────────
# Shows "searching" flavor text while time ticks. Player picks rooms.
# Not a true screen — just used for visual beat.

screen searching_room(room_name):
    modal False
    zorder 30

    frame:
        xalign 0.5 yalign 0.08
        background Frame("#000000bb", 8, 8)
        padding (20, 10)
        text "Searching: [room_name]..." size 16 color "#aaaaff"
