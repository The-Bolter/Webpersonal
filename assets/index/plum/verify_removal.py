import numpy as np
from PIL import Image

OUT = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept.png"
ORIG = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept-with-plum.png"

for name, path in [("RESULT", OUT), ("ORIGINAL", ORIG)]:
    img = Image.open(path).convert("RGB")
    ca = np.array(img).astype(np.int16)
    R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
    x0, x1, y0, y1 = 950, 1672, 80, 800
    subR, subG, subB = R[y0:y1, x0:x1], G[y0:y1, x0:x1], B[y0:y1, x0:x1]
    pink = (subR > 100) & (subR - subG > 25) & (subR - subB > 15)
    dark = (subR < 160) & (subG < 155) & (subB < 145)
    print(f"{name}: pink={pink.sum()}, dark={dark.sum()}, combined={(pink|dark).sum()}")
    # average background color of the region (excluding nothing)
    print(f"  avg R={subR.mean():.0f} G={subG.mean():.0f} B={subB.mean():.0f}")

# Also verify other regions unchanged (compare diff outside branch bbox)
orig = Image.open(ORIG).convert("RGB")
res = Image.open(OUT).convert("RGB")
oa = np.array(orig).astype(np.int16)
ra = np.array(res).astype(np.int16)
diff = np.abs(oa - ra).sum(axis=2)
# outside region
outside = np.ones_like(diff, dtype=bool)
outside[y0:y1, x0:x1] = False
changed_outside = (diff[outside] > 10).sum()
print(f"\nChanged pixels OUTSIDE branch region (>10 diff): {changed_outside}")
