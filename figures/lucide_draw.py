"""Draw Lucide line icons as vector paths on a site_style Sheet (y downward, 1 unit = 1 px).

Lucide icons use only path, circle, rect, line, polyline, polygon and ellipse on a
24 x 24 view box, so this small reader covers them without an SVG library: SVG path
commands M L H V C S Q T A Z (absolute and relative), arcs turned into cubic Beziers.

    import lucide_draw as li
    li.draw(sheet.ax, "mountain", cx, cy, 18, ink)
    li.write_licence_log(HERE / "data_to_results_icons.csv")

Icons: Lucide 1.61.0, ISC licence (no attribution needed in a figure; the licence is kept
with the icon files in figures/icons/lucide/). Only the icons the figures use are copied.
"""

from __future__ import annotations

import csv
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath

# Lucide 1.61.0 icons (ISC licence, figures/icons/lucide/LICENSE), copied as they are.
LUCIDE = Path(__file__).resolve().parent / "icons" / "lucide"
_USED: dict[str, dict] = {}


def _arc_to_cubics(x1, y1, rx, ry, phi_deg, large, sweep, x2, y2):
    """SVG elliptical arc (endpoint form, W3C F.6.5) as a list of cubic control triples."""
    if rx == 0 or ry == 0 or (x1 == x2 and y1 == y2):
        return [((x1, y1), (x2, y2), (x2, y2))]
    phi = math.radians(phi_deg)
    cp, sp = math.cos(phi), math.sin(phi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    rx, ry = abs(rx), abs(ry)
    lam = x1p**2 / rx**2 + y1p**2 / ry**2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx**2 * ry**2 - rx**2 * y1p**2 - ry**2 * x1p**2
    den = rx**2 * y1p**2 + ry**2 * x1p**2
    coef = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large == sweep:
        coef = -coef
    cxp, cyp = coef * rx * y1p / ry, -coef * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2
    cy = sp * cxp + cp * cyp + (y1 + y2) / 2

    def angle(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a

    t1 = angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = angle((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dt > 0:
        dt -= 2 * math.pi
    elif sweep and dt < 0:
        dt += 2 * math.pi
    n = max(1, int(math.ceil(abs(dt) / (math.pi / 2) - 1e-9)))
    step = dt / n
    k = 4 / 3 * math.tan(step / 4)
    out = []
    for i in range(n):
        a0, a1 = t1 + i * step, t1 + (i + 1) * step

        def pt(a, d=0.0):
            ex, ey = rx * (math.cos(a) - d * math.sin(a)), ry * (math.sin(a) + d * math.cos(a))
            return (cp * ex - sp * ey + cx, sp * ex + cp * ey + cy)

        p0, p3 = pt(a0), pt(a1)
        c1 = (p0[0] - k * rx * math.sin(a0) * cp - k * ry * math.cos(a0) * sp,
              p0[1] - k * rx * math.sin(a0) * sp + k * ry * math.cos(a0) * cp)
        c2 = (p3[0] + k * rx * math.sin(a1) * cp + k * ry * math.cos(a1) * sp,
              p3[1] + k * rx * math.sin(a1) * sp - k * ry * math.cos(a1) * cp)
        out.append((c1, c2, p3))
    return out


def _parse_d(d: str):
    """Path data to matplotlib vertices and codes. Arc flags may be packed ("0 011.5 2")."""
    pos, n = 0, len(d)
    num_re = re.compile(r"\s*,?\s*([-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?)")
    flag_re = re.compile(r"\s*,?\s*([01])")
    cmd_re = re.compile(r"\s*,?\s*([MmLlHhVvCcSsQqTtAaZz])")

    def num():
        nonlocal pos
        m = num_re.match(d, pos)
        pos = m.end()
        return float(m.group(1))

    def flag():
        nonlocal pos
        m = flag_re.match(d, pos)
        pos = m.end()
        return int(m.group(1))

    verts, codes = [], []
    cmd = None
    cur = start = (0.0, 0.0)
    last_ctrl, last_cmd = None, None
    while True:
        m = cmd_re.match(d, pos)
        if m:
            cmd = m.group(1)
            pos = m.end()
        elif not num_re.match(d, pos):
            break
        rel = cmd.islower()
        c = cmd.upper()
        ox, oy = cur if rel else (0.0, 0.0)
        if c == "Z":
            verts.append(start); codes.append(MPath.CLOSEPOLY)
            cur = start
            last_cmd = "Z"
            continue
        if c == "M":
            cur = (ox + num(), oy + num())
            start = cur
            verts.append(cur); codes.append(MPath.MOVETO)
            cmd = "l" if rel else "L"
            last_cmd = "M"
            continue
        if c == "L":
            cur = (ox + num(), oy + num())
            verts.append(cur); codes.append(MPath.LINETO)
        elif c == "H":
            cur = ((cur[0] if rel else 0.0) + num(), cur[1])
            verts.append(cur); codes.append(MPath.LINETO)
        elif c == "V":
            cur = (cur[0], (cur[1] if rel else 0.0) + num())
            verts.append(cur); codes.append(MPath.LINETO)
        elif c in "CS":
            if c == "C":
                c1 = (ox + num(), oy + num())
            else:
                c1 = (2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_cmd in ("C", "S") else cur
            c2 = (ox + num(), oy + num())
            end = (ox + num(), oy + num())
            verts += [c1, c2, end]; codes += [MPath.CURVE4] * 3
            last_ctrl, cur = c2, end
            last_cmd = c
            continue
        elif c in "QT":
            if c == "Q":
                q = (ox + num(), oy + num())
            else:
                q = (2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_cmd in ("Q", "T") else cur
            end = (ox + num(), oy + num())
            verts += [q, end]; codes += [MPath.CURVE3] * 2
            last_ctrl, cur = q, end
            last_cmd = c
            continue
        elif c == "A":
            rx, ry, phi = num(), num(), num()
            large, sweep = flag(), flag()
            end = (ox + num(), oy + num())
            for c1, c2, p3 in _arc_to_cubics(*cur, rx, ry, phi, large, sweep, *end):
                verts += [c1, c2, p3]; codes += [MPath.CURVE4] * 3
            cur = end
        last_cmd = c
    return verts, codes


def _ellipse(cx, cy, rx, ry):
    k = 0.5522847498
    v = [(cx + rx, cy), (cx + rx, cy + k * ry), (cx + k * rx, cy + ry), (cx, cy + ry),
         (cx - k * rx, cy + ry), (cx - rx, cy + k * ry), (cx - rx, cy),
         (cx - rx, cy - k * ry), (cx - k * rx, cy - ry), (cx, cy - ry),
         (cx + k * rx, cy - ry), (cx + rx, cy - k * ry), (cx + rx, cy), (cx + rx, cy)]
    return v, [MPath.MOVETO] + [MPath.CURVE4] * 12 + [MPath.CLOSEPOLY]


def _shapes(name: str):
    root = ET.parse(LUCIDE / f"{name}.svg").getroot()
    out = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        a = {k: v for k, v in el.attrib.items()}
        f = lambda k, d=0.0: float(a.get(k, d))  # noqa: E731
        if tag == "path":
            out.append(_parse_d(a["d"]))
        elif tag == "circle":
            out.append(_ellipse(f("cx"), f("cy"), f("r"), f("r")))
        elif tag == "ellipse":
            out.append(_ellipse(f("cx"), f("cy"), f("rx"), f("ry")))
        elif tag == "line":
            out.append(([(f("x1"), f("y1")), (f("x2"), f("y2"))], [MPath.MOVETO, MPath.LINETO]))
        elif tag in ("polyline", "polygon"):
            nums = [float(t) for t in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)", a["points"])]
            pts = list(zip(nums[::2], nums[1::2]))
            codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 1)
            if tag == "polygon":
                pts.append(pts[0]); codes.append(MPath.CLOSEPOLY)
            out.append((pts, codes))
        elif tag == "rect":
            x, y, w, h = f("x"), f("y"), f("width"), f("height")
            r = f("rx", a.get("ry", 0))
            if r > 0:
                d = (f"M{x + r} {y}H{x + w - r}A{r} {r} 0 0 1 {x + w} {y + r}V{y + h - r}"
                     f"A{r} {r} 0 0 1 {x + w - r} {y + h}H{x + r}A{r} {r} 0 0 1 {x} {y + h - r}"
                     f"V{y + r}A{r} {r} 0 0 1 {x + r} {y}Z")
                out.append(_parse_d(d))
            else:
                out.append(([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
                            [MPath.MOVETO] + [MPath.LINETO] * 3 + [MPath.CLOSEPOLY]))
    return out


def draw(ax, name: str, cx: float, cy: float, size: float, ink: str, *, lw: float = 1.2, z: float = 6):
    """Lucide icon `name` centred on (cx, cy), size px across (24-unit view box), stroke lw pt."""
    s = size / 24.0
    for verts, codes in _shapes(name):
        xy = np.array([(cx + (x - 12) * s, cy + (y - 12) * s) for x, y in verts])
        ax.add_patch(PathPatch(MPath(xy, codes), facecolor="none", edgecolor=ink, lw=lw,
                               capstyle="round", joinstyle="round", zorder=z))
    _USED[name] = {"ref": f"lucide:{name}", "licence": "ISC", "author": "Lucide contributors",
                   "version": "1.61.0", "file": f"figures/icons/lucide/{name}.svg"}


def write_licence_log(path) -> Path:
    path = Path(path)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ref", "licence", "author", "version", "file"])
        w.writeheader()
        for row in sorted(_USED.values(), key=lambda r: r["ref"]):
            w.writerow(row)
    return path
