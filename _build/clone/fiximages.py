"""Give the export's zero-size images (width="0" height="0") the size and crop the theme intends.

The old Diginort pages were rendered before WordPress had generated the theme's custom crops, so
it fell back to the full image with 0x0 dimensions. For every such image this takes the size the
theme uses for the same widget slot (read from the theme demo, which shares Elementor element IDs
and the same original files), then points the image at that crop:
  1. the crop WordPress has since generated in the Local site's uploads, or
  2. the demo's crop, but only when the demo's original file is byte-identical to ours, or
  3. a centre crop made here with sips (WordPress's own hard-crop method), saved as JPEG.
"""
import json, os, re, subprocess, sys, urllib.request

OUT = "/Users/manuelnort/Desktop/ego/diginort"
LOCAL_UPLOADS = os.path.expanduser("~/Local Sites/diginort/app/public/wp-content/uploads")
DEMO_UPLOADS = "https://evne.bravisthemes.com/wp-content/uploads"
WIDGET = re.compile(r'data-id="([0-9a-f]+)"[^>]*data-element_type="widget"')
NEXT_ELEMENT = re.compile(r'data-id="[0-9a-f]+"[^>]*data-element_type=')


def attr(tag, name):
    m = re.search(r'\s%s="([^"]*)"' % name, tag)
    return m.group(1) if m else None


def widget_images(h):
    """[(widget id, index in widget, start, end)] for every <img> inside a widget."""
    out = []
    for m in WIDGET.finditer(h):
        nxt = NEXT_ELEMENT.search(h, m.end())
        end = nxt.start() if nxt else len(h)
        for k, img in enumerate(re.finditer(r"<img[^>]*>", h[m.end():end])):
            out.append((m.group(1), k, m.end() + img.start(), m.end() + img.end()))
    return out


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()


_same_original = {}
def demo_original_matches(rel):
    if rel not in _same_original:
        try:
            _same_original[rel] = fetch("%s/%s" % (DEMO_UPLOADS, rel)) == open(os.path.join(LOCAL_UPLOADS, rel), "rb").read()
        except Exception:
            _same_original[rel] = False
    return _same_original[rel]


def provide_crop(rel, w, h):
    """Make uploads/<crop> exist in the export; return (relative crop path, how)."""
    d, base = os.path.split(rel)
    stem, ext = os.path.splitext(base)
    crop = "%s/%s-%sx%s%s" % (d, stem, w, h, ext)
    dest = os.path.join(OUT, "wp-content/uploads", crop)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    local = os.path.join(LOCAL_UPLOADS, crop)
    if os.path.exists(local):
        open(dest, "wb").write(open(local, "rb").read())
        return crop, "wordpress crop"
    if demo_original_matches(rel):
        try:
            open(dest, "wb").write(fetch("%s/%s" % (DEMO_UPLOADS, crop)))
            return crop, "demo crop (identical original)"
        except Exception:
            pass
    crop = "%s/%s-%sx%s.jpg" % (d, stem, w, h)
    dest = os.path.join(OUT, "wp-content/uploads", crop)
    src = os.path.join(LOCAL_UPLOADS, rel)
    ow, oh = (int(x) for x in re.findall(r"pixel(?:Width|Height): (\d+)", subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", src], capture_output=True, text=True).stdout))
    scale = max(int(w) / ow, int(h) / oh)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92",
                    "-z", str(round(oh * scale)), str(round(ow * scale)),
                    "--cropToHeightWidth", str(h), str(w), src, "--out", dest], check=True, capture_output=True)
    return crop, "centre crop made with sips"


def fix_tag(tag, ref_tag, log):
    w, h = attr(ref_tag, "width"), attr(ref_tag, "height")
    src = attr(tag, "src")
    rel = src.split("wp-content/uploads/", 1)[1]
    if os.path.basename(attr(ref_tag, "src")) == os.path.basename(rel):
        new_src, how = src, "size only (already the right file)"
    else:
        crop, how = provide_crop(rel, w, h)
        new_src = src.split("wp-content/uploads/", 1)[0] + "wp-content/uploads/" + crop
    log.append("%-40s -> %sx%s  %s" % (os.path.basename(rel)[:40], w, h, how))
    tag = tag.replace('src="%s"' % src, 'src="%s"' % new_src, 1)
    return tag.replace('width="0"', 'width="%s"' % w, 1).replace('height="0"', 'height="%s"' % h, 1)


def fix_page(path, ref_html):
    h = open(path, encoding="utf-8").read()
    ref = {(wid, k): ref_html[s:e] for wid, k, s, e in widget_images(ref_html)}
    log, parts, pos = [], [], 0
    for wid, k, s, e in widget_images(h):
        tag = h[s:e]
        if attr(tag, "width") == "0":
            parts += [h[pos:s], fix_tag(tag, ref[(wid, k)], log)]
            pos = e
    open(path, "w", encoding="utf-8").write("".join(parts) + h[pos:])
    return log


def fix_fragment(path, ref_html):
    res = json.load(open(path, encoding="utf-8"))
    tags = re.findall(r"<img[^>]*>", res["data"]["html"])
    refs = re.findall(r"<img[^>]*>", ref_html)
    assert len(tags) == len(refs), path
    log = []
    for tag, ref in zip(tags, refs):
        if attr(tag, "width") == "0":
            res["data"]["html"] = res["data"]["html"].replace(tag, fix_tag(tag, ref, log), 1)
    json.dump(res, open(path, "w", encoding="utf-8"))
    return log


if __name__ == "__main__":
    total = 0
    for page in ["index", "about", "works-1", "works-2", "works-3"]:
        log = fix_page(os.path.join(OUT, page + ".html"), open("demo-%s.html" % page, encoding="utf-8", errors="ignore").read())
        if page.startswith("works"):
            log += fix_fragment(os.path.join(OUT, "wp-content/static-ajax/%s-paged-2.json" % page),
                                open("demo-ajax-%s.html" % page, encoding="utf-8").read())
        print("== %s: %d images fixed" % (page, len(log)), *log, sep="\n  ")
        total += len(log)
    print("total fixed:", total)
