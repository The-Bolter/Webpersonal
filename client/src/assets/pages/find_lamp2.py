import numpy as np
from PIL import Image
from scipy import ndimage

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\project.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

# Red/orange lantern: saturated red-orange (high R, low B, R>>G)
red = (R > 120) & (R - G > 50) & (R - B > 40)
labeled, num = ndimage.label(red)
print("Red/orange clusters (lantern candidates):")
clusters = []
for i in range(1, num+1):
    ys, xs = np.where(labeled == i)
    if len(xs) < 8:
        continue
    clusters.append((len(xs), xs.mean()/W*100, ys.mean()/H*100))
clusters.sort(reverse=True)
for size, cx, cy in clusters[:20]:
    print(f"  size={size:5d} at ({cx:.1f}%, {cy:.1f}%)")

# Also look for any distinctly colored object (pavilion roof might be dark or distinct)
# Print a coarse color map of the full image
print("\nFull image coarse map (every 8%, showing hue sign: R=red-ish, .=neutral):")
for ry in range(0, 100, 8):
    row = int(ry/100 * H)
    line = ""
    for rx in range(0, 100, 4):
        col = int(rx/100 * W)
        r, g, b = int(R[row,col]), int(G[row,col]), int(B[row,col])
        if r - g > 40 and r - b > 30:
            line += "R"  # red/orange
        elif r - g > 15 and r - b > 10:
            line += "r"  # warm
        elif lum[row,col] < 90:
            line += "#"  # dark
        elif lum[row,col] > 220:
            line += "."  # bright
        else:
            line += "+"  # mid
    print(f"  {ry:3d}%: {line}")
