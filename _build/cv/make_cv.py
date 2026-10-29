"""Public CV as a PDF for the portfolio's Download CV buttons.

Content is the version tailored on 2026-10-29 for WordPress development and client support work (hosting, SEO and
sign up form work as Emmanuel confirmed it), with the job ad's training line made general; no dashes, in line with
the site's copy rules. The page uses the site's
type (Glancyr Neue for headings, Roboto Flex for text) and its coral accent, on white so it prints well.

Usage: python3 -I make_cv.py  (writes ../portimg/Emmanuel-Nortey-CV.pdf)
"""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "portimg", "Emmanuel-Nortey-CV.pdf")
FONT = "/Users/manuelnort/Desktop/ego/diginort/wp-content/themes/evne/assets/fonts/glancyr/Glancyr-Neue-Regular.otf"
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
        "Build new WordPress sites, custom themes and templates, and write plugins when a client needs something no existing plugin does.",
        "Look after live client sites: updates, plugin changes and fixes when something stops working.",
    ]),
    ("Freelance WordPress developer", "Accra and remote", "Current", [
        "Built eight live sites in WordPress, Elementor and WooCommerce for NGOs, consultancies and service businesses in Ghana and the UK, "
        "including an online shop with checkout and a meal ordering site that takes Paystack payments.",
        "Run every project on my own, from the first call with the client and the Figma designs through the build, the launch, "
        "and showing their team how to update the site.",
        "Set up hosting, domains and SSL for client sites, move sites to new hosts when they outgrow the old one, "
        "and look after backups, DNS and business email accounts.",
        "Before launch I set up Yoast or Rank Math, connect the site to Google Search Console and Analytics, and compress images "
        "and add caching so pages load quickly. Where a client sends newsletters, I connect the sign up forms to their email list.",
        "Still support several clients after launch, such as the Mawuena Datsa Foundation and Hadassah Foundation, whose sites I maintain.",
    ]),
    ("Technician", "KA Technologies, Accra", "02/2022 to now", [
        "Find and fix hardware and software faults, and support operating systems, applications and networks.",
        "Run diagnostics and performance tuning; machines usually come back about 20% faster, with fewer failures.",
    ]),
    ("IT support and technical services (national service)", "University of Ghana, Legon", "09/2020 to 11/2021", [
        "Ran the ICT lab and was the person over 500 students and staff came to when their tech broke, "
        "from network connections and system crashes to printers.",
        "Set up hardware, peripherals and software, and explained fixes in plain language so people could keep working.",
    ]),
    ("Operations manager", "Jumeni Technologies, East Legon", "07/2021 to 08/2021", [
        "Ran daily operations and onboarded new customers, which kept more of them coming back.",
        "Designed the company's marketing material and graphics.",
    ]),
    ("Intern, graphic design and web development", "MEST Africa (Jumeni Technologies), East Legon", "06/2019 to 07/2019", [
        "Learned web development with HTML, CSS, JavaScript and WordPress on real projects, and helped make existing sites faster.",
    ]),
    ("IT support specialist", "Christ Cares", "", [
        "Diagnosed software and hardware problems and did routine maintenance to prevent downtime.",
    ]),
]

SHOWN = ("Netra Technologies GH", "The Weekend Chef", "World Movers Team", "Strategic &amp; Agile", "Agorivia",
         "Mawuena Datsa Foundation")  # the projects the CV lists

SKILLS = [
    ("WordPress", "New builds, Elementor, WooCommerce, custom themes and templates, writing plugins, setting up and updating plugins, "
                  "Paystack payments, speed, security, maintenance"),
    ("Client support", "Helpdesk and walk in support, onboarding new clients, explaining problems without jargon, "
                       "teaching client teams to update their own sites"),
    ("Hosting and SEO", "Hosting and domain setup, SSL, site migrations, backups, DNS and business email, Yoast, Rank Math, "
                        "Google Search Console and Analytics, image compression, caching"),
    ("Systems and networks", "Hardware and software troubleshooting, operating systems, network setup, security and data protection"),
    ("Web development", "HTML, CSS, JavaScript, Next.js, responsive layouts, Chrome extensions, Figma plugins"),
    ("Design and marketing", "Figma, Adobe Photoshop, Illustrator, Canva, marketing graphics, newsletter sign up forms linked to email lists"),
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
    projects = "".join(
        "<tr><td class='name'>%s%s</td><td>%s</td><td class='with'>%s</td><td class='part'>%s</td></tr>"
        % (name, "<small>%s</small>" % site if site else "", what, built, part) for name, site, what, built, part in PROJECTS if name in SHOWN)
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
  <p class="role">WordPress developer &middot; Client and technical support</p>
  <p class="contact"><a href="mailto:enortey96@gmail.com">enortey96@gmail.com</a> &middot; +233 24 633 7881 &middot; North Kaneshie, Accra, Ghana &middot; <a href="https://manuelnort.github.io/Portfolio-/">manuelnort.github.io/Portfolio-</a></p>
</header>
<h2>Profile</h2>
<p class="profile">I'm a WordPress developer at Theme Wire, where I build sites, custom themes and templates and write plugins
when a site needs one. Before that I spent years in IT support, the person students, staff and customers came to when something
stopped working, so talking a client through a problem is as normal to me as fixing it. On my own I've built eight live client
sites and run each one from the first call to launch, and I still look after several of them. I'd like a job where the
development and the client work sit together. I already handle hosting, migrations and the SEO setup on my own projects.
Email campaigns are the part I've done least, and the next thing I want to get good at.</p>
<h2>Experience</h2>
%s
<div style="break-inside: avoid"><h2>Selected WordPress work</h2>
<table>%s</table></div>
<h2>Skills</h2>
<div class="grid2">%s</div>
<h2>Education</h2>
<div class="job"><div class="job-head"><div><h3>BSc Information Technology</h3><span class="where">Kwame Nkrumah University of Science and Technology (KNUST)</span></div><span class="when">10/2022</span></div></div>
<div class="job"><div class="job-head"><div><h3>Diploma in Information Technology</h3><span class="where">Kwame Nkrumah University of Science and Technology (KNUST)</span></div><span class="when">09/2020</span></div></div>
<h2>Certificates</h2>
<div class="grid2">%s</div>
<p class="foot">References available on request.</p>
</body></html>""" % (CSS % FONT, jobs, projects, skills, certs)


if __name__ == "__main__":
    src = os.path.join(HERE, "cv.html")
    open(src, "w", encoding="utf-8").write(html())
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--user-data-dir=" + os.path.join(HERE, ".profile"),
                    "--allow-file-access-from-files", "--virtual-time-budget=5000", "--no-pdf-header-footer",
                    "--print-to-pdf=" + os.path.abspath(OUT), "file://" + src], check=True, capture_output=True)
    print("cv", os.path.abspath(OUT), os.path.getsize(OUT))
