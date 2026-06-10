## ============================================================
##  Night at CSE2 — Inventory System
## ============================================================

define ITEMS = {
    "upperclass_id": {
        "id":   "upperclass_id",
        "name": "Upperclass Husky Card",
        "icon": "images/items/upperclass_id.png",
        "desc": "A senior student's access card. It smells like something you can't identify. Or maybe you can.",
    },
    "tendon_kohaku": {
        "id":   "tendon_kohaku",
        "name": "Tendon Kohaku Set",
        "icon": "images/items/tendon_kohaku.png",
        "desc": "A perfectly prepared tempura donburi. How did you make this at 3 AM in a university building?",
    },
    "faculty_card": {
        "id":   "faculty_card",
        "name": "Faculty Husky Card",
        "icon": "images/items/faculty_card.png",
        "desc": "Prof. ___ner's card. The name is scratched half off, but the stripe looks intact.",
    },
    "chips": {
        "id":   "chips",
        "name": "BBQ Chips",
        "icon": "images/items/chips.png",
        "desc": "A bag of BBQ chips from the lobby vending machine. Still warm somehow.",
    },
}

default inventory         = []
default has_upperclass_id = False
default has_tendon_kohaku = False
default has_faculty_card  = False
default has_chips         = False

init python:
    def pickup_item(item_id):
        item = ITEMS[item_id]
        if item not in renpy.store.inventory:
            renpy.store.inventory.append(item)
            renpy.sound.play("audio/item.mp3", channel="sound")

# ── Always-visible HUD (top-left) ────────────────────────────
screen inventory_hud():
    layer "screens"
    zorder 10

    frame:
        xpos 12 ypos 12
        xpadding 10 ypadding 8
        background Frame("#000000bb", 6, 6)

        vbox:
            spacing 6
            text "ITEMS" size 11 color "#aaaaaa" xalign 0.0
            if inventory:
                hbox:
                    spacing 8
                    for item in inventory:
                        button:
                            xysize (48, 48)
                            background None
                            hover_background "#ffffff22"
                            action Show("item_detail", item=item)
                            hovered  Show("item_tooltip", name=item["name"])
                            unhovered Hide("item_tooltip")
                            add item["icon"] xalign 0.5 yalign 0.5 zoom 0.75
            else:
                text "—" size 13 color "#555555"

screen item_tooltip(name):
    frame:
        xpos 12 ypos 80
        background Frame("#000000cc", 4, 4)
        xpadding 8 ypadding 4
        text name size 13 color "#ffffff"

screen item_detail(item):
    modal True
    add "#000000aa"
    frame:
        xalign 0.5 yalign 0.5
        xpadding 30 ypadding 24
        background Frame("#111122ee", 10, 10)
        minimum (320, 180)
        vbox:
            spacing 12 xalign 0.5
            add item["icon"] xalign 0.5 zoom 2.0
            text item["name"] size 20 color "#ffffff" xalign 0.5
            text item["desc"] size 15 color "#cccccc" xalign 0.5 text_align 0.5
            textbutton "Close" xalign 0.5 action Hide("item_detail")
