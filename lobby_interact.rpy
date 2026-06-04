## ============================================================
##  Night at CSE2 — Floor 1 Point-and-Click
## ============================================================

default lobby_examined  = set()
default chud_appeared   = False
default cooking_done    = False

style hotspot_btn:
    background        None
    hover_background  "#ffffff18"
    padding           (0, 0)
    xsize             90
    ysize             70

style hotspot_label:
    color       "#00000000"
    hover_color "#ffffccee"
    size        13
    outlines    [(1, "#000000cc", 0, 0)]
    text_align  0.5

# ── Hotspot screen ────────────────────────────────────────────
screen lobby_hotspots():
    modal False

    ## Elevator
    button:
        style "hotspot_btn"
        xpos 0.80 ypos 0.45 xanchor 0.5 yanchor 0.5
        action Return("elevator")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Elevator" style "hotspot_label"

    ## Stairwell door
    button:
        style "hotspot_btn"
        xpos 0.10 ypos 0.55 xanchor 0.5 yanchor 0.5
        action Return("stairwell")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Stairwell" style "hotspot_label"

    ## Break room — can cook here
    button:
        style "hotspot_btn"
        xpos 0.30 ypos 0.52 xanchor 0.5 yanchor 0.5
        action Return("breakroom")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Break room" style "hotspot_label"

    ## Lab 112 — where Chud wanders out from
    button:
        style "hotspot_btn"
        xpos 0.55 ypos 0.58 xanchor 0.5 yanchor 0.5
        action Return("lab112")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Lab 112" style "hotspot_label"

    ## Vending machine
    button:
        style "hotspot_btn"
        xpos 0.88 ypos 0.62 xanchor 0.5 yanchor 0.5
        action Return("vending")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Vending" style "hotspot_label"

    ## Bulletin board
    button:
        style "hotspot_btn"
        xpos 0.20 ypos 0.38 xanchor 0.5 yanchor 0.5
        action Return("bulletin")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Bulletin board" style "hotspot_label"

    ## Go upstairs — only after getting the ID
    if has_upperclass_id:
        button:
            style "hotspot_btn"
            xsize 160
            xpos 0.10 ypos 0.40 xanchor 0.5 yanchor 0.5
            background "#4b2e8344"
            hover_background "#4b2e8388"
            action Return("exit")
            vbox:
                xalign 0.5 spacing 2
                text "▶ Head upstairs" color "#ddbbff" \
                    hover_color "#ffffff" size 14 xalign 0.5


# ════════════════════════════════════════════════════════════
#  Main floor 1 explore loop
# ════════════════════════════════════════════════════════════

label scene1_lobby_explore:

    scene bg lobby with dissolve
    show screen inventory_hud

    if not lobby_examined:
        "Card readers blink red on every door. You need a different kind of ID."
        inner "There has to be something on this floor."

    label .loop:
        call screen lobby_hotspots

        if _return == "elevator":
            call fl1_elevator
        elif _return == "stairwell":
            call fl1_stairwell
        elif _return == "breakroom":
            call fl1_breakroom
        elif _return == "lab112":
            call fl1_lab112
        elif _return == "vending":
            call fl1_vending
        elif _return == "bulletin":
            call fl1_bulletin
        elif _return == "exit":
            jump scene1_stairwell_locked

        # Chud appears after you've poked around a bit
        if len(lobby_examined) >= 2 and not chud_appeared:
            call fl1_chud_arrives

        jump .loop


# ════════════════════════════════════════════════════════════
#  Hotspot examine labels
# ════════════════════════════════════════════════════════════

label fl1_elevator:
    $ lobby_examined.add("elevator")
    "You press the elevator button. Panel flashes red."
    inner "'After-hours access: faculty and staff Husky Cards only.'"
    inner "Or an upperclassman card, apparently. Typical."
    return

label fl1_stairwell:
    $ lobby_examined.add("stairwell")
    "Card reader blinks red. Your undergrad ID does nothing."
    if has_upperclass_id:
        inner "Chud's ID should work here."
    return

