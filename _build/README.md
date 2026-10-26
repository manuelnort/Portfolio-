# How the portfolio is built

The site in the folder above is generated. Don't edit the HTML there by hand; change the scripts here and rebuild.

It starts from a static copy of the original WordPress theme site, kept at `~/Desktop/ego/diginort`.
`portfolio.py` copies that into `~/Desktop/ego/portfolio` and rewrites it into this portfolio: copy, images,
the story chapters, the footer, the floating menu and so on. Every replacement says how many times the
original text must appear, so a change in the source can't be skipped without the build stopping.

## Rebuild the site

```
cd ~/Desktop/ego/portfolio/_build
python3 -I portfolio.py
```

The build clears the site folder first but leaves `.git`, `.gitignore` and `_build` alone.
Then commit and push from `~/Desktop/ego/portfolio` as usual.

Needs Python 3 and Google Chrome (the image and CV scripts render with headless Chrome). The QA helpers need Node 22 or later.

## What's here

| Path | What it is |
| --- | --- |
| `portfolio.py` | The build. Page by page edits, plus the hero, chapters, testimonials, contact, footer and menu markup |
| `assets/portfolio.css`, `assets/portfolio.js` | Everything added on top of the theme: backdrop, type scale, globe, scroll effects, menu |
| `portimg/` | Prepared images, copied into the site as `wp-content/uploads/portfolio/` (only the ones a page uses ship) |
| `brand/` | Name wordmarks, the EN mark and site icons |
| `logos/`, `logos-orig/` | Client logos (trimmed and original) |
| `art.py` | Logo artwork on the About page (`art-*.jpg`), rendered with Chrome |
| `projects.py`, `projects/` | Work card and gallery photos, cropped from photos on each client's site (`harvest.py` downloads them) |
| `make_images.py`, `shots/`, `certs/`, `cards/` | Certificate and experience cards and older crops from site screenshots |
| `maps.py`, `mapdata/` | Dotted world map, country map and globe points (Natural Earth data from world-atlas) |
| `toolsrc/` | Tool logos for "What I work with" (Devicon and Simple Icons) |
| `cv/make_cv.py` | The downloadable CV, written to `portimg/Emmanuel-Nortey-CV.pdf` |
| `textscan.py` | Lists any emoji or dashes left in the built pages' text |
| `shoot.mjs`, `walk.mjs`, `crop.mjs`, `trim.mjs`, `imgs.mjs`, `sheet.py` | Screenshot, crop and contact sheet helpers used for checking the site |
| `clone/` | The scripts that made the static copy of the WordPress site in the first place (they need that local site running) |

## Regenerating images

```
python3 -I art.py art-about-main.jpg          # one image, or no names for all of them
python3 -I projects.py netra                  # one project's photos
python3 -I maps.py mapdata
python3 -I cv/make_cv.py
```

Run `python3 -I portfolio.py` afterwards so the site picks them up.
