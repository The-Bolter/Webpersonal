import numpy as np
from PIL import Image

CONCEPT = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept.png"
PLUM = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\assets\index\plum\plum-branch.png"

# --- Concept art: find pink/red plum blossom pixels ---
c = Image.open(CONCEPT).convert("RGB")
ca = np.array(c).astype(np.int16)
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]

# Plum blossoms = red/pink: R high, G lower, B lower/mid
# Also detect dark branch pixels in top region
pink = (R > 120) & (R - G > 40) & (R - B > 30) & (G < 200)

ys, xs = np.where(pink)
if len(xs) > 0:
    print(f"Concept art pink pixels: {len(xs)}")
    print(f"  x range: {xs.min()} - {xs.max()}  (width {ca.shape[1]})")
    print(f"  y range: {ys.min()} - {ys.max()}  (height {ca.shape[0]})")
    # distribution by quadrant
    cx = ca.shape[1] // 2
    cy = ca.shape[0] // 2
    top = ys < cy
    right = xs > cx
    print(f"  top-half pink: {(top).sum()}, bottom-half: {(~top).sum()}")
    print(f"  right-half: {(right).sum()}, left-half: {(~right).sum()}")
    # top-right quadrant stats
    tr = top & right
    if tr.sum() > 0:
        print(f"  top-right pink: x {xs[tr].min()}-{xs[tr].max()}, y {ys[tr].min()}-{ys[tr].max()}")
    # top-left
    tl = top & (~right)
    if tl.sum() > 0:
        print(f"  top-left pink: x {xs[tl].min()}-{xs[tl].max()}, y {ys[tl].min()}-{ys[tl].max()}")
else:
    print("No pink pixels found in concept art")

# --- Plum cutout: content bounding box ---
p = Image.open(PLUM).convert("RGBA")
pa = np.array(p)
alpha = pa[:, :, 3]
ys2, xs2 = np.where(alpha > 20)
if len(xs2) > 0:
    print(f"\nPlum cutout content bbox:")
    print(f"  x: {xs2.min()} - {xs2.max()}  (width {pa.shape[1]})")
    print(f"  y: {ys2.min()} - {ys2.max()}  (height {pa.shape[0]})")
    print(f"  bbox size: {xs2.max()-xs2.min()+1} x {ys2.max()-ys2.min()+1}")
else:
    print("No content found in plum cutout")
