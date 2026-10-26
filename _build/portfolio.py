"""Turn the static clone of the theme site (~/Desktop/ego/diginort) into Emmanuel Nortey's portfolio.

Always rebuilds ~/Desktop/ego/portfolio from ~/Desktop/ego/diginort, then applies every edit below.
Run it from portfolio/_build (python3 -I portfolio.py); the site's git repository and _build are left in place.
Each replacement states how many times the original text must appear, so a template change
can't silently skip an edit.
"""
import glob, hashlib, os, re, shutil, sys

SRC = "/Users/manuelnort/Desktop/ego/diginort"
OUT = "/Users/manuelnort/Desktop/ego/portfolio"
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "portimg")   # prepared images
IMG_URL = "wp-content/uploads/portfolio/"

EMAIL, PHONE, PHONE_TEL = "enortey96@gmail.com", "+233 24 633 7881", "+233246337881"
# The CV visitors can download (made by cv/make_cv.py, copied in with the other prepared images)
CV_FILE = "Emmanuel-Nortey-CV.pdf"
WHATSAPP = "https://wa.me/233246337881"
NEXT = ' target="_blank" rel="noopener"'

PROJECTS = {  # live sites, in the order they appear in the Works grid
    "agorivia": ("Agorivia", "https://agorivia.co/"),
    "eah": ("Dr. Emele Arthur-Hayford", "https://emelearthurhayford.com/"),
    "netra": ("Netra Technologies GH", "https://netratechnologiesgh.com/"),
    "weekendchef": ("The Weekend Chef", "https://weekendchefgh.com/"),
    "strategicagile": ("Strategic &amp; Agile", "https://strategicandagile.com/"),
    "wmt": ("World Movers Team", "https://worldmoversteam.org/"),
    "mawuena": ("Mawuena Datsa Foundation", "https://mawuenadatsafoundation.org/"),
    "creativeclick": ("Creative Click Multimedia", "https://www.creativeclickmultimedia.com/"),
}


class Page:
    def __init__(self, name):
        self.name, self.path = name, os.path.join(OUT, name)
        self.h = open(self.path, encoding="utf-8").read()

    def sub(self, old, new, count=1):
        found = self.h.count(old)
        if count is not None and found != count:  # count=None: any number, including none
            sys.exit("%s: expected %d of %r, found %d" % (self.name, count, old[:70], found))
        self.h = self.h.replace(old, new)

    def resub(self, pattern, new, count=1, flags=re.S):
        self.h, n = re.subn(pattern, new, self.h, flags=flags)
        if count is not None and n != count:
            sys.exit("%s: expected %d matches of %r, got %d" % (self.name, count, pattern[:70], n))

    def element_span(self, eid):
        """(start, end) of the element with data-id=eid, balanced on its own tag name."""
        i = self.h.find('data-id="%s"' % eid)
        if i < 0:
            sys.exit("%s: element %s not found" % (self.name, eid))
        return self.balanced(self.h.rfind("<", 0, i))

    def balanced(self, start):
        """(start, end) of the element whose opening tag begins at start."""
        tag = re.match(r"<(\w+)", self.h[start:]).group(1)
        depth, pos = 0, start
        for m in re.compile(r"<(/?)%s\b[^>]*>" % tag).finditer(self.h, start):
            depth += -1 if m.group(1) else 1
            if depth == 0:
                return start, m.end()
        sys.exit("%s: unbalanced <%s> at %d" % (self.name, tag, start))

    def within(self, eid, old, new, count=1):
        s, e = self.element_span(eid)
        part = self.h[s:e]
        found = part.count(old)
        if (count is not None and found != count) or not found:
            sys.exit("%s/%s: expected %s of %r, found %d" % (self.name, eid, count, old[:70], found))
        self.h = self.h[:s] + part.replace(old, new) + self.h[e:]

    def remove(self, eid):
        s, e = self.element_span(eid)
        self.h = self.h[:s] + self.h[e:]

    def image(self, eid, index, file, w, h, alt):
        """Point the index-th <img> inside element eid at a prepared portfolio image."""
        s, e = self.element_span(eid)
        part = self.h[s:e]
        tags = re.findall(r"<img[^>]*>", part)
        tag = tags[index]
        new = re.sub(r'\ssrc="[^"]*"', ' src="%s%s"' % (IMG_URL, file), tag)
        new = re.sub(r'\swidth="[^"]*"', ' width="%d"' % w, new)
        new = re.sub(r'\sheight="[^"]*"', ' height="%d"' % h, new)
        new = re.sub(r'\s(srcset|sizes)="[^"]*"', "", new)
        new = re.sub(r'\salt="[^"]*"', ' alt="%s"' % alt, new)
        new = re.sub(r'\stitle="[^"]*"', ' title="%s"' % alt, new)
        self.h = self.h[:s] + part.replace(tag, new, 1) + self.h[e:]

    def save(self):
        open(self.path, "w", encoding="utf-8").write(self.h)


def cv_button(style="ghost", label="Download CV"):
    return ('<a class="dn-btn dn-btn--%s dn-btn--cv" href="%s%s" download="%s">%s<span class="dn-btn__icon" aria-hidden="true">&#8595;</span></a>'
            % (style, IMG_URL, CV_FILE, CV_FILE, label))


def dock(page):
    """The menu that floats at the bottom of the screen once you scroll down (shown and hidden by portfolio.js)."""
    links = "".join('<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href == page else "", label)
                    for href, label in FOOTER_PAGES)
    return ('<nav class="dn-dock" aria-label="Main">%s<a class="dn-dock__cv" href="%s%s" download="%s">CV'
            '<span aria-hidden="true">&#8595;</span></a></nav>\n' % (links, IMG_URL, CV_FILE, CV_FILE))


FOOTER_PAGES = [("index.html", "Home"), ("about.html", "About"), ("works-1.html", "Work"), ("contact.html", "Contact")]


def footer_section(page):
    """The last thing on every page: who I am and how to reach me, Accra's time (as in the hero), then the
    tagline the homepage opens with, moving across the page, and a way back to the top."""
    links = "".join('<li><a href="%s"%s>%s</a></li>' % (href, ' aria-current="page"' if href == page else "", label)
                    for href, label in FOOTER_PAGES)
    words = ('<span>Nort Just Design.</span><i aria-hidden="true"></i>'
             '<span class="dn-foot__accent">Nort Just Code.</span><i aria-hidden="true"></i>')
    return """<section class="dn-foot">
  <div class="dn-foot__top">
    <div class="dn-foot__brand">
      <a class="dn-foot__name" href="index.html">Emmanuel Nortey<span>.</span></a>
      <p>Web and WordPress developer in Accra, Ghana. I design in Figma, then build.</p>
      <span class="dn-pill"><i></i>Taking on new projects</span>
      <div class="dn-foot__cv">%(cv)s</div>
    </div>
    <nav class="dn-foot__col" aria-label="Pages"><h3>Pages</h3><ul>%(links)s</ul></nav>
    <div class="dn-foot__col"><h3>Say hello</h3><ul>
      <li><a href="mailto:%(email)s">%(email)s</a></li>
      <li><a href="%(wa)s"%(next)s>WhatsApp %(phone)s</a></li>
    </ul></div>
    <div class="dn-foot__col"><h3>Right now in Accra</h3>
      <p class="dn-foot__clock"><b data-clock>00:00:00</b> GMT</p>
      <p class="dn-foot__coords">05.60&deg; N, 00.19&deg; W</p>
    </div>
  </div>
  <div class="dn-foot__sign" aria-hidden="true"><div class="dn-foot__track">%(words)s%(words)s%(words)s%(words)s</div></div>
  <div class="dn-foot__base">
    <p>&copy; 2026 Emmanuel Nortey</p>
    <p>Designed in Figma, built in Accra</p>
    <a class="dn-btn dn-btn--ghost dn-foot__top-link" href="#">Back to top<span aria-hidden="true">&#8593;</span></a>
  </div>
</section>
""" % {"links": links, "email": EMAIL, "wa": WHATSAPP, "next": NEXT, "phone": PHONE, "words": words, "cv": cv_button()}


