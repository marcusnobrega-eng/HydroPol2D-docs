"""The Case Builder's three kinds of model area, for docs/builder/model-area.md.

Urban Basin (a city and every HydroBASINS level-12 basin upstream of it), Urban Area Only (the
urban footprint, a buffer, and the river inflows and coastal water level that can enter at its
edge) and Catchment (everything upstream of an outlet, with the three candidate outlets the
preview offers). Schematic maps, not a real place.

The tab names stay in English in every language, as in the Builder. Run from the repository root:

    python3 figures/case_builder_areas.py [preview-folder]

Output: static/img/builder/case-builder-areas.svg (en), case-builder-areas.pt.svg and
case-builder-areas.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

from matplotlib.patches import Circle, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flow_kit as fk  # noqa: E402
from site_style import INK, STATIC, WATER, Sheet, color, oklch_hex  # noqa: E402

W, H = 760, 424
NAME = "case-builder-areas"
CITY = oklch_hex(0.80, 0.105, 55)
CITY_EDGE = oklch_hex(0.62, 0.130, 50)
OUTLET = oklch_hex(0.58, 0.190, 25)
CANDIDATE = oklch_hex(0.76, 0.150, 70)
BASIN = color("deep_fill")
SEA = color("slot_wet_even")
INFLOW = oklch_hex(0.52, 0.150, 300)
FRAME = color("guide")

LABELS = {
    "en": {
        "urban": ["A city, by name or by polygon,", "and every HydroBASINS level-12", "basin upstream of it."],
        "only": ["The urban footprint and a buffer.", "River inflows and the coastal", "water level enter at the edge."],
        "catch": ["Everything upstream of an outlet,", "delineated on the model grid from", "one of three candidate outlets."],
        "legend": ["urban area", "model domain edge", "upstream basins", "rivers", "outlet you enter",
                   "candidate outlets", "river inflow (GloFAS)", "sea (GTSM level)"],
    },
    "pt": {
        "urban": ["Uma cidade, pelo nome ou por", "um polígono, e todas as bacias", "HydroBASINS nível 12", "a montante."],
        "only": ["A mancha urbana e uma faixa.", "Vazões de rios e o nível costeiro", "entram pela borda."],
        "catch": ["Tudo a montante de um exutório,", "delimitado na grade do modelo a", "partir de um de três candidatos."],
        "legend": ["área urbana", "borda do domínio", "bacias a montante", "rios", "exutório informado",
                   "exutórios candidatos", "vazão de rio (GloFAS)", "mar (nível GTSM)"],
    },
    "es": {
        "urban": ["Una ciudad, por nombre o por", "un polígono, y todas las", "cuencas HydroBASINS nivel 12", "aguas arriba."],
        "only": ["La mancha urbana y una franja.", "Caudales de ríos y el nivel", "costero entran por el borde."],
        "catch": ["Todo lo que está aguas arriba de", "una salida, delimitado en la malla", "a partir de una de tres", "candidatas."],
        "legend": ["área urbana", "borde del dominio", "cuencas aguas arriba", "ríos", "salida indicada",
                   "salidas candidatas", "caudal de río (GloFAS)", "mar (nivel GTSM)"],
    },
}

PANELS = [(20, "Urban Basin"), (270, "Urban Area Only"), (520, "Catchment")]
MAP_TOP = 56


def poly(s, ox, pts, *, fill, edge, lw=0.8, z=3, closed=True, style="-"):
    s.ax.add_patch(Polygon([(ox + x, MAP_TOP + y) for x, y in pts], closed=closed, facecolor=fill,
                           edgecolor=edge, linewidth=lw, linestyle=style, zorder=z, joinstyle="round"))


def river(s, ox, pts, lw=1.4):
    fk.line(s, [(ox + x, MAP_TOP + y) for x, y in pts], c=WATER, lw=lw, z=5)


def dot(s, ox, x, y, c, r=4.2):
    s.ax.add_patch(Circle((ox + x, MAP_TOP + y), r, facecolor=c, edgecolor="#ffffff", linewidth=1.0, zorder=8))


def urban_basin(s, ox):
    units = [
        [(60, 140), (150, 135), (175, 170), (140, 195), (70, 192), (45, 165)],
        [(60, 140), (150, 135), (160, 95), (110, 85), (55, 100)],
        [(55, 100), (110, 85), (95, 45), (50, 40), (30, 70)],
        [(110, 85), (160, 95), (190, 70), (170, 30), (120, 25), (95, 45)],
        [(95, 45), (120, 25), (105, 8), (70, 10), (50, 40)],
    ]
    for unit in units:
        poly(s, ox, unit, fill=BASIN, edge=color("guide"), lw=0.7)
    poly(s, ox, [(80, 150), (135, 147), (152, 168), (122, 186), (86, 183), (68, 166)],
         fill=CITY, edge=CITY_EDGE, z=4)
    river(s, ox, [(82, 18), (76, 58), (100, 92), (108, 140), (114, 196)])
    river(s, ox, [(168, 44), (142, 78), (104, 100)], lw=1.1)
    outer = [(45, 165), (70, 192), (140, 195), (175, 170), (150, 135), (160, 95), (190, 70), (170, 30),
             (120, 25), (105, 8), (70, 10), (50, 40), (30, 70), (55, 100), (60, 140)]
    poly(s, ox, outer, fill="none", edge=INK, lw=1.6, z=6)


def urban_only(s, ox):
    s.ax.add_patch(Polygon([(ox + x, MAP_TOP + y) for x, y in
                            [(120, 206), (140, 190), (168, 170), (190, 140), (204, 112), (212, 96),
                             (212, 206)]],
                           facecolor=SEA, edgecolor="none", zorder=2.7))
    city = [(52, 60), (120, 40), (165, 70), (170, 120), (140, 160), (80, 165), (45, 120)]
    buffer = [(30, 52), (120, 20), (185, 60), (192, 125), (152, 182), (72, 188), (22, 126)]
    poly(s, ox, buffer, fill="#ffffff", edge=INK, lw=1.6, z=3)
    poly(s, ox, city, fill=CITY, edge=CITY_EDGE, z=4)
    river(s, ox, [(5, 31), (34, 56), (90, 100), (140, 150), (170, 190)])
    river(s, ox, [(120, 0), (122, 21), (115, 70), (100, 104)], lw=1.1)
    fk.line(s, [(ox + 152, MAP_TOP + 182), (ox + 192, MAP_TOP + 125)], c=WATER, lw=3.2, z=6)
    dot(s, ox, 32, 53, INFLOW)
    dot(s, ox, 122, 21, INFLOW)


def catchment(s, ox):
    outline = [(108, 196), (80, 170), (40, 150), (22, 112), (35, 70), (62, 34), (100, 12), (148, 18),
               (182, 46), (192, 92), (178, 130), (150, 160), (124, 176)]
    poly(s, ox, outline, fill=BASIN, edge=INK, lw=1.6)
    river(s, ox, [(110, 194), (112, 150), (104, 110), (90, 70), (82, 36)])
    river(s, ox, [(112, 150), (146, 118), (170, 80)], lw=1.1)
    river(s, ox, [(104, 110), (60, 96), (42, 84)], lw=1.1)
    river(s, ox, [(90, 70), (130, 46), (150, 30)], lw=1.0)
    dot(s, ox, 103, 166, OUTLET, r=4.6)
    dot(s, ox, 111, 182, CANDIDATE, r=3.8)
    dot(s, ox, 112, 156, CANDIDATE, r=3.8)
    dot(s, ox, 124, 141, CANDIDATE, r=3.8)


def legend(s, y, labels):
    items = [
        ("swatch", CITY, CITY_EDGE), ("edge", INK, None), ("swatch", BASIN, color("guide")),
        ("river", WATER, None), ("dot", OUTLET, None), ("dot", CANDIDATE, None), ("dot", INFLOW, None),
        ("sea", SEA, WATER),
    ]
    # Two rows of four.
    for k, ((kind, c, edge), label) in enumerate(zip(items, labels)):
        x = 34 + 185 * (k % 4)
        yy = y + 20 * (k // 4)
        if kind == "swatch":
            s.box(x, yy - 6, 16, 12, fill=c, edge=edge, radius=2, lw=0.8, z=4)
        elif kind == "edge":
            s.box(x, yy - 6, 16, 12, fill="#ffffff", edge=c, radius=2, lw=1.6, z=4)
        elif kind == "sea":
            s.box(x, yy - 6, 16, 12, fill=c, edge="none", radius=2, lw=0, z=4)
            fk.line(s, [(x, yy - 6), (x + 16, yy - 6)], c=edge, lw=3.2, z=5)
        elif kind == "river":
            fk.line(s, [(x, yy), (x + 16, yy)], c=c, lw=1.6, z=4)
        else:
            s.ax.add_patch(Circle((x + 8, yy), 4.2, facecolor=c, edgecolor="#ffffff", lw=1.0, zorder=5))
        fk.text(s, x + 22, yy, label, room=160)


def draw(lang: str, preview: Path | None = None) -> None:
    t = LABELS[lang]
    s = Sheet(W, H, NAME)
    for (ox, name), draw_map, rows in zip(PANELS, (urban_basin, urban_only, catchment),
                                          (t["urban"], t["only"], t["catch"])):
        fk.panel(s, ox, 16, 220, 330)
        fk.text(s, ox + 14, 36, name, bold=True, size=10.5)
        s.box(ox + 6, MAP_TOP - 4, 208, 210, fill="#ffffff", edge=FRAME, radius=4, lw=0.6, z=2.5)
        draw_map(s, ox + 2)
        fk.lines(s, ox + 14, 282, rows, room=200)
    legend(s, 370, t["legend"])
    svg = s.save(STATIC / "builder", lang, preview)
    print("wrote", svg.name)


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
