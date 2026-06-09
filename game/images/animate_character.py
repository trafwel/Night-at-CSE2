"""
Night at CSE2 — Object-Level Character Animator (no rig required)
=================================================================
Animates the Groupmate character by keyframing individual mesh objects
directly — no armature needed.

Creates two actions saved as NLA strips on each object:
  • "groupmate_idle"   — heavy heaving breath, 60 frames @ 24 fps (loops)
  • "groupmate_scream" — WRYYY forward lunge, 30 frames @ 24 fps

HOW TO RUN:
    /Applications/Blender.app/Contents/MacOS/Blender \
      "/path/to/all.blend" \
      --python animate_character.py \
      --background

After running, render each frame range with export_anim.py:
    Idle:   FRAME_START=1  FRAME_END=60
    Scream: FRAME_START=1  FRAME_END=30
Then convert to WebM with ffmpeg as described in export_anim.py.
"""

import bpy

# ── WHICH COLLECTION TO ANIMATE ──────────────────────────────
GROUPMATE_COLLECTION = "Groupmate"

# ── BODY PART GROUPS ─────────────────────────────────────────
# Objects whose names START WITH any of these strings belong to that group.
# Upper body rises on inhale; head follows more subtly; lower body is still.
UPPER_BODY_PREFIXES = ["Upper", "Arm", "Wrist", "Fist", "Neck Shirt", "Sphere"]
HEAD_PREFIXES        = ["Face", "Hair", "ear", "eye"]
LOWER_BODY_PREFIXES  = ["BottomTorso", "Pants", "UpperPants", "Leg", "ShoeTop",
                         "ShoeBottom", "Lace"]


# ── HELPERS ──────────────────────────────────────────────────

def get_groupmate_objects():
    col = bpy.data.collections.get(GROUPMATE_COLLECTION)
    if col is None:
        print(f"[animate] ERROR: collection '{GROUPMATE_COLLECTION}' not found.")
        print(f"[animate] Available collections: {[c.name for c in bpy.data.collections]}")
        return []
    objs = [o for o in col.objects if o.type == "MESH"]
    print(f"[animate] Found {len(objs)} mesh objects in '{GROUPMATE_COLLECTION}'")
    return objs


def classify(obj):
    """Return 'upper', 'head', 'lower', or 'unknown'."""
    name = obj.name
    for p in HEAD_PREFIXES:
        if name.startswith(p):
            return "head"
    for p in UPPER_BODY_PREFIXES:
        if name.startswith(p):
            return "upper"
    for p in LOWER_BODY_PREFIXES:
        if name.startswith(p):
            return "lower"
    return "upper"   # default: treat unknowns as upper body


def key_delta(obj, frame, dx=0.0, dy=0.0, dz=0.0, rx=0.0, ry=0.0, rz=0.0):
    """Insert a delta_location + delta_rotation_euler keyframe."""
    import math
    obj.delta_location    = (dx, dy, dz)
    obj.delta_rotation_euler = (
        math.radians(rx),
        math.radians(ry),
        math.radians(rz),
    )
    obj.keyframe_insert(data_path="delta_location",       frame=frame)
    obj.keyframe_insert(data_path="delta_rotation_euler", frame=frame)


def set_interpolation(obj, interp="BEZIER"):
    """Set keyframe interpolation — handles both legacy and Blender 5.x action API."""
    if not (obj.animation_data and obj.animation_data.action):
        return
    action = obj.animation_data.action
    # Blender 5.x: fcurves live inside layers → strips → channelbags
    if hasattr(action, "layers"):
        for layer in action.layers:
            for strip in layer.strips:
                for channelbag in strip.channelbags:
                    for fc in channelbag.fcurves:
                        for kp in fc.keyframe_points:
                            kp.interpolation = interp
    else:
        # Legacy (Blender 4.x and earlier)
        for fc in action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = interp


# ── ACTION 1: IDLE HEAVE ─────────────────────────────────────

