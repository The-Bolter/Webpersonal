import numpy as np
from PIL import Image
from scipy import ndimage

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\pages\project.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

# Lamp: very bright warm glow (high R, high G, lower B, high luminance)
lamp = (R > 200) & (G > 175) & (R - B > 30) & (lum > 180)
labeled, num = ndimage.label(lamp)
print("Lamp candidate clusters (bright warm):")
clusters = []
for i in range(1, num+1):
    ys, xs = np.where(labeled == i)
    if len(xs) < 30:
        continue
    clusters.append((len(xs), xs.mean(), ys.mean()))
clusters.sort(reverse=True)
for size, cx, cy in clusters[:10]:
    print(f"  size={size:5d} center=({cx/W*100:.1f}%, {cy/H*100:.1f}%)")

# Pavilion: dark structure clusters (dark, localized)
dark = (lum < 80) & (R < 95)
labeled2, num2 = ndimage.label(dark)
print("\nDark structure clusters:")
clusters2 = []
for i in range(1, num2+1):
    ys, xs = np.where(labeled2 == i)
    if len(xs) < 25:
        continue
    clusters2.append((len(xs), xs.mean(), ys.mean(), xs.min(), xs.max(), ys.min(), ys.max()))
clusters2.sort(reverse=True)
for size, cx, cy, x0, x1, y0, y1 in clusters2[:10]:
    print(f"  size={size:5d} center=({cx/W*100:.1f}%, {cy/H*100:.1f}%) bbox x={x0/W*100:.0f}-{x1/W*100:.0f}% y={y0/H*100:.0f}-{y1/H*100:.0f}%")
