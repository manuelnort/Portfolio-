"""Brand artwork for the portfolio: logos on liquid-glass tiles over a coloured glow.

Each image is an HTML page rendered by headless Chrome at the exact size of the slot it fills.
Output goes to portimg/ (copied into the site by portfolio.py).
"""
import os, subprocess, sys, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = os.path.join(HERE, "logos")
OUT = os.path.join(HERE, "portimg")
WORK = os.path.join(HERE, "artwork")
FONT = "/Users/manuelnort/Desktop/ego/diginort/wp-content/themes/evne/assets/fonts/glancyr/Glancyr-Neue-Regular.otf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# name: (logo file or None, monogram, glow colour, second glow, logo tile height in px at 1x)
BRANDS = {
    "agorivia": ("agorivia-A.png", None, "#2f6b4f", "#c9a86a"),
    "agorivia-icon": ("agorivia-icon.png", None, "#2f6b4f", "#c9a86a"),
    "netra": ("netra.png", None, "#2f6fd6", "#e8573c"),
    "weekendchef": ("weekendchef.png", None, "#e0612b", "#c81d25"),
    "wmt": ("wmt.png", None, "#2c7be5", "#1fb6ff"),
    "strategicagile": ("strategicagile.svg", None, "#1d3a6b", "#6f8fbf"),
    "eah": ("eah-icon.png", None, "#2bb3e6", "#3c3fd6"),
    "mawuena": ("mawuena.png", None, "#a43cc9", "#f06bd1"),
    "feci": ("feci.png", None, "#6a2bd6", "#a46bff"),
    "releev": ("releev.png", None, "#14a3a8", "#2f6fd6"),
    "quickpipe": ("quickpipe-icon.png", None, "#3b5bff", "#00b3ff"),
    "creativeclick": ("creativeclick.svg", None, "#6a5cff", "#9a8cff"),
    "geoben": (None, "GH", "#c99a2e", "#7a5a12"),
    "diginort": (None, None, "#f25749", "#7a2a24"),
    "pagecast": (None, None, "#ff6a3d", "#7a4dff"),
}

# How each logo shows on the dark artwork without a tile: its official white file, the logo turned white
# (dark or same-colour-as-its-glow logos would disappear), or as it is (bright badges that already stand out)
WHITE_FILE = {"agorivia": "agorivia-white.png", "wmt": "wmt-white.png", "strategicagile": "strategicagile-white.svg"}
MAKE_WHITE = {"netra", "releev", "mawuena", "quickpipe", "creativeclick", "agorivia-icon", "eah"}
# keep as is: weekendchef, feci


def logo_img(brand, style=""):
    """The logo for a brand on dark artwork: no tile behind it, white where the colours would blend in."""
    logo, mono, c1, _ = BRANDS[brand]
    shadow = "drop-shadow(0 10px 28px rgba(0,0,0,.45))"
    if not logo:
        return '<span class="mono" style="color:#fff;%s">%s</span>' % (style, mono or "")
    if brand in WHITE_FILE:
        f = WHITE_FILE[brand]
        if f.endswith(".svg"):   # an SVG keeps its small built-in size under max-height; give it a real height
            style = style.replace("max-height", "height")
        return '<img src="file://%s/%s" style="%sfilter:%s">' % (LOGOS, f, style, shadow)
    white = "brightness(0) invert(1) " if brand in MAKE_WHITE else ""
    return '<img src="file://%s/%s" style="%sfilter:%s%s">' % (LOGOS, logo, style, white, shadow)


