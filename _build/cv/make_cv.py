"""Public CV as a PDF for the portfolio's Download CV buttons.

NOT IN USE since 2026-11-19: the site ships Emmanuel's own resume PDF as he sent it (portimg/Emmanuel-Nortey-CV.pdf).
Running this script overwrites that file, so only run it if he asks for a generated CV again.

Content is Emmanuel's own resume of 2026-11-19 (Downloads, "Emmanuel Nii Yeboah Nortey Resume.pdf"), with its typos
fixed and no dashes, in line with the site's copy rules. The project table stays in PROJECTS for the tailored CV in
~/Desktop/ego/cv-tailored, but this page no longer lists it. The page uses the site's
type (Glancyr Neue for headings, Roboto Flex for text) and its coral accent, on white so it prints well.

Usage: python3 -I make_cv.py  (writes ../portimg/Emmanuel-Nortey-CV.pdf)
"""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "portimg", "Emmanuel-Nortey-CV.pdf")
FONT = os.path.join(HERE, "..", "..", "wp-content/themes/evne/assets/fonts/glancyr/Glancyr-Neue-Regular.otf")  # the built site's copy
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PROJECTS = [  # (name, address, what it is, built with, my part)
    ("Agorivia", "agorivia.co", "Operations support for UK therapists, private clinics, care providers and founders", "Figma, WordPress, Elementor", "Figma design and WordPress build"),
    ("Dr. Emele Arthur-Hayford", "emelearthurhayford.com", "Personal site for a scientist working on health equity", "Figma, WordPress, Elementor", "Figma design and WordPress build"),
    ("Netra Technologies GH", "netratechnologiesgh.com", "IT services company with an online shop and checkout", "WordPress, WooCommerce", "Design and build"),
    ("Strategic &amp; Agile", "strategicandagile.com", "Human capital and HR consultancy in Accra", "WordPress, Elementor", "Design and build"),
    ("World Movers Team", "worldmoversteam.org", "NGO run by young people for health equity, with donations and a newsletter", "WordPress, Elementor", "Design and build"),
    ("Creative Click Multimedia", "creativeclickmultimedia.com", "Software agency site in seven languages", "Next.js", "Build"),
    ("The Weekend Chef", "weekendchefgh.com", "Homemade meals to order in Greater Accra, with online payment and chef registration", "WordPress, Elementor, Paystack", "Design and build"),
    ("Mawuena Datsa Foundation", "mawuenadatsafoundation.org", "Foundation for education, health, rescue and mentoring", "WordPress, Astra", "Build and maintenance"),
    ("Hadassah Foundation", None, "NGO run by young people in Ghana", "WordPress, then a static HTML and CSS rebuild", "Build and maintenance"),
]

JOBS = [  # (role, place, dates, points)
    ("WordPress developer", "Theme Wire, Ghana", "01/2026 to now", [
        "Build new WordPress sites, custom themes and templates, and write plugins in PHP when a client needs something no existing plugin does.",
        "Look after live client sites: updates, plugin changes and fixes when something stops working.",
    ]),
    ("Freelance WordPress and Elementor developer", "Accra and remote", "Current", [
        "Built eight live sites in WordPress, Elementor and WooCommerce for NGOs, consultancies and service businesses in Ghana and the UK, "
        "including an online shop with checkout and a meal ordering site that takes Paystack payments.",
        "Design each site in Figma first, then build it in Elementor Pro with responsive layouts that work on phones, tablets and desktops.",
        "Run every project myself, from the first call with the client through the build, the launch, and showing their team how to update the site.",
        "Before launch, set up Yoast or Rank Math, connect the site to Google Search Console and Analytics, and compress images and add caching so pages load quickly.",
        "Set up hosting, domains and SSL, move sites to new hosts, and look after backups and DNS.",
        "Still maintain sites after launch, such as the Mawuena Datsa Foundation and Hadassah Foundation.",
    ]),
    ("Technician", "KA Technologies, Accra", "02/2022 to now", [
        "Find and fix hardware and software faults, and support operating systems, applications and networks.",
    ]),
    ("IT support and technical services (national service)", "University of Ghana, Legon", "09/2020 to 11/2021", [
        "Ran the ICT lab and supported over 500 students and staff with network, system and printer problems.",
    ]),
    ("Operations manager", "Jumeni Technologies, East Legon", "07/2021 to 08/2021", [
        "Ran daily operations and onboarded new customers, and designed the company's marketing material and graphics.",
    ]),
    ("Intern, graphic design and web development", "MEST Africa (Jumeni Technologies), East Legon", "06/2019 to 07/2019", [
        "Learned web development with HTML, CSS, JavaScript and WordPress on real projects, and helped make existing sites faster.",
    ]),
]

SKILLS = [
    ("WordPress", "Elementor and Elementor Pro, WooCommerce, custom themes and templates, custom plugins in PHP, plugin setup and "
                  "integration, Paystack payments, responsive design, troubleshooting, maintenance"),
    ("Speed and SEO", "Yoast, Rank Math, Google Search Console, Google Analytics, image compression, caching, page speed"),
    ("Front end", "HTML, CSS, JavaScript, Next.js, responsive layouts"),
    ("Design", "Figma, Adobe Photoshop, Illustrator, Canva, marketing graphics"),
    ("Hosting", "Hosting and domain setup, SSL, site migrations, backups, DNS"),
    ("Working style", "Remote work with clients in Ghana and the UK, managing several projects at once, "
                      "explaining technical problems in plain language"),
]

