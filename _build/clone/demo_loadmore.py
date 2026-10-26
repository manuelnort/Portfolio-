"""Save the demo's "Load more" responses (reference for image sizes only)."""
import html, json, re, sys, urllib.parse, urllib.request
sys.path.insert(0, ".")
from jqparam import jquery_param

for page in sys.argv[1:]:
    src = open("demo-%s.html" % page, encoding="utf-8", errors="ignore").read()
    loadmore = json.loads(html.unescape(re.search(r'data-loadmore="([^"]*)"', src).group(1)))
    nonce = re.search(r'"wpnonce":"([^"]*)"', src).group(1)
    ajax = re.search(r'"ajax_url":"([^"]+)"', src).group(1).replace("\\/", "/")
    ajax = urllib.parse.urljoin("https://evne.bravisthemes.com/", ajax)
    loadmore["paged"] = int(re.search(r'data-start-page="(\d+)"', src).group(1)) + 1
    body = jquery_param({"action": "evne_load_more_post_grid", "settings": loadmore,
                         "handler_click": "loadmore", "wpnonce": nonce}).encode()
    req = urllib.request.Request(ajax, body, {"User-Agent": "Mozilla/5.0"})
    res = json.loads(urllib.request.urlopen(req, timeout=30).read())
    assert res.get("status") is True, (page, str(res)[:200])
    open("demo-ajax-%s.html" % page, "w", encoding="utf-8").write(res["data"]["html"])
    print(page, "items:", res["data"]["html"].count('class="pxl-grid-item'),
          "sizes:", re.findall(r'width="(\d+)" height="(\d+)"', res["data"]["html"]))
