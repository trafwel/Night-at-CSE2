## ============================================================
##  Night at CSE2 — Full Game Script
##  Group H: Leon, Luke, Kaung, An
## ============================================================

# ── BACKGROUNDS ──────────────────────────────────────────────
image bg uw night     = im.Scale("uw night.jpg",                       1920, 1080)
image bg exterior     = im.Scale("cseoutside.jpg",                     1920, 1080)
image bg lobby        = im.Scale("images/cse lobby.jpeg",              1920, 1080)
image bg hallway      = im.Scale("images/cse lobby.jpeg",              1920, 1080)
image bg stairwell    = im.Scale("images/cse building 1st floor inside.jpg", 1920, 1080)
image bg floor2       = im.Scale("images/second floor.jpeg",              1920, 1080)
image bg floor2_lab   = im.Scale("images/second floor.jpeg",              1920, 1080)
image bg floor3       = im.Scale("images/second floor.jpeg",              1920, 1080)
image bg elevator     = im.Scale("images/elevator inside.jpeg",           1920, 1080)
image bg seitz_office = im.Scale("images/seitz_room.jpeg",                1920, 1080)
image bg bulletin     = im.Scale("images/bg_bulletin.png", 1920, 1080)
image bg roof         = Solid("#000510")   # TODO: replace with night sky / roof photo

