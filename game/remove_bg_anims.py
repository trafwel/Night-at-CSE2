"""
Remove black backgrounds from WebM animation frames using numpy flood-fill.
Much faster than pure-Python pixel iteration.
"""

import os
import subprocess
import numpy as np
from PIL import Image
from collections import deque

THRESHOLD = 15  # R+G+B <= this = "black"
GAME_DIR = os.path.dirname(os.path.abspath(__file__))
ANIMS_DIR = os.path.join(GAME_DIR, "images", "anims")

ANIMATIONS = [
    ("MC_Shocked.webm",    "mc_shocked_frames"),
    ("MC_Scared.webm",     "mc_scared_frames"),
    ("MC_Happy.webm",      "mc_happy_frames"),
    ("jump.webm",          "mc_running_frames"),
    ("angry.webm",         "gm_angry_frames"),
    ("walking.webm",       "gm_walking_frames"),
    ("gunshooting.webm",   "gm_shooting_frames"),
    ("fnaf.webm",          "gm_jumpscare_frames"),
    ("punching.webm",      "gm_punch_frames"),
]


def flood_fill_mask(rgb_array, threshold=THRESHOLD):
    """
    Create a mask of background pixels using flood-fill from edges.
    Uses numpy for the brightness check + BFS only on border-connected dark pixels.
    Returns boolean mask where True = background (to be made transparent).
    """
    h, w, _ = rgb_array.shape
    brightness = rgb_array.astype(np.uint16).sum(axis=2)  # R+G+B
    is_dark = brightness <= threshold  # potential background pixels

    # BFS flood fill from all dark border pixels
    bg_mask = np.zeros((h, w), dtype=bool)
    queue = deque()

    # Seed from borders
    for x in range(w):
        if is_dark[0, x]:
            queue.append((0, x))
            bg_mask[0, x] = True
        if is_dark[h-1, x]:
            queue.append((h-1, x))
            bg_mask[h-1, x] = True
    for y in range(1, h-1):
        if is_dark[y, 0]:
            queue.append((y, 0))
            bg_mask[y, 0] = True
        if is_dark[y, w-1]:
            queue.append((y, w-1))
            bg_mask[y, w-1] = True

    while queue:
        cy, cx = queue.popleft()
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < h and 0 <= nx < w and not bg_mask[ny, nx] and is_dark[ny, nx]:
                bg_mask[ny, nx] = True
                queue.append((ny, nx))

    return bg_mask


def process_frame(frame_path, output_path):
    """Load frame, remove background, save as RGBA PNG."""
    img = Image.open(frame_path).convert("RGB")
    rgb = np.array(img)

    mask = flood_fill_mask(rgb)

    # Build RGBA: alpha=0 where background, 255 elsewhere
    rgba = np.zeros((rgb.shape[0], rgb.shape[1], 4), dtype=np.uint8)
    rgba[:,:,:3] = rgb
    rgba[:,:,3] = np.where(mask, 0, 255)

    Image.fromarray(rgba, "RGBA").save(output_path)


def process_animation(webm_name, output_dirname):
    webm_path = os.path.join(ANIMS_DIR, webm_name)
    output_dir = os.path.join(GAME_DIR, "images", output_dirname)
    temp_dir = os.path.join(GAME_DIR, "images", "_temp_extract")

    if not os.path.exists(webm_path):
        print(f"  SKIP — {webm_path} not found")
        return 0

    # Clean
    for d in [temp_dir, output_dir]:
        if os.path.exists(d):
            for f in os.listdir(d):
                os.remove(os.path.join(d, f))
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Extract frames
    subprocess.run([
        "ffmpeg", "-y", "-i", webm_path,
        os.path.join(temp_dir, "frame%04d.png"),
    ], capture_output=True)

    frames = sorted(f for f in os.listdir(temp_dir) if f.endswith(".png"))
    print(f"  Extracted {len(frames)} frames, processing...")

    for i, fname in enumerate(frames):
        process_frame(
            os.path.join(temp_dir, fname),
            os.path.join(output_dir, fname),
        )
        if (i + 1) % 20 == 0 or i == 0 or i == len(frames) - 1:
            print(f"    [{i+1}/{len(frames)}]")

    # Cleanup temp
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    return len(frames)


def main():
    print("=== Background Removal (numpy flood-fill) ===\n")
    for webm_name, output_dir in ANIMATIONS:
        print(f"Processing {webm_name} → {output_dir}/")
        count = process_animation(webm_name, output_dir)
        if count:
            print(f"  ✓ {count} frames done\n")
    print("=== All done! ===")


if __name__ == "__main__":
    main()
