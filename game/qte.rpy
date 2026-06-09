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
# Label-based (screen variables were resetting mid-quiz on retry).
# Usage:
#   call qte_cook_run
#   if _return == "success": ...

label qte_cook_run:
    $ cook_score = 0

    "TENDON KOHAKU SET — QUICK-FIRE!"

    menu:
        "Step 1: Pick the broth base!"

        "Dashi stock":
            $ cook_score += 1
        "Tap water":
            pass
        "Energy drink":
            pass

    menu:
        "Step 2: Tempura fry time?"

        "90 seconds":
            $ cook_score += 1
        "2 minutes":
            pass
        "Until vibes":
            pass

    menu:
        "Step 3: Sauce — how much tsuyu?"

        "Just right":
            $ cook_score += 1
        "A little":
            pass
        "A lot":
            pass

    if cook_score >= 2:
        $ cook_result = "success"
    else:
        $ cook_result = "fail"
    return


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