def global_edits(p):
    """Header, side panel, footer and menus shared by every page."""
    for href in ("works-2.html", "works-3.html", "https://evne.bravisthemes.com/portfolio/typeface-texture/"):
        p.resub(r'<li (?:id="menu-item-\d+" )?class="menu-item[^"]*"><a href="%s"><span[^>]*>.*?</span></a></li>\s*' % re.escape(href), "", None)
    p.resub(r"(<span(?: class=\"pxl-menu-item-text\")?>)Home 1", r"\1Home", None)
    p.resub(r"(<span(?: class=\"pxl-menu-item-text\")?>)Works 1", r"\1Work", None)   # "Work", as in the floating menu

    # Side panel: contact details and links
    p.sub("mailto:hello@evne.agency", "mailto:" + EMAIL, None)
    p.sub("hello@evne.agency", EMAIL, None)
    p.sub("tel:+619807523789", "tel:" + PHONE_TEL, None)
    p.sub("61 980 752 3789", PHONE, None)
    p.resub(r'<a class="" href="#">(\s*<span class="pxl-link--text" data-link-hover-scale =")Instagram(">)Instagram(</span>)',
            r'<a class="" href="%s"%s>\1WhatsApp\2WhatsApp\3' % (WHATSAPP, NEXT), None)
    p.resub(r'<a class="" href="#">(\s*<span class="pxl-link--text" data-link-hover-scale =")Behance(">)Behance(</span>)',
            r'<a class="" href="mailto:%s">\1Email\2Email\3' % EMAIL, None)

    # Footer
    p.sub("Usefull Links", "Useful links", None)
    p.resub(r'<a class="" href="#">(\s*<span class="pxl-link--text" data-link-hover-scale =")The agency(">)The agency(</span>)',
            r'<a class="" href="about.html">\1About me\2About me\3', None)
    p.resub(r'<a class="" href="#">(\s*<span class="pxl-link--text" data-link-hover-scale =")Awards won(">)Awards won(</span>)',
            r'<a class="" href="works-1.html">\1My work\2My work\3', None)
    p.resub(r'<a class="" href="#">(\s*<span class="pxl-link--text" data-link-hover-scale =")Contact(">)Contact(</span>)',
            r'<a class="" href="contact.html">\1Contact\2Contact\3', None)
    p.sub("Creative design agency", "Web &amp; WordPress development", None)
    p.resub(r"<p>©\s*<span></span>\s*<a href=\"#\">Evne</a> Creative Agency</p>",
            '<p>© 2026 <a href="index.html">Emmanuel Nortey</a></p>', None)
    p.sub('<p>Designed by <a href="https://themeforest.net/user/bravis-themes/portfolio">Bravis-Themes</a></p>',
          "<p>Designed &amp; built by Emmanuel Nortey</p>", None)

    # Portfolio styles (project cards, liquid-glass details) load after the theme's
    # ?v= changes with the file's content, so browsers fetch the new version after every edit
    version = hashlib.md5(open(os.path.join(HERE, "assets", "portfolio.css"), "rb").read()).hexdigest()[:8]
    p.sub("</head>", '<link rel="stylesheet" href="%sportfolio.css?v=%s">\n</head>' % (IMG_URL, version), 1)
    # The hero's backdrop (near-black, coral and cyan light, box grid) runs behind every page
    # (styled in portfolio.css, moved by portfolio.js)
    p.resub(r"(<body[^>]*>)", r'\1\n<div class="dn-backdrop" aria-hidden="true"><span class="dn-backdrop__glow dn-backdrop__glow--warm"></span>'
            r'<span class="dn-backdrop__glow dn-backdrop__glow--cool"></span></div>\n<div class="dn-grid" aria-hidden="true"><i></i></div>', 1)
    # Portfolio script runs after the theme's (it uses the theme's GSAP)
    js_version = hashlib.md5(open(os.path.join(HERE, "assets", "portfolio.js"), "rb").read()).hexdigest()[:8]
    p.sub("</body>", '<script src="%sportfolio.js?v=%s"></script>\n</body>' % (IMG_URL, js_version), 1)

    # Branding is Emmanuel's name only: name wordmark in the header, EN monogram for the small mark and icons
    p.sub('width="2560" height="533" src="wp-content/uploads/2025/02/digiKnort-white-1-scaled-e1757934440413.png"',
          'width="2400" height="500" src="%sname-logo-white.png"' % IMG_URL, None)
    p.sub('width="2560" height="520" src="wp-content/uploads/2025/02/digiKnort-logo-Recovered-1-scaled-e1757934504314.png"',
          'width="2400" height="500" src="%sname-logo-dark.png"' % IMG_URL, None)
    for v in ("white", "dark"):
        p.sub('name-logo-%s.png" class="attachment-full" alt=""' % v, 'name-logo-%s.png" class="attachment-full" alt="Emmanuel Nortey"' % v, None)
    for size in ("32x32", "180x180", "192x192", "270x270"):
        p.sub("wp-content/uploads/2025/09/cropped-Digi-logo-1-%s.png" % size, "%sen-icon-%s.png" % (IMG_URL, size.split("x")[0]), None)
    p.sub('title="Diginort"', 'title="Emmanuel Nortey"', None)
    p.sub('alt="Diginort"', 'alt="Emmanuel Nortey"', None)
    p.sub("wp-content/uploads/2025/03/4-1.png", IMG_URL + "en-mark.png", None)
    p.sub('<img decoding="async" src="wp-content/uploads/2025/02/logo.png" class="attachment-full" alt="" />',
          '<img decoding="async" src="%sen-mark.png" class="attachment-full" width="32" height="32" style="width:32px;height:auto" alt="Emmanuel Nortey" />' % IMG_URL, 1)

    # Old local-site addresses in the page settings (nothing on the static site calls them)
    p.resub(r"http:(?:\\?/){2}diginort\.local(?:\\?/)[^\"&]*", "", None)
    p.resub(r'"title":"([^"]*?)Diginort[^"]*"', r'"title":"\1Emmanuel%20Nortey"', None)

    p.sub("Do you want to start your project now?", "Got a project in mind?", None)

    # Contact Form 7: no page uses its form now (both contact forms post to FormSubmit instead), so its
    # scripts and styles go; left in, they ask a WordPress server that isn't there for a form schema
    p.resub(r'<script id="swv-js" src="[^"]*"></script>\s*', "", None)
    p.resub(r'<script id="contact-form-7-js-before">.*?</script>\s*', "", None)
    p.resub(r'<script id="contact-form-7-js" src="[^"]*"></script>\s*', "", None)
    p.resub(r"<link rel='stylesheet' id='contact-form-7-css'[^>]*>\s*", "", None)

    # Image tooltips that are only theme file names
    p.resub(r' title="(?:Untitled-1|icon\d?-home-?1)"', "", None)
    p.resub(r' alt="(?:Untitled-1|icon\d?-home-?1)"', ' alt=""', None)
    p.sub('placeholder="your e-mail"', 'placeholder="your email"', None)

    # Theme demo links that remain anywhere
    p.sub("https://evne.bravisthemes.com/works-1/", "works-1.html", None)
    p.sub('href="https://evne.bravisthemes.com/"', 'href="index.html"', None)

    # Last of all, the theme's footer gives way to one that closes the story (see footer_section)
    s, e = p.element_span("ffd882a")
    p.h = p.h[:s] + footer_section(p.name) + p.h[e:]
    # Phone menu button: a real button styled like the site's buttons, under its own id so the theme's
    # click code (bound to #pxl-nav-mobile) no longer runs; portfolio.js opens and closes the menu
    assert p.h.count('<div id="pxl-nav-mobile">') == 1
    s, e = p.balanced(p.h.index('<div id="pxl-nav-mobile">'))
    p.h = p.h[:s] + ('<div class="dn-menu-slot"><button type="button" class="dn-menu-btn" aria-controls="dn-mobile-menu" '
                     'aria-expanded="false" aria-label="Open menu"><span class="dn-menu-btn__label" aria-hidden="true">Menu</span>'
                     '<span class="dn-menu-btn__icon" aria-hidden="true"><i></i><i></i><i></i></span></button></div>') + p.h[e:]
    p.sub('<div class="pxl-header-menu">', '<div class="pxl-header-menu" id="dn-mobile-menu" role="dialog" aria-label="Menu">', 1)
    p.sub('<div class="pxl-menu-close pxl-hide-xl pxl-close"></div>',
          '<button type="button" class="pxl-menu-close pxl-hide-xl pxl-close" aria-label="Close menu"></button>', 1)

    # Desktop menu button: the same "Menu" button as on phones, in place of the theme's anchor button (whose
    # script left the page locked when the panel was closed with the button); portfolio.js opens the side panel
    # (twice: the header and its sticky copy that appears on scroll)
    anchor = '<div class="pxl-anchor-button pxl-cursor--cta type-default style-1  " data-target=".pxl-hidden-template-1423"'
    assert p.h.count(anchor) == 2, p.h.count(anchor)
    while anchor in p.h:
        s, e = p.balanced(p.h.index(anchor))
        p.h = p.h[:s] + ('<button type="button" class="dn-menu-btn dn-menu-btn--desk" aria-controls="dn-side-panel" aria-expanded="false" '
                         'aria-label="Open menu"><span class="dn-menu-btn__label" aria-hidden="true">Menu</span>'
                         '<span class="dn-menu-btn__icon" aria-hidden="true"><i></i><i></i><i></i></span></button>') + p.h[e:]
    p.sub('<div class="pxl-hidden-panel-popup pxl-hidden-template-1423 pxl-pos-top">',
          '<div class="pxl-hidden-panel-popup pxl-hidden-template-1423 pxl-pos-top" id="dn-side-panel" role="dialog" aria-label="Menu">', 1)

    # Phone menu: under the links, the two things people come for and a way to write
    start = p.h.index('<div class="pxl-header-menu-scroll">')
    s, e = p.balanced(start)
    close = p.h.rindex("</div>", s, e)
    p.h = p.h[:close] + ('<div class="dn-menu-extra"><a class="dn-btn dn-btn--light" href="contact.html">Start a project'
                         '<span class="dn-btn__icon" aria-hidden="true">&#8594;</span></a>%s'
                         '<a class="dn-menu-extra__mail" href="mailto:%s">%s</a></div>' % (cv_button(), EMAIL, EMAIL)) + p.h[close:]
    # the menu goes in before the portfolio script, which looks for it when it runs
    p.sub('<script src="%sportfolio.js' % IMG_URL, dock(p.name) + '<script src="%sportfolio.js' % IMG_URL, 1)


