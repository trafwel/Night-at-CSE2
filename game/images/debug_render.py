"""
debug_render.py — diagnose why objects aren't rendering, then render one test frame.
"""
import bpy, math, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE_DIR, "debug_frame.png")

# ── 1. Print full layer-collection tree ──────────────────────
def print_lc_tree(lc, indent=0):
    pad = "  " * indent
    print(f"[debug] {pad}LayerCol: '{lc.collection.name}'  "
          f"exclude={lc.exclude}  hide_vp={lc.hide_viewport}  "
          f"holdout={lc.holdout}  indirect={lc.indirect_only}")
    for child in lc.children:
        print_lc_tree(child, indent + 1)

print("\n[debug] ── View layer collection tree ──")
vl = bpy.context.scene.view_layers[0]
print_lc_tree(vl.layer_collection)

# ── 2. Print every object's render/viewport visibility ────────
print("\n[debug] ── Object visibility (Groupmate collection) ──")
col = bpy.data.collections.get("Groupmate")
if col:
    for obj in col.all_objects:
        if obj.type == "MESH":
            visible = obj.visible_get()
            print(f"[debug]   {obj.name:30s}  hide_render={obj.hide_render}  "
                  f"hide_vp={obj.hide_viewport}  visible_get={visible}  "
                  f"loc={tuple(round(v,2) for v in obj.location)}")

# ── 3. Brute-force: make EVERYTHING in the scene renderable ───
print("\n[debug] ── Forcing ALL objects visible ──")
for obj in bpy.data.objects:
    obj.hide_render   = False
    obj.hide_viewport = False

# Force every layer collection to be included
def force_all_visible(lc):
    lc.exclude       = False
    lc.hide_viewport = False
    lc.holdout       = False
    lc.indirect_only = False
    for child in lc.children:
        force_all_visible(child)

for vl in bpy.context.scene.view_layers:
    force_all_visible(vl.layer_collection)

# ── 4. Set up a simple render ─────────────────────────────────
scene  = bpy.context.scene
render = scene.render
render.engine                = "BLENDER_WORKBENCH"  # simplest possible renderer
render.resolution_x          = 540
render.resolution_y          = 1080
render.resolution_percentage = 100
render.film_transparent      = True
render.image_settings.file_format = "PNG"
render.image_settings.color_mode  = "RGBA"

# Workbench lighting
scene.display.shading.light          = "STUDIO"
scene.display.shading.color_type     = "MATERIAL"
scene.display.shading.show_shadows   = False

# ── 5. Print where objects actually are to aim camera ─────────
if col:
    locs = [obj.location for obj in col.all_objects if obj.type == "MESH"]
    if locs:
        cx = sum(v.x for v in locs) / len(locs)
        cy = sum(v.y for v in locs) / len(locs)
        cz = sum(v.z for v in locs) / len(locs)
        print(f"[debug] Average object location: ({cx:.2f}, {cy:.2f}, {cz:.2f})")

        # Place camera
        for obj in list(bpy.data.objects):
            if obj.name == "DebugCamera":
                bpy.data.objects.remove(obj, do_unlink=True)

        bpy.ops.object.camera_add(location=(cx, cy - 4.0, cz + 1.0))
        cam = bpy.context.object
        cam.name = "DebugCamera"
        dx, dy, dz = cx - cam.location.x, cy - cam.location.y, cz - cam.location.z
        cam.rotation_euler = (
            math.pi/2 + math.atan2(-dz, math.sqrt(dx**2 + dy**2)),
            0,
            math.atan2(dx, dy),
        )
        cam.data.angle = math.radians(50)
        scene.camera = cam
        print(f"[debug] Camera placed at {tuple(round(v,2) for v in cam.location)}")

scene.frame_set(1)
render.filepath = OUT
print(f"\n[debug] Rendering test frame → {OUT}")
bpy.ops.render.render(write_still=True)

# ── 6. Check output ───────────────────────────────────────────
from PIL import Image
img = Image.open(OUT).convert("RGBA")
px  = list(img.getdata())
non_transparent = [p for p in px if p[3] > 10]
print(f"[debug] Result: {len(non_transparent)} / {len(px)} non-transparent pixels")
if non_transparent:
    print("[debug] ✓ SUCCESS — character is visible!")
else:
    print("[debug] ✗ FAIL — still fully transparent.")
