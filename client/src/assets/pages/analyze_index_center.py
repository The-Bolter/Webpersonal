import numpy as np
from PIL import Image

PATH = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\client\src\assets\index\concept\index-v1-concept.png"
img = Image.open(PATH).convert("RGB")
ca = np.array(img).astype(np.int16)
H, W = ca.shape[:2]
R, G, B = ca[:, :, 0], ca[:, :, 1], ca[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B

print(f"Image: {W}x{H}")

# Center region where content sits (left 48%, top 55% → content sheet center)
# content sheet is min(54vw,760px) centered at 48%, 55%
print("\nCenter region luminance (rows 35%-75%, cols 20%-75%):")
for ry in [0.35, 0.45, 0.55, 0.65, 0.75]:
    row = int(ry * H)
    vals = []
    for rx in [0.2, 0.35, 0.48, 0.6, 0.75]:
        col = int(rx * W)
        v = int(lum[row, col])
        vals.append(f"{v:3d}")
    print(f"  y={ry:.0%}: " + " ".join(vals))

# Average luminance of center region
cx0, cx1 = int(0.25*W), int(0.7*W)
cy0, cy1 = int(0.35*H), int(0.75*H)
center = lum[cy0:cy1, cx0:cx1]
print(f"\nCenter region avg luminance: {center.mean():.0f}")
print(f"Center region min/max: {center.min()}/{center.max()}")
print(f"Dark pixels (<120) in center: {(center<120).sum()} / {center.size}")
print(f"Bright pixels (>200) in center: {(center>200).sum()} / {center.size}")

# Moon position (bright round area, upper area)
bright = lum > 230
ys, xs = np.where(bright)
print(f"\nBrightest areas: x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()}")
