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
        xpos 0.95 ypos 0.85 xanchor 0.5 yanchor 0.5
        action Return("elevator")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Elevator" style "hotspot_label"

    ## Stairwell door
    button:
        style "hotspot_btn"
        xpos 0.45 ypos 0.75 xanchor 0.5 yanchor 0.5
        action Return("stairwell")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Stairwell" style "hotspot_label"

    ## Break room — can cook here
    button:
        style "hotspot_btn"
        xpos 0.30 ypos 0.68 xanchor 0.5 yanchor 0.5
        action Return("breakroom")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Break room" style "hotspot_label"

    ## TA Room — where Chud wanders out from
    button:
        style "hotspot_btn"
        xpos 0.22 ypos 0.71 xanchor 0.5 yanchor 0.5
        action Return("lab112")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "TA Room" style "hotspot_label"

    ## Vending machine
    button:
        style "hotspot_btn"
        xpos 0.88 ypos 0.72 xanchor 0.5 yanchor 0.5
        action Return("vending")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Vending" style "hotspot_label"

    ## Bulletin board
    button:
        style "hotspot_btn"
        xpos 0.60 ypos 0.65 xanchor 0.5 yanchor 0.5
        action Return("bulletin")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            text "Bulletin board" style "hotspot_label"

    ## Chud — always present, standing near TA Room
    button:
        style "hotspot_btn"
        xsize 110
        xpos 0.57 ypos 0.70 xanchor 0.5 yanchor 0.5
        action Return("chud")
        vbox:
            xalign 0.5 spacing 2
            add "images/items/hotspot_idle.png" xalign 0.5
            if has_upperclass_id:
                text "Chud ✓" style "hotspot_label"
            else:
                text "???" style "hotspot_label"

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
                text "▶ Head upstairs" color "#ddbbff" hover_color "#ffffff" size 14 xalign 0.5


# ════════════════════════════════════════════════════════════
#  Main floor 1 explore loop
# ════════════════════════════════════════════════════════════

label scene1_lobby_explore:

    scene bg lobby with dissolve
    show screen inventory_hud
    show chud idle at chud_far with dissolve

    if not lobby_examined:
        play sound "audio/67_SQlv2Xv.mp3" volume 0.3
        "Card readers blink red on every door. You need a different kind of ID."
        inner "There has to be something on this floor."

    label .loop:
        show chud idle at chud_far
        call screen lobby_hotspots

        if _return == "elevator":
            call fl1_elevator from _call_fl1_elevator
        elif _return == "stairwell":
            call fl1_stairwell from _call_fl1_stairwell
        elif _return == "breakroom":
            call fl1_breakroom from _call_fl1_breakroom
        elif _return == "lab112":
            call fl1_lab112 from _call_fl1_lab112
        elif _return == "vending":
            call fl1_vending from _call_fl1_vending
        elif _return == "bulletin":
            call fl1_bulletin from _call_fl1_bulletin
        elif _return == "chud":
            call fl1_chud_interact from _call_fl1_chud_interact
        elif _return == "exit":
            if has_upperclass_id:
                jump scene1_stairwell_try_id
            else:
                jump scene1_stairwell_locked

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
    inner "Let's see what's on the board."
    call screen bulletin_3d_examine
    if _return == "card_found" and not has_upperclass_id:
        $ has_upperclass_id = True
        $ pickup_item("upperclass_id")
        inner "There was an Upperclass Husky Card taped to the back."
        mc "...what a chud who forgot this."
    else:
        "Research posters. Internship flyers."
        inner "Someone crossed out their entire TODO list and wrote 'Ship it anyway.'"
        inner "...I respect that."
    return