# Homepage galleries: (inner section it replaces, project, chips on the cover). Images come from art.py (logo
# panel) and projects.py (cover + photos); widths match the slots, all 500px tall.
HOME_GALLERIES = [
    ("cd850aa", "agorivia", ["WordPress", "Elementor", "Figma design"]),
    ("9cc3e24", "netra", ["WooCommerce", "Online shop", "IT services"]),
    ("ca62477", "wmt", ["Health equity", "Youth NGO", "WordPress"]),
]
GALLERY_ITEMS = [("logo", 410), ("2", 850), ("3", 410), ("4", 650), ("5", 410)]


def gallery_section(template, key, chips):
    """The Netra gallery section, refilled with this project's five images."""
    name, url = PROJECTS[key]
    items = []
    for i, (suffix, width) in enumerate(GALLERY_ITEMS):
        overlay = ""
        if i == 1:
            overlay = '<span class="dn-chips">%s</span>' % "".join('<span class="dn-chip">%s</span>' % c for c in chips)
        items.append('<div class="item-image item"><a class="image-link" href="%s"%s>'
                     '<img loading="lazy" decoding="async" src="%sgal-%s-%s.jpg" width="%d" height="500" alt="%s" />%s</a></div>'
                     % (url, NEXT, IMG_URL, key, suffix, width, name, overlay))
    m = re.search(r'<div class="pxl-image-container scrolling-wrapper">', template)
    probe = Page.__new__(Page)
    probe.name, probe.h = "gallery template", template
    s, e = probe.balanced(m.start())
    section = template[:s] + m.group(0) + "".join(items) + "</div>" + template[e:]
    section = section.replace('class="pxl-image-custom2 animate-horizontal-scroll"', 'class="pxl-image-custom2 animate-horizontal-scroll dn-gallery"')
    # Own data-ids so a later lookup of the Netra section can't land on a clone (styling uses the classes)
    section = section.replace('data-id="9cc3e24"', 'data-id="gallery-%s"' % key, 1)
    section = section.replace('data-id="8526755"', 'data-id="gallery-%s-images"' % key, 1)
    return re.sub(r'id="pxl_animate_image-8526755-\d+"', 'id="pxl_animate_image-8526755-%s"' % key, section)


def home():
    p = Page("index.html")
    global_edits(p)
    p.sub("<title>Diginort &#8211; Crafting Digital Experiences That Last</title>",
          "<title>Emmanuel Nortey | Web &amp; WordPress Developer</title>")

    # Intro under the hero
    p.sub("We are a creative agency and we strike the perfect balance between creativity and business results.",
          "Most of my sites run on WordPress, though I code some from scratch when WordPress would only get in the way. Either way it starts in Figma, so you see it before I build it.")

    # Clients and skills strips
    p.sub("We collaborate with:", "What I work with:")
    for old, new in [("UI/UX Design", "WordPress"), ("Logo Design", "WooCommerce"), ("Graphic Design", "Elementor"),
                     ("Web Development", "Web Development"), ("Web Design", "Chrome Extensions")]:
        p.within("b707ca5", '<div class="pxl-item--text pxl-empty">%s</div>' % old,
                 '<div class="pxl-item--text pxl-empty">%s</div>' % new)
    for old, new in [("User Experience", "JavaScript"), ("Development", "HTML &amp; CSS"), ("Illustration", "Next.js"),
                     ("Photography", "Figma"), ("Comunications", "IT Support"), ("Design", "Maintenance")]:
        p.within("f916afa", '<div class="pxl-item--text pxl-empty">%s</div>' % old,
                 '<div class="pxl-item--text pxl-empty">%s</div>' % new)

    # What I offer (the four cards)
    for old_t, old_d, new_t, new_d in [
        ("Disruptive creativity",
         "We specialize in breaking the mold and generating unique concepts that stand out in any industry, helping our brands stand out in a saturated market",
         "WordPress development",
         "WordPress and Elementor sites you can update yourself, without calling me every time a price changes."),
        ("Data-driven strategy",
         "Our creative is always backed by in-depth data and trend analysis, ensuring each campaign is designed to deliver tangible results.",
         "Web development",
         "When WordPress isn’t the right fit, I write it in HTML, CSS, JavaScript or Next.js. And yes, it works on phones."),
        ("Multidisciplinary team",
         "We have a diverse team of design, marketing and development experts who collaborate to deliver end-to-end solutions, from initial idea to final execution.",
         "Shops &amp; payments",
         "WooCommerce shops that take card and mobile money through Paystack. Donation pages and enquiry forms too."),
        ("Customized approach",
         "Each client is unique, which is why we tailor our strategies and processes to create campaigns that meet the specific needs and objectives of each brand.",
         "Extensions &amp; tools",
         "Chrome extensions and Figma plugins. My own, Pagecast, copies any website into Figma as layers you can edit."),
    ]:
        p.within("fb99299", old_t, new_t)
        p.within("fb99299", old_d, new_d)

    # Selected projects
    p.sub("At our creative agency, we believe the best way to showcase our expertise is through the work we’ve done.",
          "A few of the websites I’ve built for clients in Ghana and the UK.")
    for title_id, desc_id, btn_id, old_t, old_d, key, new_d in [
        ("0a61178", "4da8ef6", "56b05bb", "Brand Identity Campaign",
         "We crafted a sophisticated and memorable visual identity for a luxury brand, positioning it as a leader in its industry.",
         "agorivia",
         "Built in WordPress and Elementor, from my own Figma design, for a UK operations-support business serving clinics, therapists and founders."),
        ("4e9c084", "a5849a7", "533c9ab", "Multichannel Advertising Strategy",
         "We developed an omnichannel advertising campaign that boosted brand awareness for a global company, generating a 50% increase in conversions.",
         "netra",
         "A WordPress and WooCommerce site where customers browse IT services and buy products online in cedis."),
        ("9fe4f3e", "2af9b40", "f27a2e4", "Digital Transformation for Retail",
         "We designed and developed an interactive digital platform that increased sales by 30% in just six months for an international retail brand.",
         "wmt",
         "A WordPress site for an NGO run by young people for health equity, with projects, partners, events, donations and a newsletter."),
    ]:
        name, url = PROJECTS[key]
        p.within(title_id, old_t, name)
        p.within(title_id, ' data-wplink-url-error="true"', "", None)
        p.resub(r'(data-id="%s".*?<a href=")[^"]*("[^>]*)>' % title_id, r"\g<1>%s\2%s>" % (url, NEXT), 1)
        p.within(desc_id, old_d, new_d)
        p.within(btn_id, "Click here to see the project", "Visit the live site", None)
        p.within(btn_id, 'href="https://evne.bravisthemes.com/portfolio/typeface-texture/"', 'href="%s"%s' % (url, NEXT))
    # Every project gets the Netra-style scrolling gallery: logo panel, cover with chips, then photos
    s, e = p.element_span("9cc3e24")
    template = p.h[s:e]
    for section_id, key, chips in HOME_GALLERIES:
        s, e = p.element_span(section_id)
        p.h = p.h[:s] + gallery_section(template, key, chips) + p.h[e:]

    # About blurb and counters
    p.sub("Our headquarters are located in Montreal", "Based in Accra, Ghana")
    p.sub("(Evne) is a creative studio for new brands, led by Nolan &#8211; in search of impact 💥",
          "I build websites people actually use, and owners can update without help.")

    # One image here, the coffee-app UI design, growing to fill the frame as you scroll (portfolio.js).
    # The theme's own two images go, along with its pinned slide-up (it only runs when .image-scroll exists).
    p.remove("6c17d1d")
    p.remove("7531beb")
    s, e = p.element_span("a4f685f")
    opening = re.match(r"<section[^>]*>", p.h[s:]).group(0)
    p.h = (p.h[:s] + opening.replace('class="elementor-section ', 'class="elementor-section dn-reveal-section ', 1)
           + '<div class="dn-reveal" aria-hidden="true"><div class="dn-reveal__frame">'
           '<img src="wp-content/uploads/2025/09/original-642fa30c49259d5b203745d12a7a7ea4.webp" alt="" width="1600" height="1200">'
           '<span class="dn-reveal__shade"></span></div></div>' + p.h[s + len(opening):])
    for eid, old_n, new_n, old_t, new_t in [
        ("48e810f", "500", "10", "Successful Projects", "Projects delivered"),
        ("8c175e3", "44", "7", "Talented Team Members", "Years in IT &amp; web"),
        ("77c0fc6", "7", "500", "Countries and Counting", "Students &amp; staff supported"),
    ]:
        p.within(eid, 'data-endnumber="%s" data-to-value="%s"' % (old_n, old_n), 'data-endnumber="%s" data-to-value="%s"' % (new_n, new_n))
        p.within(eid, old_t, new_t)

    # Certificates (was: awards)
    p.sub("Award-winning creativity", "Still learning")
    p.resub(r"Our commitment to pushing creative boundaries has earned us recognition[^<]*",
            "Courses I’ve finished in UX design, IT support and cybersecurity. They come up in my work more often than you’d think.")
    for old, new in sorted([  # longest first: titles also appear inside the descriptions
        ("Effie Awards", "Google UX Design"), ("Multiple Effie Awards", "Google via Coursera"),
        ("Honored with multiple Effie Awards for our results-driven campaigns that delivered measurable success for our clients.",
         "Foundations of User Experience (UX) Design: user research, wireframing, prototyping and usability."),
        ("Yellow Dot Award", "Google IT Support"), ("Blend aesthetics", "Google via Coursera"),
        ("Recognized for exceptional design with a Yellow Dot Award, celebrating our ability to blend aesthetics with functionality in branding and digital projects.",
         "Technical Support Fundamentals, which covers troubleshooting and dealing with users who just want their computer to work."),
        ("Kyiv International Advertising Festival", "Cybersecurity Operations"), ("Global impact.", "GI-KACE, Accra"),
        ("Multiple wins at the Kyiv International Ad Festival, showcasing our innovative approach to advertising and our ability to make a global impact.",
         "Cybersecurity training at the Ghana-India Kofi Annan Centre of Excellence in ICT, mostly on spotting and stopping threats."),
    ], key=lambda pair: -len(pair[0])):
        p.sub(old, new)

    # No real testimonials yet: drop the demo ones
    p.remove("ecebf61")

    # Images: brand artwork (logos on liquid glass), your own work, certificate cards
    for eid, idx, f, w, h, alt in [
        ("39a0914", 0, "home-coffee-app.jpg", 740, 740, "Coffee ordering app UI design"),
        ("75c07d7", 0, "cert-google-ux.jpg", 630, 430, "Google UX Design certificate"),
        ("e5006d0", 0, "cert-google-it.jpg", 630, 430, "Google IT Support certificate"),
        ("9de8dd9", 0, "cert-gikace.jpg", 630, 430, "GI-KACE Cybersecurity Operations certificate"),
    ]:
        p.image(eid, idx, f, w, h, alt)

    # Header button
    p.within("1e76354", 'href="works-1.html"', 'href="contact.html"')

    # Selected projects: a tilted wall of project cards drifting in alternate directions (replaces the galleries)
    s, e = p.element_span("a6b959e")
    p.h = p.h[:s] + work_section() + p.h[e:]

    # Hero: the theme's circles and heading give way to the globe hero (drawn by portfolio.js)
    s, e = p.element_span("94db63f")
    p.h = p.h[:s] + hero_section() + p.h[e:]
    p.sub('<script src="%sportfolio.js' % IMG_URL, '<script src="%sglobe-land.js"></script>\n<script src="%sportfolio.js' % (IMG_URL, IMG_URL))

    # Testimonials after the certificates; the contact section takes the place of the theme's call to action
    s, e = p.element_span("0455e14")
    p.h = p.h[:s] + testimonials_section() + voices_section() + contact_section() + p.h[e:]

    # The page as a story, in chapters: where it started, what I do now, how a project goes, what I've built,
    # what clients say, your turn. The theme's intro, logo strip, marquees, service slider and counters give way
    # to chapters 1 to 3; the certificates and the growing Figma design are kept and moved into them.
    p.within("a4f685f", "Based in Accra, Ghana", "A coffee ordering app I designed")
    p.within("a4f685f", "I build websites people actually use, and owners can update without help.",
             "Every project starts as a design you can see and change.")
    keep = {}
    for eid in ("4e3c89d", "a4f685f"):
        s, e = p.element_span(eid)
        keep[eid] = p.h[s:e]
    work_start = p.h.index('<section class="dn-work"')
    s, e = p.balanced(work_start)
    keep["work"] = p.h[s:e]
    p.h = p.h[:s] + p.h[e:]
    anchor = p.element_span("ace0414")[0]
    for eid in ("4e3c89d", "a26c828", "a4f685f", "25e2710", "02e8ea2", "4c46881", "c5303a0", "f95c0e9", "ace0414"):
        p.remove(eid)
    p.h = (p.h[:anchor] + story_start() + keep["4e3c89d"] + story_now() + story_process() + keep["a4f685f"]
           + keep["work"] + p.h[anchor:])
    # chapter guide down the right edge
    p.sub("</body>", STORY_RAIL + "</body>", 1)
    p.save()


