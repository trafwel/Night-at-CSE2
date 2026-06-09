"""
Night at CSE2 — Blender Animation Exporter
===========================================
Renders the groupmate's idle animation as a transparent PNG sequence,
ready to be converted to WebM with the FFmpeg command below.

HOW TO RUN (from the folder containing all.blend):
    blender all.blend --python export_anim.py --background

THEN, convert the PNG frames to a looping WebM with alpha:
    ffmpeg -framerate 24 -i ./anim_frames/frame%04d.png \
           -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 \
           -auto-alt-ref 0 -loop 0 \
           groupmate_idle.webm

Copy groupmate_idle.webm into your Ren'Py project's  game/  folder.
The script.rpy already expects it there.

TWEAKS:
  FRAME_START / FRAME_END   — frame range of your idle animation in Blender.
                               Check the timeline; default assumes frames 1–60
                               (a 2.5s loop at 24 fps).
  FRAME_RATE                — must match the -framerate value in the ffmpeg command.
  OUTPUT_DIR                — where the PNG frames are saved.
  RENDER_WIDTH / HEIGHT     — sprite canvas. 540x1080 fits a half-HD portrait slot.
  CAMERA_DISTANCE/HEIGHT    — same as export_sprite.py; tune if the model is clipped.
"""

import bpy
import math
import os

# ── CONFIGURATION ────────────────────────────────────────────

FRAME_START     = 1          # first frame of the idle animation
FRAME_END       = 60         # last frame  — change to match your action length
FRAME_RATE      = 24         # fps — keep in sync with the ffmpeg -framerate flag

RENDER_WIDTH    = 540
RENDER_HEIGHT   = 1080
CAMERA_DISTANCE = 4.0
CAMERA_HEIGHT   = 1.0
CAMERA_FOV_DEG  = 40

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anim_frames")


# ── HELPERS (same logic as export_sprite.py) ─────────────────

def find_model_center_and_height():
    all_verts = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            for v in obj.data.vertices:
                all_verts.append(obj.matrix_world @ v.co)
    if not all_verts:
        return 0.0, 0.0, 1.0, 2.0
    xs = [v.x for v in all_verts]
    ys = [v.y for v in all_verts]
    zs = [v.z for v in all_verts]
    return ((min(xs)+max(xs))/2, (min(ys)+max(ys))/2,
            (min(zs)+max(zs))/2, max(zs)-min(zs))


def setup_camera():
    cx, cy, cz, model_height = find_model_center_and_height()
    target_z = cz + CAMERA_HEIGHT - (model_height / 2)

    for obj in bpy.data.objects:
        if obj.name == "ExportCamera":
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.object.camera_add(
        location=(cx, cy - CAMERA_DISTANCE, cz + CAMERA_HEIGHT)
    )
    cam = bpy.context.object
    cam.name = "ExportCamera"

    dx = cx - cam.location.x
    dy = cy - cam.location.y
    dz = target_z - cam.location.z
    cam.rotation_euler = (
        math.pi / 2 + math.atan2(-dz, math.sqrt(dx**2 + dy**2)),
        0,
        math.atan2(dx, dy)
    )
    cam.data.type  = "PERSP"
    cam.data.angle = math.radians(CAMERA_FOV_DEG)
    bpy.context.scene.camera = cam


def setup_lighting():
    existing = [o for o in bpy.context.scene.objects if o.type == "LIGHT"]
    if existing:
        for l in existing:
            if l.data.energy < 5:
                l.data.energy = 5
        return

    cx, cy, cz, _ = find_model_center_and_height()
    for name, ltype, loc, energy, colour in [
        ("KeyLight",  "SUN", (cx-2, cy-3, cz+3), 4.0, (1.0, 0.98, 0.95)),
        ("FillLight", "SUN", (cx+2, cy-2, cz+2), 1.5, (0.9, 0.95, 1.0)),
        ("RimLight",  "SUN", (cx,   cy+4, cz+2), 2.0, (1.0, 1.0,  1.0)),
    ]:
        bpy.ops.object.light_add(type=ltype, location=loc)
        l = bpy.context.object
        l.name        = name
        l.data.energy = energy
        l.data.color  = colour


# ── MAIN ─────────────────────────────────────────────────────

def main():
    print("\n[export_anim] ── Starting animation export ──")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    scene  = bpy.context.scene
    render = scene.render

    render.engine               = "CYCLES"
    render.resolution_x         = RENDER_WIDTH
    render.resolution_y         = RENDER_HEIGHT
    render.resolution_percentage = 100
    render.film_transparent     = True
    render.image_settings.file_format = "PNG"
    render.image_settings.color_mode  = "RGBA"

    if render.engine == "CYCLES":
        # Lower samples for animation — tweak up if quality is too grainy
        scene.cycles.samples        = 64
        scene.cycles.use_denoising = True

    scene.render.fps      = FRAME_RATE
    scene.frame_start     = FRAME_START
    scene.frame_end       = FRAME_END

    setup_camera()
    setup_lighting()

    total = FRAME_END - FRAME_START + 1
    for i, frame in enumerate(range(FRAME_START, FRAME_END + 1)):
        scene.frame_set(frame)
        out = os.path.join(OUTPUT_DIR, f"frame{i+1:04d}.png")
        render.filepath = out
        print(f"[export_anim] Rendering frame {frame}/{FRAME_END}  →  {out}")
        bpy.ops.render.render(write_still=True)

    print(f"\n[export_anim] ── Done! {total} frames saved to {OUTPUT_DIR} ──")
    print("[export_anim]")
    print("[export_anim] Now run FFmpeg to create the WebM:")
    print(f"[export_anim]   ffmpeg -framerate {FRAME_RATE} -i \"{OUTPUT_DIR}/frame%04d.png\" \\")
    print(f"[export_anim]          -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 \\")
    print(f"[export_anim]          -auto-alt-ref 0 -loop 0 groupmate_idle.webm")
    print("[export_anim]")
    print("[export_anim] Then copy groupmate_idle.webm into your Ren'Py project's  game/  folder.")


main()
