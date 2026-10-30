"""Where water enters, leaves or is controlled in one model domain, for
docs/theory/hydrodynamic-model.md, section 2.6 (boundary conditions and hydraulic controls).

A plan view of a schematic catchment on a regular grid (seeded, so it can be redrawn):
the open boundaries drawn along the domain perimeter (inflow hydrograph, stage
hydrograph, outlet), the closed walls, and the internal structures (a reservoir or
control structure, a culvert under a road, a detention pond). An inset shows the
groundwater boundaries on the same domain. A footer names the Studio tools and says
which structures also run on Voronoi and quadtree meshes. Every element is traced in
FACTS at the end.

The terrain, rivers, road and pond are synthetic: an illustration, not a real case.

Run from the repository root:

    python3 figures/boundaries_structures.py [preview-folder]

Output: static/img/theory/boundaries-structures.svg (en), boundaries-structures.pt.svg
and boundaries-structures.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.patches import Circle, Polygon, Rectangle
from scipy import ndimage
from shapely.geometry import LineString, Point
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import box as shapely_box
from shapely.ops import linemerge, unary_union

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_style import INK, SOFT, STATIC, WATER, Sheet, color, hex_of, oklch_hex  # noqa: E402
import flow_kit  # noqa: E402,F401  (unhinted glyphs: the room checks measure what the SVG draws)
from fig_check import _ARROWS, report, track  # noqa: E402

W, H = 760, 620       # the least height; it grows with the notes of a language
NAME = "boundaries-structures"
SEED = 20261027

# --- text per language ---------------------------------------------------------------------
# "notes" are the seven numbered notes on the right; "footer" is a list of paragraphs.
LABELS = {
    "en": {
        "title": "Boundaries and structures in a model domain",
        "notes": [
            ("Inflow hydrograph",
             [r"discharge $Q(t)$ enters through the drawn faces,",
              r"an equal share $Q(t)/N$ through each of $N$"]),
            ("Reservoir or control structure",
             [r"internal boundary: a source cell of depth $h$",
              r"releases $Q = k\,\max(h - h_0,\,0)^{b}$ to a release cell",
              "or out of the domain; up to two, summed;",
              r"$k$ rating coefficient, $h_0$ sill depth, $b$ exponent"]),
            ("Culvert or bridge",
             ["a road crossing a stream, added as a control;",
              r"first sized as $Q = C_d\,A\,\sqrt{2g\,(h - h_0)}$ from",
              r"the opening area $A$ and a coefficient $C_d$"]),
            ("Detention pond",
             ["a level pool fed by the cells at its edge;",
              "orifice, spillway or pump to a chosen cell"]),
            ("Stage hydrograph",
             [r"each step the cells are reset to a level $\eta(t)$ or",
              r"depth $h(t)$; the volume change is boundary flow"]),
            ("Outlet",
             [r"normal depth  $Q = (w/n)\,h^{5/3}\,S_0^{1/2}$",
              r"critical depth  $Q = w\,\sqrt{g}\,h^{3/2}$",
              r"$h$ depth, $w$ face width, $n$ Manning, $S_0$ slope"]),
            ("Closed wall",
             ["every other perimeter face: no flow"]),
        ],
        "key": ["open boundary", "closed wall", "water flow", "source or release cell"],
        "gw_title": "Groundwater boundaries",
        "gw_role": "on the same domain",
        "gw": [
            ("Fixed head", [r"head $h = h_{\mathrm{D}}$ on the cells", "given in the head map"]),
            ("No flow", ["across the domain edge,", "the default"]),
            ("Outside the domain", ["no groundwater cells"]),
        ],
        "footer": [["Studio draws these under Study area: Boundaries,",
                    "Facilities, and Culverts and bridges."],
                   ["Voronoi and quadtree meshes run 2 to 4 as well",
                    "(CPU engine; no river channels or sub-grid tables)."]],
    },
    "pt": {
        "title": "Contornos e estruturas em um domínio do modelo",
        "notes": [
            ("Hidrograma de entrada",
             [r"a vazão $Q(t)$ entra pelas faces desenhadas:",
              r"$Q(t)/N$ em cada uma das $N$"]),
            ("Reservatório ou estrutura de controle",
             ["contorno interno: uma célula de origem com",
              r"profundidade $h$ libera $Q = k\,\max(h - h_0,\,0)^{b}$",
              "para uma célula de destino ou para fora do",
              r"domínio; até duas, somadas; $k$ coeficiente,",
              r"$h_0$ profundidade da soleira, $b$ expoente"]),
            ("Bueiro ou ponte",
             ["uma via que cruza um curso d'água, incluída",
              "como controle; dimensionada de início por",
              r"$Q = C_d\,A\,\sqrt{2g\,(h - h_0)}$, com a área da",
              r"abertura $A$ e um coeficiente $C_d$"]),
            ("Bacia de detenção",
             ["um reservatório de nível único, alimentado",
              "pelas células da borda; orifício, vertedor ou",
              "bomba para uma célula escolhida"]),
            ("Hidrograma de nível",
             [r"a cada passo, as células voltam ao nível $\eta(t)$",
              r"ou à profundidade $h(t)$; a variação de volume",
              "conta como fluxo pelo contorno"]),
            ("Exutório",
             [r"profundidade normal  $Q = (w/n)\,h^{5/3}\,S_0^{1/2}$",
              r"profundidade crítica  $Q = w\,\sqrt{g}\,h^{3/2}$",
              r"$h$ profundidade, $w$ largura da face, $n$ Manning,",
              r"$S_0$ inclinação"]),
            ("Parede fechada",
             ["todas as outras faces do perímetro: sem fluxo"]),
        ],
        "key": ["contorno aberto", "parede fechada", "escoamento", "célula de origem ou destino"],
        "gw_title": "Contornos das águas subterrâneas",
        "gw_role": "no mesmo domínio",
        "gw": [
            ("Carga fixa", [r"$h = h_{\mathrm{D}}$ nas células", "do mapa de carga"]),
            ("Sem fluxo", ["pela borda do domínio,", "o padrão"]),
            ("Fora do domínio", ["sem células de águas", "subterrâneas"]),
        ],
        "footer": [["No Studio: Study area > Boundaries, Facilities",
                    "e Culverts and bridges."],
                   ["Malhas Voronoi e quadtree também rodam 2 a 4",
                    "(motor de CPU; sem canais de rio nem subgrade)."]],
    },
    "es": {
        "title": "Contornos y estructuras en un dominio del modelo",
        "notes": [
            ("Hidrograma de entrada",
             [r"el caudal $Q(t)$ entra por las caras dibujadas:",
              r"$Q(t)/N$ por cada una de las $N$"]),
            ("Embalse o estructura de control",
             ["contorno interno: una celda de origen de",
              r"profundidad $h$ libera $Q = k\,\max(h - h_0,\,0)^{b}$",
              "hacia una celda de destino o fuera del",
              r"dominio; hasta dos, sumadas; $k$ coeficiente,",
              r"$h_0$ profundidad del umbral, $b$ exponente"]),
            ("Alcantarilla o puente",
             ["un camino que cruza un cauce, añadido como",
              "control; dimensionado primero con",
              r"$Q = C_d\,A\,\sqrt{2g\,(h - h_0)}$, según el área",
              r"de la abertura $A$ y un coeficiente $C_d$"]),
            ("Estanque de detención",
             ["un depósito de nivel horizontal alimentado",
              "por las celdas de su borde; orificio, vertedero",
              "o bomba hacia una celda elegida"]),
            ("Hidrograma de nivel",
             [r"en cada paso las celdas vuelven al nivel $\eta(t)$ o",
              r"a la profundidad $h(t)$; el cambio de volumen",
              "cuenta como flujo por el contorno"]),
            ("Salida",
             [r"profundidad normal  $Q = (w/n)\,h^{5/3}\,S_0^{1/2}$",
              r"profundidad crítica  $Q = w\,\sqrt{g}\,h^{3/2}$",
              r"$h$ profundidad, $w$ ancho de la cara, $n$ Manning,",
              r"$S_0$ pendiente"]),
            ("Pared cerrada",
             ["todas las demás caras del perímetro: sin flujo"]),
        ],
        "key": ["contorno abierto", "pared cerrada", "flujo de agua", "celda de origen o de destino"],
        "gw_title": "Contornos del agua subterránea",
        "gw_role": "en el mismo dominio",
        "gw": [
            ("Carga fija", [r"$h = h_{\mathrm{D}}$ en las celdas", "del mapa de carga"]),
            ("Sin flujo", ["a través del borde del", "dominio, por defecto"]),
            ("Fuera del dominio", ["sin celdas de agua", "subterránea"]),
        ],
        "footer": [["En Studio: Study area > Boundaries, Facilities",
                    "y Culverts and bridges."],
                   ["Las mallas de Voronoi y quadtree ejecutan 2 a 4",
                    "(motor de CPU; sin canales de río ni submalla)."]],
    },
}
SYMBOLS = {"q_t": r"$Q(t)$", "h_t": r"$\eta(t)$"}

# --- colours: palette tokens; SURFACE_WATER as in the cell water budget figure ---------------
SURFACE_WATER = oklch_hex(0.72, 0.090, 245)   # ponded and river water
TERRAIN_RAMP = [hex_of(k) for k in ("soil_3", "soil_2", "soil_1", "rock_b", "rock_a")]  # low to high
EDGE = color("card_edge")
LINE = color("guide")
GW_FILL = color("slot_wet_even")
ROAD_CASE = color("text_soft")

# --- geometry (cell units u = column, v = row; px = origin + cell * u) ----------------------
CELL, NC, NR = 13, 30, 22
MX0, MY0 = 24, 62
GW_CELL, GX0, GY0 = 6, 40, 446
GW_PANEL = (420, 606)  # inset top and bottom, on a card of height H
KEY_Y = 383

OUTLINE = [(9, 2.2), (13, 1.2), (19, 0.9), (23, 1.8), (26.5, 3.8), (28.5, 7), (28.9, 10.5),
           (27.8, 12.5), (29.4, 14), (29.4, 18.2), (26, 19.8), (20, 20.6), (15.5, 21.5),
           (11.5, 21.5), (7, 20.2), (3.5, 18), (1.3, 14.5), (1.0, 10.5), (2.2, 7), (4.5, 4.5)]
MAIN = [(17.3, -1.0), (17.0, 2.5), (15.5, 5.5), (16.5, 8.5), (14.5, 11.5), (14.8, 14.5),
        (13.2, 17.5), (13.5, 20.0), (13.4, 23.0)]
TRIB = [(3.2, 8.4), (5.5, 9.4), (8.5, 11.2), (11.5, 12.4), (14.6, 12.6)]
ROAD = [(8.6, 1.5), (8.1, 7.0), (7.4, 12.0), (6.6, 21.0)]
POND = [(19.6, 11.4), (23.3, 11.1), (24.1, 13.4), (22.8, 15.1), (19.5, 14.7)]
DAM_ROW = 6              # the dam sits on this row line (a cell face)
NOTE_X = 452             # badge column of the notes
NOTE_GAP = 8
NOTE_PITCH = 17      # between the lines of a note


def P(u, v):
    return MX0 + u * CELL, MY0 + v * CELL


def chaikin(points, rounds=2):
    """Corner cutting of a closed outline."""
    pts = np.asarray(points, dtype=float)
    for _ in range(rounds):
        nxt = np.roll(pts, -1, axis=0)
        out = np.empty((2 * len(pts), 2))
        out[0::2], out[1::2] = 0.75 * pts + 0.25 * nxt, 0.25 * pts + 0.75 * nxt
        pts = out
    return pts


def smooth_line(points, n=200):
    """Catmull-Rom through the points (cell units)."""
    p = np.asarray(points, dtype=float)
    p = np.vstack([2 * p[0] - p[1], p, 2 * p[-1] - p[-2]])
    out = []
    for k in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[k - 1], p[k], p[k + 1], p[k + 2]
        for t in np.linspace(0, 1, n // (len(p) - 3), endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(p[-2])
    return LineString(out)


def build_domain():
    rng = np.random.default_rng(SEED)
    outline = ShapelyPolygon(chaikin(OUTLINE))
    active = np.zeros((NR, NC), dtype=bool)
    for j in range(NR):
        for i in range(NC):
            active[j, i] = outline.contains(Point(i + 0.5, j + 0.5))
    labels, n = ndimage.label(active)            # keep the largest D4 component, no holes
    sizes = ndimage.sum(active, labels, range(1, n + 1))
    active = ndimage.binary_fill_holes(labels == 1 + int(np.argmax(sizes)))
    main, trib = smooth_line(MAIN), smooth_line(TRIB)
    noise = ndimage.gaussian_filter(rng.normal(size=(NR, NC)), 1.6)
    noise = noise / np.abs(noise).max()
    z = np.full((NR, NC), np.nan)
    for j in range(NR):
        for i in range(NC):
            if active[j, i]:
                c = Point(i + 0.5, j + 0.5)
                d = min(main.distance(c), trib.distance(c))
                z[j, i] = (0.42 * (1 - j / NR) + 0.38 * (1 - i / NC) + 0.06 * min(d, 4.0)
                           + 0.06 * noise[j, i])
    z = (z - np.nanmin(z)) / (np.nanmax(z) - np.nanmin(z))
    return active, z, main, trib


def perimeter_faces(active):
    """(i, j, side, segment) for every face between an active cell and the outside."""
    faces = []
    for j in range(NR):
        for i in range(NC):
            if not active[j, i]:
                continue
            for side, (di, dj), seg in (("W", (-1, 0), ((i, j), (i, j + 1))),
                                        ("E", (1, 0), ((i + 1, j), (i + 1, j + 1))),
                                        ("N", (0, -1), ((i, j), (i + 1, j))),
                                        ("S", (0, 1), ((i, j + 1), (i + 1, j + 1)))):
                ii, jj = i + di, j + dj
                if not (0 <= ii < NC and 0 <= jj < NR) or not active[jj, ii]:
                    faces.append((i, j, side, seg))
    return faces


def pick_faces(faces, side, target, radius):
    tx, ty = target
    out = [f for f in faces if f[2] == side
           and np.hypot((f[3][0][0] + f[3][1][0]) / 2 - tx, (f[3][0][1] + f[3][1][1]) / 2 - ty) <= radius]
    return out




def notes_layout(T):
    """Heading and line positions of the numbered notes, and the y after the last one."""
    y = 58
    notes = []
    for n, (head, lines) in enumerate(T["notes"], start=1):
        yy = y + 19
        rows = []
        for line in lines:
            tall = r"\sqrt" in line                 # a radical needs a little more room above
            deep = "_0^" in line                    # and S_0^{1/2} a little below
            yy += 3 if tall else 0
            rows.append((line, yy))
            yy += NOTE_PITCH + (2 if tall else 0) + (2 if deep else 0)
        notes.append((n, y, head, rows))
        y = yy - NOTE_PITCH + 19 + NOTE_GAP
    return notes, y


def footer_layout(T, notes_end):
    """(line, x, y, room) of the footer paragraphs. Each paragraph goes under the column
    that ends higher: the notes on the right, or the groundwater inset on the left."""
    columns = {"right": [NOTE_X - 8, notes_end + 6, W - 10 - (NOTE_X - 8)],
               "left": [30, GW_PANEL[1] + 20, 424 - 30]}
    rows = []
    for paragraph in T["footer"]:
        column = min(columns.values(), key=lambda col: col[1])
        x, y, room = column
        for line in paragraph:
            rows.append((line, x, y, room))
            y += 17
        column[1] = y + 6
    return rows


def draw(lang: str, preview: Path | None = None) -> Path:
    T = LABELS[lang]
    _ARROWS.clear()  # fig_check keeps the arrows of every sheet; check this one only
    notes, notes_end = notes_layout(T)
    footer = footer_layout(T, notes_end)
    height = max(H, int(np.ceil(max(y for _, _, y, _ in footer) + 23)), int(np.ceil(notes_end + 12)))
    # The left column keeps its place; a taller card leaves room below the inset.
    key_y = KEY_Y
    panel_y0, panel_y1 = GW_PANEL
    gw_y0 = GY0

    s = Sheet(W, height, NAME)
    ax = s.ax
    renderer = RendererAgg(W, height, 100)

    def width_of(artist):
        return artist.get_window_extent(renderer).width

    def put(x, y, text, *, room=None, **kw):
        artist = s.text(x, y, text, **kw)
        if room is not None and width_of(artist) > room:
            print(f"WARNING: '{text[:44]}' is {width_of(artist):.0f} px, room {room} px")
        return artist

    def badge(x, y, n):
        ax.add_patch(Circle((x, y), 8.2, facecolor=INK, edgecolor="white", linewidth=1.2, zorder=20))
        s.text(x, y + 0.4, str(n), bold=True, size=9.5, c="white", ha="center", z=21)

    def cell_outline(i, j, *, c=INK, lw=1.3, z=12):
        x, y = P(i, j)
        ax.add_patch(Rectangle((x, y), CELL, CELL, facecolor="none", edgecolor=c, linewidth=lw,
                               zorder=z, joinstyle="miter"))

    def flow(points, **kw):
        kw.setdefault("width", (1.2, 3.8))
        kw.setdefault("head", (12, 11))
        with track(ax):
            s.arrow(points, c=WATER, **kw)

    def path_px(line):
        xy = np.asarray(line.coords)
        return MX0 + xy[:, 0] * CELL, MY0 + xy[:, 1] * CELL

    active, z, main_river, trib = build_domain()
    lake = []
    faces = perimeter_faces(active)
    domain = unary_union([shapely_box(i, j, i + 1, j + 1) for j in range(NR) for i in range(NC) if active[j, i]])

    put(24, 26, T["title"], bold=True, size=11)

    # --- terrain cells ------------------------------------------------------------------------
    for j in range(NR):
        for i in range(NC):
            if active[j, i]:
                x, y = P(i, j)
                k = min(int(z[j, i] * len(TERRAIN_RAMP)), len(TERRAIN_RAMP) - 1)
                ax.add_patch(Rectangle((x, y), CELL, CELL, facecolor=TERRAIN_RAMP[k], edgecolor=EDGE,
                                       linewidth=0.35, zorder=2))

    # --- rivers, clipped to the domain --------------------------------------------------------
    for line, lw in ((main_river, 3.0), (trib, 2.2)):
        clipped = line.intersection(domain)
        for g in getattr(clipped, "geoms", [clipped]):
            if g.geom_type == "LineString":
                xs, ys = path_px(g)
                ax.plot(xs, ys, color=SURFACE_WATER, linewidth=lw, solid_capstyle="round", zorder=4)

    # --- reservoir: lake behind a dam on a cell face, a source cell and a release cell ---------
    def river_u(line, v):
        """Column where a river crosses the row line v (first crossing)."""
        hit = line.intersection(LineString([(-5, v), (NC + 5, v)]))
        pts = [hit] if hit.geom_type == "Point" else list(hit.geoms)
        return pts[0].x

    dam_v = DAM_ROW
    for i, j in [(i, j) for j in range(dam_v - 4, dam_v) for i in range(NC)]:
        if not active[j, i]:
            continue
        reach = 0.9 + 0.55 * (j - (dam_v - 4))            # wider towards the dam
        if abs(i + 0.5 - river_u(main_river, j + 0.5)) <= reach:
            lake.append((i, j))
    for i, j in lake:
        x, y = P(i, j)
        ax.add_patch(Rectangle((x, y), CELL, CELL, facecolor=SURFACE_WATER, edgecolor=EDGE,
                               linewidth=0.35, zorder=5))
    u_dam = river_u(main_river, dam_v)
    lake_cols = [i for i, j in lake if j == dam_v - 1]
    dx0, dy0 = P(min(lake_cols) - 0.4, dam_v)
    dx1, dy1 = P(max(lake_cols) + 1.4, dam_v)
    s.line([dx0, dx1], [dy0, dy1], c=INK, lw=3.6, z=9)
    dam_pt = Point(u_dam, dam_v)

    def cell_of(pt):
        return int(np.floor(pt.x)), int(np.floor(pt.y))

    src = (int(np.floor(river_u(main_river, dam_v - 0.5))), dam_v - 1)
    rel = (int(np.floor(river_u(main_river, dam_v + 3.5))), dam_v + 3)
    cell_outline(*src)
    cell_outline(*rel)
    sx, sy = P(src[0] + 1.0, src[1] + 0.5)
    rx, ry = P(rel[0] + 1.0, rel[1] + 0.5)
    flow([(sx, sy), (sx + 30, sy + 6), (rx + 22, ry - 8), (rx + 1, ry)])

    # --- culvert: a road over the tributary, source and release cells on either side ------------
    road = smooth_line(ROAD).intersection(domain)
    for g in getattr(road, "geoms", [road]):
        xs, ys = path_px(g)
        ax.plot(xs, ys, color=ROAD_CASE, linewidth=4.2, solid_capstyle="butt", zorder=6)
        ax.plot(xs, ys, color="white", linewidth=2.0, solid_capstyle="butt", zorder=7)
    cross = smooth_line(ROAD).intersection(trib)
    cs = trib.project(cross if cross.geom_type == "Point" else cross.geoms[0])
    c_src = cell_of(trib.interpolate(cs - 1.7))
    c_rel = cell_of(trib.interpolate(cs + 1.7))
    cell_outline(*c_src)
    cell_outline(*c_rel)
    ax0, ay0 = P(c_src[0] + 1.0, c_src[1] + 0.5)      # right edge of the source cell
    ax1, ay1 = P(c_rel[0] + 0.5, c_rel[1])            # top edge of the release cell
    flow([(ax0, ay0), (ax1 - 2, ay0 + 1), (ax1, ay1 - 10), (ax1, ay1 - 0.5)])

    # --- detention pond with one device to a chosen cell ----------------------------------------
    pond_px = [P(u, v) for u, v in POND]
    ax.add_patch(Polygon(pond_px, closed=True, facecolor=SURFACE_WATER, edgecolor=INK, linewidth=1.0,
                         zorder=8))
    dev = P(19.57, 12.5)
    p_rel = (16, 12)
    cell_outline(*p_rel)
    flow([(dev[0] - 1, dev[1]), P(p_rel[0] + 1, p_rel[1] + 0.5)])

    # --- domain outline (closed walls) and the open boundaries ---------------------------------
    ox, oy = domain.exterior.xy
    s.line([MX0 + u * CELL for u in ox], [MY0 + v * CELL for v in oy], c=INK, lw=1.5, z=14)

    def open_boundary(sel):
        merged = linemerge([LineString(f[3]) for f in sel])
        for g in getattr(merged, "geoms", [merged]):
            xs, ys = path_px(g)
            ax.plot(xs, ys, color=WATER, linewidth=4.2, solid_capstyle="butt", solid_joinstyle="miter",
                    zorder=15)
        return merged

    inflow = open_boundary(pick_faces(faces, "N", (17.1, 1.0), 1.8))
    outlet = open_boundary(pick_faces(faces, "S", (13.4, 21.5), 1.8))
    stage = open_boundary(pick_faces(faces, "E", (29.0, 16.1), 2.3))

    # inflow arrow and hydrograph glyph
    ix = MX0 + inflow.centroid.x * CELL
    iy = MY0 + inflow.bounds[1] * CELL
    flow([(ix, iy - 30), (ix, iy - 3)])
    gx, gy = ix - 56, iy - 34
    s.line([gx, gx, gx + 34], [gy, gy + 20, gy + 20], c=SOFT, lw=0.8, z=12)
    tt = np.linspace(0, 1, 40)
    qq = np.exp(-((tt - 0.32) / 0.16) ** 2) * 0.8 + 0.12
    ax.plot(gx + 2 + tt * 30, gy + 20 - qq * 18, color=WATER, linewidth=1.3, zorder=12)
    put(gx - 4, gy + 10, SYMBOLS["q_t"], size=10, ha="right")

    # outlet arrow
    ox_ = MX0 + outlet.centroid.x * CELL
    oy_ = MY0 + outlet.bounds[3] * CELL
    flow([(ox_, oy_ + 3), (ox_, oy_ + 30)])

    # stage glyph: water-level triangle outside the edge
    stx = MX0 + stage.bounds[2] * CELL + 15
    sty = MY0 + stage.centroid.y * CELL
    ax.add_patch(Polygon([(stx - 6, sty - 6), (stx + 6, sty - 6), (stx, sty + 2)], closed=True,
                         facecolor=WATER, edgecolor="none", zorder=12))
    s.line([stx - 7, stx + 7], [sty + 5, sty + 5], c=WATER, lw=1.0, z=12)
    s.line([stx - 4, stx + 4], [sty + 8, sty + 8], c=WATER, lw=1.0, z=12)
    put(stx + 2, sty + 21, SYMBOLS["h_t"], size=10, ha="center")

    # --- badges on the map ---------------------------------------------------------------------
    badge(ix + 16, iy - 22, 1)
    badge(*P(max(lake_cols) + 2.6, dam_v - 1.6), 2)
    badge(*P(c_src[0] - 1.0, c_src[1] - 0.9), 3)
    badge(*P(24.9, 11.3), 4)
    badge(stx, sty - 20, 5)
    badge(ox_ + 18, oy_ + 18, 6)
    badge(*P(2.6, 4.6), 7)

    # --- notes ---------------------------------------------------------------------------------
    tx_ = NOTE_X + 15
    room = W - 10 - tx_
    for n, y, head, rows in notes:
        badge(NOTE_X, y, n)
        put(tx_, y, head, bold=True, size=10, room=room)
        for line, yy in rows:
            put(tx_, yy, line, room=room)

    # --- key under the map ------------------------------------------------------------------
    k0, k1, ky = 30, 236, key_y
    s.line([k0, k0 + 22], [ky, ky], c=WATER, lw=4.2)
    put(k0 + 30, ky, T["key"][0])
    s.line([k1, k1 + 22], [ky, ky], c=INK, lw=1.5)
    put(k1 + 30, ky, T["key"][1])
    ky += 21
    with track(ax):
        s.arrow([(k0, ky), (k0 + 24, ky)], c=WATER, width=(1.2, 3.8), head=(12, 11))
    put(k0 + 30, ky, T["key"][2])
    ax.add_patch(Rectangle((k1 + 4.5, ky - 6.5), CELL, CELL, facecolor="none", edgecolor=INK,
                           linewidth=1.3, zorder=12))
    put(k1 + 30, ky, T["key"][3])

    # --- groundwater inset ----------------------------------------------------------------------
    s.box(24, panel_y0, 400, panel_y1 - panel_y0, fill=color("card"), edge=EDGE)
    title = put(40, panel_y0 + 18, T["gw_title"], bold=True, size=10.5)
    put(40 + width_of(title) + 8, panel_y0 + 18, T["gw_role"], c=SOFT)
    fixed = [(i, j) for (i, j, side, _) in pick_faces(faces, "E", (29.0, 16.1), 2.3)]
    fixed += [(i - 1, j) for (i, j) in fixed if active[j, i - 1]]
    for j in range(NR):
        for i in range(NC):
            if active[j, i]:
                x, y0 = GX0 + i * GW_CELL, gw_y0 + j * GW_CELL
                ax.add_patch(Rectangle((x, y0), GW_CELL, GW_CELL, edgecolor="white", linewidth=0.3,
                                       zorder=3, facecolor=WATER if (i, j) in fixed else GW_FILL))
    s.line([GX0 + u * GW_CELL for u in ox], [gw_y0 + v * GW_CELL for v in oy], c=INK, lw=1.2, z=6)
    lx = GX0 + NC * GW_CELL + 22
    gy_ = gw_y0 + 12
    yk = gy_
    for k, (head, lines) in enumerate(T["gw"]):
        if k:
            yk += 18 + 16 * len(T["gw"][k - 1][1]) + 4
        if k == 0:
            ax.add_patch(Rectangle((lx, yk - 5), 10, 10, facecolor=WATER, edgecolor="none", zorder=6))
        elif k == 1:
            s.line([lx - 2, lx + 12], [yk, yk], c=INK, lw=1.5)
        else:
            ax.add_patch(Rectangle((lx, yk - 5), 10, 10, facecolor="white", edgecolor=LINE,
                                   linewidth=0.8, zorder=6))
        put(lx + 18, yk, head, bold=True, size=10, room=424 - lx - 30)
        for m, line in enumerate(lines):
            put(lx + 18, yk + 18 + 16 * m, line, room=424 - lx - 30)

    for line, xf, yf, room_f in footer:
        put(xf, yf, line, c=SOFT, room=room_f)

    print(lang, f"H = {height}", end=": ")
    report(s)
    svg = s.save(STATIC / "theory", lang, preview)
    print(lang, "->", svg, "active cells:", int(active.sum()), "lake cells:", len(lake))
    return svg


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


# --- what each element shows and where it is stated -----------------------------------------
# Docs pages under docs/: HM theory/hydrodynamic-model, GW theory/groundwater-model,
# AM validation/ancillary-modules, GD configuration/general_data, OF inputs/optional-forcing,
# PT inputs/parameter-tables, SB studio/building-a-model, LI validation/limitations.
# "Code" means the HydroPol2D-Python routing, structure and groundwater code and the Studio
# map tools, read on 2026-10-29; "MATLAB" the HydroPol2D MATLAB code of the same date.
FACTS = {
    "domain on a regular grid, cells outside the domain not computed": "GW 8.3; code",
    "open boundaries are drawn along the perimeter and snap to cell faces":
        "SB (Study area); code: a boundary face must lie on the active-domain perimeter",
    "1 inflow hydrograph, Q(t) split equally over its N faces":
        "HM 2.6; AM (VAL-BC-INFLOW-001); OF (inflow hydrographs); GD (flag_inflow); code",
    "2 reservoir or control structure, Q = k max(h - h0, 0)^b, up to two controls summed, "
    "release to a cell or out of the domain":
        "HM 1.13; PT (internal boundary conditions); GD (flag_reservoir); code; MATLAB "
        "(a (0, 0) destination leaves the model)",
    "3 culvert or bridge as a control, first sizing Q = Cd A sqrt(2 g (h - h0))":
        "SB (road and river crossings); PT; code: a reviewed crossing becomes an internal "
        "boundary with exponent 0.5 and k = Cd A sqrt(2 g); bridges need review",
    "4 detention pond, level pool, orifice, spillway or pump to a chosen cell":
        "SB (Facilities); code: lateral inflow over the shared faces, then the devices",
    "5 stage hydrograph, cells reset to a level or depth, change counted as boundary flow":
        "HM 2.6; AM (stage cells reset each step); OF (stage hydrographs); GD; code "
        "(absolute water-surface elevation or depth above the invert)",
    "6 outlet, normal depth (w/n) h^(5/3) S0^(1/2) or critical depth w sqrt(g) h^(3/2)":
        "HM 1.12; GD (outlet keys, slope_outlet); code; MATLAB (critical slope g n^2 h^(-1/3), "
        "the same discharge)",
    "7 closed wall, no flow across every other perimeter face": "HM 2.6; code",
    "all routing families share these boundaries": "HM 2.6, 3.4",
    "groundwater: fixed head h = hD, no flow at the edge, outside the mask":
        "GW 8; GD (GW_Dirichlet_Head_path, finite cells); code",
    "Studio tool names in the footer": "SB; code (Study area tools)",
    "structures 2 to 4 also run on Voronoi and quadtree meshes, CPU (NumPy) engine, "
    "without mesh river channels or sub-grid tables": "LI (Voronoi mesh mode); code",
}

if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
