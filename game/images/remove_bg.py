"""
remove_bg.py — Strip white background from character art
=========================================================
Run this once to convert your flat illustration into a transparent PNG
that Ren'Py can use as a proper character sprite.

USAGE:
    pip install Pillow
    python remove_bg.py

INPUT:   groupmate_source.png   (your original illustration — rename as needed)
OUTPUT:  groupmate_normal.png   (transparent-background PNG for Ren'Py)
         groupmate_angry.png    (same image, copy — replace with the angry pose
                                 art when Kaung draws it)

HOW IT WORKS:
    Replaces every pixel that is "close enough to white" with full transparency.
    The THRESHOLD controls how aggressive it is — raise it if white fringing
    remains, lower it if you're losing edge detail.
"""

from PIL import Image
import os

# ── CONFIG ───────────────────────────────────────────────────
INPUT_FILE  = "groupmate_source.png"   # rename your source file to this
THRESHOLD   = 240                       # 0–255; pixels brighter than this become transparent
OUTPUT_DIR  = os.path.dirname(os.path.abspath(__file__))


def remove_white_background(input_path, output_path, threshold=240):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for r, g, b, a in data:
        # If all channels are above threshold the pixel is "near white" — make transparent
        if r >= threshold and g >= threshold and b >= threshold:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"  Saved: {output_path}")


def main():
    input_path = os.path.join(OUTPUT_DIR, INPUT_FILE)

    if not os.path.exists(input_path):
        print(f"[remove_bg] ERROR: could not find '{INPUT_FILE}'")
        print(f"[remove_bg] Rename your illustration to '{INPUT_FILE}' and place it next to this script.")
        return

    print(f"[remove_bg] Processing '{INPUT_FILE}' with threshold={THRESHOLD} ...")

    normal_out = os.path.join(OUTPUT_DIR, "groupmate_normal.png")
    angry_out  = os.path.join(OUTPUT_DIR, "groupmate_angry.png")

    remove_white_background(input_path, normal_out, THRESHOLD)

    # Angry pose: use same image for now, replace later with real angry art
    import shutil
    shutil.copy(normal_out, angry_out)
    print(f"  Copied to: {angry_out}  (replace with angry pose art when ready)")

    print("[remove_bg] Done! Copy the PNGs into your Ren'Py game/ folder.")


main()
