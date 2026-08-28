import numpy as np
from PIL import Image

BASE = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\projects"
dark = np.array(Image.open(BASE + r"\projects-dark.png").convert("L")).astype(np.float32)
lit = np.array(Image.open(BASE + r"\projects-lit.png").convert("L")).astype(np.float32)

# Lamp region: around design (190, 620), take a generous window
x0, x1 = 120, 300
y0, y1 = 540, 720
d = dark[y0:y1, x0:x1]
l = lit[y0:y1, x0:x1]

# Full resolution correlation over small offsets
best = None
for dy in range(-3, 4):
    for dx in range(-3, 4):
        # shift d by (dx, dy), compare overlap
        ds = d[max(0,-dy):d.shape[0]-max(0,dy), max(0,-dx):d.shape[1]-max(0,dx)]
        ls = l[max(0,dy):l.shape[0]-max(0,-dy), max(0,dx):l.shape[1]-max(0,-dx)]
        score = np.mean(np.abs(ds - ls))
        if best is None or score < best[0]:
            best = (score, dx, dy)

print(f"Lamp region best offset: dx={best[1]}, dy={best[2]}, mean_abs_diff={best[0]:.1f}")

# Also the pavilion region (right side)
x0, x1 = 1350, 1600
y0, y1 = 150, 500
d = dark[y0:y1, x0:x1]
l = lit[y0:y1, x0:x1]
best2 = None
for dy in range(-3, 4):
    for dx in range(-3, 4):
        ds = d[max(0,-dy):d.shape[0]-max(0,dy), max(0,-dx):d.shape[1]-max(0,dx)]
        ls = l[max(0,dy):l.shape[0]-max(0,-dy), max(0,dx):l.shape[1]-max(0,-dx)]
        score = np.mean(np.abs(ds - ls))
        if best2 is None or score < best2[0]:
            best2 = (score, dx, dy)

print(f"Pavilion region best offset: dx={best2[1]}, dy={best2[2]}, mean_abs_diff={best2[0]:.1f}")
