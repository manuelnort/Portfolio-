"""Testimonial photos cropped from pictures on the clients' own sites.

  projects/mawuena/founder.jpg          Mawuena Datsa, from "Meet the founder" on mawuenadatsafoundation.org
  projects/agorivia/about-founder.png   the founder photo in the About section of agorivia.co/about

Writes portimg/testi-mawuena-founder.jpg (4:5, for the large testimonial card) and
portimg/voice-agorivia-founder.jpg (square, for the round photo on the client wall).

Usage: python3 testimonial_photos.py   (needs Pillow)
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "portimg")

CROPS = [  # (source, (left, top, right, bottom) as fractions of the image, output, size)
    ("projects/mawuena/founder.jpg", (.11, .03, .87, .69), "testi-mawuena-founder.jpg", (800, 1000)),
    ("projects/agorivia/about-founder.png", (.1, .03, .98, .617), "voice-agorivia-founder.jpg", (400, 400)),
]

for src, (l, t, r, b), name, size in CROPS:
    im = Image.open(os.path.join(HERE, src)).convert("RGB")
    w, h = im.size
    im = im.crop((round(l * w), round(t * h), round(r * w), round(b * h))).resize(size, Image.LANCZOS)
    im.save(os.path.join(OUT, name), quality=86)
    print(name, size)
