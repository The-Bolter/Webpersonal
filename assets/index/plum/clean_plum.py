import numpy as np
from PIL import Image, ImageFilter

SRC = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\assets\index\plum\plum-branch.png"
BACKUP = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\assets\index\plum\plum-branch-original.png"
OUT = r"C:\Users\liuwanting05\Desktop\Webpersonal\Webpersonal\assets\index\plum\plum-branch.png"

img = Image.open(SRC).convert("RGBA")
img.save(BACKUP)  # keep original

arr = np.array(img).astype(np.int16)
R, G, B, A = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

# Background = light white/cream/yellow pixels
bg = (R > 200) & (G > 180) & (B > 160)

# Content mask: 255 = keep, 0 = remove
content = (~bg).astype(np.uint8) * 255

# Feather edges with slight blur
mask_img = Image.fromarray(content, mode="L")
mask_img = mask_img.filter(ImageFilter.GaussianBlur(1.2))
mask = np.array(mask_img).astype(np.float32) / 255.0

# Apply mask to alpha (feathered edges)
new_alpha = (A * mask).clip(0, 255).astype(np.uint8)
arr[:, :, 3] = new_alpha

result = Image.fromarray(arr.astype(np.uint8), "RGBA")
result.save(OUT)

# Stats
kept = int((new_alpha > 10).sum())
total = new_alpha.size
print(f"Done. Kept {kept}/{total} opaque-ish pixels ({kept*100//total}%).")
print(f"Backup: {BACKUP}")
print(f"Output: {OUT}")
