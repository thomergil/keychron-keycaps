"""Keychron K3 Ultra 8K, ANSI 84-key layout with Dvorak legends, as in docs/keyboard.jpg.

Each key: (id, width in u, legend, upper legend). Rows run top to bottom, keys left to right.
Fn-row icons are Unicode stand-ins for Keychron's artwork, drawn from ICON_FONT.
"""

ICON_FONT = "Symbola"

# Stabilizer stem distance from the switch stem, by key width (Cherry plate-mount spacing).
STAB = {2: 11.938, 2.25: 11.938, 6.25: 50.0}

ROWS = [
    [("esc", 1, "esc", ""),
     ("f1", 1, "F1", "🔅"), ("f2", 1, "F2", "🔆"), ("f3", 1, "F3", "⧉"), ("f4", 1, "F4", "⊞"),
     ("f5", 1, "F5", "☼"), ("f6", 1, "F6", "☀"), ("f7", 1, "F7", "⏪"), ("f8", 1, "F8", "⏯"),
     ("f9", 1, "F9", "⏩"), ("f10", 1, "F10", "🔇"), ("f11", 1, "F11", "🔉"), ("f12", 1, "F12", "🔊"),
     ("screenshot", 1, "", "⛶"), ("del", 1, "del", ""), ("light", 1, "", "💡")],
    [("grave", 1, "`", "~"), ("1", 1, "1", "!"), ("2", 1, "2", "@"), ("3", 1, "3", "#"),
     ("4", 1, "4", "$"), ("5", 1, "5", "%"), ("6", 1, "6", "^"), ("7", 1, "7", "&"),
     ("8", 1, "8", "*"), ("9", 1, "9", "("), ("0", 1, "0", ")"), ("lbracket", 1, "[", "{"),
     ("rbracket", 1, "]", "}"), ("backspace", 2, "backspace", ""), ("pgup", 1, "pgup", "")],
    [("tab", 1.5, "tab", ""), ("quote", 1, "'", "\""), ("comma", 1, ",", "<"), ("period", 1, ".", ">"),
     ("p", 1, "P", ""), ("y", 1, "Y", ""), ("f", 1, "F", ""), ("g", 1, "G", ""), ("c", 1, "C", ""),
     ("r", 1, "R", ""), ("l", 1, "L", ""), ("slash", 1, "/", "?"), ("equal", 1, "=", "+"),
     ("backslash", 1.5, "\\", "|"), ("pgdn", 1, "pgdn", "")],
    [("capslock", 1.75, "capslock", ""), ("a", 1, "A", ""), ("o", 1, "O", ""), ("e", 1, "E", ""),
     ("u", 1, "U", ""), ("i", 1, "I", ""), ("d", 1, "D", ""), ("h", 1, "H", ""), ("t", 1, "T", ""),
     ("n", 1, "N", ""), ("s", 1, "S", ""), ("minus", 1, "-", "_"), ("enter", 2.25, "enter", ""),
     ("home", 1, "home", "")],
    [("lshift", 2.25, "shift", ""), ("semicolon", 1, ";", ":"), ("q", 1, "Q", ""), ("j", 1, "J", ""),
     ("k", 1, "K", ""), ("x", 1, "X", ""), ("b", 1, "B", ""), ("m", 1, "M", ""), ("w", 1, "W", ""),
     ("v", 1, "V", ""), ("z", 1, "Z", ""), ("rshift", 1.75, "shift", ""), ("up", 1, "⌃", ""),
     ("end", 1, "end", "")],
    [("lctrl", 1.25, "ctrl", ""), ("option", 1.25, "option", ""), ("lcmd", 1.25, "⌘", ""),
     ("space", 6.25, "", ""), ("rcmd", 1, "⌘", ""), ("fn", 1, "fn", ""), ("rctrl", 1, "ctrl", ""),
     ("left", 1, "‹", ""), ("down", 1, "⌄", ""), ("right", 1, "›", "")],
]

ROW_U = 16  # every row spans 16u


def keys():
    """Yield (row, id, units, legend, legend2) for every key."""
    for r, row in enumerate(ROWS):
        assert sum(k[1] for k in row) == ROW_U, f"row {r} is not {ROW_U}u"
        for kid, u, leg, leg2 in row:
            yield r, kid, u, leg, leg2
