import html, json, os, re, sys, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import rewrite_urls
from jqparam import jquery_param

OUT = sys.argv[1]


for page in sys.argv[2:]:
    src = open(page + ".html", encoding="utf-8").read()
    loadmore = json.loads(html.unescape(re.search(r'data-loadmore="([^"]*)"', src).group(1)))
    start = int(re.search(r'data-start-page="(\d+)"', src).group(1))
    nonce = re.search(r'"wpnonce":"([^"]*)"', src).group(1)
    for paged in range(start + 1, int(loadmore["maxPages"]) + 1):
        loadmore["paged"] = paged
        body = jquery_param({"action": "evne_load_more_post_grid", "settings": loadmore,
                             "handler_click": "loadmore", "wpnonce": nonce}).encode()
        res = json.loads(urllib.request.urlopen("http://diginort.local/wp-admin/admin-ajax.php", body, timeout=30).read())
        assert res.get("status") is True, (page, paged, str(res)[:300])
        # Raw copy so mirror.py can fetch the images the loaded items use
        open("ajax-%s-paged-%d.html" % (page, paged), "w", encoding="utf-8").write(res["data"]["html"])
        res["data"]["html"] = rewrite_urls(res["data"]["html"])
        dest = os.path.join(OUT, "wp-content/static-ajax/%s-paged-%d.json" % (page, paged))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        json.dump(res, open(dest, "w", encoding="utf-8"))
        items = res["data"]["html"].count('class="pxl-grid-item')
        print(page, "paged", paged, "->", items, "items, paged/max:", res["data"].get("paged"), res["data"].get("max"))
