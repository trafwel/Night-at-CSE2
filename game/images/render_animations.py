"""
Night at CSE2 — Render Both Animations (Blender 5 / EEVEE)
===========================================================
Uses to_track_quat for reliable camera pointing and keeps
materials untouched so EEVEE renders them as opaque.

HOW TO RUN:
    /Applications/Blender.app/Contents/MacOS/Blender \
      "/path/to/all.blend" \
      --python render_animations.py \
      --background
"""

import bpy, math, os
import mathutils

GROUPMATE_COLLECTION = "Groupmate"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RENDER_WIDTH    = 540
RENDER_HEIGHT   = 1080
FRAME_RATE      = 24
CAMERA_DISTANCE = 3.0   # Y distance from character centre
CAMERA_HEIGHT   = 0.2   # camera slightly above model centre
CAMERA_FOV_DEG  = 38
CAMERA_AIM_Z    = 0.7   # aim above model centre (toward head)

ANIMATIONS = [
    {"suffix": "idle",   "start": 1, "end": 60},
    {"suffix": "scream", "start": 1, "end": 30},
]


def get_groupmate_objects():
    col = bpy.data.collections.get(GROUPMATE_COLLECTION)
    if col is None:
        print(f"[render] ERROR: '{GROUPMATE_COLLECTION}' collection not found.")
        print(f"[render] Available: {[c.name for c in bpy.data.collections]}")
        return []
    objs = [o for o in col.all_objects if o.type == "MESH"]
    print(f"[render] {len(objs)} Groupmate mesh objects.")
    return objs


def enable_render_visibility(objects):
    for vl in bpy.context.scene.view_layers:
        def walk(lc):
            if lc.collection.name == GROUPMATE_COLLECTION:
                lc.exclude = lc.hide_viewport = lc.holdout = lc.indirect_only = False
            for child in lc.children:
                walk(child)
        walk(vl.layer_collection)
    for obj in objects:
        obj.hide_render = obj.hide_viewport = False
        obj.hide_set(False)
    print(f"[render] {len(objects)} objects made renderable.")


def ensure_materials(objects):
    mat = bpy.data.materials.get("_fallback")
    if mat is None:
        mat = bpy.data.materials.new("_fallback")
        mat.diffuse_color = (0.6, 0.6, 0.6, 1.0)
    for obj in objects:
        if len(obj.material_slots) == 0:
            obj.data.materials.append(mat)


def set_all_materials_opaque(objects):
    """Force every material to opaque blend and copy viewport colour into BSDF."""
    fixed = 0
    for obj in objects:
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None:
                continue

            # Force blend mode to OPAQUE (Blender 4.x → blend_method, 5.x → surface_render_method)
            for attr in ("blend_method", "surface_render_method"):
                try:
                    setattr(mat, attr, "OPAQUE")
                except (AttributeError, TypeError):
                    pass

            # Leave Base Color alone — the original Principled BSDF already has
            # the real colours. Just ensure Alpha=1 so nothing is transparent.
            if not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    if "Alpha" in node.inputs:
                        node.inputs["Alpha"].default_value = 1.0
                    fixed += 1
                    break

    print(f"[render] {fixed} materials: OPAQUE blend + viewport colours → BSDF.")


def find_model_centre(objects):
    locs = [obj.location.copy() for obj in objects]
    cx = sum(v.x for v in locs) / len(locs)
    cy = sum(v.y for v in locs) / len(locs)
    cz = sum(v.z for v in locs) / len(locs)
    zmin = min(v.z for v in locs)
    zmax = max(v.z for v in locs)
    print(f"[render] Centre: ({cx:.2f}, {cy:.2f}, {cz:.2f})  span: {zmax-zmin:.2f}m")
    return cx, cy, cz, zmin, zmax


def setup_camera(cx, cy, cz):
    for obj in list(bpy.data.objects):
        if obj.name == "ExportCamera":
            bpy.data.objects.remove(obj, do_unlink=True)

    cam_loc = mathutils.Vector((cx, cy + CAMERA_DISTANCE, cz + CAMERA_HEIGHT))
    aim_loc = mathutils.Vector((cx, cy,                   cz + CAMERA_AIM_Z))

    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.object
    cam.name = "ExportCamera"

    # to_track_quat('-Z','Y') makes the camera's -Z axis point at the target
    direction = aim_loc - cam.location
    rot = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot.to_euler()

    cam.data.type  = "PERSP"
    cam.data.angle = math.radians(CAMERA_FOV_DEG)
    bpy.context.scene.camera = cam
    print(f"[render] Camera at {tuple(round(x,2) for x in cam_loc)}, "
          f"aimed at {tuple(round(x,2) for x in aim_loc)}")
    print(f"[render] Camera rotation: {tuple(round(math.degrees(x),1) for x in cam.rotation_euler)}")


