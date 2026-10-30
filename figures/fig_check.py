"""Layout checks for the docs schematic drafts: text overlaps, text over arrows, tiny text.

    from fig_check import track, report
    with track(sheet.ax) as arrows:   # patches added inside the block count as arrows
        sheet.arrow(...)
    report(sheet)                     # prints overlaps before save()
"""

from __future__ import annotations

from contextlib import contextmanager

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg

_ARROWS: list = []


@contextmanager
def track(ax):
    n_patches, n_lines = len(ax.patches), len(ax.lines)
    yield
    _ARROWS.extend(list(ax.patches)[n_patches:])
    _ARROWS.extend(list(ax.lines)[n_lines:])


def _text_boxes(sheet, pad=1.0):
    canvas = FigureCanvasAgg(sheet.fig)
    renderer = canvas.get_renderer()
    inv = sheet.ax.transData.inverted()
    boxes = []
    for t in sheet.ax.texts:
        if not t.get_text().strip() or not t.get_visible():
            continue
        bb = t.get_window_extent(renderer)
        (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        boxes.append((t, min(x0, x1) - pad, min(y0, y1) - pad, max(x0, x1) + pad, max(y0, y1) + pad))
    return boxes


def _vertices(artist):
    if hasattr(artist, "get_xy"):
        return np.asarray(artist.get_xy())
    if hasattr(artist, "get_xydata"):
        return np.asarray(artist.get_xydata())
    return np.empty((0, 2))


def report(sheet, *, quiet_pairs=()):
    boxes = _text_boxes(sheet)
    problems = 0
    for i, (ta, *a) in enumerate(boxes):
        for tb, *b in boxes[i + 1:]:
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                pair = (ta.get_text()[:28], tb.get_text()[:28])
                if pair not in quiet_pairs:
                    print(f"TEXT/TEXT  {pair[0]!r}  x  {pair[1]!r}")
                    problems += 1
    for t, x0, y0, x1, y1 in boxes:
        for art in _ARROWS:
            v = _vertices(art)
            if len(v) == 0:
                continue
            if len(v) < 40:  # densify straight segments
                v = np.vstack([np.linspace(v[k], v[k + 1], 20) for k in range(len(v) - 1)]) if len(v) > 1 else v
            inside = (v[:, 0] > x0) & (v[:, 0] < x1) & (v[:, 1] > y0) & (v[:, 1] < y1)
            if inside.any():
                print(f"TEXT/ARROW {t.get_text()[:40]!r} at ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
                problems += 1
                break
    for t, x0, y0, x1, y1 in boxes:
        if x0 < 6 or x1 > sheet.W - 6 or y0 < 6 or y1 > sheet.H - 6:
            print(f"OUTSIDE    {t.get_text()[:40]!r} ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
            problems += 1
        if t.get_fontsize() < 9:
            print(f"SMALL      {t.get_text()[:40]!r} {t.get_fontsize()}")
            problems += 1
    print(f"{problems} layout problem(s)")
    _ARROWS.clear()  # the next sheet (the next language) starts with its own arrows
    return boxes
