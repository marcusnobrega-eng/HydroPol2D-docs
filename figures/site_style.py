r"""Shared style for the HydroPol2D docs schematics.

Matches figures/layered_column.py: white rounded card, Helvetica Light text with Helvetica
Bold headings, Computer Modern math through mathtext, the OKLCH palette of
figures/palette.py, tapered ribbon arrows with notched heads. Coordinates are pixels
(1 unit = 1 px at 100 dpi), y downward.

    from site_style import Sheet, color, oklch_hex, ribbon_arrow, dashed_arrow, bezier, tree
    s = Sheet(760, 520, "cell-water-budget")
    s.text(40, 40, "Heading", bold=True, size=11)
    s.note(500, 120, "Infiltration", [r"capacity $f = K\,(\psi/\Delta z + 1)$"])
    s.save(STATIC / "theory", "pt")   # writes cell-water-budget.pt.svg

Each figure script draws every language of its LABELS and writes name.svg (en),
name.pt.svg and name.es.svg under static/img/. Run them from the repository root, for
example python3 figures/cell_water_budget.py [preview-folder].
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
STATIC = HERE.parent / "static" / "img"
sys.path.insert(0, str(HERE))
from layered_column import bezier, dashed_arrow, helvetica_faces, ribbon_arrow, tree  # noqa: E402,F401
from palette import REF, ROLE, color, hex_of, oklch_to_srgb  # noqa: E402,F401

# Set the math font first: a FontProperties keeps the math fontset it was created with.
plt.rcParams.update({"svg.fonttype": "path", "mathtext.fontset": "cm", "svg.hashsalt": "hydropol2d-docs"})
LIGHT, BOLD = helvetica_faces(Path(tempfile.mkdtemp(prefix="hp2d-fonts-")))

INK, SOFT, WATER = color("text"), color("text_soft"), color("water")


def oklch_hex(lightness: float, chroma: float, hue: float) -> str:
    """A colour outside palette.py, written in the same OKLCH terms (list new ones in the report)."""
    r, g, b = oklch_to_srgb(lightness, chroma, hue)
    return "#{:02x}{:02x}{:02x}".format(*(round(max(0.0, min(1.0, v)) * 255) for v in (r, g, b)))


class Sheet:
    """One figure: a card of W x H px with text, note and box helpers."""

    def __init__(self, width: int, height: int, name: str, *, card: bool = True) -> None:
        self.W, self.H, self.name = width, height, name
        self.fig = plt.figure(figsize=(width / 100, height / 100), dpi=100)
        self.ax = self.fig.add_axes((0, 0, 1, 1))
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(height, 0)
        self.ax.axis("off")
        if card:
            self.ax.add_patch(FancyBboxPatch(
                (4, 4), width - 8, height - 8, boxstyle="round,pad=0,rounding_size=12",
                facecolor=color("card"), edgecolor=color("card_edge"), linewidth=1, zorder=0))

    def text(self, x, y, s, *, bold=False, size=9.5, c=INK, z=10, **kw):
        """Text centred vertically on y. Descriptions 9.5, headings 10 to 11, notes no smaller than 9."""
        kw.setdefault("va", "center")
        return self.ax.text(x, y, s, fontproperties=BOLD if bold else LIGHT, fontsize=size,
                            color=c, zorder=z, **kw)

    def note(self, x, y, heading, lines=(), *, c=INK, size=10):
        """Bold heading, then light lines: 20 px to the first line, 17 px between lines."""
        self.text(x, y, heading, bold=True, size=size, c=c)
        for i, line in enumerate(lines):
            self.text(x, y + 20 + 17 * i, line)

    def box(self, x, y, w, h, *, fill="#ffffff", edge=None, radius=6, lw=1.0, z=2, **kw):
        patch = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                               facecolor=fill, edgecolor=edge or color("card_edge"), linewidth=lw,
                               zorder=z, **kw)
        self.ax.add_patch(patch)
        return patch

    def line(self, xs, ys, *, c=INK, lw=1.0, style="-", z=5):
        return self.ax.plot(xs, ys, color=c, linewidth=lw, linestyle=style, solid_capstyle="butt",
                            zorder=z)

    def arrow(self, points, **kw):
        """Ribbon arrow along 2 to 4 control points (straight when 2 are given)."""
        if len(points) == 2:
            (x0, y0), (x1, y1) = points
            points = [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)]
        kw.setdefault("c", INK)
        ribbon_arrow(self.ax, points, **kw)

    def dashed(self, points, **kw):
        if len(points) == 2:
            (x0, y0), (x1, y1) = points
            points = [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)]
        kw.setdefault("c", INK)
        dashed_arrow(self.ax, points, **kw)

    def save(self, folder: Path, lang: str = "en", preview: Path | None = None) -> Path:
        """Write name.svg (en) or name.<lang>.svg into folder; a PNG of it into preview, if given."""
        suffix = "" if lang == "en" else f".{lang}"
        folder.mkdir(parents=True, exist_ok=True)
        svg = folder / f"{self.name}{suffix}.svg"
        self.fig.savefig(svg, format="svg", transparent=True, metadata={"Date": None})
        if preview is not None:
            preview.mkdir(parents=True, exist_ok=True)
            self.fig.savefig(preview / f"{self.name}{suffix}.png", format="png", dpi=200,
                             facecolor="#ffffff")
        plt.close(self.fig)
        return svg
