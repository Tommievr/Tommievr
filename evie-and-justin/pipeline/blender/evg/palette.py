"""Single source of truth for colours and light variants (mirrors design/STYLE_GUIDE.md and design/character-sheets/)."""

SHADE_TINT = "#B8A4D8"      # multiplied into base colour for the toon shadow step (plum/violet shift, never grey)
GOLD = "#FFB520"

# base colours (proposed v1.1: clean, bright, saturated). Hex are sRGB.
CHARACTERS = {
    "evie":    {"fur": "#FFF6EC", "patch": "#2A2030", "ear": "#FFA9A0", "nose": "#FF8FA0", "iris": "#1E7FD6", "collar": "#D01F4B", "tag": GOLD},
    "justin":  {"fur": "#352B3D", "ear": "#FF9FA0", "ear_back": "#FFEBDD", "nose": "#E0707A", "iris": "#3FB52A", "collar": "#17121C", "tag": GOLD},
    "cotton":  {"wool": "#FFF3DF", "face": "#FFE7CF", "ear": "#FFA8A0", "nose": "#FF9FA8", "iris": "#1E7FD6", "collar": "#7FB8F0", "bell": GOLD, "hoof": "#5A4040"},
    "toffee":  {"wool": "#9C4A1C", "cream": "#FFE9CF", "ear_out": "#7A3A16", "ear": "#FF9C90", "nose": "#FF9FA8", "iris": "#5CC236", "collar": "#43A047", "bell": GOLD, "hoof": "#4A2E26"},
}

# special drink (Ep.1 lore, design/props/SPECIAL_DRINK.md): lilac + gold, deliberately not green/red (poison/medicine) or amber (alcohol)
DRINK = {"liquid": "#B9A2FF", "liquid_deep": "#7A5FE0", "sparkle": "#FFE08A", "petal": "#E9D8FF", "stem": "#6CC070",
         "acorn": "#B9763A", "glass": "#DDEBFF", "cork": "#C99A5B"}

# lighting variants (see STYLE_GUIDE section 3.5). azimuth: degrees from the camera axis (0 = behind camera, + = to the right).
VARIANTS = {
    "day":    {"sun_elev": 45, "sun_az": 40, "key": "#FFE9C4", "key_w": 4.0, "fill": "#9EC5FF", "fill_w": 1.4, "rim": "#FFF1D6", "rim_w": 5,
               "sky_top": "#6FB8F0", "sky_horizon": "#CFE9FA", "ground_bounce": "#F7D9B0"},
    "golden": {"sun_elev": 17, "sun_az": 40, "key": "#FFC76B", "key_w": 3.5, "fill": "#9EC5FF", "fill_w": 1.0, "rim": "#FFD9A8", "rim_w": 8,
               "sky_top": "#8EC8F0", "sky_horizon": "#FFD9A8", "ground_bounce": "#F7B58A"},
    "dusk":   {"sun_elev": 5,  "sun_az": 40, "key": "#F2A5A0", "key_w": 1.6, "fill": "#7C8FD8", "fill_w": 0.8, "rim": "#FFB48A", "rim_w": 6,
               "sky_top": "#2B2D52", "sky_horizon": "#F7B58A", "ground_bounce": "#C77F8F"},
}


def hex_to_rgb(h):
    """'#RRGGBB' -> (r, g, b) floats 0..1 in sRGB."""
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_linear_rgba(h, alpha=1.0):
    """Blender colour sockets/properties expect linear values."""
    r, g, b = hex_to_rgb(h)
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b), alpha)
