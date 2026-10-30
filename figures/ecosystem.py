""""One mesh package, two solvers": schematic for docs/getting-started/ecosystem-architecture.md.

HydroBathyDEM writes one versioned mesh package; HydroPol2D-Python (with Studio) and
HydroPol2D-MATLAB validate it on load and run on it, and both reject a malformed package.
The items follow the page's repository table and mesh-contract list and the contract checks
of both solvers. No version numbers: the release candidates move faster than the figure.

Run from the repository root:

    python3 figures/ecosystem.py [preview-folder]

Output: static/img/getting-started/ecosystem.svg (en), ecosystem.pt.svg and ecosystem.es.svg,
and a PNG of each in the preview folder when one is given.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.patches import Circle, Polygon

from site_style import INK, SOFT, STATIC, WATER, Sheet, color, hex_of, oklch_hex

NAME = "ecosystem"
SECTION = "getting-started"
W = 760

# A list item is a string, or a list of strings for an item that wraps (no bullet on the
# continuation lines).
LABELS = {
    "en": {
        "title": "One mesh package, two solvers",
        "gen_name": "HydroBathyDEM",
        "gen_role": "generates the mesh package",
        "gen_items": [
            ["regular and Voronoi meshes", "terrain products", "conservative raster overlap",
             "subgrid tables"],
            ["UGRID files", "GeoPackage inspection layers", "mesh QA"],
        ],
        "old_name": "HydroPolMesh",
        "old_lines": ["archived migration prototype;", "not a runtime dependency. Its",
                      "useful validated capabilities", "are being kept in HydroBathyDEM"],
        "writes": "writes",
        "pkg_name": "Mesh package",
        "pkg_role": "versioned, follows mesh contract 1.0",
        "files": [
            ("Hydraulic mesh", "UGRID file"),
            ("Raster overlap", "conservative weights"),
            ("Subgrid tables", "when subgrid is on"),
            ("GeoPackage", "inspection layers"),
        ],
        "declare_head": "The package must declare",
        "declare": [
            "cell and face geometry: connectivity, areas, lengths, orientation",
            "zero-based file indices, converted to one-based in MATLAB",
            "cell CFL widths: minimum centre separation normal to a face",
            "CRS, units, source resolution, provenance and contract version",
            "conservative raster-to-cell overlap weights",
            "matching cell and face subgrid tables, when subgrid routing is on",
        ],
        "py_name": "HydroPol2D-Python",
        "py_role": "model engine and Studio",
        "py_lines": ["validates the package on load, then runs on it;",
                     "never regenerates mesh geometry. The Studio mesh",
                     "step runs HydroBathyDEM and validates its output"],
        "ml_name": "HydroPol2D-MATLAB",
        "ml_role": "reference implementation",
        "ml_lines": ["validates the same package on load, then runs on it;",
                     "never regenerates mesh geometry; converts the",
                     "zero-based file indices to one-based"],
        "fail": "if a check fails, the run stops and names the check",
        "reject_head": "Both solvers reject a malformed package; neither rebuilds missing properties",
        "reject": [
            "malformed indices", "zero-length faces", "zero or negative areas",
            "missing units or CRS", "undefined CFL widths", "non-conservative overlap",
            "incompatible subgrid tables", "missing contract version",
        ],
    },
    "pt": {
        "title": "Um pacote de malha, dois solvers",
        "gen_name": "HydroBathyDEM",
        "gen_role": "gera o pacote de malha",
        "gen_items": [
            ["malhas regulares e Voronoi", "produtos de terreno", "sobreposição raster conservativa",
             "tabelas subgrade"],
            ["arquivos UGRID", ["camadas de inspeção", "em GeoPackage"], "QA da malha"],
        ],
        "old_name": "HydroPolMesh",
        "old_lines": ["protótipo de migração arquivado;", "não é dependência de execução.",
                      "O que tinha de útil e validado", "fica no HydroBathyDEM"],
        "writes": "grava",
        "pkg_name": "Pacote de malha",
        "pkg_role": "versionado, segue o contrato de malha 1.0",
        "files": [
            ("Malha hidráulica", "arquivo UGRID"),
            ("Sobreposição", "pesos conservativos"),
            ("Tabelas subgrade", "com subgrade ativa"),
            ("GeoPackage", "camadas de inspeção"),
        ],
        "declare_head": "O pacote precisa declarar",
        "declare": [
            ["geometria de células e faces: conectividade,", "áreas, comprimentos e orientação"],
            ["índices de arquivo com base zero, convertidos", "para base um no MATLAB"],
            ["larguras de CFL das células: menor distância", "entre centros, normal a uma face"],
            ["CRS, unidades, resolução de origem, proveniência", "e versão do contrato"],
            "pesos conservativos de sobreposição entre raster e células",
            ["tabelas subgrade compatíveis de células e faces,", "com o roteamento subgrade ativo"],
        ],
        "py_name": "HydroPol2D-Python",
        "py_role": "motor do modelo e Studio",
        "py_lines": ["valida o pacote ao carregar e roda sobre ele;",
                     "nunca regenera a geometria da malha. A etapa",
                     "de malha do Studio roda o HydroBathyDEM e",
                     "valida o resultado"],
        "ml_name": "HydroPol2D-MATLAB",
        "ml_role": "implementação de referência",
        "ml_lines": ["valida o mesmo pacote ao carregar e roda sobre ele;",
                     "nunca regenera a geometria da malha; converte os",
                     "índices de arquivo de base zero para base um"],
        "fail": "se uma verificação falha, a simulação para e diz qual",
        "reject_head": "Os dois solvers rejeitam um pacote malformado; nenhum reconstrói propriedades ausentes",
        "reject": [
            "índices malformados", "faces de comprimento zero", "áreas nulas ou negativas",
            "unidades ou CRS ausentes", "larguras de CFL indefinidas", "sobreposição não conservativa",
            "tabelas subgrade incompatíveis", "versão do contrato ausente",
        ],
    },
    "es": {
        "title": "Un paquete de malla, dos solucionadores",
        "gen_name": "HydroBathyDEM",
        "gen_role": "genera el paquete de malla",
        "gen_items": [
            ["mallas regulares y de Voronoi", "productos de terreno",
             "superposición ráster conservativa", "tablas de submalla"],
            ["archivos UGRID", ["capas de inspección", "en GeoPackage"],
             "control de calidad de la malla"],
        ],
        "old_name": "HydroPolMesh",
        "old_lines": ["prototipo de migración archivado;", "no es dependencia de ejecución.",
                      "Lo útil y ya validado se está", "conservando en HydroBathyDEM"],
        "writes": "escribe",
        "pkg_name": "Paquete de malla",
        "pkg_role": "versionado, sigue el contrato de malla 1.0",
        "files": [
            ("Malla hidráulica", "archivo UGRID"),
            ("Superposición", "pesos conservativos"),
            ("Tablas de submalla", "con submalla activa"),
            ("GeoPackage", "capas de inspección"),
        ],
        "declare_head": "El paquete debe declarar",
        "declare": [
            ["geometría de celdas y caras: conectividad, áreas,", "longitudes y orientación"],
            ["índices de archivo con base cero, convertidos a", "base uno en MATLAB"],
            ["anchos CFL de celda: separación mínima entre", "centros, normal a una cara"],
            ["CRS, unidades, resolución de origen, procedencia", "y versión del contrato"],
            "pesos conservativos de superposición entre ráster y celdas",
            ["tablas de submalla compatibles de celdas y caras,", "con el enrutamiento con submalla activo"],
        ],
        "py_name": "HydroPol2D-Python",
        "py_role": "motor del modelo y Studio",
        "py_lines": ["valida el paquete al cargarlo y luego lo usa;",
                     "nunca regenera la geometría de la malla. El paso",
                     "de malla de Studio ejecuta HydroBathyDEM y",
                     "valida el resultado"],
        "ml_name": "HydroPol2D-MATLAB",
        "ml_role": "implementación de referencia",
        "ml_lines": ["valida el mismo paquete al cargarlo y luego lo usa;",
                     "nunca regenera la geometría de la malla; convierte",
                     "los índices de archivo de base cero a base uno"],
        "fail": "si falla una verificación, el modelo se detiene y la nombra",
        "reject_head": "Ambos solucionadores rechazan un paquete mal formado; ninguno reconstruye lo que falta",
        "reject": [
            "índices mal formados", "caras de longitud cero", "áreas nulas o negativas",
            "unidades o CRS ausentes", "anchos CFL no definidos", "superposición no conservativa",
            "tablas de submalla incompatibles", "versión del contrato ausente",
        ],
    },
}

# Colours: palette tokens first.
GEN_FILL, GEN_EDGE = hex_of("soil_1"), hex_of("soil_3")        # terrain-side generator
PKG_FILL, PKG_EDGE = color("deep_fill"), WATER                    # the shared package
SOL_FILL, SOL_EDGE = hex_of("rock_a"), color("guide")             # the two consumers
LINE = color("guide")
# New: a red pair for rejection, at the lightness and chroma of deep_fill and water.
REJ_FILL = oklch_hex(0.955, 0.018, 25)
REJ_EDGE = oklch_hex(0.52, 0.130, 25)

HEAD = (11, 10)          # one arrowhead for the whole figure
SHAFT = (1.6, 2.8)
BUS_LW = 1.15            # points; about the 1.6 px start of a ribbon shaft
PITCH = 17


def _rows(items):
    """Flatten list items into (text, is_first_line_of_item) rows."""
    rows = []
    for item in items:
        lines = [item] if isinstance(item, str) else list(item)
        rows += [(line, k == 0) for k, line in enumerate(lines)]
    return rows


def build(lang: str = "en") -> Sheet:
    t = LABELS[lang]
    renderer = RendererAgg(W, 1000, 100)   # measures in px at 100 dpi, i.e. in data units

    # Heights that grow with the text: the package (its declare list) and the solver boxes.
    declare_rows = _rows(t["declare"])
    gy0, gy1 = 44, 150
    py0 = 176
    py1 = py0 + 69 + PITCH * (len(declare_rows) - 1) + 12          # 342 for six rows
    # The solver role goes under the name when the two do not share a line (measured below).
    scratch = Sheet(W, 100, NAME)           # only to measure text

    def measure(text, *, bold=False, size=9.5):
        return scratch.text(0, 0, text, bold=bold, size=size).get_window_extent(renderer).width

    sx = [(24, 368), (392, 736)]
    roles_below = any(
        measure(name, bold=True, size=11) + measure("   " + role) > (x1 - x0 - 28)
        for (x0, x1), name, role in ((sx[0], t["py_name"], t["py_role"]),
                                     (sx[1], t["ml_name"], t["ml_role"]))
    )
    solver_lines = max(len(t["py_lines"]), len(t["ml_lines"])) + (1 if roles_below else 0)
    stem_top = py1
    bus_y, sy0 = py1 + 18, py1 + 44
    sy1 = sy0 + 41 + PITCH * (solver_lines - 1) + 13                 # 474 for three lines
    ry0 = sy1 + 28
    reject_rows = (len(t["reject"]) + 2) // 3
    ry1 = ry0 + 39 + 16 * (reject_rows - 1) + 9                       # 582 for three rows
    height = ry1 + 24
    name_w = max(measure(name, bold=True, size=10) for name, _ in t["files"])
    desc_w = max(measure(desc) for _, desc in t["files"])
    plt.close(scratch.fig)

    s = Sheet(W, height, NAME)
    problems: list[str] = []

    def width_of(artist):
        return artist.get_window_extent(renderer).width

    def put(x, y, text, *, room=None, **kw):
        artist = s.text(x, y, text, **kw)
        if room is not None and width_of(artist) > room:
            problems.append(f"'{text[:40]}' is {width_of(artist):.0f} px, room {room:.0f} px")
        return artist

    def run(x, y, pieces, *, room=None):
        """Pieces (text, bold, size, colour) set one after another on a line."""
        x0 = x
        for text, bold, size, c in pieces:
            x += width_of(s.text(x, y, text, bold=bold, size=size, c=c))
        if room is not None and x - x0 > room:
            problems.append(f"line at y={y} is {x - x0:.0f} px, room {room:.0f} px")

    def bullet(x, y, c):
        s.ax.add_patch(Circle((x, y), 1.9, facecolor=c, edgecolor="none", zorder=10))

    def document(x, y, c_fill, c_edge, w=14, h=18, fold=5):
        pts = [(x, y), (x + w - fold, y), (x + w, y + fold), (x + w, y + h), (x, y + h)]
        s.ax.add_patch(Polygon(pts, closed=True, facecolor=c_fill, edgecolor=c_edge,
                               linewidth=0.9, zorder=6))
        s.ax.add_patch(Polygon([(x + w - fold, y), (x + w - fold, y + fold), (x + w, y + fold)],
                               closed=True, facecolor=c_edge, edgecolor=c_edge, linewidth=0.9,
                               zorder=7))
        for k in range(3):
            yy = y + 8 + 3.5 * k
            s.line([x + 3.5, x + w - 3.5], [yy, yy], c=c_edge, lw=0.6, z=7)

    # --- title -----------------------------------------------------------------------
    put(24, 28, t["title"], bold=True, size=11, room=W - 48)

    # --- row 1: generator and the archived prototype ------------------------------------
    gx0, gx1 = 24, 468
    s.box(gx0, gy0, gx1 - gx0, gy1 - gy0, fill=GEN_FILL, edge=GEN_EDGE)
    run(40, gy0 + 20, [(t["gen_name"], True, 11, INK), ("   " + t["gen_role"], False, 9.5, INK)],
        room=gx1 - 56)
    for x, x_end, items in zip((48, 262), (262 - 10, gx1 - 14), t["gen_items"]):
        rows = _rows(items)
        if len(rows) > 4:
            problems.append(f"generator column at {x} has {len(rows)} rows, room for 4")
        for i, (item, first) in enumerate(rows):
            y = gy0 + 42 + 17 * i
            if first:
                bullet(x - 7, y + 0.5, GEN_EDGE)
            put(x, y, item, room=x_end - x)

    ox0, ox1 = 504, 736
    s.box(ox0, gy0, ox1 - ox0, gy1 - gy0, fill=color("card"), edge=LINE, linestyle=(0, (4, 3)))
    put(ox0 + 16, gy0 + 20, t["old_name"], bold=True, size=10.5, c=SOFT)
    for i, line in enumerate(t["old_lines"]):
        put(ox0 + 16, gy0 + 42 + 17 * i, line, c=SOFT, room=ox1 - ox0 - 28)
    s.dashed([(ox0, gy0 + 51), (gx1 + 1, gy0 + 51)], c=LINE, lw=1.2, head=HEAD)

    # --- arrow down to the package ---------------------------------------------------
    px0, px1 = 24, 736
    ax_x = 246
    s.arrow([(ax_x, gy1), (ax_x, py0)], width=SHAFT, head=HEAD)
    put(ax_x + 10, (gy1 + py0) / 2, t["writes"], c=SOFT)

    # --- row 2: the package ----------------------------------------------------------
    s.box(px0, py0, px1 - px0, py1 - py0, fill=PKG_FILL, edge=PKG_EDGE)
    run(40, py0 + 20, [(t["pkg_name"], True, 11, INK), ("   " + t["pkg_role"], False, 9.5, INK)],
        room=680)
    # File names, then their descriptions, then the divider: each column as wide as its text.
    desc_x = max(176.0, 60 + name_w + 10)
    div_x = max(312.0, desc_x + desc_w + 12)
    for k, (name, desc) in enumerate(t["files"]):
        y = py0 + 50 + 28 * k
        document(40, y - 9, "#ffffff", PKG_EDGE)
        put(60, y, name, bold=True, size=10, room=desc_x - 68)
        put(desc_x, y, desc, room=div_x - desc_x - 10)
    s.line([div_x, div_x], [py0 + 40, py1 - 14], c=color("card_edge"), lw=1.0)
    dx = div_x + 14
    put(dx, py0 + 48, t["declare_head"], bold=True, size=10)
    for i, (item, first) in enumerate(declare_rows):
        y = py0 + 69 + 17 * i
        if first:
            bullet(dx + 3, y + 0.5, PKG_EDGE)
        put(dx + 11, y, item, room=px1 - dx - 24)

    # --- fan-out to the two solvers ----------------------------------------------------
    centres = [(a + b) / 2 for a, b in sx]
    stem_x = 380
    s.line([stem_x, stem_x], [stem_top, bus_y], lw=BUS_LW)
    s.line([centres[0], centres[1]], [bus_y, bus_y], lw=BUS_LW)
    for cx in centres:
        s.arrow([(cx, bus_y), (cx, sy0)], width=(1.6, 2.6), head=HEAD)

    # --- row 3: the solvers ------------------------------------------------------------
    for (x0, x1), name, role, lines in (
        (sx[0], t["py_name"], t["py_role"], t["py_lines"]),
        (sx[1], t["ml_name"], t["ml_role"], t["ml_lines"]),
    ):
        s.box(x0, sy0, x1 - x0, sy1 - sy0, fill=SOL_FILL, edge=SOL_EDGE)
        if roles_below:
            put(x0 + 16, sy0 + 20, name, bold=True, size=11)
            lines = [role] + list(lines)
        else:
            run(x0 + 16, sy0 + 20, [(name, True, 11, INK), ("   " + role, False, 9.5, INK)],
                room=x1 - x0 - 28)
        for i, line in enumerate(lines):
            put(x0 + 16, sy0 + 41 + 17 * i, line, room=x1 - x0 - 28)

    # --- row 4: rejections -------------------------------------------------------------
    for cx in centres:
        s.dashed([(cx, sy1), (cx, ry0)], c=REJ_EDGE, lw=1.2, head=HEAD)
    put(380, (sy1 + ry0) / 2, t["fail"], c=REJ_EDGE, ha="center", room=2 * (centres[1] - 380) - 16)
    s.box(24, ry0, 712, ry1 - ry0, fill=REJ_FILL, edge=REJ_EDGE)
    put(40, ry0 + 18, t["reject_head"], bold=True, size=10, c=REJ_EDGE, room=680)
    for k, item in enumerate(t["reject"]):
        col, row = k % 3, k // 3
        x, y = 48 + 232 * col, ry0 + 39 + 16 * row
        bullet(x - 7, y + 0.5, REJ_EDGE)
        put(x, y, item, room=216)

    for problem in problems:
        print(f"ROOM [{lang}]:", problem)
    return s


def main(preview: Path | None = None) -> None:
    for lang in LABELS:
        svg = build(lang).save(STATIC / SECTION, lang, preview)
        print("wrote", svg.relative_to(STATIC.parent.parent))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
