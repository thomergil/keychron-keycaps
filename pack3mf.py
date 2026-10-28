"""Pack cap + inlay STL pairs into a 3MF: one object per key, each with two parts."""
import os, sys, zipfile, trimesh

COLORS = {"cap": "#1A1A1AFF", "inlay": "#F0F0F0FF"}

def mesh_xml(oid, name, m, pindex):
    v = "".join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in m.vertices)
    t = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in m.faces)
    return (f'<object id="{oid}" name="{name}" type="model" pid="1" pindex="{pindex}">'
            f'<mesh><vertices>{v}</vertices><triangles>{t}</triangles></mesh></object>')

def pack(out, keys, stl_dir, gap=4, bed=220):
    """Place keys left to right in rows no wider than bed (mm). A key without inlay_<key>.stl is blank."""
    objs, build, oid = [], [], 2
    x = y = row_d = 0
    for k in keys:
        comps, lo, hi = [], None, None
        for j, part in enumerate(["cap", "inlay"]):
            path = f"{stl_dir}/{part}_{k}.stl"
            if not os.path.exists(path):
                continue
            m = trimesh.load(path)
            if part == "cap":
                (lo, hi) = m.bounds[0][:2], m.bounds[1][:2]
            objs.append(mesh_xml(oid, f"{k} {part}", m, j)); comps.append(oid); oid += 1
        c = "".join(f'<component objectid="{i}"/>' for i in comps)
        objs.append(f'<object id="{oid}" name="{k}" type="model"><components>{c}</components></object>')
        w, d = hi - lo
        if x and x + w > bed:
            x, y, row_d = 0, y - row_d - gap, 0
        tx, ty = x - lo[0], y - hi[1]
        build.append(f'<item objectid="{oid}" transform="1 0 0 0 1 0 0 0 1 {tx:.4f} {ty:.4f} 0"/>'); oid += 1
        x, row_d = x + w + gap, max(row_d, d)
    mats = "".join(f'<base name="{p}" displaycolor="{c}"/>' for p, c in COLORS.items())
    model = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<resources><basematerials id="1">{mats}</basematerials>{"".join(objs)}</resources>'
             f'<build>{"".join(build)}</build></model>')
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr("_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr("3D/3dmodel.model", model)

if __name__ == "__main__":
    # pack3mf.py <stl_dir> <out.3mf> <key> [<key> ...]; reads cap_<key>.stl and, if present, inlay_<key>.stl
    stl_dir, out, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
    pack(out, keys, stl_dir)