# ── Ace Attorney-style 3D bulletin board examine ──────────────
screen bulletin_3d_examine():
    modal True

    default angle    = 0       # 0–359 degrees
    default dragging = False
    default drag_x   = 0
    default card_seen = False

    $ frame_idx = (angle // 10) % 36
    $ on_back   = 90 < angle < 270

    # Dark backdrop
    add "#000000dd"

    # Rotating billboard frame
    add ( "images/bulletin_3d/frame%02d.png" % frame_idx ) xalign 0.5 yalign 0.48

    # Hint text
    frame:
        xalign 0.5 yalign 0.06
        background Frame("#00000099", 6, 6)
        padding (18, 6)
        text "← Click to flip →" size 14 color "#aaaaaa"

    # Left zone — flip to back if on front, flip to front if on back
    button:
        xsize 640 yfill True
        xpos 0 ypos 0
        background None
        hover_background "#ffffff08"
        action If(on_back, SetScreenVariable("angle", 0), SetScreenVariable("angle", 180))

    # Right zone — same flip behaviour
    button:
        xsize 640 yfill True
        xpos 1280 ypos 0
        background None
        hover_background "#ffffff08"
        action If(on_back, SetScreenVariable("angle", 0), SetScreenVariable("angle", 180))

    # Centre zone — no-op
    button:
        xsize 640 yfill True
        xpos 640 ypos 0
        background None
        action NullAction()

    # Back-face discovery prompt
    if on_back:
        $ card_seen = True
        frame:
            xalign 0.5 yalign 0.88
            background Frame("#1a0a0099", 8, 8)
            padding (24, 10)
            hbox:
                spacing 16
                xalign 0.5
                textbutton "Take Husky Card":
                    action Return("card_found")
                    text_color "#ffe080"
                    text_hover_color "#ffffff"
                    text_size 15

    # Done button
    frame:
        xalign 0.5 yalign 0.94
        background Frame("#000000bb", 6, 6)
        padding (20, 8)
        textbutton "← Put it down":
            action Return("done")
            text_color "#cccccc"
            text_hover_color "#ffffff"
            text_size 14

label fl1_vending:
    $ lobby_examined.add("vending")
    inner "A vending machine. HUSKYSNAX."
    call screen vending_examine
    if _return == "dispensed":
        if not has_chips:
            $ has_chips = True
            $ pickup_item("chips")
            play sound "audio/bp02.mp3" volume 0.5
            inner "BBQ chips at 3 AM. This is fine."
        else:
            inner "I already have chips. One bag is enough. Probably."
    return


screen vending_examine():
    modal True

    default angle    = 0
    default dispensed = False

    $ frame_idx = (angle // 10) % 36
    $ on_front  = angle < 90 or angle > 270

    add "#000000ee"

    # Rotating vending machine
    add ( "images/vending_3d/frame%02d.png" % frame_idx ) xalign 0.5 yalign 0.5

    # Flip zones
    button:
        xsize 300 yfill True xpos 0 ypos 0
        background None hover_background "#ffffff06"
        action If(on_front, SetScreenVariable("angle", 180), SetScreenVariable("angle", 0))

    button:
        xsize 300 yfill True xpos 780 ypos 0
        background None hover_background "#ffffff06"
        action If(on_front, SetScreenVariable("angle", 180), SetScreenVariable("angle", 0))

    # Dispense button — only on front face, centred
    if on_front:
        frame:
            xalign 0.5 yalign 0.78
            background Frame("#00000000", 0, 0)
            padding (0, 0)
            # Invisible hit area over the on-screen dispense button
            button:
                xysize (160, 80)
                background None
                hover_background "#ff330033"
                action Return("dispensed")

    # Hint
    frame:
        xalign 0.5 yalign 0.06
        background Frame("#00000099", 6, 6)
        padding (16, 6)
        text "Click the DISPENSE button to vend" size 13 color "#aaaaaa"

    # Done
    frame:
        xalign 0.5 yalign 0.94
        background Frame("#000000bb", 6, 6)
        padding (20, 8)
        textbutton "← Step back":
            action Return("none")
            text_color "#cccccc" text_hover_color "#ffffff" text_size 14

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

    call qte_cook_run from _call_qte_cook_run

    if cook_result == "success":
        $ cooking_done = True
        $ has_tendon_kohaku = True
        play sound "audio/lego.mp3"
        $ pickup_item("tendon_kohaku")

        play audio "audio/sizzle.ogg"
        "It comes together. Perfect crunch on the shrimp. Sauce ratio is {i}right{/i}."
        play sound "audio/vine-boom.mp3" volume 0.5
        "The smell fills the entire floor."

        inner "I am built different."
        return

    else:
        play sound "audio/tmp_7901-951678082.mp3" volume 0.3
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
#  Chud — interactive NPC, always standing near Lab 112
# ════════════════════════════════════════════════════════════

label fl1_chud_interact:

    # Show sleeping animation first, then wake up into talking
    show chud sleeping at chud_spot with dissolve
    pause 1.0
    show chud talking at chud_spot with None

    if has_upperclass_id:
        # Already has the ID — brief dismissal
        chud "You still here? Go. Go go go."
        show mc idle at player_spot with dissolve
        mc "Right. Going."
        show chud idle at chud_far with dissolve
        hide mc with dissolve
        return

    if (has_tendon_kohaku or has_chips) and not chud_appeared:
        # Has food, approaching Chud for the first time
        $ chud_appeared = True
        show mc idle at player_spot with dissolve
        "They're leaning against the wall near Lab 112. Hoodie. Badge upside down. Eyes half-closed."
        "Then they sniff the air."
        if has_tendon_kohaku:
            chud "...Is that Tendon Kohaku."
            mc "I— yes. I made it. In the break room."
            chud "At three in the morning."
            mc "There was a hotplate and I panicked."
            chud "I have been in that lab for eleven days."
            chud "The last thing I ate was a granola bar I found in my own jacket."
        else:
            chud "...are those chips."
            mc "BBQ. From the vending machine."
            chud "I have been in that lab for eleven days."
            chud "The last thing I ate was a granola bar I found in my own jacket."
            chud "...I will accept the chips."
        jump fl1_chud_give_id

    elif not chud_appeared:
        # First time talking — no food yet
        $ chud_appeared = True
        show mc idle at player_spot with dissolve
        "They're slumped against the wall outside Lab 112. Hoodie. Eyes half-open."
        chud "...hey."
        mc "Hey. Are you okay?"
        chud "I've been in that lab for eleven days."
        mc "...That's not healthy."
        chud "No it is not."
        "They sniff the air."
        show chud thinking at chud_spot with None
        chud "...You smoke?"
        mc "Occasionally."
        show chud talking at chud_spot with None
        chud "I can smell it on you. I needed that. That's a real-world smell."
        chud "You trying to get upstairs?"
        mc "How did you—"
        chud "There are like four of you every other week."
        "They look at you properly."
        show chud thinking at chud_spot with None
        pause 0.6
        show chud talking at chud_spot with None
        chud "I'd give you my card but... I'm starving. You got anything to eat?"
        mc "I'll see what I can find."
        show chud thinking at chud_far with dissolve
        hide mc with dissolve
        inner "They want food. The vending machine's right there, or the break room..."
        return

    elif has_tendon_kohaku or has_chips:
        # Talked before, now has food
        show mc idle at player_spot with dissolve
        if has_tendon_kohaku:
            chud "...Wait. Is that—"
            mc "Tendon Kohaku Set. Just made it."
            chud "You absolute legend."
        else:
            chud "...You came back with chips?"
            mc "BBQ chips. It's what the machine had."
            chud "I respect the commitment."
        jump fl1_chud_give_id

    else:
        # Talked before, still no food
        show mc idle at player_spot with dissolve
        chud "You find anything yet?"
        mc "Still looking."
        chud "I'll be here. Obviously."
        show chud thinking at chud_far with dissolve
        hide mc with dissolve
        return


label fl1_chud_give_id:

    show chud thinking at chud_spot with None
    show mc idle at player_spot with None

    pause 0.5
    show chud talking at chud_spot with None
    chud "You're trying to get to the third floor, aren't you."
    mc "How did you—"
    chud "There are like four of you down here at night every other week."

    "They unclip their ID and hold it out."

    show chud thinking at chud_spot with None
    pause 0.4
    show chud talking at chud_spot with None
    chud "Gets you to floor two, maybe three if the reader's bugged."
    chud "Bring it back. Eventually."
    show chud thinking at chud_spot with None

    if has_tendon_kohaku:
        chud "Leave the food."
        mc "Obviously."
    elif has_chips:
        chud "Leave the chips."
        mc "They're yours."

    $ has_upperclass_id = True
    $ pickup_item("upperclass_id")

    play sound "audio/rizz-sound-effect.mp3" volume 0.4
    hide chud with dissolve
    hide mc with dissolve

    inner "That was the most efficient transaction I have ever made."
    "A ▶ prompt glows near the stairwell door."
    return
