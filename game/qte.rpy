## ============================================================
##  Night at CSE2 — QTE / Timed Challenge System
## ============================================================

# Key pool for dodge QTEs — spread across keyboard, no lookalike chars
define QTE_KEYS = ["e", "f", "g", "r", "t", "v", "x", "z"]

# ── Quick-Time Event: press the right key in time ─────────────
# Usage:
#   call screen qte_dodge(prompt="The groupmate turns the corner—", time_limit=5.0)
#   if _return == "success": ...
#
screen qte_dodge(prompt="DODGE!", time_limit=5.0):
    modal True
    zorder 50

    # Pick a random key once when the screen opens
    default qte_key = renpy.random.choice(QTE_KEYS)

    # Timeout → fail
    timer time_limit action Return("fail")

    # Key bindings: correct key = success, every other pool key = immediate fail
    for k in QTE_KEYS:
        if k == qte_key:
            key k action Return("success")
        else:
            key k action Return("fail")

    # Red vignette border
    frame:
        xfill True yfill True
        background "#cc000044"

    frame:
        xalign 0.5
        yalign 0.55
        background Frame("#0a0a0aee", 14, 14)
        padding (60, 36)

        vbox:
            spacing 16
            xalign 0.5

            # Situation prompt
            text prompt:
                size 24
                color "#ffcccc"
                xalign 0.5
                text_align 0.5

            # Big key display
            frame:
                xalign 0.5
                background Frame("#cc2222cc", 10, 10)
                padding (28, 18)

                text "[qte_key!u]":
                    size 80
                    color "#ffffff"
                    bold True
                    xalign 0.5

            text "PRESS NOW":
                size 14
                color "#ff8888"
                xalign 0.5
                text_align 0.5

            # Countdown bar — drains left to right over time_limit seconds
            bar:
                value AnimatedValue(0, time_limit, time_limit)
                range time_limit
                xsize 380
                ysize 14
                xalign 0.5
                left_bar  Frame("#ff3333", 0, 0)
                right_bar Frame("#2a0000", 0, 0)
                thumb      None

style qte_key_text:
    size 80
    color "#ffffff"
    bold True


# ── Timed cooking challenge ───────────────────────────────────
# Label-based (screen variables were resetting mid-quiz on retry).
# Usage:
#   call qte_cook_run
#   cook_result == "success" or "fail" after return

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
screen searching_room(room_name):
    modal False
    zorder 30

    frame:
        xalign 0.5 yalign 0.08
        background Frame("#000000bb", 8, 8)
        padding (20, 10)
        text "Searching: [room_name]..." size 16 color "#aaaaff"
