"""World maps for the homepage, built from Natural Earth 1:110m data (world-atlas@2.0.2, in mapdata/).

  portimg/world-dots.svg       dotted land (a dot pattern clipped to the land shape), behind the testimonials
  portimg/world-countries.svg  country shapes with light borders, behind the contact form
  portimg/globe-land.js        points spread evenly over the sphere that fall on land, for the hero globe

Usage: python3 -I maps.py <mapdata dir>
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = sys.argv[1]
OUT = os.path.join(HERE, "portimg")
W = 1000                      # SVG width; Miller projection, latitudes 60S to 84N
LAT_MIN, LAT_MAX = -60, 84


def decode(topo, name):
    """Polygons (lists of rings of (lon, lat)) per geometry of the named object."""
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x, y = x + dx, y + dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(indexes):
        pts = []
        for i in indexes:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(a[1:] if pts else a)
        # Rings that cross the date line (Russia, Fiji) jump by ~360 degrees: unwrap them into one run
        out, shift = [pts[0]], 0
        for (x0, _), (x1, y1) in zip(pts, pts[1:]):
            if x1 - x0 > 180:
                shift -= 360
            elif x0 - x1 > 180:
                shift += 360
            out.append((x1 + shift, y1))
        return out

    out = []
    for g in topo["objects"][name]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]] if g["type"] == "Polygon" else []
        out.append([[ring(r) for r in poly] for poly in polys])
    return out


def miller_y(lat):
    return 1.25 * math.log(math.tan(math.pi / 4 + 0.4 * math.radians(lat)))


Y_TOP, Y_BOTTOM = miller_y(LAT_MAX), miller_y(LAT_MIN)
SCALE = W / (2 * math.pi)
H = round((Y_TOP - Y_BOTTOM) * SCALE)


def project(lon, lat):
    lat = max(LAT_MIN, min(LAT_MAX, lat))
    return (lon + 180) / 360 * W, (Y_TOP - miller_y(lat)) * SCALE


def path(polys):
    d = []
    for poly in polys:
        if max(lat for r in poly for _, lat in r) < LAT_MIN + 2:   # Antarctica, cut off by the crop
            continue
        for r in poly:
            lons = [lon for lon, _ in r]
            # An unwrapped ring that runs past the date line is drawn again from the other side
            for offset in [0] + ([-360] if max(lons) > 180 else []) + ([360] if min(lons) < -180 else []):
                pts = [project(lon + offset, lat) for lon, lat in r]
                d.append("M" + "L".join("%.1f %.1f" % p for p in pts) + "Z")
    return "".join(d)


def inside(lon, lat, polys):
    return any(inside_one(lon + o, lat, polys) for o in (0, -360, 360))


def inside_one(lon, lat, polys):
    hit = False
    for poly in polys:
        for r in poly:
            j = len(r) - 1
            for i in range(len(r)):
                (xi, yi), (xj, yj) = r[i], r[j]
                if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
                    hit = not hit
                j = i
    return hit


land = decode(json.load(open(os.path.join(DATA, "land-110m.json"))), "land")
countries = decode(json.load(open(os.path.join(DATA, "countries-110m.json"))), "countries")
land_polys = [p for g in land for p in g]

# Dotted land: a dot pattern clipped to the land outline keeps the file small
open(os.path.join(OUT, "world-dots.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">'
    '<defs><pattern id="d" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.25" fill="#fff"/></pattern>'
    '<clipPath id="l"><path d="%s"/></clipPath></defs>'
    '<rect width="%d" height="%d" fill="url(#d)" clip-path="url(#l)"/></svg>' % (W, H, path(land_polys), W, H))

# Country shapes: dark fill, hairline borders
open(os.path.join(OUT, "world-countries.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><g fill="#2a2a2e" stroke="#6b6b72" stroke-width=".5" stroke-linejoin="round">%s</g></svg>'
    % (W, H, "".join('<path d="%s"/>' % path(g) for g in countries if g)))

# Globe: a Fibonacci sphere (even spacing), kept where the point is on land; "lon,lat" in tenths of a degree
N, points = 9000, []
golden = math.pi * (3 - math.sqrt(5))
for i in range(N):
    z = 1 - 2 * (i + 0.5) / N
    lat = math.degrees(math.asin(z))
    lon = (math.degrees(i * golden) + 180) % 360 - 180
    if lat > -60 and inside(lon, lat, land_polys):
        points.append("%d,%d" % (round(lon * 10), round(lat * 10)))
open(os.path.join(OUT, "globe-land.js"), "w").write(
    "/* Land points for the hero globe (Natural Earth 1:110m), lon,lat in tenths of a degree. Built by maps.py. */\n"
    'window.DN_GLOBE_LAND="%s";\n' % " ".join(points))
print("map %dx%d, globe points %d" % (W, H, len(points)))
