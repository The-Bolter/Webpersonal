import numpy as np
from PIL import Image
from scipy import ndimage

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\project.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

# Warm "light" = R notably higher than B (warm tint), and brighter than surroundings
# Look for local warm-bright peaks: warm AND lum > local average
warm_tint = (R - B > 35) & (R > 140) & (lum > 130)
labeled, num = ndimage.label(warm_tint)
clusters = []
for i in range(1, num+1):
    ys, xs = np.where(labeled == i)
    if len(xs) < 20:
        continue
    # filter: keep clusters that are NOT the huge background
    clusters.append((len(xs), xs.mean()/W*100, ys.mean()/H*100))
clusters.sort(reverse=True)
print("Warm-tint clusters (R-B>35, R>140, lum>130), top 20:")
for size, cx, cy in clusters[:20]:
    print(f"  size={size:6d} at ({cx:.1f}%, {cy:.1f}%)")

# Dense grid scan: find the SINGLE brightest warm pixel region (lamp core)
# Lamp core: R>230, G>200, B<180 (very warm bright, concentrated)
core = (R > 230) & (G > 195) & (B < 185)
print(f"\nLamp core (R>230,G>195,B<185): {core.sum()} pixels")
if core.sum() > 0:
    ys, xs = np.where(core)
    print(f"  at x {xs.min()}-{xs.max()} ({xs.min()/W*100:.1f}%-{xs.max()/W*100:.1f}%), y {ys.min()}-{ys.max()} ({ys.min()/H*100:.1f}%-{ys.max()/H*100:.1f}%)")
    # centroid
    print(f"  centroid ({xs.mean()/W*100:.1f}%, {ys.mean()/H*100:.1f}%)")
