import numpy as np
from PIL import Image

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\studio-bg.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

print(f"Image: {W}x{H} (aspect {W/H:.4f})")

# Scan left-bottom region for the lantern (x 5-18%, y 55-80%)
print("\nLeft-bottom region detail (lantern search), cols 4%-18%, rows 52%-82%:")
for ry in [0.52, 0.56, 0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78, 0.80, 0.82]:
    row = int(ry * H)
    vals = []
    for rx in [0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18]:
        col = int(rx * W)
        r, g, b = int(R[row,col]), int(G[row,col]), int(B[row,col])
        vals.append(f"({r:3d},{g:3d},{b:3d})")
    print(f"  y={ry:.0%}: " + " ".join(vals))

# Find the warmest concentrated spot in left-bottom (lantern core)
sub = ca[int(0.5*H):int(0.85*H), int(0.0*W):int(0.25*W)]
sR, sG, sB = sub[:,:,0], sub[:,:,1], sub[:,:,2]
slum = 0.299*sR + 0.587*sG + 0.114*sB
warm = (sR - sB > 45) & (sR > 150) & (slum > 120)
ys, xs = np.where(warm)
if len(xs) > 0:
    # centroid weighted by warmth
    weights = (sR - sB)[warm].astype(float)
    cx = (xs * weights).sum() / weights.sum()
    cy = (ys * weights).sum() / weights.sum()
    print(f"\nLantern weighted centroid: ({cx/25/0.04 + 0:.1f}%, ...) -> x={0 + cx/W*100:.1f}%, y={0.5*100 + cy/H*100:.1f}%")
    print(f"  (raw: x={cx/W*100:.1f}% of full, y={cy/H*100:.1f}% of full)")

# Pavilion region (right side)
print("\nRight region (pavilion), cols 70%-95%, rows 15%-80%:")
for ry in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    row = int(ry * H)
    vals = []
    for rx in [0.70, 0.78, 0.86, 0.94]:
        col = int(rx * W)
        vals.append(f"{int(lum[row,col]):3d}")
    print(f"  y={ry:.0%}: " + " ".join(vals))