BASE_CSS = """
@font-face{font-family:Glancyr;src:url("file://%(font)s")}
*{box-sizing:border-box}
html,body{margin:0;width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{background:#0f1013;font-family:Glancyr,system-ui,sans-serif;color:#fff;position:relative}
.glow{position:absolute;inset:0;background:
  radial-gradient(60%% 70%% at %(gx)s %(gy)s, %(c1)s 0%%, transparent 70%%),
  radial-gradient(45%% 55%% at %(hx)s %(hy)s, %(c2)s 0%%, transparent 70%%);opacity:.75;filter:saturate(120%%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.055) 1px,transparent 1px);
  background-size:%(cell)dpx %(cell)dpx;-webkit-mask-image:radial-gradient(80%% 80%% at 50%% 45%%,#000 30%%,transparent 100%%)}
.vignette{position:absolute;inset:0;background:radial-gradient(120%% 100%% at 50%% 40%%,transparent 55%%,rgba(0,0,0,.55) 100%%)}
.orb{position:absolute;border-radius:50%%;backdrop-filter:blur(10px) saturate(160%%);-webkit-backdrop-filter:blur(10px) saturate(160%%);
  background:linear-gradient(140deg,rgba(255,255,255,.28),rgba(255,255,255,.04) 55%%);border:1px solid rgba(255,255,255,.35);
  box-shadow:inset 0 2px 6px rgba(255,255,255,.35),inset 0 -10px 30px rgba(0,0,0,.25),0 20px 60px rgba(0,0,0,.35)}
.tile{position:absolute;left:50%%;top:%(ty)s;transform:translate(-50%%,-50%%);display:flex;align-items:center;justify-content:center;
  padding:%(pad)dpx %(padx)dpx}
.tile img{display:block;max-height:%(lh)dpx;max-width:%(lw)dpx;position:relative}
.mono{font-size:%(mono)dpx;letter-spacing:.02em;color:#fff;position:relative;line-height:1;text-shadow:0 10px 28px rgba(0,0,0,.45)}
.chips{position:absolute;left:0;right:0;bottom:%(cb)s;display:flex;gap:%(cg)dpx;justify-content:center;flex-wrap:wrap;padding:0 6%%}
.chip{padding:%(cp)dpx %(cpx)dpx;border-radius:999px;font-size:%(cf)dpx;letter-spacing:.08em;text-transform:uppercase;color:#fff;
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.28);backdrop-filter:blur(12px) saturate(160%%);-webkit-backdrop-filter:blur(12px) saturate(160%%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 8px 24px rgba(0,0,0,.25)}
.big{position:absolute;left:8%%;top:50%%;transform:translateY(-50%%);font-size:%(bigf)dpx;line-height:.9;letter-spacing:-.02em;color:rgba(255,255,255,.95)}
.big small{display:block;font-size:.22em;letter-spacing:.2em;text-transform:uppercase;opacity:.7;margin-bottom:.6em}
"""


