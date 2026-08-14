import numpy as np
from PIL import Image

CONCEPT = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept.png"
PLUM = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\assets\index\plum\plum-branch.png"

c = Image.open(CONCEPT).convert("RGB")
ca = np.array(c).astype(np.int16)
H, W = ca.shape[:2]
print(f"Concept art: {W}x{H}")

R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]

# Broad "plum branch" detection in right half: pink blossoms + dark branches
# Pink: R-G>30 and R-B>25 (red/pink hue)
pink = (R > 110) & (R - G > 30) & (R - B > 20)
# Dark branch: low luminance but not sky/mist
lum = 0.299*R + 0.587*G + 0.114*B
dark = (lum < 100) & (R > 20)
branch = pink | dark

# Restrict to right half + top 60%
right = np.zeros_like(branch, dtype=bool)
right[:, W//2:] = True
top = np.zeros_like(branch, dtype=bool)
top[:int(H*0.6), :] = True
region = branch & right & top

ys, xs = np.where(region)
if len(xs) > 0:
    print(f"\nConcept plum (branch+pink) in right-top region:")
    print(f"  x: {xs.min()} - {xs.max()}  ({xs.min()/W*100:.1f}% - {xs.max()/W*100:.1f}%)")
    print(f"  y: {ys.min()} - {ys.max()}  ({ys.min()/H*100:.1f}% - {ys.max()/H*100:.1f}%)")
    print(f"  bbox: {xs.max()-xs.min()+1} x {ys.max()-ys.min()+1}")

# Also check: where does the branch start from top edge?
for col in range(W//2, W, 50):
    col_pixels = np.where(region[:, col])[0]
    if len(col_pixels) > 0:
        print(f"  column x={col} ({col/W*100:.0f}%): first branch pixel at y={col_pixels.min()} ({col_pixels.min()/H*100:.1f}%)")

# Cutout: content bounding box
p = Image.open(PLUM).convert("RGBA")
pa = np.array(p)
alpha = pa[:, :, 3]
ys2, xs2 = np.where(alpha > 20)
print(f"\nCutout content bbox:")
print(f"  x: {xs2.min()} - {xs2.max()}  ({xs2.min()/pa.shape[1]*100:.1f}% - {xs2.max()/pa.shape[1]*100:.1f}%)")
print(f"  y: {ys2.min()} - {ys2.max()}  ({ys2.min()/pa.shape[0]*100:.1f}% - {ys2.max()/pa.shape[0]*100:.1f}%)")
