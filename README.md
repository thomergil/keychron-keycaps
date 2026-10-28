# Keychron K3 Ultra keycaps

3D-printable LSA keycaps for the [Keychron K3 Ultra 8K](https://www.keychron.com/products/keychron-k3-ultra-8k-wireless-custom-mechanical-keyboard) (ANSI), with legends in a second color.

Keychron sells the [same keycap set](https://www.keychron.com/products/black-transparent-low-profile-lsa-full-set-keycap-set) for the [K3 Pro](https://www.keychron.com/products/keychron-k3-pro-qmk-via-wireless-custom-mechanical-keyboard) and [K3 Max](https://www.keychron.com/products/keychron-k3-max-qmk-via-wireless-custom-mechanical-keyboard); these caps are untested on those. They do not fit the original [K3](https://www.keychron.com/products/keychron-k3-wireless-mechanical-keyboard), whose stabilizer stems are offset.

### QWERTY (macOS)
![QWERTY, macOS](docs/qwerty-macos.png)

### QWERTY (Windows)
![QWERTY, Windows](docs/qwerty-windows.png)

### Dvorak (macOS)
![Dvorak, macOS](docs/dvorak-macos.png)

### Dished, with homing bumps
![Dished, with homing bumps](docs/dished-bump.png)

## Files

`keys/<variant>/r<row>-<key>.3mf`, for example `keys/dished/r3-f.3mf`. Row 0 is the Fn row, row 5 the space bar row. Key names are in [`layout.py`](layout.py).

| Variant | Top | Homing bump |
|---|---|---|
| `flat` | flat | no |
| `flat-bump` | flat | yes |
| `dished` | 0.4 mm spherical dish | no |
| `dished-bump` | 0.4 mm spherical dish | yes |

Both macOS (`option`, `⌘`) and Windows (`win`, `alt`) modifiers are included. Every row has the same profile, so Dvorak and other layouts use the same files.

## Printing

Each 3MF has two parts: `cap` and `inlay` (the legend). Assign a filament to each. Caps are exported stem down.

Stabilizer stem spacing (backspace, enter, left shift, space) is the Cherry standard, not measured on a K3 Ultra. Print backspace first to check the fit.

## Homing ridge

The bump is 1.65 mm wide and 0.33 mm tall, 10% larger than stock.

A drop of resin is smoother than a printed bump. Print a cap without a bump, add a tiny drop of resin with a toothpick, and let it cure.