# ── ANIMATIONS (definitions in mc_sprites.rpy / groupmate_sprites.rpy) ──
# Assets live in game/images/anims/
#
# MC — WebM (ready):
#   mc thinking   → MC_Thinking.webm
#   mc shocked    → MC_Shocked.webm
#   mc panicked   → MC_Scared.webm
#   mc running    → jump.webm
#   mc celebrate  → MC_Happy.webm
#
# MC — placeholder PNG (TODO: add WebM):
#   mc idle, mc hiding, mc cooking, mc typing
#   mc clutching_head, mc deep_breath
#
# GROUPMATE — WebM (ready):
#   groupmate angry      → angry.webm
#   groupmate walking    → walking.webm
#   groupmate shooting   → gunshooting.webm
#   groupmate jumpscare  → fnaf.webm
#   groupmate punch      → punching.webm  (unused in script)
#
# GROUPMATE — PNG ATL (ready):
#   groupmate normal     → images/groupmate_idle/
#
# GROUPMATE — TODO: dance anim (true ending)
#
# Placeholder PNGs still used below for MC states without a WebM yet.
image mc idle:
    block:
        "images/mc_idle_frames/frame0001.png"
        pause 0.041667
        "images/mc_idle_frames/frame0002.png"
        pause 0.041667
        "images/mc_idle_frames/frame0003.png"
        pause 0.041667
        "images/mc_idle_frames/frame0004.png"
        pause 0.041667
        "images/mc_idle_frames/frame0005.png"
        pause 0.041667
        "images/mc_idle_frames/frame0006.png"
        pause 0.041667
        "images/mc_idle_frames/frame0007.png"
        pause 0.041667
        "images/mc_idle_frames/frame0008.png"
        pause 0.041667
        "images/mc_idle_frames/frame0009.png"
        pause 0.041667
        "images/mc_idle_frames/frame0010.png"
        pause 0.041667
        "images/mc_idle_frames/frame0011.png"
        pause 0.041667
        "images/mc_idle_frames/frame0012.png"
        pause 0.041667
        "images/mc_idle_frames/frame0013.png"
        pause 0.041667
        "images/mc_idle_frames/frame0014.png"
        pause 0.041667
        "images/mc_idle_frames/frame0015.png"
        pause 0.041667
        "images/mc_idle_frames/frame0016.png"
        pause 0.041667
        "images/mc_idle_frames/frame0017.png"
        pause 0.041667
        "images/mc_idle_frames/frame0018.png"
        pause 0.041667
        "images/mc_idle_frames/frame0019.png"
        pause 0.041667
        "images/mc_idle_frames/frame0020.png"
        pause 0.041667
        "images/mc_idle_frames/frame0021.png"
        pause 0.041667
        "images/mc_idle_frames/frame0022.png"
        pause 0.041667
        "images/mc_idle_frames/frame0023.png"
        pause 0.041667
        "images/mc_idle_frames/frame0024.png"
        pause 0.041667
        "images/mc_idle_frames/frame0025.png"
        pause 0.041667
        "images/mc_idle_frames/frame0026.png"
        pause 0.041667
        "images/mc_idle_frames/frame0027.png"
        pause 0.041667
        "images/mc_idle_frames/frame0028.png"
        pause 0.041667
        "images/mc_idle_frames/frame0029.png"
        pause 0.041667
        "images/mc_idle_frames/frame0030.png"
        pause 0.041667
        "images/mc_idle_frames/frame0031.png"
        pause 0.041667
        "images/mc_idle_frames/frame0032.png"
        pause 0.041667
        "images/mc_idle_frames/frame0033.png"
        pause 0.041667
        "images/mc_idle_frames/frame0034.png"
        pause 0.041667
        "images/mc_idle_frames/frame0035.png"
        pause 0.041667
        "images/mc_idle_frames/frame0036.png"
        pause 0.041667
        "images/mc_idle_frames/frame0037.png"
        pause 0.041667
        "images/mc_idle_frames/frame0038.png"
        pause 0.041667
        "images/mc_idle_frames/frame0039.png"
        pause 0.041667
        "images/mc_idle_frames/frame0040.png"
        pause 0.041667
        "images/mc_idle_frames/frame0041.png"
        pause 0.041667
        "images/mc_idle_frames/frame0042.png"
        pause 0.041667
        "images/mc_idle_frames/frame0043.png"
        pause 0.041667
        "images/mc_idle_frames/frame0044.png"
        pause 0.041667
        "images/mc_idle_frames/frame0045.png"
        pause 0.041667
        "images/mc_idle_frames/frame0046.png"
        pause 0.041667
        "images/mc_idle_frames/frame0047.png"
        pause 0.041667
        "images/mc_idle_frames/frame0048.png"
        pause 0.041667
        "images/mc_idle_frames/frame0049.png"
        pause 0.041667
        "images/mc_idle_frames/frame0050.png"
        pause 0.041667
        "images/mc_idle_frames/frame0051.png"
        pause 0.041667
        "images/mc_idle_frames/frame0052.png"
        pause 0.041667
        "images/mc_idle_frames/frame0053.png"
        pause 0.041667
        "images/mc_idle_frames/frame0054.png"
        pause 0.041667
        "images/mc_idle_frames/frame0055.png"
        pause 0.041667
        "images/mc_idle_frames/frame0056.png"
        pause 0.041667
        "images/mc_idle_frames/frame0057.png"
        pause 0.041667
        "images/mc_idle_frames/frame0058.png"
        pause 0.041667
        "images/mc_idle_frames/frame0059.png"
        pause 0.041667
        "images/mc_idle_frames/frame0060.png"
        pause 0.041667
        repeat

