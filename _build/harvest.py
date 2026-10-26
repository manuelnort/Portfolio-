"""Download the photos a project's live site uses (img tags, srcsets, og:image, Elementor CSS backgrounds).

Usage: python3 -I harvest.py <project> <url>   ->  projects/<project>/site-NN.<ext> (skips logos, icons, tiny files)
"""
import html, os, re, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/155 Safari/537.36"}
SKIP = re.compile(r"logo|icon|favicon|emoji|avatar|gravatar|flag|payment|badge|sprite|placeholder|\.svg", re.I)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def candidates(base, page):
    found = []
    found += re.findall(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', page)
    for srcset in re.findall(r'srcset="([^"]+)"', page):
        best = max((p.strip().split(" ") for p in srcset.split(",") if p.strip()),
                   key=lambda p: int(re.sub(r"\D", "", p[1]) or 0) if len(p) > 1 else 0)
        found.append(best[0])
    found += re.findall(r'<img[^>]+(?:data-src|src)="([^"]+)"', page)
    for css in re.findall(r'href="([^"]+/elementor/css/post-\d+\.css[^"]*)"', page):
        try:
            found += re.findall(r'url\("?([^")]+)"?\)', get(urllib.parse.urljoin(base, html.unescape(css))).decode("utf-8", "ignore"))
        except Exception:
            pass
    found += re.findall(r'background-image:\s*url\(&quot;([^&]+)&quot;\)', page)
    found += re.findall(r'background-image:\s*url\([\'"]?([^\'")]+)', page)
    out = []
    for u in found:
        u = urllib.parse.urljoin(base, html.unescape(u))
        if u.startswith("http") and re.search(r"\.(jpe?g|png|webp)(\?|$)", u, re.I) and not SKIP.search(u) and u not in out:
            out.append(u)
    return out


if __name__ == "__main__":
    project, url = sys.argv[1], sys.argv[2]
    dest = os.path.join(HERE, "projects", project)
    os.makedirs(dest, exist_ok=True)
    page = get(url).decode("utf-8", "ignore")
    n = 0
    for u in candidates(url, page):
        # Prefer the full-size upload over a WordPress resized copy (name-300x200.jpg)
        full = re.sub(r"-\d{2,4}x\d{2,4}(\.\w+)$", r"\1", u.split("?")[0])
        for attempt in (full, u):
            try:
                data = get(attempt)
            except Exception:
                continue
            if len(data) < 25000:
                break
            n += 1
            ext = os.path.splitext(urllib.parse.urlparse(attempt).path)[1].lower() or ".jpg"
            open(os.path.join(dest, "site-%02d%s" % (n, ext)), "wb").write(data)
            print("site-%02d%s" % (n, ext), len(data) // 1024, "KB", attempt)
            break
        if n >= 14:
            break
