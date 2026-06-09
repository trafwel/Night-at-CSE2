"""
inspect_blend.py — Print everything in the .blend scene
Run:
    /Applications/Blender.app/Contents/MacOS/Blender \
      "/path/to/all.blend" \
      --python inspect_blend.py \
      --background
"""
import bpy

print("\n[inspect] ── All objects in scene ──────────────────────")
for obj in bpy.context.scene.objects:
    print(f"[inspect]   type={obj.type:12s}  name={obj.name}")

print("\n[inspect] ── All collections ───────────────────────────")
for col in bpy.data.collections:
    print(f"[inspect]   {col.name}")

print("\n[inspect] ── All meshes ─────────────────────────────────")
for mesh in bpy.data.meshes:
    print(f"[inspect]   {mesh.name}  (verts={len(mesh.vertices)})")

print("\n[inspect] ── All armatures ──────────────────────────────")
for arm in bpy.data.armatures:
    print(f"[inspect]   {arm.name}  (bones={len(arm.bones)})")
    for bone in arm.bones:
        print(f"[inspect]     bone: {bone.name}")

print("\n[inspect] ── All objects across ALL scenes ──────────────")
for scene in bpy.data.scenes:
    for obj in scene.objects:
        print(f"[inspect]   scene={scene.name}  type={obj.type:12s}  name={obj.name}")

print("[inspect] ── Done ───────────────────────────────────────\n")
