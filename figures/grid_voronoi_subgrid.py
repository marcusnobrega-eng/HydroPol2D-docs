"""Three ways to represent the land surface, for docs/validation/voronoi-mesh.md.

Top row: the regular D4 grid and the Voronoi mesh (the same mesh mode runs quadtrees),
each with its routing methods and optional modules. Bottom rows: the subgrid options on
each, with the routing method each one needs. The bottom note says the three subgrid
formulations are distinct and at most one is selected.

The meshes are drawn from seeded random points (scipy Voronoi), and the fine terrain in
the lookup-table cards is a synthetic valley: illustrations, not a real case. The seed is
reset for every language, so the drawing is the same in all three.

Run from the repository root:

    python3 figures/grid_voronoi_subgrid.py [preview-folder]

Output: static/img/validation/grid-voronoi-subgrid.svg (en), grid-voronoi-subgrid.pt.svg
and grid-voronoi-subgrid.es.svg, and a PNG of each in the preview folder, if given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
from scipy.spatial import Voronoi
from shapely.geometry import LineString, Point
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import box as shapely_box

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_style import INK, SOFT, STATIC, WATER, Sheet, color, hex_of  # noqa: E402

W = 760
NAME = "grid-voronoi-subgrid"
SEED = 20261027

# Figure text per language. Math stays the same in every language.
LABELS = {
    "en": {
        "title": "Three ways to represent the land surface",
        "grid_name": "Regular grid",
        "grid_role": "the production raster workflow",
        "grid_cells": ("Square cells", [r"equal squares, $\Delta x$ wide"]),
        "grid_links": ("D4 links", ["flow crosses the four faces", "of each cell"]),
        "grid_routing_head": "Routing: all five families",
        "grid_routing": [["local inertial", "full momentum", "diffusive"],
                         ["kinematic", "cellular automata"]],
        "grid_mods_head": "Optional modules",
        "grid_mods": ["all of them, including the slide and", "topple classification (mode 3)"],
        "vor_name": "Voronoi mesh",
        "vor_role": "a separate mode, also for quadtrees",
        "vor_cells": ("Polygons", ["exact areas; finer cells", "near rivers and towns"]),
        "vor_links": ("Edges", ["flow crosses every edge", "shared with a neighbour"]),
        "vor_table_head": ("Routing", "resolved 2D", "Neal graph"),
        "vor_table": [("Local inertial", True, True), ("Kinematic", True, False),
                      ("Explicit diffusive", True, False), ("Full momentum", True, False)],
        "yes": "yes", "no": "no",
        "vor_note": "validated on the CPU; a JAX engine also runs on a GPU",
        "vor_mods_head": "Optional modules, on the CPU (NumPy) engine",
        "vor_mods": ["snow, water quality, human risk index, reservoirs,",
                     "urban drainage, green infrastructure, detention ponds"],
        "vor_mods_not": ["not the slide and topple classification (mode 3)"],
        "sub_head_grid": "Subgrid options on the regular grid",
        "sub_head_mesh": "Subgrid options on the Voronoi mesh",
        "sub_note": ["Neal channel, structured lookup and Voronoi subgrid are distinct formulations, "
                     "not aliases: select at most one."],
        "neal_name": "Neal channel",
        "neal_lines": ["rectangular channel narrower", "than the cell; channel and",
                       "floodplain flows at each face"],
        "graph_name": "Neal channel graph",
        "graph_lines": ["rivers narrower than the mesh:", "channel nodes in host polygons",
                        "joined by links and transitions"],
        "lookup_name": "Structured lookup",
        "lookup_lines": ["SFINCS-style cell and face", "tables against water level;",
                         "parity with MATLAB pending"],
        "paused": "paused",
        "vsub_name": "Voronoi subgrid",
        "vsub_lines": ["tables of cell volume and face", "area, wetted perimeter and",
                       "conveyance against water level"],
        "li_only": "local inertial only",
    },
    "pt": {
        "title": "Três formas de representar a superfície do terreno",
        "grid_name": "Grade regular",
        "grid_role": "o fluxo de produção raster",
        "grid_cells": ("Células quadradas", [r"quadrados de lado $\Delta x$"]),
        "grid_links": ("Ligações D4", ["o escoamento atravessa as", "quatro faces de cada célula"]),
        "grid_routing_head": "Roteamento: as cinco famílias",
        "grid_routing": [["inercial local", "momento completo", "difusivo"],
                         ["cinemático", "autômatos celulares"]],
        "grid_mods_head": "Módulos opcionais",
        "grid_mods": ["todos, inclusive a classificação de", "deslizamento e tombamento (modo 3)"],
        "vor_name": "Malha Voronoi",
        "vor_role": "modo separado, também quadtree",
        "vor_cells": ("Polígonos", ["áreas exatas; menores", "perto de rios e cidades"]),
        "vor_links": ("Arestas", ["o escoamento cruza cada", "aresta com uma vizinha"]),
        "vor_table_head": ("Roteamento", "2D resolvido", "grafo de Neal"),
        "vor_table": [("Inercial local", True, True), ("Cinemático", True, False),
                      ("Difusivo explícito", True, False), ("Momento completo", True, False)],
        "yes": "sim", "no": "não",
        "vor_note": "validada em CPU; um motor JAX também roda em GPU",
        "vor_mods_head": "Módulos opcionais, no motor de CPU (NumPy)",
        "vor_mods": ["neve, qualidade da água, índice de risco humano,",
                     "reservatórios, drenagem urbana, infraestrutura",
                     "verde, bacias de detenção"],
        "vor_mods_not": ["não a classificação de deslizamento e tombamento", "(modo 3)"],
        "sub_head_grid": "Opções de subgrade na grade regular",
        "sub_head_mesh": "Opções de subgrade na malha Voronoi",
        "sub_note": ["Canal de Neal, tabela de consulta estruturada e subgrade Voronoi são formulações "
                     "distintas, não sinônimos:", "escolha no máximo uma."],
        "neal_name": "Canal de Neal",
        "neal_lines": ["canal retangular mais estreito", "que a célula; vazão no canal",
                       "e na planície em cada face"],
        "graph_name": "Grafo de canais de Neal",
        "graph_lines": ["rios mais estreitos que a malha:", "nós de canal nos polígonos",
                        "ligados por trechos e transições"],
        "lookup_name": "Tabela de consulta",
        "lookup_lines": ["tabelas de célula e de face", "por nível, no estilo SFINCS;",
                         "paridade MATLAB pendente"],
        "paused": "pausado",
        "vsub_name": "Subgrade Voronoi",
        "vsub_lines": ["tabelas de volume da célula", "e de área, perímetro molhado",
                       "e condutância da face por nível"],
        "li_only": "só inercial local",
    },
    "es": {
        "title": "Tres formas de representar la superficie del terreno",
        "grid_name": "Malla ráster regular",
        "grid_role": "el flujo de producción",
        "grid_cells": ("Celdas cuadradas", [r"cuadrados de lado $\Delta x$"]),
        "grid_links": ("Enlaces D4", ["el flujo atraviesa las", "cuatro caras de cada celda"]),
        "grid_routing_head": "Enrutamiento: las cinco familias",
        "grid_routing": [["inercial local", "momento completo", "difusivo"],
                         ["cinemático", "autómatas celulares"]],
        "grid_mods_head": "Módulos opcionales",
        "grid_mods": ["todos, incluida la clasificación de", "deslizamiento y vuelco (modo 3)"],
        "vor_name": "Malla de Voronoi",
        "vor_role": "modo aparte, también quadtree",
        "vor_cells": ("Polígonos", ["áreas exactas; más finos", "cerca de ríos y ciudades"]),
        "vor_links": ("Aristas", ["el flujo cruza cada arista", "común con una vecina"]),
        "vor_table_head": ("Enrutamiento", "2D resuelto", "grafo de Neal"),
        "vor_table": [("Inercial local", True, True), ("Cinemático", True, False),
                      ("Difusivo explícito", True, False), ("Momento completo", True, False)],
        "yes": "sí", "no": "no",
        "vor_note": "validada en CPU; un motor JAX la ejecuta en GPU",
        "vor_mods_head": "Módulos opcionales, motor de CPU (NumPy)",
        "vor_mods": ["nieve, calidad del agua, índice de riesgo humano,",
                     "embalses, drenaje urbano, infraestructura verde,",
                     "estanques de detención"],
        "vor_mods_not": ["no la clasificación de deslizamiento y vuelco (modo 3)"],
        "sub_head_grid": "Opciones de submalla: malla ráster regular",
        "sub_head_mesh": "Opciones de submalla: malla de Voronoi",
        "sub_note": ["Canal de Neal, tabla de consulta estructurada y submalla de Voronoi son "
                     "formulaciones distintas, no sinónimos:", "elija como máximo una."],
        "neal_name": "Canal de Neal",
        "neal_lines": ["un canal rectangular más", "estrecho que la celda; flujos",
                       "de canal y llanura por cara"],
        "graph_name": "Grafo de canales de Neal",
        "graph_lines": ["ríos más estrechos que la malla", "nodos de canal en polígonos",
                        "con enlaces y transiciones"],
        "lookup_name": "Tabla de consulta",
        "lookup_lines": ["tablas de celda y de cara", "según el nivel, estilo SFINCS;",
                         "aún sin paridad con MATLAB"],
        "paused": "en pausa",
        "vsub_name": "Submalla de Voronoi",
        "vsub_lines": ["tablas de volumen de la celda y", "de área, perímetro mojado y",
                       "conducción de la cara por nivel"],
        "li_only": "solo inercial local",
    },
}

# Colours: palette tokens only.
LINE = color("guide")
EDGE = color("card_edge")
LAND = hex_of("rock_a")
HIGHLIGHT = hex_of("wet_a")
RIVER = hex_of("wet_b")
HOST = color("deep_fill")
SOIL = color("ground")
TERRAIN_RAMP = [hex_of(k) for k in ("soil_3", "soil_2", "soil_1", "rock_b", "rock_a")]  # low to high


# --- geometry helpers -------------------------------------------------------------------


def poisson_seeds(rng, bounds, radius, tries=8000):
    """Dart throwing with a spatially varying spacing radius(x, y)."""
    x0, y0, x1, y1 = bounds
    pts, radii = [], []
    for _ in range(tries):
        p = rng.uniform((x0, y0), (x1, y1))
        r = radius(p)
        if all(np.hypot(*(p - q)) >= 0.5 * (r + rq) for q, rq in zip(pts, radii)):
            pts.append(p)
            radii.append(r)
    return np.array(pts)


def clipped_voronoi(seeds, bounds):
    """Voronoi cells of the seeds, clipped to the rectangle, plus the neighbour pairs."""
    x0, y0, x1, y1 = bounds
    span = max(x1 - x0, y1 - y0)
    far = np.array([[x0 - 3 * span, y0 - 3 * span], [x1 + 3 * span, y0 - 3 * span],
                    [x1 + 3 * span, y1 + 3 * span], [x0 - 3 * span, y1 + 3 * span]])
    vor = Voronoi(np.vstack([seeds, far]))
    frame = shapely_box(x0, y0, x1, y1)
    cells = []
    for i in range(len(seeds)):
        region = vor.regions[vor.point_region[i]]
        cells.append(ShapelyPolygon(vor.vertices[region]).intersection(frame))
    pairs = [(a, b) for a, b in vor.ridge_points if a < len(seeds) and b < len(seeds)]
    return cells, pairs


def terrain(x, y, x0, y0, wdt, hgt):
    """Synthetic valley: a sinuous channel, banks rising to both sides (0 low, 1 high)."""
    u, v = (x - x0) / wdt, (y - y0) / hgt
    axis = 0.5 + 0.16 * np.sin(2 * np.pi * (u * 0.9 + 0.1))
    return float(np.clip(0.15 + 2.2 * abs(v - axis) ** 0.85 + 0.08 * u, 0, 1))


def ramp(z):
    return TERRAIN_RAMP[min(int(z * len(TERRAIN_RAMP)), len(TERRAIN_RAMP) - 1)]


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        draw(lang, preview)


def draw(lang: str, preview: Path | None = None) -> None:
    t = LABELS[lang]
    rng = np.random.default_rng(SEED)

    # Vertical layout: the top panels grow with the optional-module notes of the mesh, and
    # the subgrid rows move down by the same amount; the card grows with the bottom note.
    mesh_mod_lines = len(t["vor_mods"]) + len(t["vor_mods_not"])
    py0 = 44
    mods_y = 346                                       # optional-module headings
    py1 = mods_y + 18 + 17 * (mesh_mod_lines - 1) + 14
    dy = py1 - 336                                     # shift of everything below the panels
    note_y = 596 + dy
    H = int(note_y + 17 * (len(t["sub_note"]) - 1) + 24)

    s = Sheet(W, H, NAME)
    ax = s.ax
    renderer = RendererAgg(W, H, 100)   # measures in px at 100 dpi, i.e. in data units

    def width_of(artist):
        return artist.get_window_extent(renderer).width

    def put(x, y, text, *, room=None, **kw):
        artist = s.text(x, y, text, **kw)
        if room is not None and width_of(artist) > room:
            print(f"WARNING [{lang}]: '{text[:40]}' is {width_of(artist):.0f} px, room {room} px")
        return artist

    def run(x, y, pieces, *, room=None):
        x_start = x
        for text, bold, size, c in pieces:
            x += width_of(s.text(x, y, text, bold=bold, size=size, c=c))
        if room is not None and x - x_start > room:
            print(f"WARNING [{lang}]: line at y={y} is {x - x_start:.0f} px, room {room} px")

    def note(x, y, heading, lines, room):
        put(x, y, heading, bold=True, size=10, room=room)
        for i, line in enumerate(lines):
            put(x, y + 18 + 17 * i, line, room=room)

    def bullet(x, y, c=INK):
        ax.add_patch(Circle((x, y), 1.9, facecolor=c, edgecolor="none", zorder=10))

    def dot(x, y, r=1.8, c=INK, z=9):
        ax.add_patch(Circle((x, y), r, facecolor=c, edgecolor="none", zorder=z))

    def poly(shape, *, fill, edge=LINE, lw=0.6, z=3):
        for g in getattr(shape, "geoms", [shape]):
            if g.geom_type == "Polygon" and not g.is_empty:
                ax.add_patch(Polygon(np.asarray(g.exterior.coords), closed=True, facecolor=fill,
                                     edgecolor=edge, linewidth=lw, zorder=z))

    def lines_of(shape, *, c, lw, z=6, **kw):
        for g in getattr(shape, "geoms", [shape]):
            if g.geom_type == "LineString" and not g.is_empty:
                xy = np.asarray(g.coords)
                ax.plot(xy[:, 0], xy[:, 1], color=c, linewidth=lw, solid_capstyle="round",
                        zorder=z, **kw)

    def chip(x, y, text, *, fill=HOST, edge=WATER, c=WATER, room=None):
        """Small rounded tag, left edge at x, centred on y."""
        artist = s.text(x + 8, y, text, c=c, z=12)
        w = width_of(artist) + 16
        if room is not None and w > room:
            print(f"WARNING [{lang}]: chip '{text}' is {w:.0f} px, room {room} px")
        ax.add_patch(FancyBboxPatch((x, y - 9), w, 18, boxstyle="round,pad=0,rounding_size=9",
                                    facecolor=fill, edgecolor=edge, linewidth=0.8, zorder=11))

    # --- title and the two panels ----------------------------------------------------
    put(24, 28, t["title"], bold=True, size=11)
    pa, pb = (24, 352), (376, 736)
    for x0, x1 in (pa, pb):
        s.box(x0, py0, x1 - x0, py1 - py0, fill=color("card"), edge=EDGE)

    # Panel a: regular grid with D4 links.
    run(40, py0 + 20, [(t["grid_name"], True, 11, INK), ("   " + t["grid_role"], False, 9.5, SOFT)],
        room=pa[1] - 52)
    gx0, gy0, side, ncol, nrow = 40, 98, 24, 5, 4
    hi = (2, 1)
    for i in range(ncol):
        for j in range(nrow):
            ax.add_patch(Rectangle((gx0 + i * side, gy0 + j * side), side, side,
                                   facecolor=HIGHLIGHT if (i, j) == hi else LAND,
                                   edgecolor=LINE, linewidth=0.6, zorder=3))

    def centre(i, j):
        return gx0 + (i + 0.5) * side, gy0 + (j + 0.5) * side

    for i in range(ncol):
        for j in range(nrow):
            dot(*centre(i, j), r=1.3, c=SOFT)
    hx, hy = centre(*hi)
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = centre(hi[0] + di, hi[1] + dj)
        s.line([hx, nx], [hy, ny], c=WATER, lw=1.6, z=6)
        dot(nx, ny, r=2.2, c=WATER, z=7)
    dot(hx, hy, r=2.6, c=INK, z=8)
    nx0 = gx0 + ncol * side + 16
    note(nx0, 108, *t["grid_cells"], room=pa[1] - nx0 - 12)
    note(nx0, 166, *t["grid_links"], room=pa[1] - nx0 - 12)

    put(40, 232, t["grid_routing_head"], bold=True, size=10)
    for x, items in zip((48, 196), t["grid_routing"]):
        for k, item in enumerate(items):
            bullet(x - 7, 254 + 17 * k + 0.5, SOFT)
            put(x, 254 + 17 * k, item, room=140)
    put(40, mods_y, t["grid_mods_head"], bold=True, size=10)
    for k, line in enumerate(t["grid_mods"]):
        put(40, mods_y + 18 + 17 * k, line, room=pa[1] - pa[0] - 32)

    # Panel b: Voronoi mesh, finer along a river.
    run(pb[0] + 16, py0 + 20, [(t["vor_name"], True, 11, INK), ("   " + t["vor_role"], False, 9.5, SOFT)],
        room=pb[1] - pb[0] - 28)
    vb = (pb[0] + 16, 98, pb[0] + 176, 194)          # drawing bounds
    river = LineString([(vb[0] - 4 + 2.0 * k, 0.5 * (vb[1] + vb[3]) + 4
                         + 20 * np.sin(k / 12.0 + 0.4) - 5 * np.cos(k / 5.5)) for k in range(0, 86)])
    seeds = poisson_seeds(rng, vb, lambda p: 8 + 22 * float(np.clip((river.distance(Point(p)) - 9.0) / 34.0, 0.0, 1.0)))
    cells, pairs = clipped_voronoi(seeds, vb)
    # Highlight a mid-sized cell at the edge of the fine band, away from the drawing border.
    inner = shapely_box(vb[0] + 30, vb[1] + 14, vb[2] - 30, vb[3] - 14)

    def neighbours_of(k):
        return sorted({q for p_, q in pairs if p_ == k} | {p_ for p_, q in pairs if q == k})

    candidates = [k for k, c in enumerate(cells)
                  if 12.0 <= river.distance(Point(seeds[k])) <= 30.0 and inner.contains(c.centroid)
                  and c.within(shapely_box(*vb).buffer(-3.0))
                  and 5 <= len(neighbours_of(k)) <= 7]
    k_hi = max(candidates, key=lambda k: cells[k].area)
    neighbours = neighbours_of(k_hi)
    for k, cell in enumerate(cells):
        poly(cell, fill=HIGHLIGHT if k == k_hi else LAND, edge=LINE, lw=0.6, z=3)
    lines_of(river.intersection(shapely_box(*vb)), c=RIVER, lw=2.4, z=4)
    for k in range(len(seeds)):
        dot(*seeds[k], r=1.2, c=SOFT, z=5)
    for k in neighbours:
        s.line([seeds[k_hi][0], seeds[k][0]], [seeds[k_hi][1], seeds[k][1]], c=WATER, lw=1.6, z=6)
        dot(*seeds[k], r=2.2, c=WATER, z=7)
    dot(*seeds[k_hi], r=2.6, c=INK, z=8)
    nx1 = vb[2] + 16
    note(nx1, 108, *t["vor_cells"], room=pb[1] - nx1 - 12)
    note(nx1, 166, *t["vor_links"], room=pb[1] - nx1 - 12)

    head, col_a, col_b = t["vor_table_head"]
    cx_a, cx_b = pb[0] + 192, pb[0] + 300
    put(pb[0] + 16, 232, head, bold=True, size=10)
    put(cx_a, 232, col_a, bold=True, size=10, ha="center")
    put(cx_b, 232, col_b, bold=True, size=10, ha="center")
    s.line([pb[0] + 16, pb[1] - 16], [242, 242], c=EDGE, lw=0.8)
    for k, (mode, a, b) in enumerate(t["vor_table"]):
        y = 254 + 16 * k
        put(pb[0] + 16, y, mode, room=150)
        for cx, ok in ((cx_a, a), (cx_b, b)):
            put(cx, y, t["yes"] if ok else t["no"], c=INK if ok else SOFT, ha="center")
    put(pb[0] + 16, 254 + 16 * 4 + 4, t["vor_note"], c=SOFT, room=pb[1] - pb[0] - 32)
    put(pb[0] + 16, mods_y, t["vor_mods_head"], bold=True, size=10, room=pb[1] - pb[0] - 32)
    rows = [(line, INK) for line in t["vor_mods"]] + [(line, SOFT) for line in t["vor_mods_not"]]
    for k, (line, c) in enumerate(rows):
        put(pb[0] + 16, mods_y + 18 + 17 * k, line, c=c, room=pb[1] - pb[0] - 32)

    # --- row 2: subgrid options --------------------------------------------------------
    put(pa[0], 354 + dy, t["sub_head_grid"], bold=True, size=10.5, room=pa[1] - pa[0])
    put(pb[0], 354 + dy, t["sub_head_mesh"], bold=True, size=10.5, room=pb[1] - pb[0])
    r1, r2 = (368 + dy, 468 + dy), (478 + dy, 578 + dy)
    for k, line in enumerate(t["sub_note"]):
        put(24, note_y + 17 * k, line, room=712)
    for (x0, x1) in (pa, pb):
        for (y0, y1) in (r1, r2):
            s.box(x0, y0, x1 - x0, y1 - y0, fill=color("card"), edge=EDGE)
    ta, tb = 140, 158         # text column offsets in the grid and mesh cards

    def card_text(x0, x1, y0, name, lines, dx, status, status_style):
        room = x1 - (x0 + dx) - 12
        put(x0 + dx, y0 + 17, name, bold=True, size=10, room=room)
        for i, line in enumerate(lines):
            put(x0 + dx, y0 + 35 + 16 * i, line, room=room)
        chip(x0 + dx, y0 + 84, status, room=room, **status_style)

    li_style = {}
    paused_style = {"fill": hex_of("rock_b"), "edge": LINE, "c": SOFT}

    # Card 1: Neal channel, cross-section of one coarse cell.
    x0, y0 = pa[0], r1[0]
    a, b = x0 + 22, x0 + 122                 # cell faces, delta x apart
    g = y0 + 34                              # floodplain level
    cw, chh = 28, 22                         # channel width and bank height
    c0 = (a + b) / 2 - cw / 2
    base = y0 + 62
    ground = [(a - 8, g), (c0, g), (c0, g + chh), (c0 + cw, g + chh), (c0 + cw, g), (b + 8, g)]
    ax.add_patch(Polygon(ground + [(b + 8, base), (a - 8, base)], closed=True,
                         facecolor=hex_of("soil_1"), edgecolor="none", zorder=3))
    level = g + 8
    ax.add_patch(Rectangle((c0, level), cw, g + chh - level, facecolor=HIGHLIGHT,
                           edgecolor="none", zorder=4))
    s.line([c0, c0 + cw], [level, level], c=WATER, lw=1.2, z=5)
    gx, gy = zip(*ground)
    s.line(gx, gy, c=SOIL, lw=1.8, z=6)
    for xf in (a, b):
        s.line([xf, xf], [y0 + 14, base + 4], c=LINE, lw=0.9, style=(0, (3, 2)), z=6)
    s.line([c0, c0 + cw], [g - 4, g - 4], c=INK, lw=0.7, z=6)
    for xf in (c0, c0 + cw):
        s.line([xf, xf], [g - 7, g - 1], c=INK, lw=0.7, z=6)
    put((a + b) / 2, g - 13, r"$w$", size=10, ha="center")
    put(c0 + cw + 5, g + chh / 2 + 1, r"$H$", size=10)
    dim = base + 12
    s.line([a, b], [dim, dim], c=INK, lw=0.7, z=6)
    for xf in (a, b):
        s.line([xf, xf], [dim - 4, dim + 4], c=INK, lw=0.7, z=6)
    put((a + b) / 2, dim + 12, r"$\Delta x$", size=10, ha="center")
    card_text(x0, pa[1], y0, t["neal_name"], t["neal_lines"], ta, t["li_only"], li_style)

    # Card 2: Neal channel graph on a coarse Voronoi patch.
    x0, y0 = pb[0], r1[0]
    gb = (x0 + 12, y0 + 10, x0 + 146, y0 + 90)
    jitter = [(gb[0] + 12 + 26 * i + rng.uniform(-5, 5), gb[1] + 12 + 28 * j + rng.uniform(-5, 5))
              for i in range(6) for j in range(3)]
    gseeds = np.array([p for p in jitter if gb[0] < p[0] < gb[2] and gb[1] < p[1] < gb[3]])
    gcells, _ = clipped_voronoi(gseeds, gb)
    path = LineString([(gb[0], gb[1] + 50), (gb[0] + 26, gb[1] + 57), (gb[0] + 54, gb[1] + 40),
                       (gb[0] + 84, gb[1] + 34), (gb[0] + 110, gb[1] + 44), (gb[0] + 128, gb[1] + 42)])
    resolved = int(np.argmin(np.hypot(*(gseeds - np.array([gb[2] - 4, gb[1] + 42])).T)))
    nodes = []
    for k, cell in enumerate(gcells):
        inside = path.intersection(cell)
        host = (not inside.is_empty) and inside.length > 8 and k != resolved
        poly(cell, fill=HIGHLIGHT if k == resolved else (HOST if host else LAND), edge=LINE, lw=0.6)
        if host:
            mid = inside.interpolate(0.5, normalized=True)
            nodes.append((path.project(mid), mid.x, mid.y))
    lines_of(path, c=RIVER, lw=1.6, z=4)
    nodes.sort()
    for (_, xa, ya), (_, xb, yb) in zip(nodes, nodes[1:]):
        s.line([xa, xb], [ya, yb], c=WATER, lw=2.0, z=6)
    for _, xn, yn in nodes:
        dot(xn, yn, r=2.8, c=WATER, z=7)
    rx, ry = gseeds[resolved]
    s.line([nodes[-1][1], rx], [nodes[-1][2], ry], c=WATER, lw=1.4, style=(0, (2.5, 2)), z=6)
    dot(rx, ry, r=2.2, c=INK, z=7)
    card_text(x0, pb[1], y0, t["graph_name"], t["graph_lines"], tb, t["li_only"], li_style)

    # Card 3: structured lookup tables: fine terrain in 2 x 2 coarse cells, and V(level).
    x0, y0 = pa[0], r2[0]
    fx0, fy0, coarse, fine = x0 + 14, y0 + 13, 36, 6
    for i in range(12):
        for j in range(12):
            xx, yy = fx0 + i * fine, fy0 + j * fine
            ax.add_patch(Rectangle((xx, yy), fine, fine, edgecolor="none", zorder=3,
                                   facecolor=ramp(terrain(xx + 3, yy + 3, fx0, fy0, 72, 72))))
    for k in range(3):
        s.line([fx0 + k * coarse] * 2, [fy0, fy0 + 2 * coarse], c=INK, lw=0.8, z=5)
        s.line([fx0, fx0 + 2 * coarse], [fy0 + k * coarse] * 2, c=INK, lw=0.8, z=5)
    s.line([fx0 + coarse] * 2, [fy0, fy0 + coarse], c=WATER, lw=2.4, z=6)     # one face
    cx0, cy1, cw_, ch_ = x0 + 98, y0 + 80, 26, 62
    s.line([cx0, cx0, cx0 + cw_], [cy1 - ch_, cy1, cy1], c=SOFT, lw=0.8, z=5)
    vv = np.linspace(0, 1, 40)
    eta = np.where(vv < 0.18, vv / 0.18 * 0.55, 0.55 + (vv - 0.18) / 0.82 * 0.40)
    ax.plot(cx0 + vv * (cw_ - 2), cy1 - eta * (ch_ - 6), color=WATER, linewidth=1.4, zorder=6)
    put(cx0 + cw_ - 2, cy1 + 10, r"$V$", size=10, ha="center")
    put(cx0, cy1 - ch_ - 8, r"$\eta$", size=10, ha="center")
    card_text(x0, pa[1], y0, t["lookup_name"], t["lookup_lines"], ta, t["paused"], paused_style)

    # Card 4: Voronoi subgrid: fine terrain inside one polygon and a face cross-section.
    x0, y0 = pb[0], r2[0]
    pbx = (x0 + 12, y0 + 12, x0 + 76, y0 + 88)
    wide = (pbx[0] - 40, pbx[1] - 40, pbx[2] + 40, pbx[3] + 40)
    pseeds = poisson_seeds(np.random.default_rng(SEED + 1), wide, lambda p: 44.0)
    pcells, _ = clipped_voronoi(pseeds, wide)
    mid = np.array([(pbx[0] + pbx[2]) / 2, (pbx[1] + pbx[3]) / 2])
    xs, ys = np.asarray(pcells[int(np.argmin(np.hypot(*(pseeds - mid).T)))].exterior.coords).T
    sc = min((pbx[2] - pbx[0]) / np.ptp(xs), (pbx[3] - pbx[1]) / np.ptp(ys))
    xs = pbx[0] + (xs - xs.min()) * sc
    ys = pbx[1] + (ys - ys.min()) * sc
    ax.add_patch(Polygon(np.column_stack([xs, ys]), closed=True, facecolor="none", edgecolor=INK,
                         linewidth=0.9, zorder=6))
    clip = Polygon(np.column_stack([xs, ys]), closed=True, transform=ax.transData)
    for i in range(int((pbx[2] - pbx[0]) / fine) + 1):
        for j in range(int((pbx[3] - pbx[1]) / fine) + 1):
            xx, yy = pbx[0] + i * fine, pbx[1] + j * fine
            z = terrain(xx + 3, yy + 3, pbx[0], pbx[1], pbx[2] - pbx[0], pbx[3] - pbx[1])
            patch = Rectangle((xx, yy), fine, fine, facecolor=ramp(z), edgecolor="none", zorder=3)
            ax.add_patch(patch)
            patch.set_clip_path(clip)
    # The face shown in section: a long edge whose outward side faces the section (right).
    ring = list(zip(xs, ys))
    cxp, cyp = xs[:-1].mean(), ys[:-1].mean()

    def facing_right(e):
        (xa, ya), (xb, yb) = e
        length = np.hypot(xb - xa, yb - ya)
        nx_, ny_ = (yb - ya) / length, -(xb - xa) / length
        if nx_ * ((xa + xb) / 2 - cxp) + ny_ * ((ya + yb) / 2 - cyp) < 0:
            nx_ = -nx_
        return nx_ * min(length, 30.0)

    face = max(zip(ring[:-1], ring[1:]), key=facing_right)
    s.line([face[0][0], face[1][0]], [face[0][1], face[1][1]], c=WATER, lw=2.6, z=7)
    # Face cross-section: wet flow area A and wetted perimeter P, with a dotted zoom cone.
    sx0, sx1, top, bottom = x0 + 92, x0 + 146, y0 + 36, y0 + 80
    (fa_x, fa_y), (fb_x, fb_y) = sorted(face, key=lambda q: q[1])     # upper, lower end
    for (fx, fy), (qx, qy) in (((fa_x, fa_y), (sx0 - 2, top - 6)), ((fb_x, fb_y), (sx0 - 2, bottom))):
        s.line([fx, qx], [fy, qy], c=LINE, lw=0.8, style=(0, (1, 2)), z=5)
    u = np.array([0, 0.12, 0.28, 0.40, 0.52, 0.66, 0.84, 1.0])
    depth = np.array([0.10, 0.30, 0.55, 0.95, 1.0, 0.70, 0.30, 0.12])
    bed = [(sx0 + uu * (sx1 - sx0), top + dd * (bottom - top - 6)) for uu, dd in zip(u, depth)]
    wl = top + 0.40 * (bottom - top - 6)
    above_bed = ShapelyPolygon([(sx0, top - 20)] + bed + [(sx1, top - 20)])
    water = above_bed.intersection(shapely_box(sx0, wl, sx1, bottom + 10))
    wet = water if water.geom_type == "Polygon" else max(water.geoms, key=lambda q: q.area)
    ax.add_patch(Polygon(bed + [(sx1, bottom), (sx0, bottom)], closed=True,
                         facecolor=hex_of("soil_1"), edgecolor="none", zorder=3))
    poly(wet, fill=HIGHLIGHT, edge="none", lw=0, z=4)
    bx, by = zip(*bed)
    s.line(bx, by, c=SOIL, lw=1.2, z=5)
    lines_of(LineString(bed).intersection(shapely_box(sx0, wl, sx1, bottom + 10)), c=WATER, lw=2.4)
    wxs, _ = np.asarray(wet.exterior.coords).T
    s.line([wxs.min(), wxs.max()], [wl, wl], c=WATER, lw=1.0, z=6)
    put(wet.centroid.x, wl + 8, r"$A$", size=10, ha="center", z=12)
    put(wet.centroid.x + 4, bottom + 6, r"$P$", size=10, ha="center", c=WATER)
    card_text(x0, pb[1], y0, t["vsub_name"], t["vsub_lines"], tb, t["li_only"], li_style)

    svg = s.save(STATIC / "validation", lang, preview)
    print("wrote", svg.name, "voronoi cells:", len(seeds))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
