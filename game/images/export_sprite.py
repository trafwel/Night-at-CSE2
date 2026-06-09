"""
Night at CSE2 — Blender Sprite Exporter
========================================
Renders the groupmate model as a transparent-background PNG
sprite ready to drop into your Ren'Py  game/images/  folder.

HOW TO RUN (from your terminal, in the same folder as all.blend):
    blender all.blend --python export_sprite.py --background

Output:  groupmate_normal.png  and  groupmate_angry.png
         saved next to this script (or wherever OUTPUT_DIR points).

TWEAKS YOU MAY NEED:
  - OUTPUT_DIR        where the PNGs land
  - RENDER_WIDTH/H    sprite canvas size  (default = 540 × 1080, half-HD portrait)
  - CAMERA_DISTANCE   how far back the camera sits — increase if the model is clipped
  - CAMERA_HEIGHT     vertical offset — raise if the head is cut off
  - SUN_STRENGTH      main light brightness
  - POSE_FRAMES       dict of { output_name : frame_number }
                      — if your model has an action / NLA track, map frame numbers to
                        the expression you want.  If there's no animation, leave as-is
                        (both entries will render the same rest pose; just delete one).
"""

import bpy
import math
import os

# ── CONFIGURATION ────────────────────────────────────────────

OUTPUT_DIR      = os.path.dirname(os.path.abspath(__file__))  # same folder as this script
RENDER_WIDTH    = 540       # pixels wide  (Ren'Py sprites are usually portrait)
RENDER_HEIGHT   = 1080      # pixels tall
CAMERA_DISTANCE = 4.0       # metres from the model origin — increase if model is cut off
CAMERA_HEIGHT   = 1.0       # metres above origin — raise if model is too low
CAMERA_FOV_DEG  = 40        # degrees — lower = less perspective distortion (more "flat" look)

# Map output filename → timeline frame to render.
# If your model has no animation, both frames will be the same (that's fine).
POSE_FRAMES = {
    "groupmate_normal": 1,   # rest / neutral pose
    "groupmate_angry":  1,   # change to the frame number of the angry pose if animated
}

# ── SETUP ────────────────────────────────────────────────────

def setup_render_settings():
    """Configure the renderer for a transparent PNG."""
    scene = bpy.context.scene
    render = scene.render

    render.engine          = "CYCLES"          # or "BLENDER_EEVEE" — Cycles is higher quality
    render.resolution_x    = RENDER_WIDTH
    render.resolution_y    = RENDER_HEIGHT
    render.resolution_percentage = 100
    render.film_transparent = True             # transparent background!
    render.image_settings.file_format = "PNG"
    render.image_settings.color_mode  = "RGBA" # keep the alpha channel

    # Cycles sample count — lower = faster, higher = cleaner
    if render.engine == "CYCLES":
        scene.cycles.samples            = 128
        scene.cycles.use_denoising     = True


def find_model_center_and_height():
    """
    Walk every mesh object and return (center_x, center_y, center_z, total_height).
    Used to aim the camera sensibly even if the model isn't centred at the origin.
    """
    all_verts = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            world_matrix = obj.matrix_world
            for v in obj.data.vertices:
                all_verts.append(world_matrix @ v.co)

    if not all_verts:
        # No mesh found — fall back to scene origin
        return 0.0, 0.0, 1.0, 2.0

    xs = [v.x for v in all_verts]
    ys = [v.y for v in all_verts]
    zs = [v.z for v in all_verts]

    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    cz = (min(zs) + max(zs)) / 2
    height = max(zs) - min(zs)

    return cx, cy, cz, height


