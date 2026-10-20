"""Shared schematic palette for the HydroPol2D docs figures.

Reference tokens are OKLCH (L, C, h); semantic roles map onto them. Run this file to
print the hex values, WCAG contrast of every text/fill pair, and colour-vision-deficiency
and grayscale checks of the layer fills.
"""

from __future__ import annotations

import math

# --- reference tokens: OKLCH (lightness 0-1, chroma, hue in degrees) -------------------
REF = {
    "ink": (0.25, 0.010, 250),
    "ink_soft": (0.42, 0.010, 250),
    "line": (0.72, 0.008, 250),
    "card": (1.00, 0.000, 0),
    "card_edge": (0.88, 0.006, 250),
    "soil_1": (0.88, 0.050, 78),
    "soil_2": (0.79, 0.066, 68),
    "soil_3": (0.70, 0.074, 60),
    "rock_a": (0.955, 0.010, 85),
    "rock_b": (0.915, 0.012, 85),
    "wet_a": (0.86, 0.040, 238),
    "wet_b": (0.81, 0.046, 238),
    "water": (0.50, 0.130, 252),
    "ground": (0.55, 0.110, 145),
    "deep_fill": (0.955, 0.018, 238),
    "bedrock": (0.80, 0.010, 60),
    "bark": (0.40, 0.055, 55),
    "root": (0.42, 0.070, 55),
    "leaf_dark": (0.55, 0.115, 145),
    "leaf_light": (0.68, 0.125, 135),
}

# --- semantic roles --------------------------------------------------------------------
ROLE = {
    "text": "ink",
    "text_soft": "ink_soft",
    "card": "card",
    "card_edge": "card_edge",
    "slot_near_surface": "soil_1",
    "slot_root_zone": "soil_2",
    "slot_transmission": "soil_3",
    "slot_rock_even": "rock_a",
    "slot_rock_odd": "rock_b",
    "slot_wet_even": "wet_a",
    "slot_wet_odd": "wet_b",
    "water": "water",
    "ground": "ground",
    "boundary": "ink",
    "guide": "line",
    "deep_fill": "deep_fill",
    "bedrock_hatch": "bedrock",
    "trunk": "bark",
    "roots": "root",
    "canopy_shade": "leaf_dark",
    "canopy_light": "leaf_light",
}


def oklch_to_srgb(lightness: float, chroma: float, hue: float) -> tuple[float, float, float]:
    """OKLCH -> gamma-encoded sRGB in [0, 1] (Ottosson 2020), clipped."""
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_**3, m_**3, s_**3
    lin = (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )

    def encode(x: float) -> float:
        x = min(max(x, 0.0), 1.0)
        return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055

    return tuple(encode(x) for x in lin)


def hex_of(token: str) -> str:
    r, g, b = oklch_to_srgb(*REF[token])
    return "#{:02x}{:02x}{:02x}".format(*(round(255 * v) for v in (r, g, b)))


def color(role: str) -> str:
    """Hex colour of a semantic role."""
    return hex_of(ROLE[role])


def _linear(hex_value: str) -> tuple[float, float, float]:
    rgb = [int(hex_value[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb)


def luminance(hex_value: str) -> float:
    r, g, b = _linear(hex_value)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


# Machado et al. (2009) CVD matrices at severity 1.0, applied to linear RGB.
CVD = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def _oklab_from_linear(r: float, g: float, b: float) -> tuple[float, float, float]:
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    )


def delta_e_ok(hex_a: str, hex_b: str, deficiency: str | None = None) -> float:
    def lab(h: str):
        rgb = _linear(h)
        if deficiency:
            mat = CVD[deficiency]
            rgb = tuple(sum(mat[i][j] * rgb[j] for j in range(3)) for i in range(3))
        return _oklab_from_linear(*(min(max(v, 0.0), 1.0) for v in rgb))

    return math.dist(lab(hex_a), lab(hex_b))


if __name__ == "__main__":
    for role in ROLE:
        print(f"{role:20s} {ROLE[role]:10s} {color(role)}")
    print("\nText contrast (WCAG 2):")
    pairs = [("text", f) for f in ("card", "slot_near_surface", "slot_root_zone", "slot_transmission",
                                    "slot_rock_odd", "slot_wet_odd", "deep_fill")]
    pairs += [("water", "card"), ("text_soft", "card"), ("ground", "card")]
    pairs += [("roots", "slot_near_surface"), ("roots", "slot_root_zone"), ("canopy_shade", "card")]
    for fg, bg in pairs:
        print(f"  {fg:10s} on {bg:20s} {contrast(color(fg), color(bg)):5.2f}:1")
    print("\nAdjacent fills, Delta E_OK (normal / protan / deutan / tritan) and lightness step:")
    stack = ["slot_near_surface", "slot_root_zone", "slot_transmission", "slot_rock_even", "slot_rock_odd",
             "slot_wet_even", "slot_wet_odd", "deep_fill"]
    for a, b in zip(stack, stack[1:]):
        des = [delta_e_ok(color(a), color(b), d) for d in (None, "protan", "deutan", "tritan")]
        dl = REF[ROLE[a]][0] - REF[ROLE[b]][0]
        print(f"  {a:18s} | {b:18s} " + " ".join(f"{d:.3f}" for d in des) + f"   dL={dl:+.3f}")
    print("\nWet vs dry rock (same slot, grayscale dL):",
          f"{REF['rock_a'][0] - REF['wet_a'][0]:+.3f}, {REF['rock_b'][0] - REF['wet_b'][0]:+.3f}")
