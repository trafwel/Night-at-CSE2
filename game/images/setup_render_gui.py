"""
Night at CSE2 — GUI Render Setup (all-in-one)
=============================================
Run inside Blender's Scripting tab. Sets up camera, lights, animations,
and render settings. Then use Render → Render Animation.

STEPS:
  1. File → Revert  (fresh blend with all colours)
  2. Scripting tab → open this file → ▶ Run Script
  3. Render → Render Animation        (idle, 60 frames)
  4. In Python Console type: setup_scream()
  5. Render → Render Animation        (scream, 30 frames)
"""

import bpy, math, os
import mathutils

GROUPMATE_COLLECTION = "Groupmate"
BASE_DIR = "/Users/lukeprasarttongosoth/CSE457/demo checkpoint/Night at CSE2/game/images"

RENDER_WIDTH    = 540
RENDER_HEIGHT   = 1080
FRAME_RATE      = 24

# ── Camera — pull back enough to see full body ────────────────────────────────
CAMERA_DISTANCE = 5.5   # Y distance from character
CAMERA_HEIGHT   = 0.0   # level with mid-body
CAMERA_FOV_DEG  = 45    # standard portrait FOV
# Aim at the vertical centre of the character's bounding box (computed below)

# ── Body part classification ──────────────────────────────────────────────────
UPPER_PREFIXES = ["Upper", "Arm", "Wrist", "Fist", "Neck", "Sphere"]
HEAD_PREFIXES  = ["Face", "Hair", "ear",  "eye"]
# Everything else = lower body


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_groupmate_objects():
    col = bpy.data.collections.get(GROUPMATE_COLLECTION)
    if col is None:
        print(f"ERROR: '{GROUPMATE_COLLECTION}' not found. Collections: {[c.name for c in bpy.data.collections]}")
        return []
    objs = [o for o in col.all_objects if o.type == "MESH"]
    print(f"Found {len(objs)} Groupmate mesh objects.")
    return objs


def classify(obj):
    n = obj.name
    for p in HEAD_PREFIXES:
        if n.startswith(p): return "head"
    for p in UPPER_PREFIXES:
        if n.startswith(p): return "upper"
    return "lower"


def hide_extra_characters():
    """Hide every non-Groupmate mesh from the render (keeps materials intact)."""
    groupmate_col = bpy.data.collections.get(GROUPMATE_COLLECTION)
    keep = {o.name for o in groupmate_col.all_objects} if groupmate_col else set()
    hidden = 0
    for obj in bpy.data.objects:
        if obj.name not in keep and obj.type not in ("CAMERA", "LIGHT"):
            obj.hide_render = obj.hide_viewport = True
            hidden += 1
    print(f"Hid {hidden} non-Groupmate objects.")


def enable_visibility(objects):
    for vl in bpy.context.scene.view_layers:
        def walk(lc):
            if lc.collection.name == GROUPMATE_COLLECTION:
                lc.exclude = lc.hide_viewport = lc.holdout = lc.indirect_only = False
            for c in lc.children: walk(c)
        walk(vl.layer_collection)
    for obj in objects:
        obj.hide_render = obj.hide_viewport = False
        obj.hide_set(False)


def force_opaque(objects):
    for obj in objects:
        for slot in obj.material_slots:
            mat = slot.material
            if not mat: continue
            for attr in ("blend_method", "surface_render_method"):
                try: setattr(mat, attr, "OPAQUE")
                except (AttributeError, TypeError): pass
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == "BSDF_PRINCIPLED":
                        if "Alpha" in node.inputs:
                            node.inputs["Alpha"].default_value = 1.0
                        break


def find_bounds(objects):
    locs = [o.location.copy() for o in objects]
    cx   = sum(v.x for v in locs) / len(locs)
    cy   = sum(v.y for v in locs) / len(locs)
    cz   = sum(v.z for v in locs) / len(locs)
    zmin = min(v.z for v in locs)
    zmax = max(v.z for v in locs)
    print(f"Centre: ({cx:.2f}, {cy:.2f}, {cz:.2f})  Z: {zmin:.2f}→{zmax:.2f}  span: {zmax-zmin:.2f}m")
    return cx, cy, cz, zmin, zmax


# ─────────────────────────────────────────────────────────────────────────────
#  Animation — baked directly so the blend file doesn't need pre-existing actions
# ─────────────────────────────────────────────────────────────────────────────