def build_idle(objects):
    print("[animate] Building idle breathing animation …")

    for obj in objects:
        role = classify(obj)

        # Clear existing animation on this object
        obj.animation_data_clear()

        # Frame 1 — rest
        key_delta(obj, 1)

        if role == "upper":
            # Inhale: rise 0.06 units, tiny backward lean
            key_delta(obj, 14,  dz= 0.06, rx=-2.0)
            key_delta(obj, 18,  dz= 0.06, rx=-2.0)   # hold
            # Exhale: slight forward slump (angry exhale)
            key_delta(obj, 32,  dz=-0.01, rx= 3.0)
            key_delta(obj, 60)                         # back to rest = loops

        elif role == "head":
            # Head follows upper body but less dramatically
            key_delta(obj, 14,  dz= 0.04, rx=-1.0)
            key_delta(obj, 18,  dz= 0.04, rx=-1.0)
            key_delta(obj, 32,  dz= 0.0,  rx= 1.5)
            key_delta(obj, 60)

        else:  # lower body — barely moves
            key_delta(obj, 14,  dz= 0.01)
            key_delta(obj, 18,  dz= 0.01)
            key_delta(obj, 32,  dz= 0.0)
            key_delta(obj, 60)

        set_interpolation(obj, "BEZIER")

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end   = 60
    print("[animate] Idle done — 60 frames.")


# ── ACTION 2: SCREAM (WRYYY) ─────────────────────────────────

def build_scream(objects):
    """
    30-frame scream sequence.
    The whole character lunges forward (positive Y toward camera),
    upper body bends aggressively forward, head flings back.
    """
    print("[animate] Building scream / WRYYY animation …")

    for obj in objects:
        role = classify(obj)
        obj.animation_data_clear()

        # Frame 1 — neutral
        key_delta(obj, 1)

        if role == "upper":
            # Wind-up: pull back (frame 6)
            key_delta(obj, 6,  dy=-0.04, rx=-6.0)
            # LUNGE peak: drive forward aggressively (frame 14)
            key_delta(obj, 14, dy= 0.12, rx= 18.0)
            # Hold scream (frame 22)
            key_delta(obj, 22, dy= 0.12, rx= 18.0)
            # Settle into angry lean (frame 30)
            key_delta(obj, 30, dy= 0.06, rx= 10.0)

        elif role == "head":
            # Head whips BACK as body lunges forward (open-mouth scream)
            key_delta(obj, 6,  dy=-0.04, rx=-4.0)
            key_delta(obj, 14, dy= 0.08, rx=-22.0)   # head flung back
            key_delta(obj, 22, dy= 0.08, rx=-22.0)
            key_delta(obj, 30, dy= 0.04, rx=-8.0)

        else:  # lower body — hips drive the lunge
            key_delta(obj, 6,  dy=-0.02)
            key_delta(obj, 14, dy= 0.08, rx= 8.0)
            key_delta(obj, 22, dy= 0.08, rx= 8.0)
            key_delta(obj, 30, dy= 0.04, rx= 4.0)

        set_interpolation(obj, "BEZIER")

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end   = 30
    print("[animate] Scream done — 30 frames.")


# ── MAIN ─────────────────────────────────────────────────────

def main():
    print("\n[animate] ── Starting object-level animator ──")

    objects = get_groupmate_objects()
    if not objects:
        return

    # Print what we found and how each part is classified
    print("[animate] Object classification:")
    for obj in sorted(objects, key=lambda o: o.name):
        print(f"[animate]   {classify(obj):6s}  {obj.name}")

    # Build idle first (sets frame range to 1–60 for render)
    build_idle(objects)

    # Save idle as a named action on each object, then build scream
    print("[animate] Stashing idle actions …")
    for obj in objects:
        if obj.animation_data and obj.animation_data.action:
            obj.animation_data.action.name = f"{obj.name}_idle"

    build_scream(objects)
    print("[animate] Stashing scream actions …")
    for obj in objects:
        if obj.animation_data and obj.animation_data.action:
            obj.animation_data.action.name = f"{obj.name}_scream"

    bpy.ops.wm.save_mainfile()
    print(f"\n[animate] Saved: {bpy.data.filepath}")
    print("\n[animate] Next steps:")
    print("[animate]  Idle render:   set FRAME_START=1 FRAME_END=60 in export_anim.py")
    print("[animate]  Scream render: set FRAME_START=1 FRAME_END=30 in export_anim.py")
    print("[animate]  But first — re-assign the action you want before rendering:")
    print("[animate]  e.g. assign all *_idle actions back to animate idle,")
    print("[animate]  or just run export_anim.py right after this script (idle is active).")


main()
