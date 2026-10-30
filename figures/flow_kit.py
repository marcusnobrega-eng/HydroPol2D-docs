"""Flowchart helpers on a site_style Sheet: measured text, mixed bold runs, button chips,
right-angle arrows with the site's notched head, buses, junction dots and brackets.

Units are px (1 unit = 1 px at 100 dpi), y downward. One arrowhead for every figure:
HEAD = (10, 9) px, shaft SHAFT = 1.6 px; plain line segments use the same width in points.
"""

from __future__ import annotations

import warnings

import matplotlib.pyplot as plt
from matplotlib import _text_helpers
from matplotlib.ft2font import LoadFlags
from matplotlib.patches import Circle
from matplotlib.textpath import TextToPath

from site_style import BOLD, INK, LIGHT, SOFT, color, ribbon_arrow

HEAD = (10, 9)
SHAFT = 1.6
LINE_PT = SHAFT * 0.72  # px to pt at 100 dpi
_TTP = TextToPath()
# The PNG preview is drawn by Agg; without hinting its glyph advances match the SVG paths.
plt.rcParams["text.hinting"] = "none"
plt.rcParams["text.hinting_factor"] = 1


def width(sheet, text: str, *, bold=False, size=9.5) -> float:
    """Advance width of a text run in px (spaces counted), from the same unhinted glyph layout
    that the SVG text-to-path output uses."""
    prop = BOLD if bold else LIGHT
    if text.count("$") >= 2:  # mathtext run: width from the math parser, in pt
        q = prop.copy()
        q.set_size(size)
        w, _, _ = _TTP.get_text_width_height_descent(text, q, ismath=True)
        return w * 100 / 72
    font = _TTP._get_font(prop)
    font.set_size(_TTP.FONT_SCALE, _TTP.DPI)
    last = None
    for item in _text_helpers.layout(text, font):
        last = item
    if last is None:
        return 0.0
    glyph = last.ft_object.load_glyph(last.glyph_index, flags=LoadFlags.NO_HINTING)
    end = last.x + glyph.linearHoriAdvance / 65536
    return end * size / _TTP.FONT_SCALE * 100 / 72


def text(sheet, x, y, s, *, bold=False, size=9.5, c=INK, room=None, ha="left", **kw):
    """Sheet.text with an optional room check (px available from the anchor)."""
    t = sheet.text(x, y, s, bold=bold, size=size, c=c, ha=ha, **kw)
    if room is not None:
        w = width(sheet, s, bold=bold, size=size)
        if w > room:
            warnings.warn(f"text {s!r} is {w:.0f} px, room {room:.0f} px", stacklevel=2)
    return t


def rich(sheet, x, y, parts, *, size=9.5, c=INK, room=None, ha="left"):
    """A line of light and bold runs: parts = [("text", bold), ...]. Returns the line width."""
    total = sum(width(sheet, p, bold=b, size=size) for p, b in parts)
    if room is not None and total > room:
        warnings.warn(f"line {''.join(p for p, _ in parts)!r} is {total:.0f} px, room {room:.0f} px", stacklevel=2)
    x0 = x - total / 2 if ha == "center" else (x - total if ha == "right" else x)
    base = y + baseline_offset(size)
    for p, b in parts:
        sheet.text(x0, base, p, bold=b, size=size, c=c, va="baseline")
        x0 += width(sheet, p, bold=b, size=size)
    return total


def baseline_offset(size=9.5) -> float:
    """px from a va='center' anchor down to the baseline, for plain Helvetica text."""
    q = LIGHT.copy()
    q.set_size(size)
    h, d = _TTP.get_text_width_height_descent("lp", q, ismath=False)[1:]
    return (h / 2 - d) * 100 / 72


def chip(sheet, x, y, label, *, size=9.5, ha="left", pad=7, h=19, fill="#ffffff", edge=None, c=INK, z=4):
    """A Studio button: bold label in a rounded outline. Returns (x0, x1)."""
    w = width(sheet, label, bold=True, size=size) + 2 * pad
    x0 = x - w / 2 if ha == "center" else (x - w if ha == "right" else x)
    sheet.box(x0, y - h / 2, w, h, fill=fill, edge=edge or color("guide"), radius=4, lw=0.8, z=z)
    sheet.text(x0 + pad, y + 0.5, label, bold=True, size=size, c=c, z=z + 1)
    return x0, x0 + w


def line(sheet, pts, *, c=INK, lw=LINE_PT, style="-", z=5):
    xs, ys = zip(*pts)
    sheet.ax.plot(xs, ys, color=c, linewidth=lw, linestyle=style, solid_capstyle="butt",
                  solid_joinstyle="miter", zorder=z)


def arrow(sheet, p0, p1, *, c=INK, z=6):
    """Straight arrow p0 -> p1 with a constant shaft and the notched head."""
    (x0, y0), (x1, y1) = p0, p1
    length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    if length < 1.4 * HEAD[0]:
        warnings.warn(f"arrow {p0}->{p1} is {length:.0f} px, shorter than 1.4 heads", stacklevel=2)
    ribbon_arrow(sheet.ax, [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)], width=(SHAFT, SHAFT),
                 head=HEAD, c=c, z=z)


def route(sheet, pts, *, c=INK, z=6, dashed=False):
    """Right-angle route through pts; the last segment carries the head."""
    if len(pts) > 2:
        # Extend the plain part half a shaft into the arrow so the corner closes.
        line(sheet, pts[:-1], c=c, z=z, style=(0, (4, 3)) if dashed else "-")
    arrow(sheet, pts[-2], pts[-1], c=c, z=z)


def dot(sheet, x, y, *, c=INK, r=2.6, z=7):
    sheet.ax.add_patch(Circle((x, y), r, facecolor=c, edgecolor="none", zorder=z))


def bracket(sheet, x, y0, y1, label, *, c=SOFT, size=10, bold=True, tick=6, gap=12):
    """Left bracket from y0 to y1 at x, label rotated and centred to its left (site style)."""
    sheet.ax.plot([x + tick, x, x, x + tick], [y0, y0, y1, y1], color=c, linewidth=1.0, zorder=3)
    sheet.text(x - gap, (y0 + y1) / 2, label, bold=bold, size=size, c=c, rotation=90, ha="center")


def panel(sheet, x, y, w, h, *, fill="#ffffff", edge=None, radius=7, lw=1.0, z=2):
    return sheet.box(x, y, w, h, fill=fill, edge=edge or color("card_edge"), radius=radius, lw=lw, z=z)


def lines(sheet, x, y, rows, *, size=9.5, pitch=17, c=INK, room=None):
    """Several lines from y downward. A row is a string or a list of (text, bold) parts."""
    for i, row in enumerate(rows):
        yy = y + i * pitch
        if isinstance(row, str):
            text(sheet, x, yy, row, size=size, c=c, room=room)
        else:
            rich(sheet, x, yy, row, size=size, c=c, room=room)
    return y + (len(rows) - 1) * pitch
