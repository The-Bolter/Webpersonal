import numpy as np
from PIL import Image
from scipy import ndimage

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\studio-bg.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

print(f"Image: {W}x{H}")

# Overall luminance stats
print(f"Avg luminance: {lum.mean():.0f}, dark(<80): {(lum<80).sum()}, bright(>200): {(lum>200).sum()}")

# Warm bright spots (lamp candidates)
warm = (R > 190) & (G > 160) & (R - B > 30) & (lum > 160)
labeled, num = ndimage.label(warm)
clusters = []
for i in range(1, num+1):
    ys, xs = np.where(labeled == i)
    if len(xs) < 40:
        continue
    clusters.append((len(xs), xs.mean()/W*100, ys.mean()/H*100))
clusters.sort(reverse=True)
print("\nWarm bright clusters (lamp candidates):")
for size, cx, cy in clusters[:8]:
    print(f"  size={size:6d} at ({cx:.1f}%, {cy:.1f}%)")

# Dark structures (pavilion)
dark = (lum < 70)
labeled2, num2 = ndimage.label(dark)
clusters2 = []
for i in range(1, num2+1):
    ys, xs = np.where(labeled2 == i)
    if len(xs) < 30:
        continue
    clusters2.append((len(xs), xs.mean()/W*100, ys.mean()/H*100))
clusters2.sort(reverse=True)
print("\nDark structure clusters (pavilion candidates):")
for size, cx, cy in clusters2[:8]:
    print(f"  size={size:6d} at ({cx:.1f}%, {cy:.1f}%)")

# Luminance grid
print("\nLuminance grid (rows 15%-85%, cols 10%-90%):")
for ry in [0.15, 0.3, 0.45, 0.6, 0.75, 0.85]:
    row = int(ry * H)
    vals = []
    for rx in [0.1, 0.25, 0.4, 0.55, 0.7, 0.85]:
        col = int(rx * W)
        vals.append(f"{int(lum[row,col]):3d}")
    print(f"  y={ry:.0%}: " + " ".join(vals))
