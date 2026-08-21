import numpy as np
from PIL import Image
from scipy import ndimage

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\project.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

print(f"Image: {W}x{H}")

# Lamp: very bright, warm, concentrated (high R, high G, R>>B)
# Use stricter threshold for a true lamp (small bright warm source)
lamp = (R > 220) & (G > 190) & (R - B > 50) & (lum > 210)
labeled, num = ndimage.label(lamp)
print("Very bright warm clusters (strong lamp candidates):")
clusters = []
for i in range(1, num+1):
    ys, xs = np.where(labeled == i)
    if len(xs) < 10:
        continue
    clusters.append((len(xs), xs.mean()/W*100, ys.mean()/H*100, xs.min()/W*100, xs.max()/W*100, ys.min()/H*100, ys.max()/H*100))
clusters.sort(reverse=True)
for size, cx, cy, x0, x1, y0, y1 in clusters[:15]:
    print(f"  size={size:5d} center=({cx:.1f}%,{cy:.1f}%) bbox=({x0:.0f}%-{x1:.0f}%, {y0:.0f}%-{y1:.0f}%)")

# Also check specific candidate regions
print("\nSample specific points (RGB + luminance):")
for (rx, ry) in [(0.15, 0.55), (0.2, 0.5), (0.1, 0.6), (0.15, 0.7), (0.25, 0.75), (0.85, 0.5), (0.8, 0.4), (0.75, 0.35), (0.9, 0.35)]:
    col, row = int(rx*W), int(ry*H)
    print(f"  ({rx:.0%},{ry:.0%}): R={R[row,col]} G={G[row,col]} B={B[row,col]} lum={int(lum[row,col])}")