image mc hiding:
    block:
        "images/anim_frames_scream/frame0001.png"
        pause 0.041667
        "images/anim_frames_scream/frame0002.png"
        pause 0.041667
        "images/anim_frames_scream/frame0003.png"
        pause 0.041667
        "images/anim_frames_scream/frame0004.png"
        pause 0.041667
        "images/anim_frames_scream/frame0005.png"
        pause 0.041667
        "images/anim_frames_scream/frame0006.png"
        pause 0.041667
        "images/anim_frames_scream/frame0007.png"
        pause 0.041667
        "images/anim_frames_scream/frame0008.png"
        pause 0.041667
        "images/anim_frames_scream/frame0009.png"
        pause 0.041667
        "images/anim_frames_scream/frame0010.png"
        pause 0.041667
        "images/anim_frames_scream/frame0011.png"
        pause 0.041667
        "images/anim_frames_scream/frame0012.png"
        pause 0.041667
        "images/anim_frames_scream/frame0013.png"
        pause 0.041667
        "images/anim_frames_scream/frame0014.png"
        pause 0.041667
        "images/anim_frames_scream/frame0015.png"
        pause 0.041667
        "images/anim_frames_scream/frame0016.png"
        pause 0.041667
        "images/anim_frames_scream/frame0017.png"
        pause 0.041667
        "images/anim_frames_scream/frame0018.png"
        pause 0.041667
        "images/anim_frames_scream/frame0019.png"
        pause 0.041667
        "images/anim_frames_scream/frame0020.png"
        pause 0.041667
        "images/anim_frames_scream/frame0021.png"
        pause 0.041667
        "images/anim_frames_scream/frame0022.png"
        pause 0.041667
        "images/anim_frames_scream/frame0023.png"
        pause 0.041667
        "images/anim_frames_scream/frame0024.png"
        pause 0.041667
        "images/anim_frames_scream/frame0025.png"
        pause 0.041667
        "images/anim_frames_scream/frame0026.png"
        pause 0.041667
        "images/anim_frames_scream/frame0027.png"
        pause 0.041667
        "images/anim_frames_scream/frame0028.png"
        pause 0.041667
        "images/anim_frames_scream/frame0029.png"
        pause 0.041667
        "images/anim_frames_scream/frame0030.png"
        pause 0.041667
        repeat

image mc cooking  = "images/anim_frames_idle/frame0001.png"
image mc typing   = "images/anim_frames_idle/frame0001.png"

# ── NPC SPRITES ──────────────────────────────────────────────
image seitz idle  = "images/seitz_placeholder.png"
image chud idle   = "images/chud_placeholder.png"
image paul idle   = "images/paul_placeholder.png"    # [TODO: 3D model]

# ── CHARACTER POSITIONS ──────────────────────────────────────
transform player_spot:
    xalign 0.12 ypos 0.8 yanchor 1.0 zoom 0.74

transform npc_spot:
    xalign 0.80 yalign 1.0 zoom 0.82

transform npc_far:
    xalign 0.57 yalign 1.0 zoom 0.62

transform center_stage:
    xalign 0.5 yalign .0 zoom 0.82

transform paul_spot:
    xpos 0.5 ypos 0.32
    xanchor 0.5 yanchor 0.5
    zoom 2

# ── TRANSITIONS ──────────────────────────────────────────────
define flash           = Fade(0.1,  0.0, 0.4, color="#ffffff")
define jumpscare_flash = Fade(0.05, 0.0, 0.6, color="#cc0000")
define red_flash       = Fade(0.05, 0.0, 0.3, color="#880000")

# ── JUMPSCARE TRANSFORM ───────────────────────────────────────
transform jumpscare_rush:
    xalign -0.35 yalign 0.85 zoom 0.9 alpha 1.0
    easeout 0.30 xalign 0.5 yalign 0.5 zoom 3.6

# ── AUDIO (game/audio/) ──────────────────────────────────────
define audio.glock       = "audio/glock.ogg"
define audio.jumpscare   = "audio/jumpscare.ogg"
define audio.sizzle      = "audio/sizzle.ogg"
define audio.door_beep   = "audio/door_beep.ogg"
define audio.fnaf        = "audio/fnaf.mp3"

# ── CHARACTERS ───────────────────────────────────────────────
define mc        = Character("You",            color="#87ceeb")
define inner     = Character(None,             what_italic=True, what_color="#b8f0b8")
define groupmate = Character("Groupmate",      color="#ff6b6b")
define seitz     = Character("Prof. Seitz",    color="#ffcc66")
define chud      = Character("Grad Student",   color="#cc9966")
define paul      = Character("Paul G. Allen",  color="#ffd700")

# ── GAME STATE ───────────────────────────────────────────────
default report_quality   = 0    # 0-5, determines ending
default laptop_found     = False
default talked_to_seitz  = False


# ════════════════════════════════════════════════════════════
#  INTRO — 3 AM, THE FOUNTAIN
# ════════════════════════════════════════════════════════════