def setup_render():
    scene  = bpy.context.scene
    render = scene.render
    render.engine                = "BLENDER_EEVEE"
    render.resolution_x          = RENDER_WIDTH
    render.resolution_y          = RENDER_HEIGHT
    render.resolution_percentage = 100
    render.film_transparent      = True
    render.image_settings.file_format = "PNG"
    render.image_settings.color_mode  = "RGBA"
    scene.render.fps = FRAME_RATE

    eevee = scene.eevee
    for attr, val in [("taa_render_samples", 16), ("use_gtao", False),
                      ("use_bloom", False), ("use_ssr", False),
                      ("use_raytracing", False)]:
        try:
            setattr(eevee, attr, val)
        except AttributeError:
            pass
    print(f"[render] Engine: {render.engine}, transparent film.")


def setup_lighting(cx, cy, cz):
    # Remove existing lights
    for obj in list(bpy.data.objects):
        if obj.type == "LIGHT":
            bpy.data.objects.remove(obj, do_unlink=True)

    # Three SUN lights explicitly aimed at the character from the +Y side.
    # SUN light direction = where its -Z axis points after rotation.
    # We want light to travel in -Y direction (shining from +Y toward character).
    # Camera -Z points in -Y when rotation_euler = (pi/2, 0, 0).
    lights = [
        # (name, energy, location_offset, extra_x_tilt_deg)
        ("Front",  8.0, (0.0,  3.0,  1.0), 0),    # directly in front
        ("Front_R",4.0, (2.0,  2.5,  0.5), 15),   # front-right
        ("Front_L",4.0, (-2.0, 2.5,  0.5), 15),   # front-left
        ("Top",    3.0, (0.0,  0.5,  4.0), -60),   # overhead (angled down)
    ]

    target = mathutils.Vector((cx, cy, cz))

    for name, energy, (dx, dy, dz), _ in lights:
        loc = mathutils.Vector((cx + dx, cy + dy, cz + dz))
        bpy.ops.object.light_add(type="SUN", location=loc)
        sun = bpy.context.object
        sun.name = name
        sun.data.energy = energy

        # Use to_track_quat to aim the SUN's -Z at the character
        direction = target - loc
        rot = direction.to_track_quat('-Z', 'Y')
        sun.rotation_euler = rot.to_euler()

    print(f"[render] {len(lights)} SUN lights aimed at character.")


def assign_actions(objects, suffix):
    missing = 0
    for obj in objects:
        action = bpy.data.actions.get(f"{obj.name}_{suffix}")
        if action is None:
            missing += 1
            continue
        if obj.animation_data is None:
            obj.animation_data_create()
        obj.animation_data.action = action
    if missing:
        print(f"[render]   {missing} objects had no '{suffix}' action (normal).")


def render_animation(suffix, frame_start, frame_end, objects):
    out_dir = os.path.join(BASE_DIR, f"anim_frames_{suffix}")
    os.makedirs(out_dir, exist_ok=True)
    assign_actions(objects, suffix)
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end   = frame_end
    print(f"\n[render] Rendering '{suffix}' ({frame_end - frame_start + 1} frames) …")

    for i, frame in enumerate(range(frame_start, frame_end + 1)):
        bpy.context.scene.frame_set(frame)
        out_path = os.path.join(out_dir, f"frame{i+1:04d}.png")
        bpy.context.scene.render.filepath = out_path
        bpy.ops.render.render(write_still=True)
        if i == 0 or (i + 1) % 10 == 0:
            print(f"[render]   {frame}/{frame_end} → frame{i+1:04d}.png")

    print(f"[render] '{suffix}' done.")


def main():
    print("\n[render] ── Starting render ──")
    objects = get_groupmate_objects()
    if not objects:
        return

    enable_render_visibility(objects)
    ensure_materials(objects)
    set_all_materials_opaque(objects)

    cx, cy, cz, zmin, zmax = find_model_centre(objects)

    setup_render()
    setup_lighting(cx, cy, cz)
    setup_camera(cx, cy, cz)

    for anim in ANIMATIONS:
        render_animation(anim["suffix"], anim["start"], anim["end"], objects)

    print("\n[render] ── Done. Encode with ffmpeg (VP8 for Ren'Py alpha): ──")
    print(f'\n  cd "{BASE_DIR}"')
    print('\n  ffmpeg -y -framerate 24 -i ./anim_frames_idle/frame%04d.png \\')
    print('         -c:v libvpx -pix_fmt yuva420p -b:v 1M -auto-alt-ref 0 -loop 0 ../groupmate_idle.webm')
    print('\n  ffmpeg -y -framerate 24 -i ./anim_frames_scream/frame%04d.png \\')
    print('         -c:v libvpx -pix_fmt yuva420p -b:v 1M -auto-alt-ref 0 -loop 0 ../groupmate_scream.webm')


main()
