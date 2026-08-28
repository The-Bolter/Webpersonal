import numpy as np
from PIL import Image
from scipy import ndimage

BASE = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\projects"
dark = np.array(Image.open(BASE + r"\projects-dark.png").convert("L")).astype(np.float32)
lit = np.array(Image.open(BASE + r"\projects-lit.png").convert("L")).astype(np.float32)

print(f"dark: {dark.shape[1]}x{dark.shape[0]}")
print(f"lit:  {lit.shape[1]}x{lit.shape[0]}")

# Use edges (gradient magnitude) for registration — edges are stable across lighting changes
dark_edge = np.abs(np.gradient(dark)[0]) + np.abs(np.gradient(dark)[1])
lit_edge = np.abs(np.gradient(lit)[0]) + np.abs(np.gradient(lit)[1])

# Downsample for speed
step = 4
d = dark_edge[::step, ::step]
l = lit_edge[::step, ::step]

# Try small integer offsets (in downsampled units, 1 step = 4px)
best = None
for dy in range(-8, 9):
    for dx in range(-8, 9):
        if dx == 0 and dy == 0:
            continue
        shifted = np.roll(np.roll(d, dy, axis=0), dx, axis=1)
        # correlation (sum of min, to focus on overlapping edges)
        score = np.sum(np.minimum(shifted, l))
        if best is None or score > best[0]:
            best = (score, dx * step, dy * step)

print(f"\nBest offset (px): dx={best[1]}, dy={best[2]}, score={best[0]:.0f}")
print("(positive dx = lit is to the right of dark; positive dy = lit is below dark)")

# Also check correlation without offset for comparison
score0 = np.sum(np.minimum(d, l))
print(f"Score at (0,0): {score0:.0f}")
