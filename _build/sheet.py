"""Contact sheet: python3 -I sheet.py <dir> <out.jpg> [cols] [thumb width]"""
import glob, os, sys
from PIL import Image
d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
tw = int(sys.argv[4]) if len(sys.argv) > 4 else 480
files = sorted(glob.glob(os.path.join(d, "*.jpg")) + glob.glob(os.path.join(d, "*.png")))
ims = [Image.open(f).convert("RGB") for f in files]
ims = [im.resize((tw, round(im.height * tw / im.width))) for im in ims]
th = max(im.height for im in ims)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 8) + 8), (255, 0, 255))
for i, im in enumerate(ims):
    sheet.paste(im, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
sheet.save(out, quality=80)
print(out, sheet.size)
