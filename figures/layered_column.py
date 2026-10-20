"""Layered soil-over-regolith column schematic for docs/theory/layered-subsurface.md.

Text: Helvetica Light (labels) and Helvetica Bold (headings), extracted from the macOS
system font collection. Math: Computer Modern (the TeX fonts) through matplotlib
mathtext. All text is written as vector paths, so the SVG looks the same everywhere.
Arrows are tapered ribbons with notched heads, drawn as filled polygons.

Run from the repository root:

    python3 figures/layered_column.py [preview.png]

Output: static/img/theory/layered-column.svg (and an optional PNG preview on a dark
background, to check the card edge).
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("svg")
import matplotlib.pyplot as plt
from fontTools.ttLib import TTCollection
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).parent))
from palette import color  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static/img/theory/layered-column.svg"
HELVETICA = Path("/System/Library/Fonts/Helvetica.ttc")

W, H = 760, 612  # figure size in px (1 data unit = 1 px at 100 dpi)

# Column geometry (px, y downward).
X0, X1 = 95, 355
GROUND = 120
SOIL = [  # (top, bottom, role, label)
    (120, 144, "slot_near_surface", "1  near surface"),
    (144, 198, "slot_root_zone", "2  root zone"),
    (198, 250, "slot_transmission", "3  transmission"),
]
ROOT_DEPTH, SOIL_BASE = 198, 250
ROCK = [(250, 264), (264, 284), (284, 314), (314, 362), (362, 430), (430, 498)]
TABLE, COLUMN_BASE = 334, 498
NOTE_X, LEADER_END = 392, 382


def helvetica_faces(folder: Path) -> tuple[FontProperties, FontProperties]:
    """Extract Helvetica Light and Bold from the system collection."""
    faces = {}
    for font in TTCollection(str(HELVETICA)).fonts:
        full = font["name"].getDebugName(4)
        if full in ("Helvetica Light", "Helvetica Bold"):
            path = folder / f"{full.replace(' ', '-')}.ttf"
            font.save(str(path))
            faces[full] = FontProperties(fname=str(path))
    return faces["Helvetica Light"], faces["Helvetica Bold"]


# --- arrows ------------------------------------------------------------------------------


def bezier(points, n: int = 60) -> np.ndarray:
    """Points along a quadratic or cubic Bezier curve."""
    p = np.asarray(points, dtype=float)
    t = np.linspace(0.0, 1.0, n)[:, None]
    if len(p) == 3:
        return (1 - t) ** 2 * p[0] + 2 * (1 - t) * t * p[1] + t**2 * p[2]
    return (1 - t) ** 3 * p[0] + 3 * (1 - t) ** 2 * t * p[1] + 3 * (1 - t) * t**2 * p[2] + t**3 * p[3]


def _normals(curve: np.ndarray) -> np.ndarray:
    tangent = np.gradient(curve, axis=0)
    tangent /= np.linalg.norm(tangent, axis=1, keepdims=True)
    return np.column_stack([-tangent[:, 1], tangent[:, 0]])


def _kite_head(tip, direction, length, width, notch=0.32):
    """Notched head: tip, two wings and a notch pulled back into the shaft."""
    d = np.asarray(direction, float) / np.linalg.norm(direction)
    n = np.array([-d[1], d[0]])
    tip = np.asarray(tip, float)
    base = tip - d * length
    return [tip, base + n * width / 2, tip - d * length * (1 - notch), base - n * width / 2]


def _tapered(curve: np.ndarray, w0: float, w1: float) -> np.ndarray:
    half = np.linspace(w0, w1, len(curve))[:, None] / 2
    normals = _normals(curve)
    return np.vstack([curve + normals * half, (curve - normals * half)[::-1]])


def ribbon_arrow(ax, points, *, width=(1.5, 4.0), head=(13, 12), c="#000", alpha=1.0, z=5):
    """Tapered ribbon along a Bezier curve, ending in a notched head."""
    curve = bezier(points)
    direction = curve[-1] - curve[-4]
    head_len, head_w = head
    shaft_end = curve[-1] - direction / np.linalg.norm(direction) * head_len * 0.62
    keep = np.linalg.norm(curve - curve[0], axis=1) <= np.linalg.norm(shaft_end - curve[0])
    shaft = np.vstack([curve[keep], shaft_end])
    ax.add_patch(Polygon(_tapered(shaft, *width), closed=True, facecolor=c, edgecolor="none",
                         alpha=alpha, zorder=z))
    ax.add_patch(Polygon(_kite_head(curve[-1], direction, head_len, head_w), closed=True,
                         facecolor=c, edgecolor="none", alpha=alpha, zorder=z))


def dashed_arrow(ax, points, *, c="#000", lw=1.3, head=(10, 9), z=5):
    """Dashed curve with the same notched head (a secondary, partial flux)."""
    curve = bezier(points)
    direction = curve[-1] - curve[-4]
    ax.plot(curve[:-3, 0], curve[:-3, 1], color=c, linewidth=lw, linestyle=(0, (4, 3)),
            dash_capstyle="round", zorder=z)
    ax.add_patch(Polygon(_kite_head(curve[-1], direction, *head), closed=True,
                         facecolor=c, edgecolor="none", zorder=z))


# --- tree ---------------------------------------------------------------------------------


def tree(ax, x: float, ground: float, root_depth: float) -> None:
    """Stylised tree: canopy above the ground, roots down to the root depth."""
    bark, roots = color("trunk"), color("roots")
    shade, light = color("canopy_shade"), color("canopy_light")

    # Roots: tapered curves from the trunk base; the deepest tips reach the root depth.
    reach = root_depth - ground
    root_paths = [
        ([(x, ground), (x + 2, ground + 0.45 * reach), (x - 3, ground + reach - 1)], (3.4, 0.8)),
        ([(x - 2, ground + 2), (x - 26, ground + 0.35 * reach), (x - 38, ground + 0.95 * reach)], (2.6, 0.6)),
        ([(x + 2, ground + 2), (x + 28, ground + 0.30 * reach), (x + 40, ground + 0.90 * reach)], (2.6, 0.6)),
        ([(x - 3, ground + 1), (x - 34, ground + 0.10 * reach), (x - 52, ground + 0.40 * reach)], (1.8, 0.5)),
        ([(x + 3, ground + 1), (x + 36, ground + 0.08 * reach), (x + 54, ground + 0.36 * reach)], (1.8, 0.5)),
        ([(x - 14, ground + 0.40 * reach), (x - 8, ground + 0.70 * reach), (x - 18, ground + reach - 2)], (1.2, 0.4)),
        ([(x + 15, ground + 0.36 * reach), (x + 10, ground + 0.66 * reach), (x + 22, ground + reach - 3)], (1.2, 0.4)),
    ]
    for pts, (w0, w1) in root_paths:
        ax.add_patch(Polygon(_tapered(bezier(pts, 40), w0, w1), closed=True, facecolor=roots,
                             edgecolor="none", zorder=4))

    # Trunk with a slight flare at the ground, and two branches.
    trunk = [(x - 6, ground + 1), (x - 3.2, ground - 14), (x - 2.6, ground - 44),
             (x + 2.6, ground - 44), (x + 3.2, ground - 14), (x + 6, ground + 1)]
    ax.add_patch(Polygon(trunk, closed=True, facecolor=bark, edgecolor="none", zorder=6))
    for (x_a, y_a), (x_b, y_b) in (((x - 1, ground - 30), (x - 13, ground - 46)),
                                   ((x + 1, ground - 36), (x + 14, ground - 52))):
        ax.plot([x_a, x_b], [y_a, y_b], color=bark, linewidth=2.2, solid_capstyle="round", zorder=6)

    # Canopy: overlapping discs, shade below, light above.
    top = ground - 62
    for dx, dy, r in ((-22, 8, 17), (22, 8, 17), (0, 12, 19)):
        ax.add_patch(Circle((x + dx, top + dy), r, facecolor=shade, edgecolor="none", zorder=7))
    for dx, dy, r in ((-12, -6, 17), (13, -4, 16), (0, -16, 16), (-26, -2, 11), (27, 0, 11)):
        ax.add_patch(Circle((x + dx, top + dy), r, facecolor=light, edgecolor="none", zorder=8))
    ax.add_patch(Ellipse((x, ground + 0.5), 46, 4, facecolor=shade, edgecolor="none", alpha=0.35, zorder=5))


# --- figure -------------------------------------------------------------------------------


def main(preview: Path | None = None) -> None:
    plt.rcParams.update(
        {
            "svg.fonttype": "path",
            "svg.hashsalt": "hydropol2d-layered-column",
            "mathtext.fontset": "cm",
        }
    )
    with tempfile.TemporaryDirectory() as tmp:
        light, bold = helvetica_faces(Path(tmp))
        draw(light, bold, preview)


def draw(light: FontProperties, bold: FontProperties, preview: Path | None = None) -> None:
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    ink, soft, water = color("text"), color("text_soft"), color("water")

    def text(x, y, s, *, font=light, size=9.5, c=ink, z=10, **kw):
        ax.text(x, y, s, fontproperties=font, fontsize=size, color=c, va="center", zorder=z, **kw)

    def note(y, heading, lines=(), *, c=ink):
        """Bold heading, then light lines: 20 px to the first line, 17 px between lines."""
        text(NOTE_X, y, heading, font=bold, size=10, c=c)
        for i, line in enumerate(lines):
            text(NOTE_X, y + 20 + 17 * i, line)

    def leader(y, c, lw, style="-"):
        ax.plot([88, LEADER_END], [y, y], color=c, linewidth=lw, linestyle=style,
                solid_capstyle="butt", zorder=9)

    # Card.
    ax.add_patch(
        FancyBboxPatch((4, 4), W - 8, H - 8, boxstyle="round,pad=0,rounding_size=12",
                       facecolor=color("card"), edgecolor=color("card_edge"), linewidth=1)
    )

    # Soil slots.
    for top, bot, role, label in SOIL:
        ax.add_patch(Rectangle((X0, top), X1 - X0, bot - top, facecolor=color(role), linewidth=0))
        text(X0 + 10, (top + bot) / 2, label)

    # Regolith slots (schematic thicknesses), split by the water table.
    for k, (top, bot) in enumerate(ROCK):
        parity = "even" if k % 2 == 0 else "odd"
        dry_bot = min(bot, TABLE)
        if dry_bot > top:
            ax.add_patch(Rectangle((X0, top), X1 - X0, dry_bot - top,
                                   facecolor=color(f"slot_rock_{parity}"), linewidth=0))
        wet_top = max(top, TABLE)
        if bot > wet_top:
            ax.add_patch(Rectangle((X0, wet_top), X1 - X0, bot - wet_top,
                                   facecolor=color(f"slot_wet_{parity}"), linewidth=0))
        label = f"{k + 4}" if k < len(ROCK) - 1 else f"{k + 4} …"
        label_y = (top + dry_bot) / 2 if dry_bot - top >= 10 else (top + bot) / 2
        text(X0 + 10, label_y, label, size=8, c=soft)
    text(X0 + 118, 470, r"saturated, $\theta = \theta_s$", size=9, c=soft)

    # Column outline, bedrock and the deep reservoir.
    ax.add_patch(Rectangle((X0, GROUND), X1 - X0, COLUMN_BASE - GROUND, fill=False,
                           edgecolor=color("guide"), linewidth=0.8, zorder=3))
    ax.add_patch(Rectangle((X0, COLUMN_BASE), X1 - X0, 86, facecolor=color("card"),
                           edgecolor=color("bedrock_hatch"), hatch="////", linewidth=0))
    ax.add_patch(
        FancyBboxPatch((128, 518), 194, 54, boxstyle="round,pad=0,rounding_size=7",
                       facecolor=color("deep_fill"), edgecolor=water, linewidth=1, zorder=4)
    )
    text(225, 536, "deep linear reservoir", size=9, ha="center")
    text(225, 555, r"$Q = S/\tau$", size=11, ha="center")

    # Boundaries, extended as leaders to the notes.
    leader(GROUND, color("ground"), 2.6)
    leader(ROOT_DEPTH, soft, 0.9, (0, (1, 2.5)))
    leader(SOIL_BASE, ink, 1.2, (0, (5, 3)))
    leader(TABLE, water, 2.2)
    leader(COLUMN_BASE, ink, 2.6)

    # Tree with roots down to the root depth.
    tree(ax, 290, GROUND, ROOT_DEPTH)

    # Water-table symbol: inverted triangle on the line, two ticks below it.
    ax.add_patch(Polygon([(132, TABLE - 11), (148, TABLE - 11), (140, TABLE - 1)], closed=True,
                         facecolor=water, edgecolor="none", zorder=9))
    ax.plot([133, 147], [TABLE + 5, TABLE + 5], color=water, linewidth=1.2, zorder=9)
    ax.plot([136, 144], [TABLE + 9, TABLE + 9], color=water, linewidth=1.2, zorder=9)

    # Drainage down the unsaturated slots: a tapered ribbon with a slight S.
    ribbon_arrow(ax, [(232, 206), (222, 250), (242, 282), (232, 324)], width=(1.2, 4.2),
                 head=(13, 12), c=ink)
    text(250, 268, "drainage", size=9)
    text(250, 286, r"$K_v\,K_r(S_e)$", size=10)

    # Darcy flux at the table: recharge down, capillary rise up, side by side.
    ribbon_arrow(ax, [(316, TABLE - 32), (319, TABLE - 15), (316, TABLE + 3)], width=(1.4, 4.4),
                 head=(11, 11), c=water)
    ribbon_arrow(ax, [(338, TABLE + 30), (335, TABLE + 13), (338, TABLE - 5)], width=(1.4, 4.4),
                 head=(11, 11), c=water)

    # Lateral flow: a broad ribbon leaving the column, with two thin streamlines.
    ribbon_arrow(ax, [(150, 410), (240, 402), (300, 410), (378, 406)], width=(3, 13),
                 head=(20, 24), c=water)
    for dy, x_end in ((-26, 330), (24, 318)):
        ribbon_arrow(ax, [(190, 410 + dy), (250, 406 + dy), (x_end, 410 + dy)], width=(0.6, 1.6),
                     head=(8, 7), c=water)

    # A fraction f_d of the recharge reaching the table goes to the deep reservoir.
    dashed_arrow(ax, [(176, TABLE + 4), (152, 430), (208, 470), (198, 514)], c=ink)
    text(183, 357, r"$f_d$", size=10)

    # Left brackets: soil and regolith.
    for top, bot, label in ((GROUND, SOIL_BASE, "soil"),
                            (SOIL_BASE, COLUMN_BASE, "regolith: 0.25, 0.5, 1, 2, 4, 4 … m")):
        ax.plot([80, 74, 74, 80], [top + 2, top + 2, bot - 2, bot - 2], color=soft, linewidth=1)
        text(62, (top + bot) / 2, label, size=9, c=soft, rotation=90, ha="center")

    # Notes.
    note(GROUND, "Ground surface")
    note(ROOT_DEPTH - 2, "Root depth", ["from the land-cover class; roots take", "soil ET from slots 1 and 2"])
    note(SOIL_BASE + 6, "Soil base", ["soil parameters end, regolith begins"])
    note(TABLE - 2, r"Water table $h$, one per cell",
         [r"rise fills $\theta_s - \theta$; fall leaves $\theta_{fc}$, so $S_y = \theta_s - \theta_{fc}$",
          r"flux $q = K(\theta)\,(\psi/\Delta z + 1)$: recharge down, rise up"],
         c=water)
    note(408, "Lateral flow", [r"$T = \Sigma\, K_h\, b$, summed over the saturated slots"], c=water)
    note(COLUMN_BASE + 8, "Column base", [r"$z_{\mathrm{surf}} - \min(D_{\mathrm{DTB}},\ 50\ \mathrm{m})$"])
    note(552, "Deep aquifer (optional)",
         [r"one reservoir per subbasin, fed by a fraction $f_d$", "of the recharge, returned to river cells"])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, format="svg", transparent=True, metadata={"Date": None})
    if preview is not None:
        fig.savefig(preview, format="png", dpi=250, facecolor="#2b2f33")
    plt.close(fig)
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