label fl1_bulletin:
    $ lobby_examined.add("bulletin")
    "Research posters. Internship flyers. A hand-drawn comic in the corner."
    "'Ship it anyway.'"
    inner "...Same."
    return

label fl1_vending:
    $ lobby_examined.add("vending")
    "A wall of vending machines. You snag some chips."
    inner "I haven't eaten since noon."
    return

label fl1_breakroom:
    $ lobby_examined.add("breakroom")
    if cooking_done:
        "The break room. The Tendon Kohaku Set sits perfectly plated."
        inner "I can't believe I made that."
        return

    "A small break room. Microwave, mini fridge, a hotplate someone left."
    "And in the fridge: shrimp, eggs, some pre-made tempura batter. Tsuyu sauce in the door."

    inner "...I could make Tendon Kohaku Set. Right now. At 3 AM."
    inner "I shouldn't. But I absolutely could."

    menu:
        "Cook the Tendon Kohaku Set. (Timed challenge)":
            jump fl1_cook_challenge
        "Leave it. Focus.":
            inner "Right. Focus."
            return

label fl1_cook_challenge:

    "You fire up the hotplate."
    "You have done this exactly once before. You remember most of the steps."

    call screen qte_cook

    if _return == "success":
        $ cooking_done = True
        $ has_tendon_kohaku = True
        $ pickup_item("tendon_kohaku")

        # play sound sizzle
        "It comes together. Perfect crunch on the shrimp. Sauce ratio is {i}right{/i}."
        "The smell fills the entire floor."

        inner "I am built different."
        return

    else:
        "You burn the tempura. The smoke alarm chirps twice and then goes back to sleep."
        inner "Never speak of this."
        return


label fl1_lab112:
    $ lobby_examined.add("lab112")

    if chud_appeared:
        "Lab 112's door is ajar. Inside, Chud's laptop is still open."
        "Their Upperclass ID is gone — because it's in your pocket."
        return

    if len(lobby_examined) < 2:
        "Lab 112. The door's closed. Lights are off inside."
        inner "Nothing here right now."
        return

    "Lab 112. The door is ajar. Inside: papers, empty cans, a sleeping bag in the corner."
    inner "Someone {i}lives{/i} here."
    return


# ════════════════════════════════════════════════════════════
#  Chud the grad student arrives
# ════════════════════════════════════════════════════════════

label fl1_chud_arrives:

    $ chud_appeared = True

    scene bg lobby with dissolve

    "From the direction of Lab 112, the door swings open."

    show chud idle at npc_spot with dissolve

    "A grad student. Hoodie. Half-asleep. Badge flipped upside down."
    "They sniff the air."

    if has_tendon_kohaku:
        chud "...Is that Tendon Kohaku."
        show mc idle at player_spot with dissolve
        mc "I— yes?"
        chud "At three in the morning."
        mc "There was a hotplate."
        chud "I have been in that lab for eleven days straight."
        chud "The last thing I ate was a granola bar I found in my own jacket pocket."
    else:
        chud "...Do you smoke?"
        show mc idle at player_spot with dissolve
        mc "I mean— occasionally—"
        chud "I can smell it on you from here."
        chud "I've been in that lab for eleven days."
        chud "I needed that."

    "They look at you. Really look at you."

    chud "You're trying to get upstairs, aren't you."

    mc "...Yes."

    chud "Third floor?"

    mc "How did you—"

    chud "There are like four of you down here at night every other week."

    "They unclip their ID badge and hold it out."

    chud "It'll get you to floor two. Maybe three if the reader's bugged."
    chud "Bring it back. Eventually."

    if has_tendon_kohaku:
        chud "And leave the food."
        mc "Done."

    $ has_upperclass_id = True
    $ pickup_item("upperclass_id")

    hide chud with dissolve
    hide mc   with dissolve

    "They take the bowl — or disappear back into Lab 112 — and the door closes."
    inner "That was the nicest interaction I've had all week."

    "A ▶ prompt glows near the stairwell door."
    return