def page(w, h, brand, chips=(), orbs=(), ty="46%", scale=1.0, big=None, mosaic=None, wlogo=None, invert=False, capture=False):
    logo, mono, c1, c2 = BRANDS[brand]
    s = min(w, h)
    v = dict(font=FONT, w=w, h=h, c1=c1, c2=c2, gx="22%", gy="12%", hx="85%", hy="90%", cell=max(24, s // 14),
             ty=ty, pad=int(s * .07 * scale), padx=int(s * .1 * scale), r=int(s * .06 * scale), s1=int(s * .04), s2=int(s * .1),
             lh=int(s * .2 * scale), lw=int(w * .5 * scale), mono=int(s * .2 * scale), cb="9%", cg=max(6, s // 60),
             cp=max(5, s // 70), cpx=max(10, s // 30), cf=max(10, s // 42), bigf=int(s * .3))
    body = ['<div class="glow"></div><div class="grid"></div><div class="vignette"></div>']
    for (ox, oy, od) in orbs:
        body.append('<div class="orb" style="left:%s;top:%s;width:%dpx;height:%dpx"></div>' % (ox, oy, int(s * od), int(s * od)))
    if big:  # size the word so it fits the width (Glancyr averages ~0.62em per letter)
        size = min(int(s * .3), int(w * .84 / (len(big[1]) * .62)))
        body.append('<div class="big" style="font-size:%dpx"><small>%s</small>%s</div>' % (size, H.escape(big[0]), H.escape(big[1])))
    if mosaic:
        for (b, x, y, sc) in mosaic:
            size = "max-height:%dpx;max-width:%dpx;font-size:%dpx;" % (int(s * .13 * sc), int(s * .36 * sc), int(s * .12 * sc))
            body.append('<div class="tile" style="left:%s;top:%s;padding:0">%s</div>' % (x, y, logo_img(b, size)))
    elif capture:  # Pagecast: a web page (glass browser) becoming Figma layers (glass layer panel)
        glass = ("position:absolute;border-radius:%dpx;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.3);"
                 "backdrop-filter:blur(16px) saturate(170%%);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 30px 60px rgba(0,0,0,.4);" % int(s * .03))
        bar = '<div style="height:%dpx;margin:%dpx %dpx 0;border-radius:6px;background:rgba(255,255,255,%s);width:%s"></div>'
        win = ''.join(bar % (int(s * .022), int(s * .03), int(s * .04), a, wd) for a, wd in
                      ((".55", "55%"), (".25", "80%"), (".25", "70%"), (".18", "86%"), (".18", "60%")))
        dots = ''.join('<span style="display:inline-block;width:%dpx;height:%dpx;border-radius:50%%;margin-right:%dpx;background:%s"></span>'
                       % (int(s * .018), int(s * .018), int(s * .01), c) for c in ("#ff6a3d", "#ffc23d", "#3ddc84"))
        body.append('<div style="%sleft:9%%;top:14%%;width:52%%;height:58%%"><div style="padding:%dpx %dpx">%s</div>%s</div>'
                    % (glass, int(s * .03), int(s * .04), dots, win))
        rows = ''.join('<div style="display:flex;align-items:center;gap:%dpx;margin:%dpx %dpx 0">'
                       '<span style="width:%dpx;height:%dpx;border-radius:4px;border:2px solid rgba(255,255,255,.7)"></span>'
                       '<span style="height:%dpx;border-radius:5px;background:rgba(255,255,255,.3);width:%s"></span></div>'
                       % (int(s * .02), int(s * .028), int(s * .035), int(s * .03), int(s * .03), int(s * .018), wd)
                       for wd in ("60%", "45%", "70%", "50%", "62%"))
        body.append('<div style="%sleft:55%%;top:30%%;width:36%%;height:56%%">'
                    '<div style="margin:%dpx %dpx 0;font-size:%dpx;letter-spacing:.12em;color:rgba(255,255,255,.8)">LAYERS</div>%s</div>'
                    % (glass, int(s * .035), int(s * .035), int(s * .026), rows))
        body.append('<div style="position:absolute;left:47%%;top:44%%;font-size:%dpx;color:#fff;text-shadow:0 4px 20px rgba(0,0,0,.5)">&#8594;</div>' % int(s * .08))
    elif wlogo:
        body.append('<img src="file://%s/%s" style="position:absolute;left:50%%;top:%s;transform:translate(-50%%,-50%%);'
                    'max-width:%d%%;max-height:%dpx;%sfilter:%sdrop-shadow(0 10px 30px rgba(0,0,0,.45))">'
                    % (LOGOS, wlogo, ty, int(72 * scale), int(h * .3 * scale), "", "brightness(0) invert(1) " if invert else ""))
    elif not big:
        body.append('<div class="tile">%s</div>' % logo_img(brand))
    if chips:
        body.append('<div class="chips">%s</div>' % "".join('<span class="chip">%s</span>' % H.escape(c) for c in chips))
    return "<!doctype html><html><head><meta charset='utf-8'><style>%s</style></head><body>%s</body></html>" % (BASE_CSS % v, "".join(body))


ART = [
    # Works card cover for Pagecast (Chrome extension + Figma plugin)
    ("proj-pagecast-card.jpg", 960, 800, dict(brand="pagecast", capture=True, orbs=(("70%", "-12%", .4),))),
    # Homepage gallery: logo panels (white logo, no tile)
    ("gal-wmt-logo.jpg", 820, 1000, dict(brand="wmt", wlogo="wmt-white.png", orbs=(("58%", "-8%", .55), ("-18%", "72%", .45)), scale=1.0)),
    ("gal-netra-logo.jpg", 820, 1000, dict(brand="netra", wlogo="netra.png", invert=True, orbs=(("55%", "-10%", .55), ("-15%", "70%", .45)))),
    ("gal-agorivia-logo.jpg", 820, 1000, dict(brand="agorivia", wlogo="agorivia-white.png", orbs=(("60%", "-8%", .55), ("-15%", "72%", .45)), scale=1.0)),
    # Homepage: selected projects
    ("art-agorivia-1.jpg", 1600, 1200, dict(brand="agorivia", chips=("Figma design", "WordPress", "Elementor"), orbs=(("72%", "8%", .34),), scale=1.3)),
    ("art-agorivia-2.jpg", 1200, 800, dict(brand="agorivia-icon", chips=("UK operations support",), orbs=(("6%", "58%", .4),))),
    ("art-netra-1.jpg", 410, 500, dict(brand="netra", orbs=(("55%", "-10%", .55),), scale=1.15)),
    ("art-netra-2.jpg", 850, 500, dict(brand="netra", chips=("WooCommerce", "Online shop", "IT services"), orbs=(("78%", "5%", .5),))),
    ("art-netra-3.jpg", 410, 500, dict(brand="netra", chips=("Shop in cedis",), orbs=(("-20%", "55%", .6),), scale=1.15)),
    ("art-wmt-1.jpg", 1200, 839, dict(brand="wmt", chips=("Health equity", "Youth-led NGO"), orbs=(("74%", "6%", .4),), scale=1.2)),
    ("art-wmt-2.jpg", 1200, 858, dict(brand="wmt", chips=("Donations", "Projects", "Events"), orbs=(("4%", "50%", .45),), scale=1.2)),
    # Homepage: studio blurb images
    ("art-weekendchef-small.jpg", 400, 320, dict(brand="weekendchef", scale=1.2)),
    ("art-strategicagile.jpg", 1040, 840, dict(brand="strategicagile", chips=("Human-capital consulting",), orbs=(("70%", "-6%", .4),), scale=1.2)),
    # About
    ("art-about-main.jpg", 1200, 796, dict(brand="diginort", orbs=(("82%", "-12%", .45),), mosaic=[
        ("agorivia", "27%", "24%", 1.25), ("netra", "72%", "24%", 1.3), ("weekendchef", "16%", "58%", 1.5),
        ("wmt", "50%", "52%", 1.45), ("feci", "84%", "58%", 1.5), ("releev", "33%", "83%", 1.25), ("strategicagile", "71%", "83%", 1.1)])),
    ("art-collage-1.jpg", 810, 800, dict(brand="feci", orbs=(("62%", "-8%", .5),), scale=1.1)),
    ("art-collage-2.jpg", 1040, 1200, dict(brand="releev", chips=("Health AI",), orbs=(("-15%", "60%", .6),), scale=1.1)),
    ("art-collage-3.jpg", 830, 620, dict(brand="eah", orbs=(("72%", "-10%", .5),), scale=1.1)),
    ("art-collage-4.jpg", 1040, 1400, dict(brand="mawuena", chips=("Nonprofit",), orbs=(("60%", "6%", .55),), scale=1.3)),
    ("art-collage-5.jpg", 830, 720, dict(brand="quickpipe", chips=("Sales AI",), orbs=(("-10%", "40%", .5),), scale=1.1)),
    ("art-process.jpg", 1800, 900, dict(brand="diginort", orbs=(("85%", "-15%", .5), ("5%", "65%", .35)), mosaic=[
        ("creativeclick", "22%", "40%", 1.6), ("eah", "42%", "64%", 1.5), ("geoben", "62%", "38%", 1.5), ("quickpipe", "80%", "62%", 1.5)])),
    ("art-small-1.jpg", 600, 440, dict(brand="geoben", scale=1.2)),
    ("art-small-2.jpg", 600, 440, dict(brand="creativeclick", scale=1.2)),
    ("art-step-discover.jpg", 600, 600, dict(brand="diginort", big=("Step 01", "Discover"), orbs=(("62%", "8%", .42),))),
    ("art-step-design.jpg", 600, 600, dict(brand="creativeclick", big=("Step 02", "Design"), orbs=(("60%", "60%", .45),))),
    ("art-step-build.jpg", 600, 600, dict(brand="netra", big=("Step 03", "Build"), orbs=(("66%", "10%", .4),))),
    ("art-step-launch.jpg", 600, 600, dict(brand="releev", big=("Step 04", "Launch"), orbs=(("58%", "58%", .48),))),
]


def render(name, w, h, opts):
    os.makedirs(WORK, exist_ok=True)
    src = os.path.join(WORK, name.rsplit(".", 1)[0] + ".html")
    open(src, "w", encoding="utf-8").write(page(w, h, **opts))
    png = src[:-5] + ".png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--user-data-dir=" + os.path.join(WORK, ".profile"),
                    "--allow-file-access-from-files", "--window-size=%d,%d" % (w, h), "--virtual-time-budget=4000",
                    "--screenshot=" + png, "file://" + src], check=True, capture_output=True)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", png, "--out", os.path.join(OUT, name)],
                   check=True, capture_output=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    for name, w, h, opts in ART:
        if only and name not in only:
            continue
        render(name, w, h, opts)
        print("art", name, "%dx%d" % (w, h))
