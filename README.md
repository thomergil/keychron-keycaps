# Keychron K3 Ultra keycaps

3D-printable LSA keycaps for the [Keychron K3 Ultra 8K](https://www.keychron.com/products/keychron-k3-ultra-8k-wireless-custom-mechanical-keyboard) (ANSI). Two-color legends.

### QWERTY (macOS)
![QWERTY, macOS](docs/qwerty-macos.png)

### QWERTY (Windows)
![QWERTY, Windows](docs/qwerty-windows.png)

### Dvorak (macOS)
![Dvorak, macOS](docs/dvorak-macos.png)

### Dished, with homing bumps
![Dished, with homing bumps](docs/dished-bump.png)

## Compatibility

Fits the [K3 Ultra 8K](https://www.keychron.com/products/keychron-k3-ultra-8k-wireless-custom-mechanical-keyboard). Should fit the [K3 Pro](https://www.keychron.com/products/keychron-k3-pro-qmk-via-wireless-custom-mechanical-keyboard) and [K3 Max](https://www.keychron.com/products/keychron-k3-max-qmk-via-wireless-custom-mechanical-keyboard), which take the [same keycaps](https://www.keychron.com/products/black-transparent-low-profile-lsa-full-set-keycap-set). Does not fit the original [K3](https://www.keychron.com/products/keychron-k3-wireless-mechanical-keyboard) (offset stabilizer stems).

## Files

`keys/<variant>/r<row>-<key>.3mf`. Key ids: [`layout.py`](layout.py).

| Variant | Top | Homing bump |
|---|---|---|
| `flat` | flat | no |
| `flat-bump` | flat | yes |
| `dished` | 0.4 mm spherical dish | no |
| `dished-bump` | 0.4 mm spherical dish | yes |

Each 3MF has two parts, `cap` and `inlay` (legend). Assign a filament to each. Exported stem down.

Includes macOS (`option`, `⌘`) and Windows (`win`, `alt`) modifiers. Every row has the same profile, so any layout uses the same files.

## Homing ridge

Bump: 1.65 mm wide, 0.33 mm tall, 10% larger than stock.

Better: print without a bump, add a tiny drop of resin with a toothpick, let it cure. Smoother than any print.

## Dimensions

| | |
|---|---|
| Key pitch | 19.05 mm |
| 1u skirt | 17.8 × 17.8 mm |
| 1u top | 14.0 mm |
| Height, front / back | 4.6 / 3.7 mm |
| Stem below skirt | 2.0 mm |
| Cross socket | 4.15 × 1.27 mm, 3.8 mm deep |
| Stabilizer stems | ±11.938 mm (2u, 2.25u), ±50 mm (6.25u) |

Stabilizer spacing is Cherry standard, not measured. Print backspace first.

## Building

Needs OpenSCAD 2023.09+ (Manifold), Python 3, `pip install -r requirements.txt`, fonts DejaVu Sans and Symbola.

```sh
python build.py                       # all keys, all variants, into keys/
python build.py u h f j --bump u h    # one 3MF, bumps on U and H
python build.py space --flat          # flat space bar
python preview.py                     # docs/ images (needs xvfb-run if headless)
```

`$OPENSCAD` overrides the `openscad` path.

## Customizing

- Legends, widths, layouts: `layout.py`
- Shape, stem, bump: top of `keycap.scad`
- Socket fit: `openscad -D 'part="coupons"' -o coupons.stl keycap.scad` prints a 5×5 grid of cross sizes; set `cross_l` / `cross_w` from the snug one
