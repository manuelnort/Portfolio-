"""Photo images for each project (the per-site template).

For every project in MEDIA: a Works card photo and a second photo that fades in on hover (both 960x800,
the card's 6:5 shape at 2x), plus any homepage gallery images at their slot sizes. Each source photo is
cropped to the slot's shape around a focus point (fx, fy as fractions of the width/height), then resized.
Run:  python3 -I projects.py [project ...]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "portimg")

# project: {"card": (file, fx, fy), "hover": (file, fx, fy), "gallery": [(file, fx, fy), ...]}
# "gallery": the homepage strip after the logo panel (art.py makes that one): cover (850 wide),
# then photos (410, 650, 410), all 500 tall, made at 2x

GALLERY_SIZES = [(1700, 1000), (820, 1000), (1300, 1000), (820, 1000)]
MEDIA = {
    "wmt": {
        "card": ("4.webp", .5, .35),
        "hover": ("3.jpg", .55, .4),
        "gallery": [("6.webp", .5, .55), ("5.webp", .62, .45), ("3.jpg", .55, .45), ("7.webp", .5, .5)],
    },
    "netra": {
        "card": ("office.jpg", .5, .5),
        "hover": ("payment.webp", .5, .4),
        "gallery": [("office.jpg", .5, .5), ("payment.webp", .5, .5), ("team.jpg", .5, .45), ("watch.jpeg", .5, .5)],
    },
    "strategicagile": {
        "card": ("cover.jpg", .5, .3),
    },
    # Works cards for the other projects, from photos on their own sites (harvest.py)
    "geoben": {"card": ("site-01.jpg", .5, .45), "hover": ("site-03.jpg", .5, .5)},
    "weekendchef": {"card": ("site-01.jpg", .5, .5)},
    "mawuena": {"card": ("site-03.jpg", .5, .5), "hover": ("site-11.jpg", .5, .5)},
    "feci": {"card": ("site-04.png", .5, .3), "hover": ("site-14.jpg", .5, .4)},
    "releev": {"card": ("site-01.png", .5, .5), "hover": ("site-04.png", .5, .5)},
    "quickpipe": {"card": ("site-01.jpg", .5, .5), "hover": ("site-03.png", .5, .3)},
    "eah": {"card": ("site-04.jpg", .5, .3), "hover": ("site-12.jpg", .5, .4)},
    "creativeclick": {"card": ("site-02.jpg", .5, .5), "hover": ("site-01.jpg", .5, .4)},
    "agorivia": {  # one site photo so far: different crops of it until more photos arrive
        "card": ("hero.png", .45, .5),
        "gallery": [("hero.png", .5, .5), ("hero.png", .2, .5), ("hero.png", .6, .5), ("hero.png", .9, .5)],
    },
}


def size(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path], capture_output=True, text=True).stdout
    return [int(l.split(":")[1]) for l in out.splitlines() if "pixel" in l]


def cover(src, out_w, out_h, fx, fy):
    """Largest region of src with the output's shape, centred on the focus point as far as the edges allow."""
    w, h = size(src)
    aspect = out_w / out_h
    if w / h > aspect:
        cw, ch = round(h * aspect), h
    else:
        cw, ch = w, round(w / aspect)
    x = min(max(round(fx * w - cw / 2), 0), w - cw)
    y = min(max(round(fy * h - ch / 2), 0), h - ch)
    return {"x": x, "y": y, "w": cw, "h": ch, "outW": out_w, "outH": out_h}


def build(project):
    src_dir = os.path.join(HERE, "projects", project)
    spec = MEDIA[project]
    jobs = []
    for role in ("card", "hover"):
        if role in spec:
            f, fx, fy = spec[role]
            jobs.append(dict(cover(os.path.join(src_dir, f), 960, 800, fx, fy), src=os.path.join(src_dir, f),
                             name="proj-%s-%s.jpg" % (project, role)))
    for i, ((f, fx, fy), (w, h)) in enumerate(zip(spec.get("gallery", []), GALLERY_SIZES), 2):
        jobs.append(dict(cover(os.path.join(src_dir, f), w, h, fx, fy), src=os.path.join(src_dir, f),
                         name="gal-%s-%d.jpg" % (project, i)))
    for j in jobs:
        j["out"] = os.path.join(OUT, j["name"][:-4] + ".png")
    spec_file = os.path.join(OUT, "_proj.json")
    json.dump(jobs, open(spec_file, "w"))
    subprocess.run(["node", os.path.join(HERE, "crop.mjs"), spec_file], check=True, capture_output=True)
    os.remove(spec_file)
    for j in jobs:
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84", j["out"], "--out", os.path.join(OUT, j["name"])],
                       check=True, capture_output=True)
        os.remove(j["out"])
        print("made", j["name"], "%dx%d" % (j["outW"], j["outH"]))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for project in sys.argv[1:] or MEDIA:
        build(project)
