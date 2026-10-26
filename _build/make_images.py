"""Crop the project screenshots into the exact image sizes the portfolio pages use.

Each spec: output name, source image, left x, top y, crop width (crop height follows from the output's
aspect ratio), output width, output height. The crop is cut first, then resized to the slot.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
OUT = os.path.join(HERE, "portimg")
UP = "/Users/manuelnort/Desktop/ego/diginort/wp-content/uploads/2025/09"
COFFEE = os.path.join(UP, "original-642fa30c49259d5b203745d12a7a7ea4.webp")
MERCH = os.path.join(UP, "Untitled-1-1-740x740.png")


def shot(name):
    return os.path.join(SHOTS, name + ".png")


AGORIVIA_HERO = os.path.join(SHOTS, "test.png")  # first capture: has the header, cookie bar below y=720

SPECS = [
    # Homepage: selected projects
    ("home-agorivia-1.jpg", shot("agorivia-full"), 0, 2480, 1440, 1600, 1200),
    ("home-agorivia-2.jpg", AGORIVIA_HERO, 100, 0, 1080, 1200, 800),
    ("home-netra-1.jpg", shot("netra-mobile"), 0, 0, 390, 410, 500),
    ("home-netra-2.jpg", shot("netra-desktop"), 0, 50, 1440, 850, 500),
    ("home-netra-3.jpg", shot("netra-full"), 420, 1500, 700, 410, 500),
    ("home-wmt-1.jpg", shot("wmt-desktop"), 440, 0, 1000, 1200, 839),
    ("home-wmt-2.jpg", shot("wmt-projects-desktop"), 82, 0, 1259, 1200, 858),
    # Homepage: studio blurb, intro square, certificates
    ("home-weekendchef-small.jpg", shot("weekendchef-desktop"), 300, 60, 840, 200, 160),
    ("home-strategicagile.jpg", shot("strategicagile-full"), 0, 870, 1440, 520, 420),
    ("home-coffee-app.jpg", COFFEE, 200, 0, 1200, 740, 740),
    # About
    ("about-main.jpg", shot("eah-desktop"), 0, 0, 1357, 1200, 796),
    ("about-collage-1.jpg", shot("creativeclick-full"), 700, 2450, 740, 405, 400),
    ("about-collage-2.jpg", shot("weekendchef-mobile"), 0, 0, 390, 520, 600),
    ("about-collage-3.jpg", shot("strategicagile-full"), 0, 3720, 1440, 415, 310),
    ("about-collage-4.jpg", shot("eah-mobile"), 0, 0, 390, 520, 700),
    ("about-collage-5.jpg", shot("mawuena-full"), 0, 900, 1440, 415, 360),
    ("about-process.jpg", shot("creativeclick-desktop"), 0, 0, 1440, 1800, 900),
    ("about-small-1.jpg", shot("netra-desktop"), 300, 0, 840, 300, 220),
    ("about-small-2.jpg", shot("wmt-about-desktop"), 0, 0, 1227, 300, 220),
    ("about-step-discover.jpg", shot("strategicagile-full"), 200, 2050, 1040, 600, 600),
    ("about-step-design.jpg", COFFEE, 200, 0, 1200, 600, 600),
    ("about-step-build.jpg", shot("netra-full"), 420, 1450, 900, 600, 600),
    ("about-step-launch.jpg", shot("mawuena-full"), 120, 2400, 1200, 600, 600),
    # Works grid
    ("grid-agorivia.jpg", AGORIVIA_HERO, 120, 0, 720, 420, 420),
    ("grid-eah.jpg", shot("eah-desktop"), 40, 0, 900, 420, 420),
    ("grid-netra.jpg", shot("netra-desktop"), 270, 0, 900, 420, 420),
    ("grid-weekendchef.jpg", shot("weekendchef-desktop"), 270, 0, 900, 420, 420),
    ("grid-strategicagile.jpg", shot("strategicagile-full"), 0, 870, 1160, 420, 420),
    ("grid-wmt.jpg", shot("wmt-desktop"), 0, 0, 900, 420, 420),
    ("grid-mawuena.jpg", shot("mawuena-full"), 0, 850, 1200, 420, 420),
    ("grid-creativeclick.jpg", shot("creativeclick-desktop"), 0, 0, 900, 420, 420),
    ("grid-coffee-app.jpg", COFFEE, 200, 0, 1200, 420, 420),
    ("grid-merch.jpg", MERCH, 0, 0, 740, 420, 420),
]


def size(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path], capture_output=True, text=True).stdout
    vals = [int(l.split(":")[1]) for l in out.splitlines() if "pixel" in l]
    return vals[0], vals[1]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    # Cropping runs in Chrome (crop.mjs): sips's crop offsets turned out to be unreliable
    jobs = []
    for name, src, x, y, w, out_w, out_h in SPECS:
        sw, sh = size(src)
        h = round(w * out_h / out_w)
        if x + w > sw or y + h > sh:
            sys.exit("%s: crop %dx%d at %d,%d is outside %s (%dx%d)" % (name, w, h, x, y, os.path.basename(src), sw, sh))
        jobs.append({"out": os.path.join(OUT, name[:-4] + ".png"), "src": src, "x": x, "y": y, "w": w, "h": h,
                     "outW": out_w, "outH": out_h})
    spec_file = os.path.join(OUT, "_specs.json")
    json.dump(jobs, open(spec_file, "w"))
    subprocess.run(["node", os.path.join(HERE, "crop.mjs"), spec_file], check=True)
    os.remove(spec_file)
    for job, (name, *_rest, out_w, out_h) in zip(jobs, SPECS):
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", job["out"],
                        "--out", os.path.join(OUT, name)], check=True, capture_output=True)
        os.remove(job["out"])
        print("made", name, "%dx%d" % size(os.path.join(OUT, name)))
    # Diginort mark in place of the theme demo's logo mark (same 120px square)
    subprocess.run(["sips", "-z", "120", "120", os.path.join(UP, "cropped-Digi-logo-1-270x270.png"),
                    "--out", os.path.join(OUT, "diginort-mark.png")], check=True, capture_output=True)
    print("made diginort-mark.png")
    # Certificate and experience cards were rendered as PNG at 2x; ship them as JPEG
    for folder in ("certs", "cards"):
        for f in sorted(os.listdir(os.path.join(HERE, folder))):
            if f.endswith(".png"):
                subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", os.path.join(HERE, folder, f),
                                "--out", os.path.join(OUT, f[:-4] + ".jpg")], check=True, capture_output=True)
                print("made", f[:-4] + ".jpg")
