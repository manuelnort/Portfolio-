import re, sys

PAGES = {"": "index.html", "about/": "about.html", "contact/": "contact.html",
         "works-1/": "works-1.html", "works-2/": "works-2.html", "works-3/": "works-3.html"}

# Answers the Works grids' "Load more" request from a saved response instead of admin-ajax.php
GRID_SHIM = """<script id="static-grid-loadmore">
jQuery.ajaxPrefilter(function (options) {
    if (typeof options.data !== 'string' || !/(^|&)action=evne_load_more_post_grid(&|$)/.test(options.data)) return;
    var paged = (options.data.match(/(^|&)settings%5Bpaged%5D=(\\d+)/) || [])[2] || '1';
    var page = location.pathname.split('/').pop().replace(/\\.html$/, '') || 'index';
    options.url = 'wp-content/static-ajax/' + page + '-paged-' + paged + '.json';
    options.type = 'GET';
    options.data = '';
    options.dataTypes = ['text', 'json'];
});
</script>
"""


def rewrite_urls(h):
    # Asset URLs -> relative paths, query strings dropped (files are saved without them)
    h = re.sub(r"https?:\\/\\/diginort\.local\\/((?:wp-content|wp-includes)\\/[^\"'\s<>)?]+)(?:\?[^\"'\s<>)]*)?",
               lambda m: m.group(1), h)
    h = re.sub(r"https?://diginort\.local/((?:wp-content|wp-includes)/[^\"'\s<>)?,]+)(?:\?ver=[^\"'\s<>),&]*(?:&#038;[^\"'\s<>),]*)?)?",
               lambda m: m.group(1), h)
    # Page links: exported pages -> their .html file, anything else is not part of this export
    h = re.sub(r"(href|action)=\"https?://diginort\.local/([^\"#]*)(#[^\"]*)?\"",
               lambda m: '%s="%s%s"' % (m.group(1), PAGES.get(m.group(2), "#"), (m.group(3) or "") if m.group(2) in PAGES else ""), h)
    return h


def build_page(h):
    # WordPress-only head tags (feeds, REST discovery, oEmbed, RSD, generators)
    h = re.sub(r"<link rel=(['\"])(profile|alternate|https://api\.w\.org/|EditURI|canonical|shortlink)\1[^>]*>\s*", "", h)
    h = re.sub(r"<meta name=(['\"])generator\1[^>]*>\s*", "", h)
    h = re.sub(r"<script type=\"speculationrules\">.*?</script>\s*", "", h, flags=re.S)
    # WooCommerce add-to-cart handler (no WooCommerce on a static page)
    h = re.sub(r"<script type=\"text/javascript\">\s*jQuery\( function\(\$\) \{\s*if \( typeof wc_add_to_cart_params.*?</script>\s*", "", h, flags=re.S)
    h = rewrite_urls(h)
    # Google Fonts over https so it also loads from file:// and https hosts
    h = h.replace("http://fonts.googleapis.com", "https://fonts.googleapis.com")
    if "pxl-load-more" in h:
        h = h.replace('<script id="jquery-migrate-js" src="wp-includes/js/jquery/jquery-migrate.min.js"',
                      GRID_SHIM + '<script id="jquery-migrate-js" src="wp-includes/js/jquery/jquery-migrate.min.js"', 1)
        assert "static-grid-loadmore" in h, "jQuery migrate tag not found for grid shim"
    return h


if __name__ == "__main__":
    src, dest = sys.argv[1], sys.argv[2]
    h = build_page(open(src, encoding="utf-8").read())
    open(dest, "w", encoding="utf-8").write(h)
    left = sorted(set(re.findall(r"https?:(?:\\/|/){2}diginort\.local[^\"'\s<>&]*", h)))
    print(dest.split("/")[-1], "remaining diginort.local refs:", *left, sep="\n  ")