def key_delta(obj, frame, dx=0, dy=0, dz=0, rx=0, ry=0, rz=0):
    obj.delta_location        = (dx, dy, dz)
    obj.delta_rotation_euler  = (math.radians(rx), math.radians(ry), math.radians(rz))
    obj.keyframe_insert("delta_location",       frame=frame)
    obj.keyframe_insert("delta_rotation_euler", frame=frame)


def smooth_interpolation(obj):
    if not (obj.animation_data and obj.animation_data.action): return
    action = obj.animation_data.action
    if hasattr(action, "layers"):                       # Blender 5.x
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for kp in fc.keyframe_points: kp.interpolation = "BEZIER"
    else:                                               # Blender 4.x
        for fc in action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = "BEZIER"


def build_idle(objects):
    """
    Angry idle: upper body already hinged forward ~20°, then heaves with breath.
    Arms spread slightly outward. Looks like the reference 'angry businessman'.
    """
    print("Building IDLE animation …")
    for obj in objects:
        role = classify(obj)
        obj.animation_data_clear()

        if role == "upper":
            # Base = hunched forward 20°.  Inhale pulls back, exhale pushes further forward.
            key_delta(obj,  1, dz= 0.00, rx= 20.0, ry= 0.0)   # angry hunch
            key_delta(obj, 14, dz= 0.05, rx= 17.0)             # inhale — chest rises/opens
            key_delta(obj, 18, dz= 0.05, rx= 17.0)             # hold
            key_delta(obj, 32, dz=-0.01, rx= 23.0)             # exhale — slump deeper
            key_delta(obj, 60, dz= 0.00, rx= 20.0)             # loop back
        elif role == "head":
            # Head stays roughly level (angry glare forward) despite body bent
            key_delta(obj,  1, dz= 0.00, rx=-10.0)             # compensate for hunch
            key_delta(obj, 14, dz= 0.03, rx=-12.0)
            key_delta(obj, 18, dz= 0.03, rx=-12.0)
            key_delta(obj, 32, dz= 0.00, rx= -8.0)
            key_delta(obj, 60, dz= 0.00, rx=-10.0)
        else:   # lower body — very subtle shift
            key_delta(obj,  1)
            key_delta(obj, 14, dz= 0.01)
            key_delta(obj, 18, dz= 0.01)
            key_delta(obj, 32)
            key_delta(obj, 60)

        smooth_interpolation(obj)

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end   = 60
    print("IDLE built — 60 frames.")


def build_scream(objects):
    """
    WRYYY lunge: body drives forward hard, head whips back, arms fly out.
    """
    print("Building SCREAM animation …")
    for obj in objects:
        role = classify(obj)
        obj.animation_data_clear()

        if role == "upper":
            key_delta(obj,  1, rx= 20.0)                        # start from angry hunch
            key_delta(obj,  6, dy=-0.05, rx= 14.0)             # wind-up pull-back
            key_delta(obj, 14, dy= 0.15, rx= 35.0)             # LUNGE
            key_delta(obj, 22, dy= 0.15, rx= 35.0)             # hold
            key_delta(obj, 30, dy= 0.08, rx= 28.0)             # settle
        elif role == "head":
            key_delta(obj,  1, rx=-10.0)
            key_delta(obj,  6, dy=-0.04, rx=-14.0)
            key_delta(obj, 14, dy= 0.10, rx=-28.0)             # head whips back (mouth open scream)
            key_delta(obj, 22, dy= 0.10, rx=-28.0)
            key_delta(obj, 30, dy= 0.05, rx=-14.0)
        else:   # lower body — hips drive the lunge
            key_delta(obj,  1)
            key_delta(obj,  6, dy=-0.03)
            key_delta(obj, 14, dy= 0.10, rx= 10.0)
            key_delta(obj, 22, dy= 0.10, rx= 10.0)
            key_delta(obj, 30, dy= 0.05, rx=  5.0)

        smooth_interpolation(obj)

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end   = 30
    print("SCREAM built — 30 frames.")


def stash_actions(objects, suffix):
    """Rename current actions to {obj.name}_{suffix} so they can be reassigned later."""
    for obj in objects:
        if obj.animation_data and obj.animation_data.action:
            obj.animation_data.action.name = f"{obj.name}_{suffix}"


def assign_actions(objects, suffix):
    for obj in objects:
        action = bpy.data.actions.get(f"{obj.name}_{suffix}")
        if action:
            if not obj.animation_data:
                obj.animation_data_create()
            obj.animation_data.action = action


