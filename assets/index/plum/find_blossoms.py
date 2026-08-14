import numpy as np
from PIL import Image
from scipy import ndimage

PLUM = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\assets\index\plum\plum-branch.png"

img = Image.open(PLUM).convert("RGBA")
pa = np.array(img)
A = pa[:, :, 3].astype(np.int16)
R = pa[:, :, 0].astype(np.int16)
G = pa[:, :, 1].astype(np.int16)
B = pa[:, :, 2].astype(np.int16)

pink = (A > 100) & (R > 110) & (R - G > 25) & (R - B > 15)

print(f"Pink blossom pixels: {pink.sum()}")

labeled, num = ndimage.label(pink)
print(f"Blossom clusters: {num}")

clusters = []
for i in range(1, num + 1):
    ys, xs = np.where(labeled == i)
    if len(xs) < 40:
        continue
    cx, cy = xs.mean(), ys.mean()
    clusters.append((len(xs), cx, cy, xs.min(), xs.max(), ys.min(), ys.max()))

clusters.sort(reverse=True)
print(f"\nClusters >=40px ({len(clusters)}):")
for size, cx, cy, xmin, xmax, ymin, ymax in clusters[:20]:
    print(f"  size={size:5d}  center=({cx:5.0f},{cy:5.0f})  "
          f"({cx/pa.shape[1]*100:.1f}%, {cy/pa.shape[0]*100:.1f}%)")
