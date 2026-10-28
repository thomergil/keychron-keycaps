"""Render keycaps with ink-centered legends and pack them into two-color 3MFs.

Examples:
  python build.py                          # every key in every variant, into keys/
  python build.py u h f j                  # one 3MF with U H F J, dished, no bumps
  python build.py u h f j --bump u h       # bumps on U and H only
  python build.py space --flat --bump      # one flat spacebar with a bump
Key ids are listed in layout.py. Needs openscad (with --enable=manifold) on PATH, or $OPENSCAD, and trimesh.
"""
import argparse, os, subprocess, sys, tempfile, trimesh
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pack3mf import pack
from layout import ICON_FONT, STAB, keys

SCAD = os.path.join(HERE, "keycap.scad")
OPENSCAD = os.environ.get("OPENSCAD", "openscad")
VARIANTS = {"flat": (True, False), "flat-bump": (True, True), "dished": (False, False), "dished-bump": (False, True)}

TOP_W, PITCH, MARGIN = 14.0, 19.05, 2.5  # keycap.scad top_w and pitch; legend inset from the top edge
ICON_H = {False: 4.5, True: 3.6}  # symbol ink height (mm): alone on the key, or as one of two lines
ICON_W = 6.0                      # symbol ink width limit (mm)


def render(part, defs, out):
    args = [OPENSCAD, "-q", "--enable=manifold", "-D", f'part="{part}"']
    for k, v in defs.items():
        if isinstance(v, str):
            v = '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
        args += ["-D", f"{k}={v}"]
    subprocess.run(args + ["-o", out, SCAD], check=True)


def font_for(s):
    return ICON_FONT if any(ord(c) > 127 for c in s) else "DejaVu Sans:style=Book"


def legend_defs(units, legend, legend2, work, kid):
    """Fonts, sizes and ink-centering offsets for both legend lines, shrunk to fit the top."""
    defs = {"units": units, "legend": legend, "legend2": legend2}
    max_w = TOP_W + (units - 1) * PITCH - 2 * MARGIN
    for n, (key, text) in enumerate([("legend", legend), ("legend2", legend2)], 1):
        if not text:
            continue
        size = 4 if len(text) == 1 and not legend2 else 3
        font = font_for(text)
        probe = f"{work}/probe_{kid}_{n}.stl"
        render("probe", {**defs, "probe_line": n, f"{key}_size": size, f"{key}_font": font}, probe)
        b = trimesh.load(probe).bounds
        # Symbol glyphs vary in size within their em box; scale them to a fixed ink height.
        w, h = b[1][:2] - b[0][:2]
        k = min(ICON_H[bool(legend2)] / h, ICON_W / w) if font == ICON_FONT else 1.0
        k = min(k, max_w / w)
        defs[f"{key}_size"] = round(float(size * k), 3)
        defs[f"{key}_font"] = font
        defs[f"{key}_dx"] = round(float(-k * (b[0][0] + b[1][0]) / 2), 4)
        defs[f"{key}_dy"] = round(float(-k * (b[0][1] + b[1][1]) / 2), 4)
    if units in STAB:
        defs["stab"] = STAB[units]
    return defs


def build_key(kid, units, legend, legend2, flat, bump, work):
    """Render cap_<kid>.stl and, if the key has a legend, inlay_<kid>.stl into work."""
    defs = legend_defs(units, legend, legend2, work, kid)
    defs["homing"] = "dot" if bump else "none"
    if flat:
        defs["dish_depth"] = 0
    render("cap", defs, f"{work}/cap_{kid}.stl")
    if legend or legend2:
        render("inlay", defs, f"{work}/inlay_{kid}.stl")


def build_all(out_dir, jobs):
    todo = [(v, r, kid, u, leg, leg2) for v in VARIANTS for r, kid, u, leg, leg2 in keys()]
    with tempfile.TemporaryDirectory() as work:
        def one(t):
            v, r, kid, u, leg, leg2 = t
            d = f"{work}/{v}/{kid}"
            os.makedirs(d)
            build_key(kid, u, leg, leg2, *VARIANTS[v], d)
            os.makedirs(f"{out_dir}/{v}", exist_ok=True)
            pack(f"{out_dir}/{v}/r{r}-{kid}.3mf", [kid], d)
            return f"{v}/r{r}-{kid}.3mf"
        with ThreadPoolExecutor(jobs) as ex:
            for name in ex.map(one, todo):
                print(name, flush=True)


def main():
    ap = argparse.ArgumentParser(description="Build keycaps into 3MFs.")
    ap.add_argument("keys", nargs="*", help="key ids from layout.py; none = every key in every variant into keys/")
    ap.add_argument("--flat", action="store_true", help="flat top instead of a spherical dish")
    ap.add_argument("--bump", nargs="*", help="add a homing bump; give key ids to limit it to those keys")
    ap.add_argument("-o", "--out", help="output 3MF (default k3-caps-<keys>[-flat].3mf), or directory with no keys (default keys)")
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count(), help="parallel renders")
    a = ap.parse_args()
    if not a.keys:
        build_all(a.out or os.path.join(HERE, "keys"), a.jobs)
        return
    a.keys = [k.lower() for k in a.keys]
    a.bump = a.bump and [k.lower() for k in a.bump]
    layout = {kid: (u, leg, leg2) for _, kid, u, leg, leg2 in keys()}
    unknown = [k for k in a.keys + (a.bump or []) if k not in layout]
    if unknown:
        ap.error(f"unknown key ids: {' '.join(unknown)}")
    bumped = set(a.keys if a.bump == [] else a.bump or [])
    out = a.out or f"k3-caps-{'-'.join(a.keys)}{'-flat' if a.flat else ''}.3mf"
    with tempfile.TemporaryDirectory() as work:
        with ThreadPoolExecutor(a.jobs) as ex:
            list(ex.map(lambda k: build_key(k, *layout[k], a.flat, k in bumped, work), a.keys))
        pack(out, a.keys, work)
    print(out)


if __name__ == "__main__":
    main()