def work_section():
    """Header, then three columns of Works cards inside a rotated stage; each column's track holds its
    cards three times so a CSS animation can loop it seamlessly by one copy (outer columns drift up, the
    middle one down) while the visible window stays inside the strip."""
    tiles = [re.search(r'<a class="dn-card.*?</a>', card(*g), re.S).group(0) for g in GRID]
    columns = [tiles[0::3], tiles[1::3], tiles[2::3]]
    cols = ""
    for i, c in enumerate(columns):
        copy = "".join(c)
        hidden = copy.replace('<a class="dn-card', '<a aria-hidden="true" tabindex="-1" class="dn-card')
        cols += ('<div class="dn-work__col dn-work__col--%s"><div class="dn-work__track">%s%s%s</div></div>'
                 % ("down" if i == 1 else "up", hidden, copy, hidden))
    return ('<section class="dn-work" id="selected-work">\n'
            '  <div class="dn-work__head">%s</div>\n'
            '  <div class="dn-work__stage"><div class="dn-work__tilt">%s</div></div>\n'
            '  <div class="dn-work__foot">\n'
            '    <p class="dn-work__caption">/ A charity, a church, a chef, a couple of AI startups and more. Here’s some of what I’ve built lately.</p>\n'
            '    <a class="dn-btn dn-btn--ghost" href="works-1.html">View all work</a>\n'
            '  </div>\n'
            '</section>\n') % (chapter(4, "What I’ve built", "Recent work"), cols)


def hero_section():
    """Full-screen hero: tagline that decodes on load, a dotted globe with Accra lit and a link to the UK,
    and readouts at the globe's corners (live Accra time). portfolio.js draws the globe."""
    return """<section class="dn-hero" id="top">
  <div class="dn-hero__bg" aria-hidden="true"></div>
  <div class="dn-hero__inner">
    <div class="dn-hero__copy">
      <span class="dn-pill"><i></i>Taking on new projects</span>
      <h1 class="dn-hero__title" aria-label="Nort Just Design. Nort Just Code.">
        <span class="dn-hero__line" data-scramble aria-hidden="true">Nort Just Design.</span>
        <span class="dn-hero__line dn-hero__line--accent" data-scramble aria-hidden="true">Nort Just Code.</span>
      </h1>
      <p class="dn-hero__lede">I’m Emmanuel, a web and WordPress developer in Accra. I design every site in Figma before I build it, and I’m still around after it goes live. Most of my clients are in Ghana, with a few in the UK.</p>
      <div class="dn-hero__actions">
        <a class="dn-btn dn-btn--light" href="#contact">Start a project<span class="dn-btn__icon" aria-hidden="true">&#8594;</span></a>
        <a class="dn-btn dn-btn--ghost" href="works-1.html">See my work</a>
      </div>
    </div>
    <div class="dn-hero__globe">
      <canvas aria-hidden="true"></canvas>
      <span class="dn-hud dn-hud--tl">Lat 05.60&deg; N<br>Lon 00.19&deg; W</span>
      <span class="dn-hud dn-hud--tr">Accra <b data-clock>00:00:00</b> GMT</span>
      <span class="dn-hud dn-hud--bl">WordPress / WooCommerce<br>Next.js / Figma</span>
      <span class="dn-hud dn-hud--br">Clients in<br>Ghana and the UK</span>
    </div>
  </div>
  <div class="dn-hero__foot">
    <span class="dn-hero__scroll"><i aria-hidden="true"></i>Scroll down</span>
    <span class="dn-hero__meta">Building websites since 2019</span>
  </div>
</section>
"""