label start:

    show screen inventory_hud
    scene black with fade

    "3:00 AM."
    play music "audio/scary-start.ogg"
    "You are walking home after a long day of doomscrolling."
    "The campus is empty. Quiet. The fountain is lit up. It's kind of nice actually."

    pause 0.4

    scene bg uw night with dissolve
    show mc idle at player_spot with dissolve

    inner "I'll just finish the project later. The due date's not until six, it's fine..."

    pause 0.3

    "And then:"

    show mc shocked at player_spot with None

    show groupmate normal at npc_spot with dissolve

    groupmate "THERE YOU ARE."

    mc "Oh no."

    groupmate "I have been looking for you ALL DAY."

    mc "I was in the library—"

    groupmate "I SAW YOU ON DISCORD."

    "They reach into their jacket."

    show mc panicked at player_spot with None

    groupmate "I pulled out a knife AND a glock for this moment. You are finishing that report or you will be finished."

    mc "WHAT—"

    show groupmate shooting at npc_spot with None

    play sound "audio/glock.ogg"
    "They open fire."
    play sound "audio/glock.ogg"
    queue sound "audio/glock.ogg"

    scene bg uw night with flash

    "You run."

    hide mc with None
    hide groupmate with None

    stop music fadeout 1.0
    jump scene1_entrance


# ════════════════════════════════════════════════════════════
#  SCENE 1 — CSE2 ENTRANCE & FLOOR 1
#  Objective: get the Upperclass Husky ID from Chud
# ════════════════════════════════════════════════════════════

label scene1_entrance:

    scene bg exterior with dissolve

    "You sprint toward the CSE2 building."
    "Behind you, the groupmate {b}speedwalks{/b} in your direction. Menacingly."

    inner "WHY IS THAT MORE TERRIFYING THAN RUNNING"

    show groupmate walking at npc_far with dissolve

    groupmate "(shouting) YOU'RE NOT RUNNING AWAY FROM THIS DEAD... LINE..."

    hide groupmate with dissolve

    show mc running at player_spot with dissolve

    "You burst through the front doors of CSE2 and slam them shut."
    "You jam a chair under the handle."

    show mc panicked at player_spot with None

    "Through the glass: the groupmate stops. Stares at you."
    "Then they start walking around the building. It seems like they forgot their Husky Card? That's lucky."

    inner "That won't hold. I need to get upstairs before they find another way in."
    show mc thinking at player_spot with None
    inner "Let's see- if I can just finish my assignment... I need to get my laptop first. I think it was on the second floor somewhere?"
    inner "Wait, I forgot about that one bug with the light reflection. Shoot. Maybe I can see if there's anyone on the third floor that can help me?"
    inner "And eduroam's down too! Shoot- I'll just take it one step at a time, I guess."
    inner "But first... I need a way past these card readers. Undergrad ID won't cut it."

    hide mc with None

    scene bg lobby with dissolve

    jump scene1_lobby_explore


label scene1_stairwell_locked:

    "The stairwell door blinks red. Undergrad card won't cut it."

    if has_upperclass_id:
        inner "Wait. I have the Chud's ID."
        jump scene1_stairwell_try_id
    else:
        inner "I need a card that can open this."
        jump scene1_lobby_explore


label scene1_stairwell_try_id:

    "You hold the upperclass-class Husky Card up to the reader."

    play sound "audio/door_beep.ogg"

    "GREEN."

    mc "(quietly) Let's go."

    if has_upperclass_id and has_tendon_kohaku:
        inner "Hm... I guess I could use the card to skip straight to the roof... Is that a good idea though?"

        menu:
            "Take the stairs.":
                jump scene2_floor2
            "Take the elevator straight to the roof (Floor 4).":
                jump scene4_elevator_route

    else:
        jump scene2_floor2


# ════════════════════════════════════════════════════════════
#  SCENE 2 — SECOND FLOOR
#  Objective: find your laptop
# ════════════════════════════════════════════════════════════