def setup_camera():
    """
    Place (or reuse) a camera directly in front of the model, aimed at its centre.
    'Front' in Blender convention = negative-Y direction.
    """
    cx, cy, cz, model_height = find_model_center_and_height()

    print(f"[export_sprite] Model centre: ({cx:.2f}, {cy:.2f}, {cz:.2f}), height: {model_height:.2f}m")

    # Aim at the vertical midpoint, adjusted by CAMERA_HEIGHT offset
    target_z = cz + CAMERA_HEIGHT - (model_height / 2)

    # Remove any existing export camera so we start clean
    for obj in bpy.data.objects:
        if obj.name == "ExportCamera":
            bpy.data.objects.remove(obj, do_unlink=True)

    # Add camera
    bpy.ops.object.camera_add(
        location=(cx, cy - CAMERA_DISTANCE, cz + CAMERA_HEIGHT)
    )
    cam_obj = bpy.context.object
    cam_obj.name = "ExportCamera"

    # Point at the model centre
    direction_x = cx - cam_obj.location.x
    direction_y = cy - cam_obj.location.y   # will be ~positive (facing +Y)
    direction_z = target_z - cam_obj.location.z

    # Rotation: tilt down slightly to centre the model
    rot_x = math.atan2(-direction_z,
                        math.sqrt(direction_x**2 + direction_y**2))
    rot_z = math.atan2(direction_x, direction_y)

    cam_obj.rotation_euler = (math.pi / 2 + rot_x, 0, rot_z)

    # Field of view
    cam_obj.data.type = "PERSP"
    cam_obj.data.angle = math.radians(CAMERA_FOV_DEG)

    bpy.context.scene.camera = cam_obj
    return cam_obj


def setup_lighting():
    """
    Add a simple three-point light rig if the scene has no lights,
    or just boost existing lights.
    Three-point: key (front-left), fill (front-right, dimmer), rim (back).
    """
    existing_lights = [o for o in bpy.context.scene.objects if o.type == "LIGHT"]

    if existing_lights:
        # Scene already has lights — just make sure they're bright enough
        for light_obj in existing_lights:
            if light_obj.data.energy < 5:
                light_obj.data.energy = 5
        print(f"[export_sprite] Using {len(existing_lights)} existing light(s).")
        return

    print("[export_sprite] No lights found — adding three-point rig.")

    cx, cy, cz, _ = find_model_center_and_height()

    lights = [
        # (name,       type,    location,                   energy, colour)
        ("KeyLight",   "SUN",   (cx - 2, cy - 3, cz + 3),  4.0,   (1.0, 0.98, 0.95)),
        ("FillLight",  "SUN",   (cx + 2, cy - 2, cz + 2),  1.5,   (0.9, 0.95, 1.0)),
        ("RimLight",   "SUN",   (cx,     cy + 4, cz + 2),  2.0,   (1.0, 1.0,  1.0)),
    ]

    for name, ltype, loc, energy, colour in lights:
        bpy.ops.object.light_add(type=ltype, location=loc)
        light_obj = bpy.context.object
        light_obj.name = name
        light_obj.data.energy = energy
        light_obj.data.color  = colour


# ── MAIN ─────────────────────────────────────────────────────

def main():
    print("\n[export_sprite] ── Starting sprite export ──")

    setup_render_settings()
    setup_camera()
    setup_lighting()

    scene = bpy.context.scene

    for output_name, frame in POSE_FRAMES.items():
        scene.frame_set(frame)

        output_path = os.path.join(OUTPUT_DIR, output_name + ".png")
        scene.render.filepath = output_path

        print(f"[export_sprite] Rendering frame {frame} → {output_path}")
        bpy.ops.render.render(write_still=True)
        print(f"[export_sprite] Saved: {output_path}")

    print("[export_sprite] ── Done! ──")
    print(f"[export_sprite] Drop the PNG files into your Ren'Py project's  game/images/  folder.")
    print(f"[export_sprite] Then update script.rpy — replace the Solid(...) lines, e.g.:")
    print(f'[export_sprite]   image groupmate normal = "groupmate_normal.png"')
    print(f'[export_sprite]   image groupmate angry  = "groupmate_angry.png"')


main()
