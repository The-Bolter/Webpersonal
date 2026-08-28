import numpy as np
from PIL import Image

BASE = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\projects"
dark = np.array(Image.open(BASE + r"\projects-dark.png").convert("RGB")).astype(np.int16)
lit = np.array(Image.open(BASE + r"\projects-lit.png").convert("RGB")).astype(np.int16)
fog = np.array(Image.open(BASE + r"\projects-fog.png").convert("RGBA")).astype(np.int16)

H, W = dark.shape[:2]
print(f"Images: {W}x{H}")

# Diff between lit and dark: where the lighting changes most = lamp + environment
diff = np.abs(lit - dark).sum(axis=2)
print(f"\nDark-vs-lit diff: max={diff.max()}, mean={diff.mean():.1f}")

# Find the brightest diff region (the lamp glow location)
bright_diff = diff > 120
ys, xs = np.where(bright_diff)
if len(xs) > 0:
    # Weighted centroid of diff
    weights = diff[bright_diff].astype(float)
    cx = (xs * weights).sum() / weights.sum()
    cy = (ys * weights).sum() / weights.sum()
    print(f"Lamp glow centroid (max diff): ({cx/W*100:.1f}%, {cy/H*100:.1f}%)")
    print(f"  diff x range: {xs.min()/W*100:.0f}%-{xs.max()/W*100:.0f}%")
    print(f"  diff y range: {ys.min()/H*100:.0f}%-{ys.max()/H*100:.0f}%")

# Fog alpha: where the fog is opaque
fog_alpha = fog[:, :, 3]
fog_ys, fog_xs = np.where(fog_alpha > 100)
if len(fog_xs) > 0:
    print(f"\nFog region (alpha>100): x {fog_xs.min()/W*100:.0f}%-{fog_xs.max()/W*100:.0f}%, y {fog_ys.min()/H*100:.0f}%-{fog_ys.max()/H*100:.0f}%")
    # centroid
    print(f"  fog centroid: ({fog_xs.mean()/W*100:.1f}%, {fog_ys.mean()/H*100:.1f}%)")

# Sample diff grid (find local max diff = lamp)
print("\nDiff grid (rows 55%-85%, cols 8%-25%):")
for ry in [0.55, 0.62, 0.68, 0.72, 0.78, 0.85]:
    row = int(ry * H)
    vals = []
    for rx in [0.08, 0.12, 0.16, 0.20, 0.24]:
        col = int(rx * W)
        vals.append(f"{int(diff[row,col]):3d}")
    print(f"  y={ry:.0%}: " + " ".join(vals))