# Testimonials. DRAFTS written from each project: every client must approve (or rewrite) their quote before the
# site goes live. Featured: (photo, name, detail, quote). The wall: (photo, focus point, name, role, quote).
TESTIMONIALS = [
    ("proj-eah-card.jpg", "Dr. Emele Arthur-Hayford", "Scientist and health equity leader",
     "My research and talks were scattered all over the internet. Emmanuel pulled them into one site "
     "that finally feels like me. He never once complained about my revisions, and there were a lot of them."),
    ("proj-strategicagile-card.jpg", "Strategic &amp; Agile", "Human capital consultancy",
     "We needed a site that looked as serious as our work. Emmanuel got what we do after one conversation, "
     "and now my team updates the site without calling anyone."),
    ("testi-mawuena-founder.jpg", "Mawuena Datsa", "Founder, Mawuena Datsa Foundation",
     "People used to message us asking how to donate, and now we just send them the link. "
     "Emmanuel was patient with us and never made us feel silly for asking basic questions."),
    ("proj-wmt-card.jpg", "World Movers Team", "Youth NGO for health equity",
     "Our projects, events, donations and newsletter used to live in about five different places. "
     "Now it’s one site, and our volunteers can actually find things."),
]
VOICES = [
    ("voice-agorivia-founder.jpg", "50% 50%", "Agorivia", "Founder, operations support in the UK",
     "Seeing the whole design in Figma before anything was built saved us so much going back and forth. It went live the week he said it would."),
    ("proj-feci-card.jpg", "30% 35%", "Faith Empowered Chapel Intl.", "Church",
     "Our members can now give online and catch up on services they missed, even the ones who insist they’re not into tech."),
    ("proj-netra-card.jpg", "55% 40%", "Netra Technologies GH", "IT services and online shop",
     "We sell in cedis and the shop just works. When something needs changing, I can usually do it myself."),
    ("proj-weekendchef-card.jpg", "50% 50%", "The Weekend Chef", "Meals to order, Accra",
     "Customers order and pay with Paystack before I even start cooking, which is exactly how I wanted it."),
    ("proj-creativeclick-card.jpg", "50% 40%", "Creative Click Multimedia", "Software agency",
     "Seven languages is a lot of moving parts. He kept it all organised, and the site is quick."),
    ("proj-geoben-card.jpg", "50% 40%", "Geoben Height", "Apartments and event spaces, Accra",
     "Guests look through the apartments and event spaces before they call us now. It saves us a lot of phone calls."),
]


def testimonials_section():
    """Malan-style testimonials over a dotted world map: photo card with the client's name on a glass strip,
    the quote beside it, thumbnails that switch between clients, and a large closing quote mark."""
    photos, quotes, thumbs = "", "", ""
    for i, (img, name, detail, quote) in enumerate(TESTIMONIALS):
        on = " is-active" if i == 0 else ""
        photos += ('<figure class="dn-testi__photo%s" data-index="%d"><img src="%s%s" alt="" width="960" height="800" loading="lazy">'
                   '<figcaption><b>%s</b><span>%s</span></figcaption></figure>' % (on, i, IMG_URL, img, name, detail))
        text = quote
        quotes += '<blockquote class="pxl-blockquote dn-testi__quote%s" data-index="%d"><p>&#8220;%s&#8221;</p></blockquote>' % (on, i, text)
        thumbs += ('<button type="button" class="dn-testi__thumb%s" data-index="%d" aria-label="Show %s" aria-pressed="%s">'
                   '<img src="%s%s" alt="" width="960" height="800" loading="lazy"></button>'
                   % (on, i, name, "true" if i == 0 else "false", IMG_URL, img))
    return """<section class="dn-testi" id="testimonials">
  <img class="dn-testi__map" src="%sworld-dots.svg" alt="" aria-hidden="true">
  <div class="dn-testi__head">%s</div>
  <div class="dn-testi__body">
    <div class="dn-testi__card">%s</div>
    <div class="dn-testi__side">
      <div class="dn-testi__quotes" aria-live="polite">%s</div>
      <div class="dn-testi__foot">
        <div class="dn-testi__thumbs">%s</div>
        <svg class="dn-testi__mark" viewBox="0 0 96 80" aria-hidden="true"><path d="M8 0h30v34c0 26-12 40-34 46l-4-10c12-5 18-14 19-26H8zM58 0h30v34c0 26-12 40-34 46l-4-10c12-5 18-14 19-26H58z"/></svg>
      </div>
    </div>
  </div>
</section>
""" % (IMG_URL, chapter(5, "What clients say", "In their words", "A few notes from people I’ve built sites for."), photos, quotes, thumbs)


def voices_section():
    """Client wall after malan.design: quote cards scattered around a centred heading over a moving field of dots
    (drawn by portfolio.js); each card drifts at its own speed as you scroll."""
    cards = ""
    for i, (img, focus, name, role, quote) in enumerate(VOICES):
        cards += ('<figure class="dn-voice dn-voice--%d" data-speed="%s">'
                  '<blockquote class="pxl-blockquote dn-voice__quote"><p>&#8220;%s&#8221;</p></blockquote>'
                  '<figcaption class="dn-voice__who"><img src="%s%s" alt="" width="96" height="96" loading="lazy" style="object-position:%s">'
                  '<span><b>%s</b><small>%s</small></span></figcaption></figure>'
                  % (i + 1, ("-0.6", "0.5", "-0.35", "0.7", "-0.5", "0.4")[i], quote, IMG_URL, img, focus, name, role))
    return """<section class="dn-voices" id="clients">
  <canvas class="dn-voices__wave" aria-hidden="true"></canvas>
  <div class="dn-voices__stage">
    <h2 class="dn-voices__title"><span class="dn-voices__accent">More from the people</span><span>I&#8217;ve built for</span></h2>
    %s
  </div>
</section>
""" % cards


def chapter(number, tag, title, lede=None, level="h2"):
    """The header every chapter (and every page) opens with: a numbered tag, a title and an optional line of intro."""
    num = "<b>%02d</b>" % number if number else ""
    return ('<header class="dn-chapter"><span class="dn-chapter__tag">%s%s</span><%s class="dn-chapter__title">%s</%s>%s</header>'
            % (num, tag, level, title, level, '<p class="dn-chapter__lede">%s</p>' % lede if lede else ""))


def pagehead(tag, title, lede, actions=""):
    """Top of the About, Works and Contact pages: the same header as the homepage chapters, at page-title size."""
    return ('<section class="dn-pagehead"><div class="dn-pagehead__inner">%s%s</div></section>\n'
            % (chapter(0, tag, title, lede, level="h1"), '<div class="dn-cta__actions">%s</div>' % actions if actions else ""))


# Chapter 1. (year, place, what happened)
TIMELINE = [
    ("2019", "MEST Africa", "My internship. Graphic design, and my first real websites in HTML, CSS and WordPress."),
    ("2020", "University of Ghana", "National service in the ICT lab. I helped over 500 students and staff with whatever broke."),
    ("2021", "Jumeni Technologies", "I ran daily operations and onboarding, and ended up making the marketing graphics too."),
    ("2022", "KA Technologies", "Building and repairing laptops and sorting out networks, which I still do."),
    ("Now", "Theme Wire", "WordPress developer since January 2026. I build sites, themes, templates and plugins there, and freelance for clients in Ghana and the UK too."),
]
COUNTS = [(10, "+", "projects delivered"), (7, "", "years in IT and web"), (500, "+", "students and staff helped")]


def story_start():
    stops = "".join('<li class="dn-timeline__stop%s"><span class="dn-timeline__year">%s</span><h3>%s</h3><p>%s</p></li>'
                    % (" is-now" if year == "Now" else "", year, place, text) for year, place, text in TIMELINE)
    counts = "".join('<li><b data-count="%d">%d</b><i>%s</i><span>%s</span></li>' % (n, n, plus, label) for n, plus, label in COUNTS)
    return ('<section class="dn-story" id="story"><div class="dn-story__inner">%s'
            '<ol class="dn-timeline">%s</ol><ul class="dn-counts">%s</ul>'
            '<p class="dn-story__cv"><span>The full story, with dates and certificates, is in my CV.</span>%s</p></div></section>\n'
            % (chapter(1, "Where it started", "I started out fixing computers",
                       "Before I built websites I spent years in computer labs and at repair benches, and I still work the "
                       "same way. I find out what’s actually wrong before I touch anything."), stops, counts, cv_button()))


# Chapter 2. Services, each with the tools it uses, then every tool on a moving strip
TOOLS = [("figma", "Figma"), ("photoshop", "Photoshop"), ("wordpress", "WordPress"), ("woocommerce", "WooCommerce"),
         ("elementor", "Elementor"), ("html", "HTML"), ("css", "CSS"), ("javascript", "JavaScript"), ("nextjs", "Next.js"),
         ("chrome", "Chrome extensions")]
OFFER = [
    ("WordPress sites", ["wordpress", "elementor"], "WordPress and Elementor sites you can update yourself, without calling me every time a price changes."),
    ("Custom code", ["html", "css", "javascript", "nextjs"], "When WordPress isn’t the right fit, I write it in HTML, CSS, JavaScript or Next.js. And yes, it works on phones."),
    ("Shops and payments", ["woocommerce"], "WooCommerce shops that take card and mobile money through Paystack. Donation pages and enquiry forms too."),
    ("Extensions and plugins", ["chrome", "figma"], "Chrome extensions and Figma plugins. My own, Pagecast, copies any website into Figma as layers you can edit."),
]


def tool_logo(key):
    return '<img src="%stools/%s.svg" alt="" width="28" height="28" loading="lazy">' % (IMG_URL, key)


def story_now():
    cards = "".join('<li class="dn-offer__card"><span class="dn-offer__logos">%s</span><h3>%s</h3><p>%s</p></li>'
                    % ("".join(tool_logo(k) for k in keys), title, text) for title, keys, text in OFFER)
    chips = "".join('<li class="dn-tools__chip">%s<span>%s</span></li>' % (tool_logo(k), name) for k, name in TOOLS)
    hidden = chips.replace('<li class="dn-tools__chip">', '<li class="dn-tools__chip" aria-hidden="true">')
    return ('<section class="dn-now" id="services"><div class="dn-now__inner">%s<ul class="dn-offer">%s</ul></div>'
            '<div class="dn-tools"><h3 class="dn-tools__title">What I work with</h3>'
            '<div class="dn-tools__belt"><ul class="dn-tools__track">%s%s</ul></div></div></section>\n'
            % (chapter(2, "What I do now", "These days I build websites",
                       "Most of my sites run on WordPress. When WordPress would only get in the way, I code them from scratch instead."),
               cards, chips, hidden))


