import numpy as np
from PIL import Image

CONCEPT = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept.png"

c = Image.open(CONCEPT).convert("RGB")
ca = np.array(c).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]

# Focus on top-right region
x0, x1 = 900, W
y0, y1 = 0, int(H * 0.85)
reg_R, reg_G, reg_B = R[y0:y1, x0:x1], G[y0:y1, x0:x1], B[y0:y1, x0:x1]

# Color signatures
pink = (reg_R > 110) & (reg_R - reg_G > 30) & (reg_R - reg_B > 20)
dark = (reg_R < 90) & (reg_G < 90) & (reg_B < 90)
dark_brown = (reg_R > 40) & (reg_R < 120) & (reg_G < 100) & (reg_B < 90) & (reg_R - reg_B > 10)

print("Top-right region size:", reg_R.shape)
print(f"pink (blossoms): {pink.sum()}")
print(f"dark (all): {dark.sum()}")
print(f"dark_brown (branches): {dark_brown.sum()}")

# Where are pink pixels vertically distributed?
ys, xs = np.where(pink)
if len(ys) > 0:
    print(f"pink y range: {ys.min()+y0} - {ys.max()+y0} ({ys.min()/reg_R.shape[0]*100:.0f}% - {ys.max()/reg_R.shape[0]*100:.0f}%)")
    print(f"pink x range: {xs.min()+x0} - {xs.max()+x0}")

# Dark brown branch distribution
ys2, xs2 = np.where(dark_brown)
if len(ys2) > 0:
    print(f"dark_brown y range: {ys2.min()+y0} - {ys2.max()+y0}")
    print(f"dark_brown x range: {xs2.min()+x0} - {xs2.max()+x0}")

# Check mountain colors: sample the right-middle area (likely mountains)
print("\nSample colors (right side, various heights):")
for yy in [0.2, 0.4, 0.55, 0.7]:
    row = int(yy * H)
    for xx in [0.60, 0.75, 0.9]:
        col = int(xx * W)
        print(f"  ({col},{row}): R={R[row,col]} G={G[row,col]} B={B[row,col]}")