label scene2_floor2:

    scene bg floor2 with dissolve

    show mc panicked at player_spot with dissolve

    "Second floor. Research wing."
    "Your laptop is somewhere up here. You left it before everything went sideways. You curse the fact that you were scrolling on instagram reels for so long."

    inner "Which lab was it..."

    show mc thinking at player_spot with None

    inner "202? 204? The one with the broken whiteboard? Shoot, I can't remember!"

    hide mc with None

    $ laptop_room = renpy.random.choice(["201A", "201B", "203", "205"])

    jump scene2_search_loop


label scene2_search_loop:

    scene bg floor2 with None

    "You try the first door."

    menu:
        "Check Room 201A.":
            jump scene2_check_201a
        "Check Room 201B.":
            jump scene2_check_201b
        "Check Room 203.":
            jump scene2_check_203
        "Check Room 205.":
            jump scene2_check_205


label scene2_check_201a:
    if laptop_room == "201A":
        jump scene2_found_laptop
    "A protein powder tub. Someone's sad pile of instant noodles. No laptop."
    jump scene2_try_again

label scene2_check_201b:
    if laptop_room == "201B":
        jump scene2_found_laptop
    "A whiteboard covered in a proof that trails off with '???' at the end."
    "No laptop."
    jump scene2_try_again

label scene2_check_203:
    if laptop_room == "203":
        jump scene2_found_laptop
    "This room smells like it has been marinated in Red Bull."
    "No laptop."
    jump scene2_try_again

label scene2_check_205:
    if laptop_room == "205":
        jump scene2_found_laptop
    "An extremely comfortable-looking beanbag. You resist."
    "No laptop."
    jump scene2_try_again

label scene2_try_again:

    if laptop_found:
        jump scene2_floor2_end

    "You keep looking."

    # Groupmate can break in here
    $ break_chance = renpy.random.randint(1, 3)
    if break_chance == 1:
        jump scene2_groupmate_breaks_in

    jump scene2_search_loop


label scene2_groupmate_breaks_in:

    scene bg floor2 with red_flash

    "The stairwell door at the end of the hall SLAMS open."

    show groupmate angry at npc_far with None

    groupmate "(from the stairwell) I CAN SMELL YOUR FEAR FROM HERE. AND YOU- oh god, when was the last time you took a shower?"

    show mc panicked at player_spot with None

    hide groupmate with None

    inner "THEY GOT IN. HOW DID THEY GET IN."

    call screen qte_dodge("The groupmate rounds the corner—", 3.5)

    if _return == "success":
        "You press into a doorway. They walk past without seeing you."
        inner "Don't breathe. Don't breathe."
        "They continue down the hall. You hear a door bang."
        hide mc with None
    else:
        jump scene_jumpscare

    jump scene2_search_loop


label scene2_found_laptop:

    $ laptop_found = True
    scene bg floor2_lab with dissolve

    show mc idle at player_spot with dissolve

    "There it is. Your laptop, sitting exactly where you left it. Still running Blender, too."

    # show Polymarket popup ad as a joke
    show screen polymarket_ad

    mc "...Why do I have a Polymarket tab open."

    hide screen polymarket_ad

    show mc typing at player_spot with None

    "You grab the laptop and shove it in your bag."
    inner "Floor 3. It'll buy me some time, and Seitz's office is there. Maybe he's still there, somehow?"

    $ report_quality += 1

    hide mc with dissolve
    jump scene2_floor2_end


label scene2_floor2_end:

    scene bg floor2 with dissolve
    inner "Third floor. Seitz's office. Go."
    jump scene3_floor3


# ── Polymarket ad screen ──────────────────────────────────────
screen polymarket_ad():
    modal True
    frame:
        xalign 0.5 yalign 0.4
        background "#ffffffff"
        xpadding 30 ypadding 20
        minimum (400, 200)
        vbox:
            spacing 8 xalign 0.5
            text "POLYMARKET" size 28 color "#00aa44" bold True xalign 0.5
            text "Will you submit your CSE 457 report on time?" size 16 color "#222222" xalign 0.5
            null height 8
            hbox:
                spacing 30 xalign 0.5
                vbox:
                    text "YES" size 14 color "#00aa44" bold True xalign 0.5
                    text "23¢" size 22 color "#00aa44" bold True xalign 0.5
                vbox:
                    text "NO"  size 14 color "#cc0000" bold True xalign 0.5
                    text "77¢" size 22 color "#cc0000" bold True xalign 0.5
            null height 8
            textbutton "Close Ad" xalign 0.5 action Hide("polymarket_ad")


