import numpy as np
import cv2
from PIL import Image

CONCEPT = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept.png"
BACKUP = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept-with-plum.png"
OUT = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\design\concept\index-v1-concept.png"

img = cv2.imread(CONCEPT, cv2.IMREAD_COLOR)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Keep original backup
cv2.imwrite(BACKUP, img)

H, W = img.shape[:2]
B, G, R = img[:, :, 0].astype(np.int16), img[:, :, 1].astype(np.int16), img[:, :, 2].astype(np.int16)

# Branch region bounding box (with margin)
x0, x1 = 950, 1672
y0, y1 = 80, 800

mask = np.zeros((H, W), dtype=np.uint8)

# Detect within region only
subR, subG, subB = R[y0:y1, x0:x1], G[y0:y1, x0:x1], B[y0:y1, x0:x1]

# Plum blossoms: pink/red
pink = (subR > 100) & (subR - subG > 25) & (subR - subB > 15)
# Branches: dark brown/dark (background is light ~200+)
dark = (subR < 160) & (subG < 155) & (subB < 145)

sub_mask = (pink | dark).astype(np.uint8) * 255
mask[y0:y1, x0:x1] = sub_mask

# Dilate to cover anti-aliased edges and thin twigs
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.dilate(mask, kernel, iterations=2)

# Small openings cleanup: remove tiny specks not connected to branch
# (keep as-is for safety — inpaint handles small masks fine)

mask_px = int((mask > 0).sum())
print(f"Mask pixels: {mask_px}")

# Inpaint
result = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)

cv2.imwrite(OUT, result)
print(f"Saved: {OUT}")
print(f"Backup: {BACKUP}")
