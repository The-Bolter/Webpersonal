import numpy as np
from PIL import Image

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\journey.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

print(f"Image: {W}x{H}")

# Sample a grid of points, print luminance
print("\nLuminance grid (rows 10%-90%, cols 15%-85%):")
for ry in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    row = int(ry * H)
    vals = []
    for rx in [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]:
        col = int(rx * W)
        v = int(lum[row, col])
        vals.append(v)
    print(f"  y={ry:.0%}: " + " ".join(f"{v:3d}" for v in vals))

# Find bright (water/reflection) and dark (mountain) regions
bright = lum > 200
dark = lum < 80
print(f"\nbright pixels (>200): {bright.sum()}, dark (<80): {dark.sum()}")

# Distribution of bright pixels by column (to find stream location)
col_bright = bright.sum(axis=0)
for rx in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    col = int(rx * W)
    print(f"  col {rx:.0%}: bright count = {col_bright[col]}")