# ════════════════════════════════════════════════════════════
#  SCENE 3 — THIRD FLOOR: SEITZ'S OFFICE
#  Objective: sneak past the groupmate to reach the office
# ════════════════════════════════════════════════════════════

label scene3_floor3:

    scene bg floor3 with dissolve

    show mc idle at player_spot with dissolve

    "Third floor. Faculty offices."
    "At the far end of the corridor is a light under Prof. Seitz's door."

    inner ".. how is he still here? You know what, never mind. Far be it from me to look a gift horse in the mouth."
    inner "If anyone can tell me how to salvage this project in two hours, it's him."

    show mc thinking at player_spot with None

    "You start down the corridor."

    "Then: the stairwell door behind you eases open."

    show groupmate normal at npc_far with None

    inner "HOW."

    groupmate "(barely above a whisper) ...I can hear you thinking."

    show mc panicked at player_spot with None

    hide groupmate with None

    "They haven't seen you yet. They're checking doors."

    inner "If I can get to Seitz's office before they reach this end of the hall..."

    hide mc with None

    call screen qte_dodge("The groupmate scans the corridor. Move NOW!", 4.0)

    if _return == "success":
        jump scene3_reach_seitz
    else:
        jump scene_jumpscare


label scene3_reach_seitz:

    scene bg seitz_office with dissolve

    "You make it to the door and knock."

    pause 0.8

    "Nothing."

    "You knock harder."

    show seitz idle at npc_spot with dissolve

    seitz "Who is it now?"

    show mc idle at player_spot with dissolve

    mc "Professor Seitz. It's me. CSE 457. I need help."

    seitz "It's three in the morning."

    mc "I know."

    seitz "..."

    "The door opens."

    seitz "You have ten minutes. Get in."

    $ talked_to_seitz = True

    jump scene3_seitz_advice


label scene3_seitz_advice:

    scene bg seitz_office with dissolve

    show mc typing at player_spot with dissolve
    show seitz idle at npc_spot with dissolve

    "He looks at the laptop. Looks at you. Looks at the laptop again."

    seitz "This... is not as bad as I expected."

    mc "Really?"

    seitz "No, I was joking. Your thing isn't even rendering at all."

    "He leans over and starts pointing to random blocks of code."

    seitz "I would look at how you're using the light physics here and calculating the... "

    show mc thinking at player_spot with None

    mc "Okay. But what about this bug with the object not being linked to the-"

    seitz "That's Project 1 stuff. You remember that, right?"

    mc "...Mostly."

    seitz "..."

    $ report_quality += 2

    "Twenty minutes later:"

    seitz "That's as good as it's going to get tonight. You'll probably pass. Probably."

    mc "Thank you. Seriously."

    seitz "Don't thank me. You should've come to office hours."

    "And then, from outside the door:"

    show groupmate angry at npc_far with None

    groupmate "(from the hallway) OPEN UP! I KNOW THEY'RE IN THERE!"

    hide groupmate with None

    show mc panicked at player_spot with None

    mc "That's—"

    seitz "The consequences of your actions, I would guess. Good luck."

    hide mc with None
    hide seitz with None

    jump scene3


label scene3:

    scene bg seitz_office with dissolve

    show seitz idle at npc_spot with dissolve

    "Prof. Seitz opens the office door."

    play sound "audio/fnaf.mp3"
    seitz "Hey, is that a student who slacked off on his work running downstairs?"

    "The hallway goes silent, before a frenzied series of footsteps are heard thundering towards the lower floors."

    play sound "audio/glock.ogg"

    show mc panicked at player_spot with dissolve

    seitz "(to you, quietly) The signal is bad on this floor. You need to get to the roof to upload this to Canvas."

    mc "The {i}roof{/i}?"

    seitz "Building maintenance left the hatch unlocked three weeks ago. They haven't fixed it. Go."

    inner "How does he know that."

    seitz "I have mysterious secrets."

    inner "What?"

    hide seitz with dissolve
    hide mc with dissolve

    jump scene4_roof_approach


