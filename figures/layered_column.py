"""Layered soil-over-regolith column schematic for docs/theory/layered-subsurface.md.

Text: Helvetica Light (labels) and Helvetica Bold (headings), extracted from the macOS
system font collection. Math: Computer Modern (the TeX fonts) through matplotlib
mathtext. All text is written as vector paths, so the SVG looks the same everywhere.

Run from the repository root:

    python3 figures/layered_column.py

Output: static/img/theory/layered-column.svg
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from fontTools.ttLib import TTCollection
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).parent))
from palette import color  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static/img/theory/layered-column.svg"
HELVETICA = Path("/System/Library/Fonts/Helvetica.ttc")

W, H = 760, 540  # figure size in px (1 data unit = 1 px at 100 dpi)


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

    def text(x, y, s, *, font=light, size=9.5, c=ink, **kw):
        ax.text(x, y, s, fontproperties=font, fontsize=size, color=c, va="center", **kw)

    def note(y, heading, lines=(), *, c=ink):
        text(372, y, heading, font=bold, size=10, c=c)
        for i, line in enumerate(lines, start=1):
            text(372, y + 16 * i, line)

    # Card.
    ax.add_patch(
        FancyBboxPatch((4, 4), W - 8, H - 8, boxstyle="round,pad=0,rounding_size=12",
                       facecolor=color("card"), edgecolor=color("card_edge"), linewidth=1)
    )

    x0, x1 = 95, 335
    ground, soil_base, column_base, table = 58, 188, 436, 272

    # Soil slots.
    soil = [
        (58, 82, "slot_near_surface", "1  near surface"),
        (82, 136, "slot_root_zone", "2  root zone"),
        (136, 188, "slot_transmission", "3  transmission"),
    ]
    for top, bot, role, label in soil:
        ax.add_patch(Rectangle((x0, top), x1 - x0, bot - top, facecolor=color(role), linewidth=0))
        text(x0 + 10, (top + bot) / 2, label)

    # Regolith slots (schematic thicknesses), split by the water table.
    rock = [(188, 202), (202, 222), (222, 252), (252, 300), (300, 368), (368, 436)]
    for k, (top, bot) in enumerate(rock):
        parity = "even" if k % 2 == 0 else "odd"
        dry_bot = min(bot, table)
        if dry_bot > top:
            ax.add_patch(Rectangle((x0, top), x1 - x0, dry_bot - top,
                                   facecolor=color(f"slot_rock_{parity}"), linewidth=0))
        wet_top = max(top, table)
        if bot > wet_top:
            ax.add_patch(Rectangle((x0, wet_top), x1 - x0, bot - wet_top,
                                   facecolor=color(f"slot_wet_{parity}"), linewidth=0))
        label = f"{k + 4}" if k < len(rock) - 1 else f"{k + 4} …"
        # Label each slot in the middle of its part above the table, if it has one.
        label_y = (top + dry_bot) / 2 if dry_bot - top >= 10 else (top + bot) / 2
        text(x0 + 10, label_y, label, size=8, c=soft)
    text(x0 + 105, 404, r"saturated, $\theta = \theta_s$", size=9, c=soft)

    # Column outline.
    ax.add_patch(Rectangle((x0, ground), x1 - x0, column_base - ground, fill=False,
                           edgecolor=color("guide"), linewidth=0.8))

    # Bedrock below the column, with the deep reservoir.
    ax.add_patch(Rectangle((x0, column_base), x1 - x0, 84, facecolor=color("card"),
                           edgecolor=color("bedrock_hatch"), hatch="////", linewidth=0))
    ax.add_patch(
        FancyBboxPatch((118, 452), 194, 54, boxstyle="round,pad=0,rounding_size=7",
                       facecolor=color("deep_fill"), edgecolor=water, linewidth=1)
    )
    text(215, 470, "deep linear reservoir", size=9, ha="center")
    text(215, 489, r"$Q = S/\tau$", size=11, ha="center")
    # A fraction f_d of the recharge reaching the table goes to the deep reservoir.
    ax.add_patch(FancyArrowPatch((180, table + 3), (180, 451), arrowstyle="-|>", mutation_scale=10,
                                 color=ink, linewidth=1.2, linestyle=(0, (4, 3))))
    text(187, 300, r"$f_d$", size=10)

    # Horizontal boundaries extended as leaders to the notes.
    ax.plot([88, 362], [ground, ground], color=color("ground"), linewidth=2.6, solid_capstyle="butt")
    ax.plot([88, 362], [soil_base, soil_base], color=ink, linewidth=1.2, linestyle=(0, (5, 3)))
    ax.plot([88, 362], [table, table], color=water, linewidth=2.2, solid_capstyle="butt")
    ax.plot([88, 362], [column_base, column_base], color=ink, linewidth=2.6, solid_capstyle="butt")

    # Water-table symbol: inverted triangle over the line, two ticks below it.
    ax.add_patch(Polygon([(142, table - 11), (158, table - 11), (150, table - 1)], closed=True,
                         facecolor=water, edgecolor="none"))
    ax.plot([143, 157], [table + 5, table + 5], color=water, linewidth=1.2)
    ax.plot([146, 154], [table + 9, table + 9], color=water, linewidth=1.2)

    # Drainage down the unsaturated slots.
    ax.add_patch(FancyArrowPatch((250, 68), (250, 262), arrowstyle="-|>", mutation_scale=11,
                                 color=ink, linewidth=1.4))
    text(258, 207, "drainage", size=9)
    text(258, 224, r"$K_v\,K_r(S_e)$", size=10)

    # Darcy flux at the table: both directions.
    ax.add_patch(FancyArrowPatch((305, table - 22), (305, table + 22), arrowstyle="<|-|>",
                                 mutation_scale=10, color=water, linewidth=1.6))

    # Lateral flow in the saturated slots.
    ax.add_patch(FancyArrowPatch((205, 346), (362, 346), arrowstyle="-|>", mutation_scale=12,
                                 color=water, linewidth=2))

    # Left brackets: soil and regolith.
    for top, bot, label in ((ground, soil_base, "soil"),
                            (soil_base, column_base, "regolith: 0.25, 0.5, 1, 2, 4, 4 … m")):
        ax.plot([80, 74, 74, 80], [top + 2, top + 2, bot - 2, bot - 2], color=soft, linewidth=1)
        text(62, (top + bot) / 2, label, size=9, c=soft, rotation=90, ha="center")

    # Notes.
    note(ground, "Ground surface")
    note(soil_base, "Soil base", ["soil parameters end, regolith begins"])
    note(228, "Darcy flux at the table",
         [r"$q = K(\theta)\,(\psi/\Delta z + 1)$: recharge down, capillary rise up"])
    note(table + 6, r"Water table $h$",
         [r"one head per cell; a rise fills $\theta_s - \theta$,", r"a fall leaves $\theta_{fc}$, so $S_y = \theta_s - \theta_{fc}$"],
         c=water)
    note(346, "Lateral flow", [r"$T = \Sigma\, K_h\, b$, summed over the saturated slots"], c=water)
    note(column_base, "Column base",
         [r"$z_{\mathrm{surf}} - \min(D_{\mathrm{DTB}},\ 50\ \mathrm{m})$"])
    note(484, "Deep aquifer (optional)",
         ["one reservoir per subbasin, fed by a fraction", r"$f_d$ of the recharge, returned to river cells"])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, format="svg", transparent=True, metadata={"Date": None})
    if preview is not None:
        fig.savefig(preview, format="png", dpi=250, facecolor="#2b2f33")
    plt.close(fig)
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    # Optional: a PNG preview path, rendered on a dark background to check the card edge.
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