# Chapter 3. (title, what happens)
STEPS = [
    ("We talk", "A call about what the site is for and who will use it. You show me whatever content you already have, and we agree on scope and a timeline."),
    ("I design it in Figma", "You see every page and ask for changes before I write any code."),
    ("I build it", "Usually in WordPress and Elementor, with whatever forms or payments you need. I check it on my phone as I go."),
    ("We launch", "I set up analytics and show your team how to update things. If anything breaks after that, message me."),
]


def story_process():
    steps = "".join('<li class="dn-steps__step"><span class="dn-steps__num">%02d</span><h3>%s</h3><p>%s</p></li>'
                    % (i + 1, title, text) for i, (title, text) in enumerate(STEPS))
    return ('<section class="dn-process" id="process"><div class="dn-process__inner">%s<ol class="dn-steps">%s</ol></div></section>\n'
            % (chapter(3, "How a project goes", "Here’s how we’d work together",
                       "You see the design before I build anything, and once the site is live you can update it yourself."), steps))


STORY_RAIL = ('<nav class="dn-rail" aria-label="Chapters"><ol>'
              + "".join('<li><a href="#%s"><i></i><span>%s</span></a></li>' % (target, label) for target, label in [
                  ("top", "Intro"), ("story", "Where it started"), ("services", "What I do now"), ("process", "How a project goes"),
                  ("selected-work", "What I’ve built"), ("testimonials", "What clients say"), ("contact", "Your turn")])
              + "</ol></nav>\n")


SERVICES = ["WordPress website", "Online shop", "Web app or custom site", "Chrome extension or Figma plugin",
            "Maintenance and support", "Something else"]
BUDGETS = ["Under $500", "$500 to $1,500", "$1,500 to $5,000", "Over $5,000", "Not sure yet"]


def contact_section(page=False):
    """Malan-style contact: heading and direct details on the left, the enquiry form in a card on the right,
    over a map of the world. The form posts to FormSubmit, which emails it to EMAIL; if that fails it opens the
    visitor's email app with the message filled in instead (portfolio.js).
    On the contact page the page header above already says what this is, so the intro keeps only the details."""
    options = lambda items: "".join("<option>%s</option>" % o for o in items)
    intro = "" if page else (chapter(6, "Your turn", "Let’s build yours",
                                     "Got something in mind? Tell me a bit about it, even if it’s only a rough idea for now.")
                             + '<a class="dn-btn dn-btn--light" href="contact.html">Start a project'
                               '<span class="dn-btn__icon" aria-hidden="true">&#8594;</span></a>')
    return """<section class="dn-contact%(mod)s" id="contact">
  <img class="dn-contact__map" src="%(img)sworld-countries.svg" alt="" aria-hidden="true">
  <div class="dn-contact__inner">
    <div class="dn-contact__intro">
      %(intro)s
      <ul class="dn-contact__direct">
        <li><span>Email</span><a href="mailto:%(email)s">%(email)s</a></li>
        <li><span>WhatsApp</span><a href="%(wa)s"%(next)s>%(phone)s</a></li>
        <li><span>Based in</span>Accra, Ghana</li>
        <li><span>CV</span><a href="%(img)s%(cvfile)s" download="%(cvfile)s">Download (PDF, 2 pages)</a></li>
      </ul>
    </div>
    <form class="dn-form" data-email="%(email)s" novalidate>
      <input class="dn-form__trap" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="dn-form__row">
        <label class="dn-field"><span>Name</span><input name="name" type="text" autocomplete="name" placeholder="Ama Mensah" required></label>
        <label class="dn-field"><span>Email</span><input name="email" type="email" autocomplete="email" placeholder="ama@example.com" required></label>
      </div>
      <div class="dn-form__row">
        <label class="dn-field"><span>Service</span><select name="service" required><option value="" selected disabled>Select an option</option>%(services)s</select></label>
        <label class="dn-field"><span>Budget</span><select name="budget"><option value="" selected disabled>Select an option</option>%(budgets)s</select></label>
      </div>
      <label class="dn-field"><span>Message</span><textarea name="message" rows="5" placeholder="Tell me about your project" required></textarea></label>
      <button class="dn-form__submit" type="submit">Send message</button>
      <p class="dn-form__note" role="status">I usually reply within a day.</p>
    </form>
  </div>
</section>
""" % {"img": IMG_URL, "email": EMAIL, "wa": WHATSAPP, "next": NEXT, "phone": PHONE, "intro": intro,
       "mod": " dn-contact--page" if page else "", "cvfile": CV_FILE, "services": options(SERVICES), "budgets": options(BUDGETS)}