# ─────────────────────────────────────────────────────────────────────────────
#  Scene setup
# ─────────────────────────────────────────────────────────────────────────────

def setup_camera(cx, cy, cz, zmin, zmax):
    for obj in list(bpy.data.objects):
        if obj.name == "ExportCamera":
            bpy.data.objects.remove(obj, do_unlink=True)

    mid_z  = (zmin + zmax) / 2          # true vertical centre of character
    cam_loc = mathutils.Vector((cx, cy + CAMERA_DISTANCE, mid_z + CAMERA_HEIGHT))
    aim_loc = mathutils.Vector((cx, cy,                   mid_z))

    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.object
    cam.name = "ExportCamera"
    cam.rotation_euler = (aim_loc - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.type  = "PERSP"
    cam.data.angle = math.radians(CAMERA_FOV_DEG)
    bpy.context.scene.camera = cam
    print(f"Camera: {tuple(round(x,2) for x in cam_loc)}, aim mid_z={mid_z:.2f}")


def setup_lights(cx, cy, cz):
    for obj in list(bpy.data.objects):
        if obj.type == "LIGHT":
            bpy.data.objects.remove(obj, do_unlink=True)
    target = mathutils.Vector((cx, cy, cz))
    for name, (dx, dy, dz), energy in [
        ("Front",  (0,   5.0,  1.0), 6.0),
        ("FrontR", (2.5, 4.0,  0.5), 3.0),
        ("FrontL", (-2.5,4.0,  0.5), 3.0),
        ("Top",    (0,   1.0,  5.0), 2.5),
    ]:
        loc = mathutils.Vector((cx+dx, cy+dy, cz+dz))
        bpy.ops.object.light_add(type="SUN", location=loc)
        sun = bpy.context.object
        sun.name = name
        sun.data.energy = energy
        sun.rotation_euler = (target - loc).to_track_quat('-Z','Y').to_euler()
    print("Lights set.")


def setup_render_settings():
    s = bpy.context.scene
    r = s.render
    r.engine = "BLENDER_EEVEE"
    r.resolution_x = RENDER_WIDTH
    r.resolution_y = RENDER_HEIGHT
    r.resolution_percentage = 100
    r.film_transparent = True
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode  = "RGBA"
    s.render.fps = FRAME_RATE
    eevee = s.eevee
    for attr, val in [("taa_render_samples", 32), ("use_gtao", False),
                      ("use_bloom", False), ("use_ssr", False), ("use_raytracing", False)]:
        try: setattr(eevee, attr, val)
        except AttributeError: pass
    print("Render: EEVEE, 32 samples, transparent RGBA.")


# ─────────────────────────────────────────────────────────────────────────────
#  Public helpers — call from Python Console after script runs
# ─────────────────────────────────────────────────────────────────────────────

def setup_scream():
    objects = get_groupmate_objects()
    assign_actions(objects, "scream")
    out_dir = os.path.join(BASE_DIR, "anim_frames_scream")
    os.makedirs(out_dir, exist_ok=True)
    s = bpy.context.scene
    s.frame_start = 1
    s.frame_end   = 30
    s.render.filepath = os.path.join(out_dir, "frame####")
    print("\n✓ SCREAM ready → Render → Render Animation")


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("\n=== Night at CSE2 — GUI Render Setup ===")

    objects = get_groupmate_objects()
    if not objects:
        return

    hide_extra_characters()
    enable_visibility(objects)
    force_opaque(objects)

    cx, cy, cz, zmin, zmax = find_bounds(objects)

    # Build both animations and stash them as named actions
    build_idle(objects)
    stash_actions(objects, "idle")

    build_scream(objects)
    stash_actions(objects, "scream")

    # Configure scene for IDLE render first
    assign_actions(objects, "idle")

    setup_render_settings()
    setup_lights(cx, cy, cz)
    setup_camera(cx, cy, cz, zmin, zmax)

    out_dir = os.path.join(BASE_DIR, "anim_frames_idle")
    os.makedirs(out_dir, exist_ok=True)
    s = bpy.context.scene
    s.frame_start = 1
    s.frame_end   = 60
    s.render.filepath = os.path.join(out_dir, "frame####")

    print("""
==============================================
✓ IDLE ready  →  Render → Render Animation
  (60 frames → anim_frames_idle/)

When done, in the Python Console type:
  setup_scream()
Then:  Render → Render Animation
  (30 frames → anim_frames_scream/)
==============================================
""")


main()
