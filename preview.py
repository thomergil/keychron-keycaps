"""Render the README images in docs/ from keys/: a top view per layout, an angled view, and one cap from below.

  python preview.py
Needs openscad (or $OPENSCAD) and, on a headless machine, xvfb-run.
"""
import os, re, shutil, subprocess, sys, tempfile, zipfile
import numpy as np, trimesh
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from layout import LAYOUTS, keys, rows

OPENSCAD = os.environ.get("OPENSCAD", "openscad")
PITCH = 19.05
ROW_OF = {kid: r for r, kid, *_ in keys()}
OBJ = re.compile(r'name="[^"]* (cap|inlay)" type="model" pid[^>]*><mesh><vertices>(.*?)</vertices>'
                 r'<triangles>(.*?)</triangles>')


def parts(path):
    """Meshes in a key 3MF written by pack3mf, by part name."""
    model = zipfile.ZipFile(path).read("3D/3dmodel.model").decode()
    out = {}
    for part, v, t in OBJ.findall(model):
        v = np.array(re.findall(r'x="([-\d.]+)" y="([-\d.]+)" z="([-\d.]+)"', v), float)
        t = np.array(re.findall(r'v1="(\d+)" v2="(\d+)" v3="(\d+)"', t), int)
        out[part] = trimesh.Trimesh(v, t, process=False)
    return out


def assemble(layout, variant, work):
    """Write the whole keyboard as cap.stl and inlay.stl; return the scene .scad."""
    meshes = {"cap": [], "inlay": []}
    for r, row in enumerate(rows(layout)):
        x = 0
        for kid in row:
            u = next(k[2] for k in keys() if k[1] == kid)
            for part, m in parts(f"{HERE}/keys/{variant}/r{ROW_OF[kid]}-{kid}.3mf").items():
                m.apply_translation([x + u * PITCH / 2, -r * PITCH, 0])
                meshes[part].append(m)
            x += u * PITCH
    for part, ms in meshes.items():
        trimesh.util.concatenate(ms).export(f"{work}/{part}.stl")
    return write_scene(work)


def single(kid, variant, work):
    """Write one key as cap.stl and inlay.stl; return the scene .scad."""
    for part, m in parts(f"{HERE}/keys/{variant}/r{ROW_OF[kid]}-{kid}.3mf").items():
        m.export(f"{work}/{part}.stl")
    return write_scene(work, "#a0a0a0")


def write_scene(work, cap_color="#3a3a3a"):
    scad = f"{work}/scene.scad"
    with open(scad, "w") as f:
        f.write(f'color("{cap_color}") import("cap.stl");\ncolor("#f0f0f0") import("inlay.stl");\n')
    return scad


def shoot(scad, out, size, camera, ortho):
    cmd = [OPENSCAD, f"--imgsize={size}", f"--camera={camera}", "--colorscheme=Tomorrow", "-o", out, scad]
    if ortho:
        cmd.insert(1, "--projection=o")
    if shutil.which("xvfb-run") and not os.environ.get("DISPLAY"):
        cmd = ["xvfb-run", "-a"] + cmd
    subprocess.run(cmd, check=True, capture_output=True)
    im = Image.open(out).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
    l, t, r, b = ImageChops.difference(im, bg).getbbox()
    im = im.crop((max(l - 20, 0), max(t - 20, 0), min(r + 20, im.width), min(b + 20, im.height)))
    im.thumbnail((1600, 1600))
    im.save(out, optimize=True)


def slug(name):
    return re.sub(r"[^a-z]+", "-", name.lower()).strip("-")


def main():
    os.makedirs(f"{HERE}/docs", exist_ok=True)
    with tempfile.TemporaryDirectory() as work:
        for name in LAYOUTS:
            shoot(assemble(name, "flat", work), f"{HERE}/docs/{slug(name)}.png",
                  "2400,900", "152.4,-47.6,60,0,0,0,330", True)
            print(f"docs/{slug(name)}.png")
        shoot(assemble("QWERTY (macOS)", "dished-bump", work), f"{HERE}/docs/dished-bump.png",
              "2400,1100", "152.4,-52,0,50,0,0,330", False)
        print("docs/dished-bump.png")
        shoot(single("f", "dished", work), f"{HERE}/docs/underside.png",
              "1200,1000", "30,-38,-30,0,0,2.5", False)
        print("docs/underside.png")


if __name__ == "__main__":
    main()
