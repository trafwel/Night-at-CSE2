"""
Process all sprite images:
1. Remove backgrounds from Chud and Seitz placeholders (gray bg)
2. Re-run animation frame background removal with improved settings:
   - Lower threshold (8 instead of 15) to prevent leaking into dark clothing
   - 1px alpha erosion to clean up jagged edges
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from collections import deque
import subprocess

GAME_DIR = os.path.dirname(os.path.abspath(__file__))
ANIMS_DIR = os.path.join(GAME_DIR, "images", "anims")


def flood_fill_mask(rgb_array, threshold=8):
    """Flood-fill from edges. Returns mask where True = background."""
    h, w, _ = rgb_array.shape
    brightness = rgb_array.astype(np.uint16).sum(axis=2)
    is_dark = brightness <= threshold

    bg_mask = np.zeros((h, w), dtype=bool)
    queue = deque()

    for x in range(w):
        if is_dark[0, x]:
            queue.append((0, x)); bg_mask[0, x] = True
        if is_dark[h-1, x]:
            queue.append((h-1, x)); bg_mask[h-1, x] = True
    for y in range(1, h-1):
        if is_dark[y, 0]:
            queue.append((y, 0)); bg_mask[y, 0] = True
        if is_dark[y, w-1]:
            queue.append((y, w-1)); bg_mask[y, w-1] = True

    while queue:
        cy, cx = queue.popleft()
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < h and 0 <= nx < w and not bg_mask[ny, nx] and is_dark[ny, nx]:
                bg_mask[ny, nx] = True
                queue.append((ny, nx))

    return bg_mask


def flood_fill_gray_mask(rgb_array, threshold=40):
    """Flood-fill from edges for GRAY backgrounds (Chud/Seitz images)."""
    h, w, _ = rgb_array.shape
    r, g, b = rgb_array[:,:,0].astype(float), rgb_array[:,:,1].astype(float), rgb_array[:,:,2].astype(float)
    
    # Gray pixels: low saturation (R≈G≈B) and within gray range
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    spread = max_c - min_c  # color spread — gray has low spread
    
    # Consider a pixel "background-like" if it's grayish (spread < threshold)
    # and within the gray background range (roughly 60-110 for these images)
    avg = (r + g + b) / 3.0
    is_bg_like = (spread < threshold) & (avg > 40) & (avg < 130)
    
    bg_mask = np.zeros((h, w), dtype=bool)
    queue = deque()

    for x in range(w):
        if is_bg_like[0, x]:
            queue.append((0, x)); bg_mask[0, x] = True
        if is_bg_like[h-1, x]:
            queue.append((h-1, x)); bg_mask[h-1, x] = True
    for y in range(1, h-1):
        if is_bg_like[y, 0]:
            queue.append((y, 0)); bg_mask[y, 0] = True
        if is_bg_like[y, w-1]:
            queue.append((y, w-1)); bg_mask[y, w-1] = True

    while queue:
        cy, cx = queue.popleft()
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < h and 0 <= nx < w and not bg_mask[ny, nx] and is_bg_like[ny, nx]:
                bg_mask[ny, nx] = True
                queue.append((ny, nx))

    return bg_mask


def apply_alpha_erosion(img, radius=1):
    """Erode the alpha channel by radius pixels to clean up edge artifacts."""
    arr = np.array(img)
    alpha = Image.fromarray(arr[:,:,3])
    # MinFilter shrinks white (opaque) regions — erodes the alpha
    eroded = alpha.filter(ImageFilter.MinFilter(size=radius*2+1))
    arr[:,:,3] = np.array(eroded)
    return Image.fromarray(arr)


def auto_crop(img, padding=5):
    """Crop to bounding box of non-transparent pixels."""
    arr = np.array(img)
    alpha = arr[:,:,3]
    rows = np.any(alpha > 0, axis=1)
    cols = np.any(alpha > 0, axis=0)
    if not rows.any():
        return img
    y1, y2 = np.where(rows)[0][[0, -1]]
    x1, x2 = np.where(cols)[0][[0, -1]]
    h, w = arr.shape[:2]
    y1 = max(0, y1 - padding)
    x1 = max(0, x1 - padding)
    y2 = min(h - 1, y2 + padding)
    x2 = min(w - 1, x2 + padding)
    return img.crop((x1, y1, x2 + 1, y2 + 1))


def process_static_image(input_path, output_path, bg_type="gray"):
    """Process a single static image (Chud/Seitz placeholders)."""
    img = Image.open(input_path).convert("RGB")
    rgb = np.array(img)
    
    if bg_type == "gray":
        mask = flood_fill_gray_mask(rgb)
    else:
        mask = flood_fill_mask(rgb)
    
    rgba = np.zeros((rgb.shape[0], rgb.shape[1], 4), dtype=np.uint8)
    rgba[:,:,:3] = rgb
    rgba[:,:,3] = np.where(mask, 0, 255)
    
    result = Image.fromarray(rgba, "RGBA")
    result = apply_alpha_erosion(result, radius=1)
    result = auto_crop(result)
    result.save(output_path)
    print(f"  Saved {output_path} ({result.size[0]}x{result.size[1]})")


def process_animation_dir(webm_name, output_dirname):
    """Extract, remove bg, erode, then find common bbox and crop all frames."""
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
    print(f"  Extracted {len(frames)} frames")

    # Pass 1: Remove bg + erode, save to output, track bbox
    min_x, min_y = 99999, 99999
    max_x, max_y = 0, 0

    for i, fname in enumerate(frames):
        img = Image.open(os.path.join(temp_dir, fname)).convert("RGB")
        rgb = np.array(img)
        mask = flood_fill_mask(rgb, threshold=8)

        rgba = np.zeros((rgb.shape[0], rgb.shape[1], 4), dtype=np.uint8)
        rgba[:,:,:3] = rgb
        rgba[:,:,3] = np.where(mask, 0, 255)

        result = Image.fromarray(rgba, "RGBA")
        result = apply_alpha_erosion(result, radius=1)
        result.save(os.path.join(output_dir, fname))

        # Track bbox
        arr = np.array(result)
        alpha = arr[:,:,3]
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)
        if rows.any():
            y1, y2 = np.where(rows)[0][[0, -1]]
            x1, x2 = np.where(cols)[0][[0, -1]]
            min_x = min(min_x, x1)
            min_y = min(min_y, y1)
            max_x = max(max_x, x2)
            max_y = max(max_y, y2)

        if (i + 1) % 30 == 0 or i == 0 or i == len(frames) - 1:
            print(f"    [{i+1}/{len(frames)}]")

    # Pass 2: Crop all frames to common bbox
    pad = 5
    h, w = 1080, 1920  # original frame size
    min_x = max(0, min_x - pad)
    min_y = max(0, min_y - pad)
    max_x = min(w - 1, max_x + pad)
    max_y = min(h - 1, max_y + pad)

    for fname in frames:
        fpath = os.path.join(output_dir, fname)
        img = Image.open(fpath)
        cropped = img.crop((min_x, min_y, max_x + 1, max_y + 1))
        cropped.save(fpath)

    crop_w = max_x - min_x + 1
    crop_h = max_y - min_y + 1
    print(f"  Cropped to {crop_w}x{crop_h}")

    # Cleanup temp
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    return len(frames)


def main():
    print("=== Processing Static Sprites ===\n")

    # Chud
    chud_src = os.path.join(GAME_DIR, "more images", "chudplaceholder.png")
    chud_dst = os.path.join(GAME_DIR, "images", "chud_placeholder.png")
    print(f"Chud: {chud_src}")
    process_static_image(chud_src, chud_dst, bg_type="gray")

    # Seitz
    seitz_src = os.path.join(GAME_DIR, "more images", "setizplaceholder.png")
    seitz_dst = os.path.join(GAME_DIR, "images", "seitz_placeholder.png")
    print(f"Seitz: {seitz_src}")
    process_static_image(seitz_src, seitz_dst, bg_type="gray")

    print("\n=== Processing Animation Frames ===\n")

    animations = [
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

    for webm_name, output_dir in animations:
        print(f"Processing {webm_name} → {output_dir}/")
        count = process_animation_dir(webm_name, output_dir)
        if count:
            print(f"  ✓ {count} frames done\n")

    # Also process mc_thinking source frames (already RGBA, just need crop)
    print("Processing mc_thinking (crop only — already has alpha)")
    thinking_dir = os.path.join(GAME_DIR, "images", "mc_thinking")
    frames = sorted(f for f in os.listdir(thinking_dir) if f.endswith(".png"))
    min_x, min_y = 99999, 99999
    max_x, max_y = 0, 0
    for fname in frames:
        img = Image.open(os.path.join(thinking_dir, fname)).convert("RGBA")
        arr = np.array(img)
        alpha = arr[:,:,3]
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)
        if rows.any():
            y1, y2 = np.where(rows)[0][[0, -1]]
            x1, x2 = np.where(cols)[0][[0, -1]]
            min_x = min(min_x, x1); min_y = min(min_y, y1)
            max_x = max(max_x, x2); max_y = max(max_y, y2)
    pad = 5
    h, w = img.size[1], img.size[0]
    min_x = max(0, min_x - pad); min_y = max(0, min_y - pad)
    max_x = min(w - 1, max_x + pad); max_y = min(h - 1, max_y + pad)
    for fname in frames:
        fpath = os.path.join(thinking_dir, fname)
        img = Image.open(fpath).convert("RGBA")
        cropped = img.crop((min_x, min_y, max_x + 1, max_y + 1))
        cropped.save(fpath)
    print(f"  ✓ {len(frames)} frames cropped to {max_x-min_x+1}x{max_y-min_y+1}\n")

    print("=== All done! ===")


if __name__ == "__main__":
    main()