CERTS = [
    ("Foundations of User Experience (UX) Design", "Google, via Coursera"),
    ("JavaScript Basics", "Google, via Coursera"),
    ("Technical Support Fundamentals", "Google, via Coursera"),
    ("Cybersecurity Operations", "Ghana&#8209;India Kofi Annan Centre of Excellence in ICT (GI&#8209;KACE)"),
]

CSS = """
@font-face { font-family: Glancyr; src: url("file://%s"); }
@page { size: A4; margin: 13mm 15mm 11mm; }
* { box-sizing: border-box; }
body { margin: 0; font: 400 9pt/1.4 "Roboto Flex", system-ui, sans-serif; color: #2a2b30; }
h1, h2, h3 { font-family: Glancyr, sans-serif; font-weight: 400; color: #0a0b0e; margin: 0; }
h1 { font-size: 25pt; line-height: 1.05; letter-spacing: -.01em; }
h1 span { color: #f87060; }
.role { margin: 6pt 0 0; font-size: 10.5pt; color: #0a0b0e; }
.contact { margin: 6pt 0 0; color: #5d5f66; }
.contact a { color: inherit; text-decoration: none; }
header { padding-bottom: 10pt; border-bottom: 1.5pt solid #f87060; margin-bottom: 4pt; }
h2 { font-size: 11.5pt; margin: 10pt 0 4pt; display: flex; align-items: center; gap: 8pt; }
h2::before { content: ""; width: 6pt; height: 6pt; border-radius: 50%%; background: #f87060; }
p { margin: 0; }
.profile { font-size: 9.4pt; color: #2a2b30; }
table { width: 100%%; border-collapse: collapse; }
td { padding: 3.2pt 6pt 3.2pt 0; vertical-align: top; border-bottom: .5pt solid #e4e5e8; }
td.name { width: 27%%; font-weight: 600; color: #0a0b0e; }
td.name small { display: block; font-weight: 400; color: #8a8c93; font-size: 8pt; }
td.with { width: 22%%; color: #5d5f66; }
td.part { width: 18%%; color: #5d5f66; }
.job { margin: 0 0 5.5pt; break-inside: avoid; }
.job-head { display: flex; justify-content: space-between; gap: 12pt; }
.job h3 { font-size: 10.2pt; }
.job .where { color: #5d5f66; }
.job .when { color: #f87060; white-space: nowrap; font-weight: 500; }
ul { margin: 3pt 0 0; padding-left: 12pt; }
li { margin: .8pt 0; }
li::marker { color: #f87060; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0 22pt; }
.skill { margin: 0 0 4pt; break-inside: avoid; }
table.certs td.name { width: 40%%; }
.skill b { color: #0a0b0e; font-weight: 600; }
.product { break-inside: avoid; }
.foot { margin-top: 10pt; color: #8a8c93; font-size: 8.5pt; }
"""


def html():
    jobs = "".join(
        "<div class='job'><div class='job-head'><div><h3>%s</h3><span class='where'>%s</span></div><span class='when'>%s</span></div>"
        "<ul>%s</ul></div>" % (role, where, when, "".join("<li>%s</li>" % p for p in points)) for role, where, when, points in JOBS)
    skills = "".join("<p class='skill'><b>%s:</b> %s</p>" % s for s in SKILLS)
    certs = "".join("<p class='skill'><b>%s</b><br>%s</p>" % c for c in CERTS)
    return """<!doctype html><html><head><meta charset="utf-8"><title>Emmanuel Nortey CV</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,400;8..144,500;8..144,600&display=swap">
<style>%s</style></head><body>
<header>
  <h1>Emmanuel Nii Yeboah Nortey<span>.</span></h1>
  <p class="role">WordPress and Elementor Pro developer &middot; Web designer</p>
  <p class="contact"><a href="mailto:enortey96@gmail.com">enortey96@gmail.com</a> &middot; +233 24 633 7881 &middot; Accra, Ghana</p>
</header>
<h2>Summary</h2>
<p class="profile">A WordPress developer with a track record of delivering eight live websites for NGOs, consultancies, and service
businesses in Ghana and the UK. Skilled in designing user focused experiences in Figma and building responsive WordPress sites and
e&#8209;commerce solutions with Elementor Pro and WooCommerce, including online shops and payment enabled ordering systems.
Experienced in developing custom plugins and configuring SEO, image optimization, and caching to support site performance.
Adept at working remotely with UK clients and managing projects independently from discovery through launch.</p>
<h2>Experience</h2>
%s
<h2>Education</h2>
<div class="job"><div class="job-head"><div><h3>BSc, Information Technology</h3><span class="where">Kwame Nkrumah University of Science and Technology (KNUST)</span></div><span class="when">10/2022</span></div></div>
<div class="job"><div class="job-head"><div><h3>Diploma, Information Technology</h3><span class="where">Kwame Nkrumah University of Science and Technology (KNUST)</span></div><span class="when">09/2020</span></div></div>
<div style="break-inside: avoid"><h2>Skills</h2>
<div class="grid2">%s</div></div>
<h2>Certifications</h2>
<div class="grid2">%s</div>
</body></html>""" % (CSS % FONT, jobs, skills, certs)

if __name__ == "__main__":
    src = os.path.join(HERE, "cv.html")
    open(src, "w", encoding="utf-8").write(html())
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--user-data-dir=" + os.path.join(HERE, ".profile"),
                    "--allow-file-access-from-files", "--virtual-time-budget=5000", "--no-pdf-header-footer",
                    "--print-to-pdf=" + os.path.abspath(OUT), "file://" + src], check=True, capture_output=True)
    print("cv", os.path.abspath(OUT), os.path.getsize(OUT))