# ════════════════════════════════════════════════════════════
#  SCENE 4 — THE ROOF
#  Objective: upload the report. Hide from the groupmate.
# ════════════════════════════════════════════════════════════

label scene4_elevator_route:

    scene bg elevator with dissolve

    "You take the elevator and wait in your brief moment of peace."

    inner "I'll just finish this real quick. This should be easy."
    inner "(This isn't easy.)"

    jump scene4_roof_approach


label scene4_roof_approach:

    play music "audio/action.ogg" fadein 0.8

    scene bg stairwell with dissolve

    show mc running at player_spot with dissolve

    "Up the final flight. The maintenance hatch."
    "It's unlocked, just like Seitz said."

    hide mc with dissolve

    scene bg roof with dissolve

    show mc idle at player_spot with dissolve

    "The roof."
    "Cold air. The city spread out below. The UW campus quiet in every direction."
    "Your phone has three bars. Hopefully it'll be enough.."

    show mc typing at player_spot with None

    "You open the laptop. Find the Canvas submission portal."

    inner "Come on. Come on."

    "Upload: 12%%..."
    "28%%..."
    "51%%..."

    "The hatch behind you BURSTS open."

    show mc panicked at player_spot with None

    show groupmate angry at npc_spot with dissolve

    groupmate "END OF THE LINE. THE DEAD LINE. BY WHICH I MEAN YOU'RE DEAD."

    hide mc with None

    jump scene4_hiding_sequence


label scene4_hiding_sequence:

    "The roof is mostly open. You rarely come up here, but it's nice."

    groupmate "(advancing) Don't make this harder than it needs to be."

    menu:
        "Sprint behind the maintenance shed.":
            jump scene4_hide_shed
        "Try to keep uploading and don't move.":
            jump scene4_stand_ground
        "Run to the far edge to buy signal time.":
            jump scene4_edge


label scene4_hide_shed:

    show mc hiding at player_spot with dissolve
    "You duck behind the maintenance shed. Signal drops to one bar."
    inner "No. No, I need signal."
    hide mc with None

    call screen qte_dodge("The groupmate rounds the shed—", 3.0)
    if _return == "success":
        show mc hiding at player_spot with None
        "They walk past. You breathe."
        hide mc with None
        jump scene4_upload_climax
    else:
        jump scene_jumpscare


label scene4_edge:

    show mc running at player_spot with dissolve
    "You move to the far edge. Signal jumps to three bars."
    inner "Yes! Come on—"
    hide mc with None

    call screen qte_dodge("They're right behind you—", 3.5)
    if _return == "success":
        "You sidestep. They slide past. Nearly go over the edge."
        show groupmate normal at npc_far with None
        groupmate "..."
        hide groupmate with None
        jump scene4_upload_climax
    else:
        jump scene_jumpscare


label scene4_stand_ground:

    show mc typing at player_spot with dissolve
    "You don't move. Just keep uploading. 74%%..."
    hide mc with None

    show groupmate normal at npc_spot with dissolve
    groupmate "..."
    "They stop. They're looking at the screen."
    groupmate "...Is that the report?"
    mc "(not looking up) 79%%."
    groupmate "..."
    hide groupmate with None

    jump scene4_upload_climax


label scene4_upload_climax:

    scene bg roof with dissolve

    show mc typing at player_spot with dissolve

    "83%%..."
    "91%%..."
    "99%%..."

    show groupmate normal at npc_spot with dissolve

    "The groupmate stands ten feet away. Watching."

    "100%%."
    "{b}SUBMISSION CONFIRMED — 5:59 AM{/b}"

    show mc celebrate at player_spot with None

    mc "IT'S IN."

    "A long silence."

    groupmate "..."

    hide mc with None
    hide groupmate with None

    jump scene4_ending_branch