def about():
    p = Page("about.html")
    global_edits(p)
    p.sub("<title>About &#8211; Diginort</title>", "<title>About | Emmanuel Nortey</title>", None)

    p.sub("Who We Are, What We Believe", "I build websites, and I like fixing things")
    p.resub(r"We are more than just a creative agency—we are storytellers[^<]*",
            "I’m Emmanuel Nii Yeboah Nortey, based in Accra. I design in Figma first, then build. Before all this I spent years fixing computers and networks, and that still comes in handy")
    p.within("d03595b", 'data-endnumber="10" data-to-value="10"', 'data-endnumber="7" data-to-value="7"')
    p.sub("Years of Excellence", "Years in IT &amp; web")
    p.sub("For over 10 years, Evne has been at the forefront of creativity and technology, delivering top-tier solutions that drive real results.",
          "I started as an intern at MEST Africa in 2019 and have moved between IT support, startup operations and web work ever since. These days it’s mostly WordPress sites for NGOs and small businesses, plus the odd web app or browser extension.")

    # Process video block: no video yet, so keep the image and title only
    p.within("3f5d0af", "Our Work Process", "From Figma to launch")
    p.resub(r'(data-id="3f5d0af".*?)<a class="pxl-btn-video[^"]*"[^>]*>.*?</a>', r"\1", 1)

    p.sub("We believe in pushing boundaries", "What I believe")
    p.resub(r"A Vision for Bold Brands\. Led by(\s*<span class=\"pxl-title--highlight\">\s*)creativity",
            r"Websites you can update yourself. Designed in\1Figma")
    p.sub(", driven by impact.", ", then built properly.")

    # Process accordion
    steps = [
        ("Communications", "Discover",
         "We start with a call about what the site is for and who will use it, and you show me whatever content you already have. Then we agree on scope and a timeline."),
        ("Brand Strategy", "Design",
         "I plan the pages and design them in Figma. You see every screen and ask for changes before I write any code."),
        ("Consulting", "Build",
         "I build it, usually in WordPress and Elementor, with whatever forms or payments you need, and I keep checking it on my phone as I go."),
        ("Design", "Launch &amp; support",
         "Once it’s live I set up analytics and show your team how to update things. If anything breaks after that, message me."),
    ]
    for old, new, _ in reversed(steps):  # "Design" is both an old and a new title
        p.within("c26b77a", '<span class="pxl-title--text">%s</span>' % old, '<span class="pxl-title--text">%s</span>' % new)
    desc = iter(d for _, _, d in steps)
    s, e = p.element_span("c26b77a")
    part, n = re.subn(r"Whether you're navigating a new business direction or fine-tuning your existing operations, our consulting services provide the insights and expertise you need[^<]*",
                      lambda m: next(desc), p.h[s:e])
    assert n == 4, n
    p.h = p.h[:s] + part + p.h[e:]

    # Value cards become experience
    for old_t, old_d, new_t, new_d in [
        ("Innovative Solutions", "We deliver forward-thinking, creative solutions that push the boundaries of what’s possible, helping your brand stand out in a crowded marketplace.",
         "Technician · KA Technologies", "2022 to now. I build and repair laptops and sort out system and network problems. Slow machines usually leave about 20% faster."),
        ("Strategic Excellence", "We craft intelligent, data-driven strategies designed to maximize your impact and position your brand ahead in a constantly evolving market.",
         "IT Support · University of Ghana", "National service, 2020 to 2021. I looked after the ICT lab and helped over 500 students and staff with their tech problems."),
        ("Human-Centered Design", "We create thoughtful, intuitive experiences that connect with real people, building stronger relationships between your brand and its audience.",
         "Operations · Jumeni Technologies", "2021. I ran daily operations and customer onboarding, and ended up making the marketing graphics too."),
        ("Agile Execution", "We move quickly and adapt with precision, turning bold ideas into real-world results that keep your business ahead of the curve.",
         "Intern · MEST Africa", "2019. This is where it started, with graphic design and my first real websites in HTML, CSS, JavaScript and WordPress."),
    ]:
        p.within("9a0b92c", "<span>%s</span>" % old_t, "<span>%s</span>" % new_t)
        p.within("9a0b92c", old_d, new_d)
    s, e = p.element_span("9a0b92c")
    part, n = re.subn(r'<div class="pxl-item--link">\s*<a href="#" class="btn pxl-btn">.*?</a>\s*</div>', "", p.h[s:e], flags=re.S)
    assert n == 4, n
    p.h = p.h[:s] + part + p.h[e:]
    p.sub("Collaboration that drives success.", "Where I learned the job.")

    # Images
    collage = ["art-collage-%d.jpg" % i for i in range(1, 6)]
    collage_sizes = [(405, 400), (520, 600), (415, 310), (520, 700), (415, 360)]
    collage_alt = ["Faith Empowered Chapel International", "Releev AI", "Dr. Emele Arthur-Hayford", "Mawuena Datsa Foundation", "Quickpipe AI"]
    for idx in range(10):  # the collage repeats its five images for the scrolling loop
        w, h = collage_sizes[idx % 5]
        p.image("581cddf", idx, collage[idx % 5], w, h, collage_alt[idx % 5])
    for old, new in zip(["8fa93343cf9bdbe14bc7d9bf1eb42a3d", "4324ae79fa0422afb817f318fa5391d3", "de0bb65ef5740654d47813d896ae7a70",
                         "4173023d61331f8e939fba13137d0d92", "2babb225d0185cf6deac931bc3304062"], collage):
        p.within("581cddf", 'href="wp-content/uploads/2025/03/%s.webp"' % old, 'href="%s%s"' % (IMG_URL, new), 2)
    for eid, idx, f, w, h, alt in [
        ("a56db2c", 0, "art-about-main.jpg", 1200, 796, "Logos of client websites"),
        ("3f5d0af", 0, "art-process.jpg", 1800, 900, "Client logos"),
        ("6a392ec", 0, "art-small-1.jpg", 300, 220, "Geoben Height"),
        ("cee361c", 0, "art-small-2.jpg", 300, 220, "Creative Click Multimedia"),
        ("c26b77a", 0, "art-step-discover.jpg", 600, 600, "Discover"),
        ("c26b77a", 1, "art-step-design.jpg", 600, 600, "Design"),
        ("c26b77a", 2, "art-step-build.jpg", 600, 600, "Build"),
        ("c26b77a", 3, "art-step-launch.jpg", 600, 600, "Launch and support"),
        ("9a0b92c", 0, "exp-ka.jpg", 300, 300, "KA Technologies"),
        ("9a0b92c", 1, "exp-ug.jpg", 300, 300, "University of Ghana"),
        ("9a0b92c", 2, "exp-jumeni.jpg", 300, 300, "Jumeni Technologies"),
        ("9a0b92c", 3, "exp-mest.jpg", 300, 300, "MEST Africa"),
    ]:
        p.image(eid, idx, f, w, h, alt)

    # Fake testimonials and team: removed; the page ends the way the homepage does, with your turn
    p.remove("e1ce964")
    p.remove("9006f24")
    s, e = p.element_span("23e7ae5")
    p.h = p.h[:s] + ('<section class="dn-cta"><div class="dn-cta__inner">%s<div class="dn-cta__actions">'
                     '<a class="dn-btn dn-btn--light" href="contact.html">Start a project<span class="dn-btn__icon" aria-hidden="true">&#8594;</span></a>'
                     '<a class="dn-btn dn-btn--ghost" href="works-1.html">See my work</a></div></div></section>\n'
                     % chapter(0, "Your turn", "Got a project? Let’s talk",
                               "Tell me a bit about it, even if it’s only a rough idea for now.")) + p.h[e:]
    # Experience: the theme's placeholder logo grid goes, and the heading that trailed after the cards
    # becomes a chapter header in front of them
    for eid in ("cde6d26", "13b9eab", "26d3998"):
        p.remove(eid)
    s, e = p.element_span("9227bc7")
    p.h = p.h[:s] + ('<section class="dn-band"><div class="dn-band__inner">%s</div></section>\n'
                     % chapter(0, "Experience", "Where I learned the job",
                               "Four places, from my first internship to the repair bench I still work at.")) + p.h[s:]
    # Page header in the same style as every other page
    s, e = p.element_span("83751b7")
    p.h = p.h[:s] + pagehead("About", "I build websites, and I like fixing things",
                             "I’m Emmanuel Nii Yeboah Nortey, based in Accra. I design in Figma first, then build. Before all this "
                             "I spent years fixing computers and networks, and that still comes in handy.",
                             cv_button("light") + '<a class="dn-btn dn-btn--ghost" href="contact.html">Start a project</a>') + p.h[e:]
    p.save()


FILTERS = [("web", "Websites"), ("ecommerce", "Online shops"), ("nonprofit", "Nonprofits"),
           ("ai", "AI products"), ("extensions", "Extensions"), ("uiux", "UI/UX design"), ("branding", "Branding")]
# (title, category label, link, logo file or monogram, glow, second glow, filter slugs, cover image for design pieces)
GRID = [
    ("Geoben Height", "Hospitality", "https://geobenheight.com/", "GH", "#c99a2e", "#5a420d", ["web"], None),
    ("Netra Technologies GH", "Technology", PROJECTS["netra"][1], "netra.png", "#2f6fd6", "#e8573c", ["web", "ecommerce"], None),
    ("The Weekend Chef", "Food &amp; hospitality", PROJECTS["weekendchef"][1], "weekendchef.png", "#e0612b", "#8f1218", ["web", "ecommerce"], None),
    ("Pagecast", "Chrome extension · Coming soon", None, "pagecast.png", "#ff6a3d", "#7a4dff", ["extensions", "uiux"], None),
    ("Agorivia", "Operations", PROJECTS["agorivia"][1], "agorivia-A.png", "#2f6b4f", "#8a6a3a", ["web", "uiux"], None),
    ("Mawuena Datsa Foundation", "Nonprofit", PROJECTS["mawuena"][1], "mawuena.png", "#a43cc9", "#5a1a6e", ["web", "nonprofit"], None),
    ("Faith Empowered Chapel Intl.", "Faith", "https://faithempoweredchapelinternational.org/", "feci.png", "#6a2bd6", "#2b1066", ["web", "nonprofit"], None),
    ("World Movers Team", "Health &amp; nonprofit", PROJECTS["wmt"][1], "wmt.png", "#2c7be5", "#0d3f7a", ["web", "nonprofit"], None),
    ("Releev AI", "Health AI", "https://releevai.com/", "releev.png", "#14a3a8", "#0d4f7a", ["web", "ai"], None),
    ("Quickpipe AI", "Sales AI", "https://quickpipe.ai/", "quickpipe-icon.png", "#3b5bff", "#1a2a8a", ["ai"], None),
    ("Dr. Emele Arthur-Hayford", "Personal brand", PROJECTS["eah"][1], "eah-icon.png", "#2bb3e6", "#3c3fd6", ["web", "uiux"], None),
    ("Strategic &amp; Agile", "Consulting", PROJECTS["strategicagile"][1], "strategicagile.svg", "#1d3a6b", "#6f8fbf", ["web"], None),
    ("Creative Click Multimedia", "Software agency", PROJECTS["creativeclick"][1], "creativeclick.svg", "#6a5cff", "#2a1f8a", ["web", "uiux"], None),
    ("Coffee ordering app", "Mobile app UI", "wp-content/uploads/2025/09/original-642fa30c49259d5b203745d12a7a7ea4.webp", None, "#c98a3a", "#5a3a12", ["uiux"], "grid-coffee-app.jpg"),
    ("Merch mockup", "Branding", "wp-content/uploads/2025/09/Untitled-1-1-740x740.png", None, "#a3322a", "#5a1a12", ["branding"], "grid-merch.jpg"),
]
# Projects with their own photos (see projects.py): logo, short description, logo placement, logo style.
# Placement: "center" over the middle of the photo; "corner" keeps it clear of a face (portraits).
# Style: "white" (a white logo file), "invert" (a coloured logo shown in white), "badge" (a self-contained
# coloured badge, shown as is), "text" (no logo file: the name set in type).
# A hover photo is used when projects.py made one.
PHOTO_CARDS = {
    "Geoben Height": ("geoben", "Geoben Height", "Apartments and event spaces in Accra. Guests can look around and book online.", "center", "text"),
    "Netra Technologies GH": ("netra", "netra.png", "An IT company in Ghana with an online shop that takes cedis.", "center", "invert"),
    "Pagecast": ("pagecast", "pagecast.png", "My own Chrome extension and Figma plugin. Point it at a website and get Figma layers you can edit.", "corner", "badge"),
    "The Weekend Chef": ("weekendchef", "weekendchef.png", "Order homemade meals in Accra and pay online with Paystack.", "center", "badge"),
    "Agorivia": ("agorivia", "agorivia-white.png", "Behind the scenes operations support for UK clinics and founders.", "center", "white"),
    "Mawuena Datsa Foundation": ("mawuena", "mawuena.png", "Education, health, rescue and mentoring for young people in Ghana.", "center", "invert"),
    "Faith Empowered Chapel Intl.": ("feci", "feci.png", "Church website where members catch up on services and give online.", "corner", "badge"),
    "World Movers Team": ("wmt", "wmt-white.png", "Young people working on health equity across Africa.", "center", "white"),
    "Releev AI": ("releev", "releev.png", "AI healthcare for communities that usually get left out.", "corner", "invert"),
    "Quickpipe AI": ("quickpipe", "quickpipe-icon.png", "An AI sales pipeline for small sales teams.", "center", "invert"),
    "Dr. Emele Arthur-Hayford": ("eah", "eah-icon.png", "Personal site for a scientist working on health equity.", "corner", "invert"),
    "Strategic &amp; Agile": ("strategicagile", "strategicagile-white.svg",
                              "A consultancy that helps African organisations build stronger teams.", "corner", "white"),
    "Creative Click Multimedia": ("creativeclick", "creativeclick.svg", "Site for a young software agency, in seven languages, built with Next.js.", "center", "invert"),
}
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg>')
COLS = "col-xl-4 col-lg-4 col-md-6 col-sm-12 col-12"


