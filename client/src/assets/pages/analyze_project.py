import numpy as np
from PIL import Image

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\project.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

print(f"Image: {W}x{H}")

# Warm/bright spots (lamp light) — high R+G, low B, high luminance
warm = (R > 180) & (G > 150) & (R - B > 40) & (lum > 150)
print(f"\nWarm spots (lamp candidates): {warm.sum()}")

# Find warm spot clusters
ys, xs = np.where(warm)
if len(xs) > 0:
    print(f"  warm x range: {xs.min()}-{xs.max()} ({xs.min()/W*100:.0f}%-{xs.max()/W*100:.0f}%)")
    print(f"  warm y range: {ys.min()}-{ys.max()} ({ys.min()/H*100:.0f}%-{ys.max()/H*100:.0f}%)")
    # cluster by x thirds
    for third, (a, b) in enumerate([(0, W//3), (W//3, 2*W//3), (2*W//3, W)]):
        mask = (xs >= a) & (xs < b)
        if mask.sum() > 0:
            print(f"  third {third}: x {xs[mask].min()}-{xs[mask].max()}, y {ys[mask].min()}-{ys[mask].max()}, count {mask.sum()}")

# Dark structures (pavilion) — dark pixels in clusters
dark = (lum < 70) & (R < 90)
print(f"\nDark structures: {dark.sum()}")
ys2, xs2 = np.where(dark)
if len(xs2) > 0:
    print(f"  dark x range: {xs2.min()}-{xs2.max()} ({xs2.min()/W*100:.0f}%-{xs2.max()/W*100:.0f}%)")
    print(f"  dark y range: {ys2.min()}-{ys2.max()} ({ys2.min()/H*100:.0f}%-{ys2.max()/H*100:.0f}%)")

# Luminance grid (coarse)
print("\nLuminance grid (rows 15%-85%, cols 10%-90%):")
for ry in [0.15, 0.3, 0.45, 0.6, 0.75, 0.85]:
    row = int(ry * H)
    vals = []
    for rx in [0.1, 0.25, 0.4, 0.55, 0.7, 0.85]:
        col = int(rx * W)
        vals.append(f"{int(lum[row,col]):3d}")
    print(f"  y={ry:.0%}: " + " ".join(vals))