label scene4_ending_branch:

    stop music fadeout 1.0

    if has_tendon_kohaku:
        jump ending_true
    elif report_quality >= 3:
        jump ending_good
    else:
        jump ending_neutral


# ════════════════════════════════════════════════════════════
#  ENDINGS
# ════════════════════════════════════════════════════════════

label ending_neutral:

    scene black with fade

    "The report goes in. Barely."
    "At the demo, Prof. Seitz glances at your group and says nothing."
    "Which is somehow worse than if he'd said something."
    "He does give a special commendation for Group H though- something about a horror game? Whatever it is, they pass with flying colors."

    show mc idle at player_spot with dissolve
    show groupmate normal at npc_spot with dissolve

    groupmate "We passed."
    mc "We passed."
    groupmate "Do that again and I will personally run you over with a lawnmower."
    mc "Never again."

    hide mc with dissolve
    hide groupmate with dissolve

    scene black with fade
    "[[ END — Night at CSE2 ]"
    "[[ Group H · CSE 457 ]"
    return


label ending_good:

    scene black with fade

    "The demo goes well."
    "Your methodology holds up. Seitz nods twice during your section."
    "Twice."
    "He does give a special commendation for Group H though- something about a horror game? Whatever it is, they pass with flying colors."

    show mc idle at player_spot with dissolve
    show groupmate normal at npc_spot with dissolve

    groupmate "...It was good."
    mc "It was good."
    groupmate "You're buying the RedBull for the rest of our years."
    mc "Deal."

    hide mc with dissolve
    hide groupmate with dissolve

    scene black with fade
    "[[ GOOD END — Night at CSE2 ]"
    "[[ Group H · CSE 457 ]"
    return


label ending_true:

    scene bg roof with dissolve

    "And then, from somewhere above:"

    "A beam of golden light splits the clouds."

    show paul idle at paul_spot with dissolve

    paul "..."

    paul "Is that a Tendon Kohaku Set."

    show mc idle at player_spot with dissolve
    show groupmate normal at npc_spot with dissolve

    mc "Yes?"

    paul "I haven't eaten since 1983."

    "Paul G. Allen himself. Billionaire, philanthropist, the man whose name is on this building. He reaches down and accepts the fragrant food."

    paul "Your report. Let me see it."

    "He reads it. Right there. On the roof. At 5:59 AM."

    paul "This is... actually quite solid."

    mc "Prof. Seitz helped."

    paul "Tell him I said hello."

    "A pause."

    play sound "audio/CELEBRATION.ogg"

    paul "The grade is an A."

    groupmate "What? How- wha-"

    paul "An A."

    "The light intensifies. The groupmate screams in awe, but cannot withstand Paul G. Allen's immense presence and vanishes."

    show mc celebrate at player_spot with None

    "Music plays from nowhere."
    "Everyone busts a move."

    hide paul   with dissolve
    hide mc     with dissolve
    hide groupmate with dissolve

    scene black with fade
    "[[ TRUE END — Night at CSE2 ]"
    "[[ Everyone danced. The report got an A. Paul G. Allen ascended. ]"
    "[[ Group H · CSE 457 ]"
    return


# ════════════════════════════════════════════════════════════
#  BAD ENDING — jumpscare / caught
# ════════════════════════════════════════════════════════════

label scene_jumpscare:

    stop music fadeout 0.8

    hide mc idle
    hide mc hiding
    hide mc panicked
    hide mc running

    "You stop."
    "Things are eerily quiet- maybe he missed you some-."

    pause 0.5

    play sound "audio/jumpscare.ogg"
    $ renpy.movie_cutscene("images/anims/fnaf.webm")

    scene black with jumpscare_flash
    pause 0.2

    groupmate "FOUND YOU."

    pause 0.4

    scene black with fade

    "You wake up."
    "You're in the CSE1 dungeon."

    inner "...Oh no."

    pause 0.4

    "[[ BAD END ]"
    ""
    "[[ TWO NIGHTS AT CSE2 — COMING NEVER ]"
    "[[ Group H · CSE 457 ]"

    return
