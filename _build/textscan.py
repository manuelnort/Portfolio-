"""List emoji and dashes in the visible text (and titles/alt text) of the built pages.
Usage: python3 -I textscan.py <site dir>"""
import glob, html, os, re, sys
from html.parser import HTMLParser

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍←-⇿]")
DASH = re.compile(r"[‐-―−]|(?<=\s)-(?=\s)|\w-\w")

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip, self.out = 0, []
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        for k, v in attrs:
            if k in ("alt", "title", "aria-label", "placeholder") and v:
                self.out.append(v)
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip -= 1
    def handle_data(self, d):
        if not self.skip and d.strip():
            self.out.append(d.strip())

for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.html"))):
    t = Text(); t.feed(open(f, encoding="utf-8").read())
    seen = set()
    for s in t.out:
        if (EMOJI.search(s) or DASH.search(s)) and s not in seen:
            seen.add(s)
            print(os.path.basename(f), "|", s[:140])