def photo_card(title, label, link, glow, glow2, slugs):
    key, logo, desc, logo_pos, style = PHOTO_CARDS[title]
    if style == "text":
        mark = '<span class="dn-card__wordmark">%s</span>' % logo
    else:
        mark = '<img class="dn-card__logo dn-card__logo--%s" src="%slogos/%s" alt="%s logo">' % (style, IMG_URL, logo, title)
    hover = ""
    if os.path.exists(os.path.join(IMG, "proj-%s-hover.jpg" % key)):
        hover = '    <img class="dn-card__photo dn-card__photo--hover" src="%sproj-%s-hover.jpg" alt="" loading="lazy">\n' % (IMG_URL, key)
    return ('<div class="pxl-grid-item dn-item %s %s">\n'
            '  <a class="dn-card dn-card--photo dn-card--logo-%s" %s%s style="--glow:%s;--glow2:%s">\n'
            '    <img class="dn-card__photo" src="%sproj-%s-card.jpg" alt="%s">\n'
            '%s'
            '    <span class="dn-card__shade"></span>\n'
            '    <span class="dn-card__label">%s</span><span class="dn-card__dot"></span>\n'
            '    <span class="dn-card__stage">%s</span>\n'
            '    <span class="dn-card__bar"><span><span class="dn-card__title">%s</span><span class="dn-card__desc">%s</span></span>'
            '<span class="dn-card__btn">%s</span></span>\n'
            '  </a>\n</div>\n') % (COLS, " ".join(slugs), logo_pos, 'href="%s"' % link if link else "", NEXT if link else "", glow, glow2, IMG_URL, key, title, hover,
                                  label, mark, title, desc, ARROW)


def card(title, label, link, logo, glow, glow2, slugs, cover):
    if title in PHOTO_CARDS:
        return photo_card(title, label, link, glow, glow2, slugs)
    target = NEXT if link.startswith("http") else ' target="_blank"'
    if cover:
        stage = '<img class="dn-card__cover" src="%s%s" alt="%s" loading="lazy">' % (IMG_URL, cover, title)
        kind = " dn-card--image"
    else:
        inner = ('<img src="%slogos/%s" alt="%s logo" loading="lazy">' % (IMG_URL, logo, title) if "." in logo
                 else '<span class="dn-card__mono">%s</span>' % logo)
        stage = '<span class="dn-card__tile">%s</span>' % inner
        kind = ""
    return ('<div class="pxl-grid-item dn-item %s %s">\n'
            '  <a class="dn-card%s" href="%s"%s style="--glow:%s;--glow2:%s">\n'
            '    <span class="dn-card__label">%s</span><span class="dn-card__dot"></span>\n'
            '    <span class="dn-card__stage">%s</span>\n'
            '    <span class="dn-card__bar"><span><span class="dn-card__title">%s</span><span class="dn-card__cat">%s</span></span>'
            '<span class="dn-card__btn">%s</span></span>\n'
            '  </a>\n</div>\n') % (COLS, " ".join(slugs), kind, link, target, glow, glow2, label, stage, title, label, ARROW)


def works():
    p = Page("works-1.html")
    global_edits(p)
    p.sub("<title>Works 1 &#8211; Diginort</title>", "<title>Works | Emmanuel Nortey</title>")
    p.sub('"title":"Works%201%20', '"title":"Works%20', 1)
    p.sub("Discover Our Work", "Selected work")
    p.sub("Our portfolio is a reflection of the passion, creativity, and strategic thinking we bring to every project.",
          "Everything here is live. Click a project to open the site and have a look around.")

    # Filter: a liquid-glass pill bar; keep "All", rebuild the rest
    p.sub('<div class="pxl-grid-filter normal style-1">', '<div class="pxl-grid-filter normal style-1 dn-filter">')
    m = re.search(r'(<span class="filter-item active" data-filter="\*">All\s*<svg.*?</svg>\s*</span>)(.*?)(\s*</div>)', p.h, re.S)
    spans = "".join('\n<span class="filter-item" data-filter=".%s">%s</span>' % (slug, label) for slug, label in FILTERS)
    p.h = p.h[:m.start(2)] + spans + p.h[m.end(2):]

    # Project cards: logo on a glass tile, as on the Creative Click work page
    items = list(re.finditer(r'<div class="pxl-grid-item[^"]*">.*?(?=<div class="pxl-grid-item|<div class="grid-sizer)', p.h, re.S))
    assert len(items) == 12, len(items)
    p.h = p.h[:items[0].start()] + "".join(card(*g) for g in GRID) + p.h[items[-1].end():]
    p.sub('<div class="grid-sizer col-xl-3 col-lg-4 col-md-6 col-sm-6 col-12"></div>', '<div class="grid-sizer %s"></div>' % COLS)

    # Everything fits on one page: no "Load more"
    assert p.h.count('<div class="pxl-load-more">') == 1
    s, e = p.balanced(p.h.index('<div class="pxl-load-more">'))
    p.h = p.h[:s] + p.h[e:]
    # Page header in the same style as every other page
    s, e = p.element_span("fdb9f5e")
    p.h = p.h[:s] + pagehead("Work", "Selected work",
                             "Everything here is live. Click a project to open the site and have a look around.") + p.h[e:]
    p.save()
    os.remove(os.path.join(OUT, "wp-content/static-ajax/works-1-paged-2.json"))


def contact():
    p = Page("contact.html")
    global_edits(p)
    p.sub("<title>Contact &#8211; Diginort</title>", "<title>Contact | Emmanuel Nortey</title>")
    s, e = p.element_span("daead26")
    p.h = p.h[:s] + pagehead("Contact", "Tell me about your project",
                             "Fill in the form and it comes straight to my inbox. "
                             "Prefer WhatsApp? That works too.") + contact_section(page=True) + p.h[e:]
    p.save()


if __name__ == "__main__":
    # Start fresh each time, but keep the git repository the site is pushed from (github.com/manuelnort/Portfolio-)
    for name in (os.listdir(OUT) if os.path.isdir(OUT) else []):
        if name in (".git", ".gitignore", "_build"):   # _build: these scripts and their sources
            continue
        path = os.path.join(OUT, name)
        shutil.rmtree(path) if os.path.isdir(path) and not os.path.islink(path) else os.remove(path)
    shutil.copytree(SRC, OUT, dirs_exist_ok=True)
    for f in ("works-2.html", "works-3.html", "wp-content/static-ajax/works-2-paged-2.json", "wp-content/static-ajax/works-3-paged-2.json"):
        os.remove(os.path.join(OUT, f))
    dest = os.path.join(OUT, IMG_URL)
    shutil.copytree(IMG, dest, dirs_exist_ok=True)
    shutil.copytree(os.path.join(HERE, "logos"), os.path.join(dest, "logos"), dirs_exist_ok=True)
    shutil.copy(os.path.join(HERE, "assets", "portfolio.css"), dest)
    shutil.copy(os.path.join(HERE, "assets", "portfolio.js"), dest)
    brand = os.path.join(HERE, "brand")
    for src, name in [("wordmark-white.png", "name-logo-white.png"), ("wordmark-dark.png", "name-logo-dark.png"),
                      ("en-mark.png", "en-mark.png")] + [("en-icon-%s.png" % n, "en-icon-%s.png" % n) for n in (32, 180, 192, 270)]:
        shutil.copy(os.path.join(brand, src), os.path.join(dest, name))
    for f in glob.glob(os.path.join(OUT, "wp-content/uploads/*/*/*")):
        if re.search(r"digi", os.path.basename(f), re.I):
            os.remove(f)
    home()
    about()
    works()
    contact()

    # Ship only the portfolio files a page or the stylesheet actually uses
    used = "".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(OUT, "*.html")))
    used += open(os.path.join(dest, "portfolio.css"), encoding="utf-8").read()
    for root, _, files in os.walk(dest):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), dest)
            if f not in ("portfolio.css", "portfolio.js") and IMG_URL + rel not in used:
                os.remove(os.path.join(root, f))
    left = [f for f in glob.glob(os.path.join(OUT, "*.html")) if re.search(r"diginort|digiknort", open(f, encoding="utf-8").read(), re.I)]
    assert not left, "Diginort still mentioned in %s" % left
    print("portfolio built:", OUT)
