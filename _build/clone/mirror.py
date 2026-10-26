import re, sys, os, urllib.request, urllib.parse

HOST = "http://diginort.local/"
SRC_HTML, OUT, EXTRA = sys.argv[1], sys.argv[2], sys.argv[3]

html = open(SRC_HTML, encoding="utf-8").read()
unesc = html.replace("\\/", "/")

url_re = re.compile(r"https?://diginort\.local/[^\"'\s<>)]+")
queue = set(u.rstrip(",") for u in url_re.findall(unesc))
queue |= set(l.strip() for l in open(EXTRA) if l.strip())

ASSET_EXT = (".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg",
             ".woff", ".woff2", ".ttf", ".otf", ".eot", ".ico", ".mp4", ".webm", ".json")

def local_path(u):
    p = urllib.parse.urlparse(u).path.lstrip("/")
    return os.path.join(OUT, urllib.parse.unquote(p))

def is_asset(u):
    return urllib.parse.urlparse(u).path.lower().endswith(ASSET_EXT)

done, failed = set(), []
todo = [u for u in queue if is_asset(u)]
while todo:
    u = todo.pop()
    key = u.split("?")[0].split("#")[0]
    if key in done:
        continue
    done.add(key)
    dest = local_path(key)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        data = urllib.request.urlopen(u.replace("&#038;", "&").replace("&amp;", "&"), timeout=30).read()
    except Exception as e:
        failed.append((u, str(e)))
        continue
    open(dest, "wb").write(data)
    if key.endswith(".css"):
        css = data.decode("utf-8", "ignore")
        for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", css):
            if ref.startswith("data:") or ref.startswith("#"):
                continue
            absu = urllib.parse.urljoin(u, ref)
            if absu.startswith(HOST) and is_asset(absu):
                todo.append(absu)

print("downloaded", len(done) - len(failed))
for f in failed:
    print("FAILED", *f)
