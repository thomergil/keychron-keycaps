"""Keychron K3 Ultra 8K, ANSI 84 keys: every keycap, and the arrangements drawn in docs/.

The profile is the same on every row, so QWERTY and Dvorak use the same caps in other positions.
Fn-row icons are Unicode stand-ins for Keychron's artwork, drawn from ICON_FONT.
"""

ICON_FONT = "Symbola"

# Stabilizer stem distance from the switch stem, by key width (Cherry plate-mount spacing).
STAB = {2: 11.938, 2.25: 11.938, 6.25: 50.0}

ROW_U = 16  # every row spans 16u

# id: (width in u, legend, upper legend)
KEYS = {
    "esc": (1, "esc", ""),
    "f1": (1, "F1", "🔅"), "f2": (1, "F2", "🔆"), "f3": (1, "F3", "⧉"), "f4": (1, "F4", "⊞"),
    "f5": (1, "F5", "☼"), "f6": (1, "F6", "☀"), "f7": (1, "F7", "⏪"), "f8": (1, "F8", "⏯"),
    "f9": (1, "F9", "⏩"), "f10": (1, "F10", "🔇"), "f11": (1, "F11", "🔉"), "f12": (1, "F12", "🔊"),
    "screenshot": (1, "", "⛶"), "del": (1, "del", ""), "light": (1, "", "💡"),
    "grave": (1, "`", "~"), "1": (1, "1", "!"), "2": (1, "2", "@"), "3": (1, "3", "#"),
    "4": (1, "4", "$"), "5": (1, "5", "%"), "6": (1, "6", "^"), "7": (1, "7", "&"),
    "8": (1, "8", "*"), "9": (1, "9", "("), "0": (1, "0", ")"),
    "minus": (1, "-", "_"), "equal": (1, "=", "+"), "lbracket": (1, "[", "{"), "rbracket": (1, "]", "}"),
    "backslash": (1.5, "\\", "|"), "semicolon": (1, ";", ":"), "quote": (1, "'", "\""),
    "comma": (1, ",", "<"), "period": (1, ".", ">"), "slash": (1, "/", "?"),
    **{c: (1, c.upper(), "") for c in "abcdefghijklmnopqrstuvwxyz"},
    "backspace": (2, "backspace", ""), "tab": (1.5, "tab", ""), "capslock": (1.75, "caps\u200alock", ""),
    "enter": (2.25, "enter", ""), "lshift": (2.25, "shift", ""), "rshift": (1.75, "shift", ""),
    "pgup": (1, "pgup", ""), "pgdn": (1, "pgdn", ""), "home": (1, "home", ""), "end": (1, "end", ""),
    "lctrl": (1.25, "ctrl", ""), "option": (1.25, "option", ""), "lcmd": (1.25, "⌘", ""),
    "lwin": (1.25, "@win", ""), "lalt": (1.25, "alt", ""),
    "space": (6.25, "", ""),
    "rcmd": (1, "⌘", ""), "ralt": (1, "alt", ""), "fn": (1, "fn", ""), "rctrl": (1, "ctrl", ""),
    "up": (1, "@up", ""), "left": (1, "@left", ""), "down": (1, "@down", ""), "right": (1, "@right", ""),
}

FN_ROW = "esc f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 screenshot del light"
MAC_ROW = "lctrl option lcmd space rcmd fn rctrl left down right"
WIN_ROW = "lctrl lwin lalt space ralt fn rctrl left down right"

# Key ids per row, top to bottom.
LAYOUTS = {
    "QWERTY (macOS)": [FN_ROW,
        "grave 1 2 3 4 5 6 7 8 9 0 minus equal backspace pgup",
        "tab q w e r t y u i o p lbracket rbracket backslash pgdn",
        "capslock a s d f g h j k l semicolon quote enter home",
        "lshift z x c v b n m comma period slash rshift up end",
        MAC_ROW],
    "Dvorak (macOS)": [FN_ROW,
        "grave 1 2 3 4 5 6 7 8 9 0 lbracket rbracket backspace pgup",
        "tab quote comma period p y f g c r l slash equal backslash pgdn",
        "capslock a o e u i d h t n s minus enter home",
        "lshift semicolon q j k x b m w v z rshift up end",
        MAC_ROW],
}
LAYOUTS["QWERTY (Windows)"] = LAYOUTS["QWERTY (macOS)"][:5] + [WIN_ROW]

for name, rows in LAYOUTS.items():
    for r, row in enumerate(rows):
        assert sum(KEYS[k][0] for k in row.split()) == ROW_U, f"{name} row {r} is not {ROW_U}u"


def rows(layout):
    """Rows of key ids for a layout name."""
    return [row.split() for row in LAYOUTS[layout]]


def keys():
    """Yield (row, id, units, legend, legend2) for every keycap; row is its QWERTY row."""
    row_of = {}
    for layout in ("QWERTY (macOS)", "QWERTY (Windows)"):
        for r, row in enumerate(rows(layout)):
            for k in row:
                row_of.setdefault(k, r)
    assert row_of.keys() == KEYS.keys(), set(KEYS) ^ set(row_of)
    for kid, (u, leg, leg2) in KEYS.items():
        yield row_of[kid], kid, u, leg, leg2
